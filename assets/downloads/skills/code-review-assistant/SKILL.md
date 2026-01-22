---
name: code-review-assistant
description: Pull Request나 코드 변경사항을 분석하여 구조화된 리뷰 코멘트를 생성합니다. 코드 품질, 버그, 성능, 보안 이슈를 자동으로 체크하고 개선 제안을 제공합니다.
---

# Code Review Assistant Skill

## 주요 기능

1. **다층 분석**: Critical / Quality / Suggestion
2. **언어별 전문 분석**: Python, JS/TS, Java, C++, Go
3. **컨텍스트 인식**: Diff 비교, 영향도 분석

## 사용 시점

- Pull Request 리뷰 필요시
- 커밋 전 품질 검증
- 팀 리뷰 전 사전 체크

(전체 내용은 위 SKILL.md 섹션 참조)
```

### scripts/review_analyzer.py

```python
#!/usr/bin/env python3
"""
Git diff를 분석하여 리뷰 가능한 형태로 변환
"""
import subprocess
import re
from typing import List, Dict

class ReviewAnalyzer:
    def __init__(self, target='HEAD'):
        self.target = target
    
    def get_changed_files(self) -> List[str]:
        """변경된 파일 목록 추출"""
        result = subprocess.run(
            ['git', 'diff', '--name-only', self.target],
            capture_output=True,
            text=True
        )
        return result.stdout.strip().split('\n')
    
    def get_file_diff(self, filepath: str) -> Dict:
        """파일별 diff 정보"""
        result = subprocess.run(
            ['git', 'diff', self.target, '--', filepath],
            capture_output=True,
            text=True
        )
        
        diff = result.stdout
        stats = self._parse_stats(diff)
        hunks = self._parse_hunks(diff)
        
        return {
            'file': filepath,
            'language': self._detect_language(filepath),
            'stats': stats,
            'hunks': hunks
        }
    
    def _parse_stats(self, diff: str) -> Dict:
        """추가/삭제 라인 통계"""
        added = len(re.findall(r'^\+[^+]', diff, re.MULTILINE))
        removed = len(re.findall(r'^-[^-]', diff, re.MULTILINE))
        return {'added': added, 'removed': removed}
    
    def _parse_hunks(self, diff: str) -> List[Dict]:
        """변경 블록 파싱"""
        hunks = []
        current_hunk = None
        
        for line in diff.split('\n'):
            if line.startswith('@@'):
                if current_hunk:
                    hunks.append(current_hunk)
                current_hunk = {
                    'header': line,
                    'lines': []
                }
            elif current_hunk:
                current_hunk['lines'].append(line)
        
        if current_hunk:
            hunks.append(current_hunk)
        
        return hunks
    
    def _detect_language(self, filepath: str) -> str:
        """파일 확장자로 언어 감지"""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.go': 'go',
            '.rs': 'rust'
        }
        
        for ext, lang in ext_map.items():
            if filepath.endswith(ext):
                return lang
        
        return 'unknown'

if __name__ == '__main__':
    analyzer = ReviewAnalyzer()
    files = analyzer.get_changed_files()
    
    for file in files:
        if file:
            analysis = analyzer.get_file_diff(file)
            print(f"\n{file}:")
            print(f"  Language: {analysis['language']}")
            print(f"  +{analysis['stats']['added']} -{analysis['stats']['removed']}")
```

### scripts/issue_detector.py

```python
#!/usr/bin/env python3
"""
코드 이슈 탐지 엔진
"""
import re
from typing import List, Dict
from dataclasses import dataclass
from enum import Enum

class Severity(Enum):
    CRITICAL = "🔴 Critical"
    QUALITY = "🟡 Quality"
    SUGGESTION = "🟢 Suggestion"

@dataclass
class Issue:
    severity: Severity
    title: str
    file: str
    line: int
    description: str
    current_code: str
    suggested_code: str = None

class IssueDetector:
    def __init__(self, language: str):
        self.language = language
        self.rules = self._load_rules()
    
    def detect(self, code: str, filepath: str) -> List[Issue]:
        """코드에서 이슈 탐지"""
        issues = []
        
        # 보안 이슈
        issues.extend(self._check_security(code, filepath))
        
        # 코드 품질
        issues.extend(self._check_quality(code, filepath))
        
        # 개선 제안
        issues.extend(self._check_suggestions(code, filepath))
        
        return issues
    
    def _check_security(self, code: str, filepath: str) -> List[Issue]:
        """보안 취약점 체크"""
        issues = []
        
        if self.language == 'python':
            # SQL Injection
            if re.search(r'execute\([^)]*f["\'].*\{', code):
                issues.append(Issue(
                    severity=Severity.CRITICAL,
                    title="Potential SQL Injection",
                    file=filepath,
                    line=self._find_line(code, r'execute\('),
                    description="f-string을 SQL 쿼리에 직접 사용하면 SQL Injection 위험",
                    current_code='query = f"SELECT * FROM users WHERE id = {user_id}"',
                    suggested_code='query = "SELECT * FROM users WHERE id = %s"\ncursor.execute(query, (user_id,))'
                ))
        
        elif self.language == 'javascript':
            # eval 사용
            if 'eval(' in code:
                issues.append(Issue(
                    severity=Severity.CRITICAL,
                    title="Dangerous eval() usage",
                    file=filepath,
                    line=self._find_line(code, 'eval\\('),
                    description="eval()은 XSS 공격에 취약합니다",
                    current_code='eval(userInput)',
                    suggested_code='JSON.parse(userInput)  // 또는 다른 안전한 방법'
                ))
        
        return issues
    
    def _check_quality(self, code: str, filepath: str) -> List[Issue]:
        """코드 품질 체크"""
        issues = []
        
        # 복잡도 체크
        complexity = self._calculate_complexity(code)
        if complexity > 10:
            issues.append(Issue(
                severity=Severity.QUALITY,
                title="High Complexity",
                file=filepath,
                line=1,
                description=f"Cyclomatic Complexity: {complexity} (권장: < 10)",
                current_code="# 현재 함수가 너무 복잡함",
                suggested_code="# 작은 함수들로 분리 필요"
            ))
        
        # 중복 코드
        duplicates = self._find_duplicates(code)
        if duplicates:
            issues.append(Issue(
                severity=Severity.QUALITY,
                title="Code Duplication",
                file=filepath,
                line=duplicates[0],
                description="중복된 코드 블록 발견",
                current_code="# 동일한 로직이 반복됨"
            ))
        
        return issues
    
    def _check_suggestions(self, code: str, filepath: str) -> List[Issue]:
        """개선 제안"""
        issues = []
        
        if self.language == 'python':
            # Type hints 부재
            if re.search(r'def \w+\([^)]*\):', code) and '->' not in code:
                issues.append(Issue(
                    severity=Severity.SUGGESTION,
                    title="Add Type Hints",
                    file=filepath,
                    line=self._find_line(code, r'def '),
                    description="타입 힌트를 추가하면 IDE 지원과 버그 예방에 도움",
                    current_code='def get_user(user_id):',
                    suggested_code='def get_user(user_id: int) -> Optional[User]:'
                ))
        
        return issues
    
    def _calculate_complexity(self, code: str) -> int:
        """Cyclomatic Complexity 계산"""
        # 간단한 근사치: if, for, while, and, or 개수 + 1
        keywords = len(re.findall(r'\b(if|for|while|and|or|elif|except)\b', code))
        return keywords + 1
    
    def _find_duplicates(self, code: str) -> List[int]:
        """중복 코드 블록 찾기 (간단한 버전)"""
        lines = code.split('\n')
        seen = {}
        duplicates = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if len(line) > 20:  # 의미있는 길이의 라인만
                if line in seen:
                    duplicates.append(i + 1)
                else:
                    seen[line] = i + 1
        
        return duplicates
    
    def _find_line(self, code: str, pattern: str) -> int:
        """패턴이 있는 라인 번호 찾기"""
        for i, line in enumerate(code.split('\n'), 1):
            if re.search(pattern, line):
                return i
        return 1
    
    def _load_rules(self) -> Dict:
        """언어별 규칙 로드"""
        # 실제로는 YAML 파일에서 로드
        return {}

if __name__ == '__main__':
    detector = IssueDetector('python')
    
    test_code = """
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
"""
    
    issues = detector.detect(test_code, 'test.py')
    for issue in issues:
        print(f"{issue.severity.value}: {issue.title}")
        print(f"  File: {issue.file}:{issue.line}")
        print(f"  {issue.description}")
```

## 다운로드

> 📁 [SKILL.md 보기](/assets/downloads/skills/code-review-assistant/SKILL.html)

설치 방법:
```bash
# 1. 스킬 폴더 생성
mkdir -p ~/.claude/skills/code-review-assistant/

# 2. SKILL.md 복사 (블로그에서 다운로드)
# ~/.claude/skills/code-review-assistant/SKILL.md

# 3. Claude Code에서 사용
code-review-assistant를 사용해서 현재 PR을 리뷰해줘
```

## 활용 팁

### 1. 팀 규칙 커스터마이징

```yaml
# .claude/skills/code-review-assistant/team-rules.yml
project_conventions:
  naming:
    - "클래스는 PascalCase"
    - "함수는 snake_case"
  patterns:
    - "DTO는 dataclass 사용"
    - "Service는 싱글톤"
  
security_baseline:
  - "API 키는 환경변수"
  - "민감 로그 금지"
```

### 2. 리뷰 필터링

```bash
# Critical만 체크
claude "Critical 이슈만 리포트해줘" < current.diff

# 특정 영역만
claude "보안과 성능 관점에서만 리뷰" < current.diff
```

### 3. 학습 모드

```bash
# 좋은 패턴 학습
claude "이 코드의 좋은 점을 분석해줘" < best-practice.py

# 나쁜 패턴 학습
claude "이 코드의 안티패턴을 찾아줘" < legacy-code.java
```

## 제한사항 및 주의사항

1. **AI 판단의 한계**: 비즈니스 로직의 정확성은 사람이 검증 필요
2. **컨텍스트 부족**: 프로젝트 전체 맥락을 완벽히 이해하기 어려움
3. **False Positive**: 일부 제안은 프로젝트 특성상 적용 불가할 수 있음
4. **최종 결정은 개발자**: AI는 보조 도구일 뿐

## 관련 스킬

- **[test-case-auto-generator](/posts/test-case-auto-generator/)**: 테스트 케이스 자동 생성
- **[pre-commit-formatter](/posts/pre-commit-formatter/)**: 커밋 전 포맷팅 자동화

## 마무리

Code Review Assistant는 **코드 리뷰의 효율성을 10배 높여주는** 도구입니다.

반복적인 패턴 체크는 AI에게 맡기고, 개발자는 창의적인 문제 해결에 집중하세요. 완벽한 리뷰는 불가능하지만, 일관된 품질 기준을 유지하는 데 큰 도움이 됩니다.

지금 바로 다운로드하여 당신의 코드베이스에 적용해보세요! 🚀