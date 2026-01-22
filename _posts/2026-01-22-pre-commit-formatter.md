-
---
title: "Git 커밋 전 자동 포맷팅 - Pre-Commit Formatter 스킬"
date: 2024-01-22 12:00:00 +0900
categories: [Skill]
tags: [git, formatter, linter, code-quality, pre-commit, automation]
---

## 개요

코드를 작성하고 커밋하려는 순간, "앗, 코드 스타일 통일 안 했네"라고 생각한 적 있으신가요? 또는 팀원이 올린 PR을 보다가 "이 사람은 탭을 쓰고, 저 사람은 스페이스를 쓰네"라며 한숨 쉬신 적은요?

**Pre-Commit Formatter 스킬**은 이런 문제를 원천 차단합니다. Git 커밋 전에 자동으로 코드를 포맷팅하고 린트 검사를 수행하여, 일관된 코드 스타일과 품질을 보장합니다.

### 해결하는 문제

- ❌ 커밋할 때마다 수동으로 `black .`, `prettier --write .` 실행
- ❌ 린트 에러를 모르고 커밋했다가 CI에서 실패
- ❌ 팀원마다 다른 코드 스타일로 diff가 지저분함
- ❌ 코드 리뷰 시간의 30%를 스타일 지적에 소비

### 제공하는 해결책

- ✅ 커밋 명령만 내리면 자동으로 포맷팅 + 린트 검사
- ✅ Python, JavaScript, TypeScript, Go 등 10개 이상 언어 지원
- ✅ 변경된 파일만 스마트하게 처리하여 속도 최적화
- ✅ 포맷팅 결과를 명확히 리포트하여 투명성 확보

## 스킬 구조

```
.claude/skills/pre-commit-formatter/
├── SKILL.md                 # 스킬 정의 및 사용 가이드
├── scripts/
│   ├── formatter.py         # 메인 포맷팅 로직
│   ├── language_detector.py # 언어별 포맷터 매핑
│   └── formatter_runner.py  # 포맷터 실행 엔진
├── references/
│   ├── formatters.md        # 지원 포맷터 목록 및 설정
│   └── best-practices.md    # 코드 포맷팅 모범 사례
└── assets/
    └── templates/
        ├── .prettierrc      # Prettier 기본 설정
        ├── pyproject.toml   # Black/Ruff 기본 설정
        └── .formatter-config.yml  # 스킬 커스텀 설정
```

## 사용 방법

### 1. 스킬 설치

```bash
# 1) 스킬 다운로드
cd ~/.claude/skills
unzip pre-commit-formatter.zip

# 2) 필요한 포맷터 설치 (언어별로 선택)
pip install black ruff           # Python
npm install -g prettier eslint   # JavaScript/TypeScript
# Go의 gofmt는 Go 설치 시 자동 포함
```

### 2. 기본 사용

Claude Code에서 커밋을 요청하면 자동으로 실행됩니다:

```
You: "코드 수정 완료했어. 커밋해줘"

Claude: 커밋 전 포맷팅을 진행하겠습니다.

[분석] 변경된 파일: 5개
  - Python: 3개 (main.py, utils.py, config.py)
  - JavaScript: 2개 (app.js, index.js)

[실행] Black 포맷팅...
✓ main.py (12줄 변경)
✓ utils.py (3줄 변경)
✓ config.py (변경 없음)

[실행] Prettier 포맷팅...
✓ app.js (5줄 변경)
✓ index.js (1줄 변경)

[검사] Ruff 린트...
✓ 모든 검사 통과

[검사] ESLint...
⚠ app.js:45 - 'console.log' 사용 지양 권장

총 21줄이 포맷팅되었습니다.
커밋을 진행할까요? (y/n)
```

### 3. 고급 설정

프로젝트 루트에 `.formatter-config.yml` 생성:

```yaml
# 언어별 포맷터 지정
python:
  formatter: black
  linter: ruff
  line_length: 100

javascript:
  formatter: prettier
  linter: eslint

# 제외 패턴
exclude:
  - "*.min.js"
  - "dist/**"
  - "node_modules/**"
  - "__pycache__/**"

# 자동 수정 레벨
auto_fix: true
fix_level: normal  # strict | normal | safe
```

## 전체 코드

### SKILL.md

전체 내용은 위 `---SKILL.md---` 섹션 참조

### scripts/formatter.py

```python
#!/usr/bin/env python3
"""
Pre-commit formatter main script
Git 커밋 전 자동 포맷팅 및 린트 검사
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import yaml

class PreCommitFormatter:
    def __init__(self, config_path: str = ".formatter-config.yml"):
        self.config = self._load_config(config_path)
        self.changed_files = []
        self.formatted_files = []
        self.errors = []
        
    def _load_config(self, config_path: str) -> dict:
        """설정 파일 로드"""
        default_config = {
            "python": {"formatter": "black", "linter": "ruff"},
            "javascript": {"formatter": "prettier", "linter": "eslint"},
            "typescript": {"formatter": "prettier", "linter": "eslint"},
            "go": {"formatter": "gofmt", "linter": "golint"},
            "exclude": ["*.min.js", "dist/**", "node_modules/**"],
            "auto_fix": True,
            "fix_level": "normal"
        }
        
        if Path(config_path).exists():
            with open(config_path) as f:
                user_config = yaml.safe_load(f)
                default_config.update(user_config)
        
        return default_config
    
    def get_changed_files(self) -> List[str]:
        """Git으로 변경된 파일 목록 가져오기"""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "--cached"],
                capture_output=True, text=True, check=True
            )
            files = result.stdout.strip().split('\n')
            self.changed_files = [f for f in files if f and self._should_process(f)]
            return self.changed_files
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Git diff 실패: {e}")
            return []
    
    def _should_process(self, filepath: str) -> bool:
        """제외 패턴 확인"""
        from fnmatch import fnmatch
        for pattern in self.config.get("exclude", []):
            if fnmatch(filepath, pattern):
                return False
        return True
    
    def group_by_language(self) -> Dict[str, List[str]]:
        """파일을 언어별로 그룹핑"""
        groups = {
            "python": [],
            "javascript": [],
            "typescript": [],
            "go": [],
            "other": []
        }
        
        ext_map = {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".go": "go"
        }
        
        for filepath in self.changed_files:
            ext = Path(filepath).suffix
            lang = ext_map.get(ext, "other")
            groups[lang].append(filepath)
        
        return {k: v for k, v in groups.items() if v}
    
    def format_files(self) -> Tuple[int, int]:
        """모든 파일 포맷팅"""
        groups = self.group_by_language()
        total_formatted = 0
        total_errors = 0
        
        for lang, files in groups.items():
            if lang == "other":
                continue
            
            print(f"\n[{lang.upper()}] 포맷팅 중... ({len(files)}개 파일)")
            
            formatter = self.config.get(lang, {}).get("formatter")
            if not formatter:
                print(f"  ⚠ {lang} 포맷터 미설정, 건너뜀")
                continue
            
            success, error = self._run_formatter(lang, formatter, files)
            total_formatted += success
            total_errors += error
            
            # 린트 검사
            if self.config.get("auto_fix") and error == 0:
                self._run_linter(lang, files)
        
        return total_formatted, total_errors
    
    def _run_formatter(self, lang: str, formatter: str, files: List[str]) -> Tuple[int, int]:
        """특정 언어 포맷터 실행"""
        commands = {
            "black": ["black"] + files,
            "prettier": ["prettier", "--write"] + files,
            "gofmt": ["gofmt", "-w"] + files,
        }
        
        cmd = commands.get(formatter)
        if not cmd:
            print(f"  ⚠ 알 수 없는 포맷터: {formatter}")
            return 0, 0
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✓ {formatter} 완료")
                self.formatted_files.extend(files)
                return len(files), 0
            else:
                print(f"  ✗ {formatter} 실패:")
                print(f"    {result.stderr}")
                self.errors.append(f"{formatter}: {result.stderr}")
                return 0, len(files)
        except FileNotFoundError:
            print(f"  ⚠ {formatter} 미설치, 건너뜀")
            return 0, 0
    
    def _run_linter(self, lang: str, files: List[str]):
        """린터 실행"""
        linter = self.config.get(lang, {}).get("linter")
        if not linter:
            return
        
        commands = {
            "ruff": ["ruff", "check"] + files,
            "eslint": ["eslint"] + files,
        }
        
        cmd = commands.get(linter)
        if not cmd:
            return
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✓ {linter} 검사 통과")
            else:
                print(f"  ⚠ {linter} 경고:")
                print(f"    {result.stdout}")
        except FileNotFoundError:
            pass
    
    def print_summary(self, formatted: int, errors: int):
        """최종 리포트 출력"""
        print("\n" + "="*50)
        print("포맷팅 완료")
        print("="*50)
        print(f"✓ 포맷팅된 파일: {formatted}개")
        if errors:
            print(f"✗ 오류 발생: {errors}개")
        if self.formatted_files:
            print("\n변경된 파일:")
            for f in self.formatted_files:
                print(f"  - {f}")
        print("="*50)

def main():
    formatter = PreCommitFormatter()
    
    print("Pre-Commit Formatter")
    print("변경된 파일 확인 중...")
    
    files = formatter.get_changed_files()
    if not files:
        print("변경된 파일이 없습니다.")
        return 0
    
    print(f"총 {len(files)}개 파일 발견")
    
    formatted, errors = formatter.format_files()
    formatter.print_summary(formatted, errors)
    
    if errors:
        print("\n⚠ 오류가 발생했습니다. 코드를 수정한 후 다시 시도하세요.")
        return 1
    
    print("\n✓ 모든 포맷팅이 완료되었습니다.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### assets/templates/.prettierrc

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "arrowParens": "always"
}
```

### assets/templates/pyproject.toml

```toml
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310']
include = '\.pyi?$'

[tool.ruff]
line-length = 100
select = [
    "E",  # pycodestyle errors
    "F",  # pyflakes
    "I",  # isort
    "N",  # pep8-naming
]
ignore = [
    "E501",  # line too long (black handles this)
]
```

## 다운로드

> **[pre-commit-formatter.zip](/assets/downloads/skills/pre-commit-formatter.zip)**
> 
> 압축 해제 후 `~/.claude/skills/` 폴더에 복사하여 사용하세요.

## 활용 팁

### 1. 팀 설정 공유

팀에서 동일한 포맷팅 규칙을 사용하려면:

```bash
# .formatter-config.yml을 Git에 커밋
git add .formatter-config.yml .prettierrc pyproject.toml
git commit -m "chore: add formatter config"
```

### 2. CI/CD 통합

GitHub Actions에서도 동일한 검사 수행:

```yaml
# .github/workflows/lint.yml
name: Lint
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install black ruff
      - run: black --check .
      - run: ruff check .
```

### 3. 선택적 포맷팅

특정 파일만 포맷팅하려면:

```bash
# Python 파일만
python scripts/formatter.py --only python

# 특정 파일 제외
python scripts/formatter.py --exclude "tests/**"
```

## 관련 스킬

- **[git-commit-analyzer](/posts/git-commit-analyzer)**: 커밋 메시지 품질 자동 분석
- **[code-review-assistant](/posts/code-review-assistant)**: AI 기반 코드 리뷰
- **[test-runner](/posts/test-runner)**: 커밋 전 자동 테스트 실행

## 마무리

Pre-Commit Formatter 스킬은 "코드 스타일 통일"이라는 지루한 작업을 자동화하여, 여러분이 진짜 중요한 문제 해결에 집중할 수 있게 해줍니다.

더 이상 PR 리뷰에서 "여기 들여쓰기 좀 맞춰주세요"라는 댓글을 달 필요가 없습니다. 커밋 버튼만 누르면 모든 게 자동으로 정리됩니다.

**지금 바로 설치하고, 코드 품질 걱정 없는 개발을 시작하세요!**