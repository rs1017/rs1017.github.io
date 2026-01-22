---

# Pre-Commit Formatter Skill

코드 커밋 전 자동 포맷팅 및 린트 검사를 수행하여 코드 품질을 보장하는 스킬입니다.

## 사용 시점

다음과 같은 상황에서 이 스킬을 사용하세요:

- 사용자가 "커밋해줘", "commit" 등의 요청을 할 때
- 코드 변경 후 Git 커밋을 수행하기 전
- 코드 리뷰 전 코드 스타일 통일이 필요할 때
- 팀 코딩 컨벤션 준수가 필요할 때

## 주요 기능

1. **자동 언어 감지**: 변경된 파일의 확장자를 분석하여 사용할 포맷터 결정
2. **멀티 포맷터 지원**: Python(black, ruff), JavaScript/TypeScript(prettier), Go(gofmt) 등
3. **린트 검사**: 포맷팅 후 린트 도구로 코드 품질 검증
4. **변경 사항 리포트**: 포맷팅으로 수정된 파일 목록 출력
5. **에러 핸들링**: 포맷팅 실패 시 사용자에게 명확한 안내

## 작동 방식

```
1. git status로 변경된 파일 목록 확인
   ↓
2. 파일 확장자별 그룹핑 (.py, .js, .ts, .go 등)
   ↓
3. 각 언어별 포맷터 실행
   - Python: black . && ruff check --fix .
   - JavaScript/TypeScript: prettier --write .
   - Go: gofmt -w .
   ↓
4. 린트 검사 (선택적)
   - Python: ruff check .
   - JavaScript: eslint .
   ↓
5. 포맷팅 결과 리포트 출력
   ↓
6. 사용자에게 커밋 진행 여부 확인
```

## 사용 예시

### 기본 사용

```
사용자: "코드 수정했어. 커밋해줘"

Claude: 커밋 전에 코드 포맷팅을 진행하겠습니다.

[변경된 파일 분석]
- Python 파일: 3개
- JavaScript 파일: 2개

[포맷팅 실행]
✓ black으로 Python 파일 포맷팅 완료
✓ prettier로 JavaScript 파일 포맷팅 완료

[린트 검사]
✓ ruff 검사 통과
✓ eslint 검사 통과

[수정된 파일]
- src/main.py (2줄 변경)
- src/utils.py (5줄 변경)
- public/app.js (1줄 변경)

포맷팅이 완료되었습니다. 커밋을 진행할까요?
```

### 에러 발생 시

```
사용자: "커밋해"

Claude: 커밋 전 포맷팅을 시도합니다.

[포맷팅 실행]
✗ black 실행 실패: SyntaxError in src/broken.py

src/broken.py:15에 문법 오류가 있습니다.
먼저 코드를 수정한 후 다시 시도해주세요.

커밋을 중단합니다.
```

## 설정 방법

### 1. 포맷터 설치

```bash
# Python
pip install black ruff

# JavaScript/TypeScript
npm install -g prettier eslint

# Go
# gofmt는 Go 설치 시 포함됨
```

### 2. 설정 파일 생성 (선택)

**pyproject.toml** (Python)
```toml
[tool.black]
line-length = 88
target-version = ['py38']

[tool.ruff]
line-length = 88
select = ["E", "F", "I"]
```

**.prettierrc** (JavaScript/TypeScript)
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

### 3. Claude Code에서 활성화

이 스킬은 자동으로 커밋 관련 명령을 감지합니다. 별도 활성화 불필요합니다.

## 지원 언어 및 도구

| 언어 | 포맷터 | 린터 | 확장자 |
|------|--------|------|--------|
| Python | black, autopep8 | ruff, flake8 | .py |
| JavaScript | prettier | eslint | .js, .jsx |
| TypeScript | prettier | eslint | .ts, .tsx |
| Go | gofmt, goimports | golint | .go |
| Rust | rustfmt | clippy | .rs |
| Java | google-java-format | checkstyle | .java |
| C/C++ | clang-format | clang-tidy | .c, .cpp, .h |
| JSON | prettier | - | .json |
| YAML | prettier | yamllint | .yml, .yaml |
| Markdown | prettier | markdownlint | .md |

## 커스터마이징

### 포맷터 우선순위 변경

특정 언어에 대해 선호하는 포맷터를 지정하려면 프로젝트 루트에 `.formatter-config.yml` 생성:

```yaml
python:
  formatter: black  # 또는 autopep8
  linter: ruff      # 또는 flake8

javascript:
  formatter: prettier
  linter: eslint

# 포맷팅 제외 패턴
exclude:
  - "*.min.js"
  - "dist/**"
  - "build/**"
```

### 자동 수정 레벨 조정

```yaml
auto_fix_level: strict  # strict | normal | safe
# strict: 모든 수정 가능한 이슈 자동 수정
# normal: 안전한 수정만 자동 적용
# safe: 포맷팅만 수행, 린트는 경고만
```

## 주의사항

1. **도구 설치 확인**: 포맷터가 설치되지 않은 경우 해당 언어는 건너뜁니다
2. **큰 파일 처리**: 1000줄 이상 파일은 포맷팅 시간이 오래 걸릴 수 있습니다
3. **병합 충돌**: 포맷팅으로 인한 diff가 크면 병합 충돌 가능성 증가
4. **팀 규칙**: 팀에서 사용하는 포맷터 설정과 동일하게 유지 필요

## 트러블슈팅

### 포맷터가 실행되지 않음
- 포맷터 설치 여부 확인: `black --version`, `prettier --version`
- PATH 환경변수에 포맷터 경로 추가 확인

### 포맷팅 결과가 예상과 다름
- 프로젝트의 설정 파일 확인 (.prettierrc, pyproject.toml 등)
- 포맷터 버전 확인 (팀원과 동일한 버전 사용 권장)

### 린트 에러로 커밋 차단됨
- 린트 에러 메시지 확인 후 코드 수정
- 또는 일시적으로 린트 무시: `# noqa` (Python), `// eslint-disable-next-line` (JS)

## 관련 스킬

- **git-commit-analyzer**: 커밋 메시지 품질 분석
- **code-review-assistant**: 코드 리뷰 자동화
- **pre-push-validator**: 푸시 전 테스트 실행

## 참고 자료

- [Black - Python Code Formatter](https://black.readthedocs.io/)
- [Prettier - Code Formatter](https://prettier.io/)
- [Ruff - Python Linter](https://docs.astral.sh/ruff/)
- [ESLint - JavaScript Linter](https://eslint.org/)