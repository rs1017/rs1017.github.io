#!/usr/bin/env python3
"""
낙현아빠의 개발 블로그 - 자동 포스트 생성 스크립트 (스케줄러용)

스케줄:
- 주말 GitHub Actions 스케줄로 호출
- 기본 5개 생성 (요일 무관)
- 모든 생성 완료 후 한 번에 commit & push
- 빌드 실패 시: 최대 5회 수정 시도

사용법:
    python auto_generate.py              # 기본 5개 생성
    python auto_generate.py --count 3    # 수동으로 개수 지정
"""

import subprocess
import sys
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

# ┌─────────────────────────────────────────────────────────┐
# │  Configuration                                           │
# └─────────────────────────────────────────────────────────┘

REPO_DIR = Path(__file__).parent
GENERATOR_SCRIPT = REPO_DIR / "generator" / "generate.py"
GH_CLI = r"C:\Program Files\GitHub CLI\gh.exe"
MAX_FIX_ATTEMPTS = 5  # 오류 수정 최대 시도 횟수
WAIT_FOR_ACTIONS = 180  # Actions 완료 대기 시간 (초)

# 생성 개수 (요일 무관)
DEFAULT_COUNT = 5


# ┌─────────────────────────────────────────────────────────┐
# │  Logging                                                 │
# └─────────────────────────────────────────────────────────┘

LOG_DIR = REPO_DIR / "logs"
LOG_FILE = None  # 실행 시 설정됨


def init_log_file() -> Path:
    """로그 파일 초기화"""
    global LOG_FILE
    LOG_DIR.mkdir(exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    LOG_FILE = LOG_DIR / f"auto_generate_{today}.log"
    return LOG_FILE


def log(message: str, level: str = "INFO") -> None:
    """로그 출력 (콘솔 + 파일)"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line, flush=True)

    # 파일에도 기록
    if LOG_FILE:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")


# ┌─────────────────────────────────────────────────────────┐
# │  Helper Functions                                        │
# └─────────────────────────────────────────────────────────┘

def get_target_count() -> int:
    """생성 개수 반환 (요일 무관)"""
    return DEFAULT_COUNT


def get_day_name() -> str:
    """오늘 요일 이름"""
    days = ["월", "화", "수", "목", "금", "토", "일"]
    return days[datetime.now().weekday()]


# ┌─────────────────────────────────────────────────────────┐
# │  GitHub Actions Monitoring                               │
# └─────────────────────────────────────────────────────────┘

def check_actions_status() -> Tuple[str, Optional[str]]:
    """
    GitHub Actions 상태 확인

    Returns:
        (status, error_log): status는 'success', 'failure', 'pending', 'unknown'
    """
    try:
        result = subprocess.run(
            [GH_CLI, "run", "list", "--limit", "1", "--json", "status,conclusion,databaseId"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_DIR,
        )

        if result.returncode != 0:
            return "unknown", None

        runs = json.loads(result.stdout)
        if not runs:
            return "unknown", None

        run = runs[0]
        status = run.get("status", "unknown")
        conclusion = run.get("conclusion")
        run_id = run.get("databaseId")

        if status == "completed":
            if conclusion == "success":
                return "success", None
            else:
                error_log = get_error_log(run_id)
                return "failure", error_log
        elif status in ["in_progress", "queued"]:
            return "pending", None
        else:
            return "unknown", None

    except Exception as e:
        log(f"Actions 상태 확인 실패: {e}", "ERROR")
        return "unknown", None


def get_error_log(run_id: int) -> Optional[str]:
    """실패한 run의 에러 로그 가져오기"""
    try:
        result = subprocess.run(
            [GH_CLI, "run", "view", str(run_id), "--log-failed"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=REPO_DIR,
        )
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        log(f"에러 로그 가져오기 실패: {e}", "ERROR")
        return None


def wait_for_actions_completion() -> Tuple[str, Optional[str]]:
    """Actions 완료까지 대기"""
    log("GitHub Actions 완료 대기 중...")

    start_time = time.time()
    while time.time() - start_time < WAIT_FOR_ACTIONS:
        status, error_log = check_actions_status()

        if status == "success":
            log("Actions 성공!")
            return "success", None
        elif status == "failure":
            log("Actions 실패!")
            return "failure", error_log
        elif status == "pending":
            log("Actions 진행 중... (30초 후 재확인)")
            time.sleep(30)
        else:
            time.sleep(10)

    log("Actions 대기 시간 초과", "WARN")
    return "timeout", None


# ┌─────────────────────────────────────────────────────────┐
# │  Skill Generation                                        │
# └─────────────────────────────────────────────────────────┘

def generate_single_skill(index: int, total: int) -> bool:
    """단일 포스트 생성 (커밋 없이)"""
    log(f"[{index}/{total}] 포스트 생성 중...")

    try:
        result = subprocess.run(
            [
                sys.executable,
                str(GENERATOR_SCRIPT),
                # 에이전트 기반으로 변경됨 - 추가 인자 불필요
            ],
            capture_output=True,
            text=True,
            timeout=1200,  # 20분 타임아웃 (3회 retry 포함)
            cwd=REPO_DIR,
        )

        if result.stdout:
            # 마지막 몇 줄만 출력
            lines = result.stdout.strip().split('\n')
            for line in lines[-5:]:
                print(f"    {line}")

        if result.returncode == 0:
            log(f"[{index}/{total}] 포스트 생성 완료!")
            return True
        else:
            log(f"[{index}/{total}] 포스트 생성 실패", "WARN")
            if result.stderr:
                print(f"    Error: {result.stderr[:200]}")
            return False

    except subprocess.TimeoutExpired:
        log(f"[{index}/{total}] 타임아웃", "WARN")
        return False
    except Exception as e:
        log(f"[{index}/{total}] 오류: {e}", "ERROR")
        return False


def generate_multiple_skills(count: int) -> int:
    """여러 포스트 생성 (커밋 없이)"""
    log(f"총 {count}개 포스트 생성 시작...")

    success_count = 0
    for i in range(1, count + 1):
        if generate_single_skill(i, count):
            success_count += 1

        # 연속 생성 사이에 약간의 딜레이
        if i < count:
            time.sleep(5)

    log(f"포스트 생성 완료: {success_count}/{count}개 성공")
    return success_count


# ┌─────────────────────────────────────────────────────────┐
# │  Copy to assets/downloads                                │
# └─────────────────────────────────────────────────────────┘

def copy_to_downloads() -> None:
    """Copy source automation contents to assets/downloads/ for blog distribution"""
    import shutil

    src_base = REPO_DIR / ".agent"
    dst_base = REPO_DIR / "assets" / "downloads"

    # Copy directories
    for category in ["skills", "agents", "commands", "hooks", "scripts", "workflows", "rules"]:
        src_dir = src_base / category
        dst_dir = dst_base / category

        if src_dir.exists():
            # Copy each item
            for item in src_dir.iterdir():
                dst_item = dst_dir / item.name
                if item.is_dir():
                    if dst_item.exists():
                        shutil.rmtree(dst_item)
                    shutil.copytree(item, dst_item)
                else:
                    shutil.copy2(item, dst_item)

    log("assets/downloads/로 복사 완료")


# ┌─────────────────────────────────────────────────────────┐
# │  Git Operations                                          │
# └─────────────────────────────────────────────────────────┘

def has_changes() -> bool:
    """변경사항 있는지 확인"""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    return bool(result.stdout.strip())


def commit_and_push(skill_count: int) -> bool:
    """변경사항 커밋 및 푸시"""
    if not has_changes():
        log("커밋할 변경사항이 없습니다.")
        return True

    try:
        # Stage files
        subprocess.run(
            ["git", "add", "assets/downloads/", "_posts/", "_data/skill_registry.yml"],
            cwd=REPO_DIR,
            check=True,
        )

        # Commit
        today = datetime.now().strftime("%Y-%m-%d")
        day_name = get_day_name()
        commit_msg = f"feat(blog): Add {skill_count} posts - {today} ({day_name})"

        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=REPO_DIR,
            check=True,
        )

        # Push
        subprocess.run(
            ["git", "push"],
            cwd=REPO_DIR,
            check=True,
        )

        log(f"커밋 & 푸시 완료: {commit_msg}")
        return True

    except subprocess.CalledProcessError as e:
        log(f"Git 작업 실패: {e}", "ERROR")
        return False


# ┌─────────────────────────────────────────────────────────┐
# │  Error Fix with AI Assistant                             │
# └─────────────────────────────────────────────────────────┘

def attempt_fix_with_ai_assistant(error_log: str) -> bool:
    """AI 어시스턴트를 사용하여 오류 수정 시도"""
    log("AI 어시스턴트로 오류 수정 시도...")

    prompt = f"""GitHub Actions 빌드가 실패했습니다. 아래 에러 로그를 분석하고 문제를 수정해주세요.

## 에러 로그
```
{error_log[:3000]}
```

## 요청사항
1. 에러 원인을 파악하세요
2. 해당 파일을 수정하세요
3. 수정 후 git add, commit, push 해주세요
4. 커밋 메시지: "fix: Resolve build error - [간단한 설명]"

수정이 불가능하면 "수정 불가"라고 답변해주세요.
"""

    try:
        result = subprocess.run(
            ["ai", "-p", "--model", "sonnet"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=REPO_DIR,
        )

        response = result.stdout.strip()
        print(f"AI 응답:\n{response[:500]}...")

        if "수정 불가" in response:
            log("AI 어시스턴트가 수정 불가 판단", "WARN")
            return False

        # 수정이 완료되었는지 확인
        git_result = subprocess.run(
            ["git", "log", "-1", "--format=%s"],
            capture_output=True,
            text=True,
            cwd=REPO_DIR,
        )

        if "fix:" in git_result.stdout.lower():
            log("오류 수정 커밋 완료!")
            return True
        else:
            log("수정 커밋이 생성되지 않음", "WARN")
            return False

    except Exception as e:
        log(f"AI 어시스턴트 수정 시도 실패: {e}", "ERROR")
        return False


# ┌─────────────────────────────────────────────────────────┐
# │  Main Logic                                              │
# └─────────────────────────────────────────────────────────┘

def run_daily_generation(target_count: Optional[int] = None) -> bool:
    """
    일일 스킬 생성 실행

    Args:
        target_count: 생성할 개수 (None이면 요일에 따라 자동 결정)

    Returns:
        성공 여부
    """
    # 생성 개수 결정
    if target_count is None:
        target_count = get_target_count()

    day_name = get_day_name()

    log("=" * 60)
    log(f"낙현아빠의 개발 블로그 - 일일 포스트 생성")
    log(f"오늘: {day_name}요일 / 목표: {target_count}개")
    log("=" * 60)

    # Step 1: 포스트 생성 (커밋 없이)
    success_count = generate_multiple_skills(target_count)

    if success_count == 0:
        log("생성된 포스트가 없습니다.", "ERROR")
        return False

    # Step 2: assets/downloads/로 복사
    log("\n>>> assets/downloads/로 복사")
    copy_to_downloads()

    # Step 3: 일괄 커밋 & 푸시
    log("\n>>> 일괄 커밋 & 푸시")
    if not commit_and_push(success_count):
        log("커밋/푸시 실패", "ERROR")
        return False

    # Step 4: Actions 완료 대기 및 오류 수정
    log("\n>>> GitHub Actions 검증")
    for attempt in range(MAX_FIX_ATTEMPTS):
        log(f"--- 검증 시도 {attempt + 1}/{MAX_FIX_ATTEMPTS} ---")

        status, error_log = wait_for_actions_completion()

        if status == "success":
            log("빌드 성공! 블로그 배포 완료!")
            return True

        elif status == "failure" and error_log:
            log(f"빌드 실패. 수정 시도 {attempt + 1}/{MAX_FIX_ATTEMPTS}")

            if attempt < MAX_FIX_ATTEMPTS - 1:
                if attempt_fix_with_ai_assistant(error_log):
                    log("수정 완료. Actions 재확인...")
                    time.sleep(10)
                    continue
                else:
                    log("수정 실패", "WARN")
            else:
                log("최대 수정 시도 횟수 도달", "ERROR")

        elif status == "timeout":
            log("Actions 타임아웃", "WARN")
            break

        else:
            log("알 수 없는 상태", "WARN")
            break

    log("작업 실패", "ERROR")
    return False


def main() -> None:
    """메인 엔트리 포인트"""
    import argparse

    # 로그 파일 초기화
    init_log_file()

    parser = argparse.ArgumentParser(description="낙현아빠의 개발 블로그 - 포스트 자동 생성")
    parser.add_argument(
        "--count",
        type=int,
        help=f"생성할 포스트 개수 (미지정 시 기본값: {DEFAULT_COUNT}개)",
    )
    args = parser.parse_args()

    # 생성 개수 결정
    target_count = args.count if args.count else None

    success = run_daily_generation(target_count)

    log("=" * 60)
    if success:
        log("작업 완료!")
    else:
        log("작업 실패")
    log("=" * 60)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
