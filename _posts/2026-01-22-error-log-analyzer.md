-
---
layout: post
title: "에러 로그 자동 분석 스킬로 장애 대응 시간 단축하기"
date: 2026-01-22 12:00:00 +0900
categories: [AI, Skill]
tags: [error, log, analysis, debugging, monitoring, troubleshooting]
---

## 개요

프로덕션 환경에서 장애가 발생하면 개발자는 수천 줄의 로그 파일을 뒤져야 합니다. 반복되는 에러를 수작업으로 찾고, 패턴을 파악하고, 원인을 추론하는 과정은 시간이 오래 걸릴 뿐만 아니라 실수하기 쉽습니다.

**error-log-analyzer** 스킬은 이런 반복적이고 시간 소모적인 작업을 자동화합니다. 로그 파일에서 에러를 추출하고, 패턴별로 그룹화하며, 발생 빈도와 시간대를 분석하여 마크다운 리포트를 생성합니다.

## 스킬 구조

```
.claude/skills/error-log-analyzer/
├── SKILL.md                 # 스킬 정의 및 사용법
├── scripts/
│   ├── analyzer.py         # 로그 파싱 및 분석 엔진
│   ├── parser.py           # 다양한 로그 형식 파서
│   └── reporter.py         # 마크다운 리포트 생성기
├── references/
│   └── common-errors.yaml  # 일반적인 에러와 해결책 DB
└── assets/
    └── report-template.md  # 리포트 템플릿
```

## 사용 방법

### 1. 스킬 설치

`.claude/skills/` 폴더에 `error-log-analyzer` 스킬을 배치합니다.

### 2. 기본 사용

Claude Code에서 로그 분석을 요청합니다:

```
error-log-analyzer를 사용해서 logs/app.log를 분석해주세요
```

또는 자연어로:

```
최근 24시간 에러 로그를 분석하고 리포트 생성해줘
```

### 3. 옵션 지정

분석 옵션을 함께 전달할 수 있습니다:

```
error-log-analyzer로 app.log를 분석하되,
- 최근 24시간만
- ERROR와 FATAL만
- 발생 횟수 5회 이상만 리포트에 포함
```

## 전체 코드

### SKILL.md

```markdown
---
name: error-log-analyzer
description: 로그 파일에서 에러를 추출하고 패턴을 분석하여 원인과 해결책을 제시하는 스킬. 에러 로그 분석이 필요할 때 사용
version: 1.0.0
author: AI Skill Factory
---

# Error Log Analyzer

(위 SKILL.md 내용과 동일)
```

### scripts/analyzer.py

```python
"""
에러 로그 분석 메인 엔진
"""
import re
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Optional
from parser import LogParser
from reporter import ReportGenerator


class ErrorLogAnalyzer:
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.parser = LogParser()
        self.errors = []
        self.patterns = defaultdict(list)
        
    def analyze_file(self, log_path: str) -> Dict:
        """로그 파일 분석"""
        log_path = Path(log_path)
        if not log_path.exists():
            raise FileNotFoundError(f"Log file not found: {log_path}")
        
        # 1. 로그 파싱
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                parsed = self.parser.parse_line(line)
                if parsed and parsed['level'] in ['ERROR', 'FATAL', 'CRITICAL']:
                    parsed['line_number'] = line_num
                    self.errors.append(parsed)
        
        # 2. 시간 범위 필터링
        if 'time_range' in self.config:
            self._filter_by_time_range()
        
        # 3. 패턴 그룹화
        self._group_by_pattern()
        
        # 4. 통계 생성
        stats = self._generate_statistics()
        
        # 5. 해결책 매칭
        self._match_solutions()
        
        return {
            'file': str(log_path),
            'total_errors': len(self.errors),
            'patterns': self.patterns,
            'statistics': stats
        }
    
    def _filter_by_time_range(self):
        """시간 범위 필터링"""
        time_range = self.config['time_range']
        now = datetime.now()
        
        # 시간 범위 파싱 (예: "24h", "7d")
        match = re.match(r'(\d+)([hd])', time_range)
        if match:
            value, unit = int(match.group(1)), match.group(2)
            if unit == 'h':
                cutoff = now - timedelta(hours=value)
            else:  # 'd'
                cutoff = now - timedelta(days=value)
            
            self.errors = [
                e for e in self.errors 
                if e.get('timestamp') and e['timestamp'] >= cutoff
            ]
    
    def _group_by_pattern(self):
        """에러를 패턴별로 그룹화"""
        for error in self.errors:
            # 에러 메시지에서 변수 부분 제거하여 패턴 추출
            message = error.get('message', '')
            pattern = self._extract_pattern(message)
            
            self.patterns[pattern].append(error)
    
    def _extract_pattern(self, message: str) -> str:
        """에러 메시지에서 패턴 추출"""
        # 숫자, UUID, 파일 경로 등을 일반화
        pattern = re.sub(r'\d+', '{N}', message)
        pattern = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '{UUID}', pattern)
        pattern = re.sub(r'/[\w/.-]+', '{PATH}', pattern)
        return pattern
    
    def _generate_statistics(self) -> Dict:
        """통계 생성"""
        stats = {
            'by_pattern': {},
            'by_hour': defaultdict(int),
            'by_severity': defaultdict(int)
        }
        
        # 패턴별 통계
        for pattern, errors in self.patterns.items():
            stats['by_pattern'][pattern] = {
                'count': len(errors),
                'percentage': len(errors) / len(self.errors) * 100,
                'first_seen': min(e['timestamp'] for e in errors if 'timestamp' in e),
                'last_seen': max(e['timestamp'] for e in errors if 'timestamp' in e),
                'locations': list(set(e.get('location', 'unknown') for e in errors))
            }
        
        # 시간대별 통계
        for error in self.errors:
            if 'timestamp' in error:
                hour = error['timestamp'].hour
                stats['by_hour'][hour] += 1
        
        # 심각도별 통계
        for error in self.errors:
            level = error.get('level', 'UNKNOWN')
            stats['by_severity'][level] += 1
        
        return stats
    
    def _match_solutions(self):
        """일반적인 에러에 대한 해결책 매칭"""
        # common-errors.yaml에서 로드한 해결책 DB와 매칭
        # (실제 구현에서는 YAML 파일 로드)
        solutions_db = {
            'Connection timeout': {
                'cause': 'DB 커넥션 풀 고갈 또는 네트워크 지연',
                'solutions': [
                    '커넥션 풀 크기 증가',
                    '타임아웃 설정 조정',
                    '커넥션 리크 확인'
                ]
            },
            'NullPointerException': {
                'cause': 'Null 참조 접근',
                'solutions': [
                    'Null 체크 추가',
                    'Optional 사용',
                    '방어적 프로그래밍'
                ]
            }
        }
        
        for pattern, errors in self.patterns.items():
            for key, solution in solutions_db.items():
                if key.lower() in pattern.lower():
                    errors[0]['solution'] = solution
                    break


def main(log_file: str, config: Dict = None):
    """메인 실행 함수"""
    analyzer = ErrorLogAnalyzer(config)
    result = analyzer.analyze_file(log_file)
    
    # 리포트 생성
    reporter = ReportGenerator()
    report = reporter.generate(result)
    
    # 리포트 저장
    output_path = Path('error-analysis-report.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 분석 완료: {output_path}")
    return result


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <log_file>")
        sys.exit(1)
    
    main(sys.argv[1])
```

### scripts/parser.py

```python
"""
다양한 로그 형식 파서
"""
import re
from datetime import datetime
from typing import Optional, Dict


class LogParser:
    """로그 라인 파서"""
    
    # 로그 형식 패턴
    PATTERNS = [
        # Java/Spring: 2026-01-22 09:15:23.123 [thread] ERROR class - message
        {
            'regex': r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[(.+?)\] (\w+) (.+?) - (.+)',
            'groups': ['timestamp', 'thread', 'level', 'location', 'message'],
            'timestamp_format': '%Y-%m-%d %H:%M:%S.%f'
        },
        # Python: ERROR:root:message
        {
            'regex': r'(\w+):(.+?):(.+)',
            'groups': ['level', 'logger', 'message'],
            'timestamp_format': None
        },
        # Generic: [2026-01-22 09:15:23] ERROR: message
        {
            'regex': r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (\w+): (.+)',
            'groups': ['timestamp', 'level', 'message'],
            'timestamp_format': '%Y-%m-%d %H:%M:%S'
        }
    ]
    
    def parse_line(self, line: str) -> Optional[Dict]:
        """로그 라인 파싱"""
        line = line.strip()
        if not line:
            return None
        
        for pattern_def in self.PATTERNS:
            match = re.match(pattern_def['regex'], line)
            if match:
                result = {}
                for i, group_name in enumerate(pattern_def['groups'], 1):
                    result[group_name] = match.group(i)
                
                # 타임스탬프 파싱
                if 'timestamp' in result and pattern_def['timestamp_format']:
                    try:
                        result['timestamp'] = datetime.strptime(
                            result['timestamp'], 
                            pattern_def['timestamp_format']
                        )
                    except ValueError:
                        pass
                
                return result
        
        return None
```

### scripts/reporter.py

```python
"""
마크다운 리포트 생성기
"""
from datetime import datetime
from typing import Dict


class ReportGenerator:
    """리포트 생성"""
    
    def generate(self, analysis_result: Dict) -> str:
        """마크다운 리포트 생성"""
        report = []
        report.append("# 에러 로그 분석 리포트\n")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 요약
        report.append("## 📊 요약\n")
        report.append(f"- 분석 파일: {analysis_result['file']}")
        report.append(f"- 총 에러 수: {analysis_result['total_errors']}건")
        report.append(f"- 고유 에러 패턴: {len(analysis_result['patterns'])}개\n")
        
        # 상위 에러 패턴
        report.append("## 🔥 상위 에러 패턴\n")
        
        # 빈도순 정렬
        sorted_patterns = sorted(
            analysis_result['statistics']['by_pattern'].items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )
        
        for i, (pattern, stats) in enumerate(sorted_patterns[:10], 1):
            report.append(f"### {i}. {pattern} ({stats['count']}건, {stats['percentage']:.1f}%)\n")
            report.append(f"**발생 위치**: {', '.join(stats['locations'][:3])}")
            
            # 해결책이 있으면 추가
            errors = analysis_result['patterns'][pattern]
            if errors and 'solution' in errors[0]:
                solution = errors[0]['solution']
                report.append(f"\n**원인**: {solution['cause']}")
                report.append("\n**해결 방안**:")
                for j, sol in enumerate(solution['solutions'], 1):
                    report.append(f"{j}. {sol}")
            
            report.append("\n")
        
        # 시간대별 분석
        report.append("## 📈 시간대별 분석\n")
        report.append("```")
        
        by_hour = analysis_result['statistics']['by_hour']
        max_count = max(by_hour.values()) if by_hour else 1
        
        for hour in range(24):
            count = by_hour.get(hour, 0)
            bar_length = int(count / max_count * 10) if max_count > 0 else 0
            bar = '▇' * bar_length or '▁'
            report.append(f"{hour:02d}:00-{hour+1:02d}:00: {bar} ({count}건)")
        
        report.append("```\n")
        
        # 권장 조치사항
        report.append("## 💡 권장 조치사항\n")
        report.append("### 🚨 긴급 (24시간 내)")
        report.append("- (상위 에러 기반 자동 생성)\n")
        report.append("### ⚠️ 중요 (1주일 내)")
        report.append("- (중간 빈도 에러 기반 자동 생성)\n")
        
        return '\n'.join(report)
```

### references/common-errors.yaml

```yaml
# 일반적인 에러와 해결책 데이터베이스

database:
  - pattern: "Connection timeout"
    cause: "DB 커넥션 풀 고갈 또는 네트워크 지연"
    solutions:
      - "커넥션 풀 크기 증가 (현재 설정 확인)"
      - "커넥션 타임아웃 설정 조정"
      - "커넥션 리크 확인 (미반환 커넥션)"
      - "DB 서버 부하 점검"
    
  - pattern: "Deadlock detected"
    cause: "트랜잭션 간 리소스 경쟁"
    solutions:
      - "트랜잭션 순서 일관성 확보"
      - "트랜잭션 범위 최소화"
      - "잠금 타임아웃 설정"

application:
  - pattern: "NullPointerException"
    cause: "Null 참조 객체 접근"
    solutions:
      - "Null 체크 로직 추가"
      - "Optional 사용"
      - "방어적 프로그래밍 적용"
  
  - pattern: "OutOfMemoryError"
    cause: "힙 메모리 부족"
    solutions:
      - "JVM 힙 크기 증가 (-Xmx)"
      - "메모리 누수 확인 (프로파일링)"
      - "대용량 객체 처리 방식 개선"

network:
  - pattern: "SocketTimeoutException"
    cause: "네트워크 요청 타임아웃"
    solutions:
      - "타임아웃 설정 증가"
      - "외부 API 응답 시간 점검"
      - "재시도 로직 추가"
```

## 실행 예시

### 1. CLI에서 직접 실행

```bash
cd .claude/skills/error-log-analyzer/scripts
python analyzer.py /var/log/app.log
```

### 2. Claude Code에서 실행

```
error-log-analyzer로 logs/production.log를 분석해줘.
최근 12시간, ERROR 이상만, 3회 이상 발생한 것만 포함해줘.
```

### 생성된 리포트 예시

```markdown
# 에러 로그 분석 리포트
Generated: 2026-01-22 14:30:00

## 📊 요약
- 분석 파일: logs/production.log
- 총 에러 수: 347건
- 고유 에러 패턴: 12개

## 🔥 상위 에러 패턴

### 1. Connection timeout after {N}ms (142건, 40.9%)
**발생 위치**: DatabasePool.java:89, UserRepository.java:45

**원인**: DB 커넥션 풀 고갈 또는 네트워크 지연

**해결 방안**:
1. 커넥션 풀 크기 증가 (현재 설정 확인)
2. 커넥션 타임아웃 설정 조정
3. 커넥션 리크 확인 (미반환 커넥션)
4. DB 서버 부하 점검

### 2. NullPointerException at User.getName() (78건, 22.5%)
...

## 📈 시간대별 분석
```
00:00-01:00: ▁ (3건)
01:00-02:00: ▁ (1건)
...
09:00-10:00: ▇▇▇▇▇▇▇▇▇▇ (142건)
...
```

## 💡 권장 조치사항

### 🚨 긴급 (24시간 내)
- DB 커넥션 풀 설정 점검 및 조정

### ⚠️ 중요 (1주일 내)
- Null 체크 로직 추가 (User, Order 관련)
```

## 활용 시나리오

### 시나리오 1: 새벽 장애 대응

```
상황: 새벽 3시 장애 알림 수신
대응:
1. "error-log-analyzer로 최근 1시간 로그 분석해줘"
2. 리포트에서 가장 빈번한 에러 확인 (Connection timeout)
3. 즉시 DB 커넥션 풀 크기 증가
4. 5분 뒤 재분석하여 에러 감소 확인
```

### 시나리오 2: 주간 에러 리뷰

```
상황: 매주 월요일 에러 리뷰 미팅
대응:
1. "지난 7일간 에러 로그 분석 리포트 생성해줘"
2. 상위 10개 에러 패턴 리뷰
3. 각 패턴별 해결 티켓 생성
4. 다음 주 비교를 위해 리포트 보관
```

## 확장 아이디어

이 스킬을 기반으로 다음과 같은 확장이 가능합니다:

1. **실시간 모니터링**: 로그 파일을 tail하며 실시간 에러 감지
2. **알림 통합**: Slack/Email로 긴급 에러 자동 알림
3. **이슈 자동 생성**: GitHub/Jira에 에러 패턴별 이슈 자동 등록
4. **대시보드**: Grafana/Kibana 연동 시각화
5. **ML 기반 이상 감지**: 평소와 다른 에러 패턴 자동 탐지

## 다운로드

> [error-log-analyzer.zip](/assets/downloads/skills/error-log-analyzer.zip)

## 관련 스킬

- **log-query-builder**: 복잡한 로그 검색 쿼리 자동 생성
- **performance-log-analyzer**: 성능 지표 중심 로그 분석
- **api-error-tracker**: REST API 에러 추적 및 통계
- **debug-session-recorder**: 디버깅 세션 자동 기록 및 분석