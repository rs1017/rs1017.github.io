#!/usr/bin/env python3
"""
AI Skill Factory - 자동 생성 스크립트 (스케줄러용)

스케줄:
- 평일 (월-금): 12:30 1회 시도
- 주말 (토-일): 12:30~22:30 1시간 간격 10회 시도
- 오류 발생 시: 최대 5회 수정 시도

사용법:
    python auto_generate.py
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
WAIT_FOR_ACTIONS = 120  # Actions 완료 대기 시간 (초)


# ┌─────────────────────────────────────────────────────────┐
# │  Logging                                                 │
# └─────────────────────────────────────────────────────────┘

def log(message: str, level: str = "INFO") -> None:
    """로그 출력"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}", flush=True)


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
        # 최신 run 상태 확인
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
                # 실패 로그 가져오기
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
            log("✅ Actions 성공!")
            return "success", None
        elif status == "failure":
            log("❌ Actions 실패!")
            return "failure", error_log
        elif status == "pending":
            log("⏳ Actions 진행 중... (30초 후 재확인)")
            time.sleep(30)
        else:
            time.sleep(10)

    log("⏱️ Actions 대기 시간 초과", "WARN")
    return "timeout", None


# ┌─────────────────────────────────────────────────────────┐
# │  Skill Generation                                        │
# └─────────────────────────────────────────────────────────┘

def generate_skill() -> bool:
    """스킬 생성 실행"""
    log("🚀 스킬 생성 시작...")

    try:
        result = subprocess.run(
            [
                sys.executable,
                str(GENERATOR_SCRIPT),
                "--use-claude-cli",
                "--strategy", "auto",
                "--skip-validation",
                "--auto-git",
            ],
            capture_output=True,
            text=True,
            timeout=600,  # 10분 타임아웃
            cwd=REPO_DIR,
        )

        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        if result.returncode == 0:
            log("✅ 스킬 생성 완료!")
            return True
        else:
            log(f"❌ 스킬 생성 실패 (exit code: {result.returncode})", "ERROR")
            return False

    except subprocess.TimeoutExpired:
        log("⏱️ 스킬 생성 타임아웃", "ERROR")
        return False
    except Exception as e:
        log(f"❌ 스킬 생성 오류: {e}", "ERROR")
        return False


# ┌─────────────────────────────────────────────────────────┐
# │  Error Fix with Claude                                   │
# └─────────────────────────────────────────────────────────┘

def attempt_fix_with_claude(error_log: str) -> bool:
    """Claude를 사용하여 오류 수정 시도"""
    log("🔧 Claude로 오류 수정 시도...")

    prompt = f"""GitHub Actions 빌드가 실패했습니다. 아래 에러 로그를 분석하고 문제를 수정해주세요.

## 에러 로그
```
{error_log[:3000]}  # 로그 길이 제한
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
            ["claude", "-p", "--model", "sonnet"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=REPO_DIR,
        )

        response = result.stdout.strip()
        print(f"Claude 응답:\n{response[:500]}...")

        if "수정 불가" in response:
            log("Claude가 수정 불가 판단", "WARN")
            return False

        # 수정이 완료되었는지 git status로 확인
        git_result = subprocess.run(
            ["git", "log", "-1", "--format=%s"],
            capture_output=True,
            text=True,
            cwd=REPO_DIR,
        )

        if "fix:" in git_result.stdout.lower():
            log("✅ 오류 수정 커밋 완료!")
            return True
        else:
            log("수정 커밋이 생성되지 않음", "WARN")
            return False

    except Exception as e:
        log(f"Claude 수정 시도 실패: {e}", "ERROR")
        return False


# ┌─────────────────────────────────────────────────────────┐
# │  Main Logic                                              │
# └─────────────────────────────────────────────────────────┘

def run_with_retry() -> bool:
    """
    스킬 생성 실행 (오류 시 최대 5회 수정 시도)

    Returns:
        성공 여부
    """
    log("=" * 60)
    log("AI Skill Factory - 자동 생성 시작")
    log("=" * 60)

    # Step 1: 스킬 생성
    if not generate_skill():
        log("스킬 생성 단계에서 실패", "ERROR")
        return False

    # Step 2: Actions 완료 대기 및 결과 확인
    for attempt in range(MAX_FIX_ATTEMPTS):
        log(f"\n--- 검증 시도 {attempt + 1}/{MAX_FIX_ATTEMPTS} ---")

        status, error_log = wait_for_actions_completion()

        if status == "success":
            log("🎉 빌드 성공! 블로그 배포 완료!")
            return True

        elif status == "failure" and error_log:
            log(f"빌드 실패. 수정 시도 {attempt + 1}/{MAX_FIX_ATTEMPTS}")

            if attempt < MAX_FIX_ATTEMPTS - 1:
                if attempt_fix_with_claude(error_log):
                    log("수정 완료. Actions 재확인...")
                    time.sleep(10)  # push 후 Actions 시작 대기
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

    log("❌ 이번 차수 작업 실패", "ERROR")
    return False


def main() -> None:
    """메인 엔트리 포인트"""
    success = run_with_retry()

    log("=" * 60)
    if success:
        log("✅ 작업 완료!")
    else:
        log("❌ 작업 실패")
    log("=" * 60)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
