---
name: 코드-기반-이미지-데이터-생성-스킬
version: "1.0.0"
author: AI Skill Factory
category: Skill
difficulty: intermediate
tags: ['이미지-생성', '데이터-시각화', '코드-자동화', '파일-처리']
requires:
  - python>=3.9
  - anthropic>=0.35.0
---

```markdown
---
name: data-visualizer
description: 코드로 데이터를 시각화하여 차트, 그래프, 다이어그램 이미지 파일을 자동 생성하는 스킬
category: Skill
difficulty: intermediate
tags:
  - 이미지-생성
  - 데이터-시각화
  - 코드-자동화
  - 파일-처리
version: 1.0.0
author: AI Skill Factory
created: 2024-01-21
updated: 2024-01-21
---

# 코드 기반 이미지 데이터 생성 스킬

## 개요

이 스킬은 데이터를 입력받아 다양한 형태의 시각화 이미지(차트, 그래프, 다이어그램)를 자동으로 생성합니다. Claude의 코드 생성 능력과 데이터 분석 능력을 활용하여 복잡한 데이터를 직관적인 시각 자료로 변환합니다.

### 주요 기능

- **차트 생성**: 막대 그래프, 선 그래프, 파이 차트, 산점도 등
- **다이어그램 생성**: 플로우차트, 시퀀스 다이어그램, 관계도
- **데이터 분석**: 통계 정보 추출 및 시각화
- **자동 스타일링**: 테마 기반 색상 및 레이아웃 최적화
- **다중 포맷 지원**: PNG, SVG, PDF 출력

## 파라미터

### 필수 파라미터

- `data_source` (str): 데이터 소스 (파일 경로, JSON 문자열, CSV 문자열)
- `visualization_type` (str): 시각화 유형
  - `bar_chart`: 막대 그래프
  - `line_chart`: 선 그래프
  - `pie_chart`: 파이 차트
  - `scatter_plot`: 산점도
  - `heatmap`: 히트맵
  - `flowchart`: 플로우차트
  - `sequence_diagram`: 시퀀스 다이어그램
- `output_path` (str): 출력 파일 경로

### 선택 파라미터

- `title` (str): 차트 제목 (기본값: 자동 생성)
- `x_label` (str): X축 레이블
- `y_label` (str): Y축 레이블
- `color_scheme` (str): 색상 테마 (`default`, `pastel`, `vibrant`, `monochrome`)
- `width` (int): 이미지 너비 (기본값: 1200)
- `height` (int): 이미지 높이 (기본값: 800)
- `dpi` (int): 해상도 (기본값: 100)
- `format` (str): 출력 포맷 (`png`, `svg`, `pdf`)
- `style` (str): 스타일 프리셋 (`minimal`, `professional`, `academic`)
- `annotations` (list): 주석 리스트 (텍스트, 화살표 등)

## 사용 예제

### 예제 1: CSV 데이터로 막대 그래프 생성

```python
import anthropic
import json
import base64
import os

def generate_chart_from_csv(csv_data, output_path="chart.png"):
    """CSV 데이터를 막대 그래프로 변환"""
    
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # Claude에게 시각화 코드 생성 요청
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"""
다음 CSV 데이터를 막대 그래프로 시각화하는 Python 코드를 작성해주세요.

CSV 데이터:
{csv_data}

요구사항:
1. matplotlib과 pandas 사용
2. 전문적인 스타일 적용 (격자, 레이블, 제목)
3. 색상은 vibrant 테마 사용
4. 파일로 저장: {output_path}
5. 코드만 출력 (설명 제외)

코드를 실행 가능한 형태로 작성하고, 필요한 import문을 모두 포함하세요.
"""
        }]
    )
    
    # 생성된 코드 실행
    code = message.content[0].text
    
    # 코드 블록에서 실제 코드만 추출
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()
    
    # 코드 실행
    exec(code)
    
    print(f"차트가 생성되었습니다: {output_path}")
    return output_path

# 사용 예제
csv_data = """
Month,Sales,Expenses
January,45000,32000
February,52000,35000
March,48000,33000
April,61000,38000
May,58000,36000
June,67000,41000
"""

generate_chart_from_csv(csv_data, "monthly_sales.png")
```

### 예제 2: JSON 데이터로 파이 차트 생성

```python
def generate_pie_chart(data_dict, title, output_path="pie_chart.png"):
    """딕셔너리 데이터를 파이 차트로 변환"""
    
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"""
다음 데이터를 파이 차트로 시각화하는 Python 코드를 작성해주세요.

데이터: {json.dumps(data_dict)}
제목: {title}

요구사항:
1. matplotlib 사용
2. 퍼센트 표시 포함
3. 범례 추가
4. 파스텔 색상 사용
5. 파일로 저장: {output_path}
6. 코드만 출력

실행 가능한 완전한 코드를 작성하세요.
"""
        }]
    )
    
    code = message.content[0].text
    
    # 코드 추출 및 실행
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()
    
    exec(code)
    
    print(f"파이 차트가 생성되었습니다: {output_path}")
    return output_path

# 사용 예제
market_share = {
    "Product A": 35,
    "Product B": 28,
    "Product C": 22,
    "Product D": 15
}

generate_pie_chart(market_share, "2024 Market Share Distribution", "market_share.png")
```

### 예제 3: 복잡한 시계열 데이터 시각화

```python
def generate_multi_line_chart(time_series_data, output_path="timeline.png"):
    """여러 계열의 시계열 데이터를 선 그래프로 시각화"""
    
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"""
다음 시계열 데이터를 멀티 라인 차트로 시각화하는 Python 코드를 작성해주세요.

데이터: {json.dumps(time_series_data)}

요구사항:
1. matplotlib과 pandas 사용
2. 각 계열별 다른 색상과 마커
3. 격자 및 범례 표시
4. X축: 날짜 포맷팅
5. Y축: 값 범위 자동 조정
6. 이미지 크기: 1400x900
7. 파일로 저장: {output_path}
8. 코드만 출력

전문적인 스타일의 실행 가능한 코드를 작성하세요.
"""
        }]
    )
    
    code = message.content[0].text
    
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()
    
    exec(code)
    
    print(f"타임라인 차트가 생성되었습니다: {output_path}")
    return output_path

# 사용 예제
performance_data = {
    "dates": ["2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06"],
    "revenue": [120000, 135000, 128000, 152000, 148000, 167000],
    "costs": [85000, 92000, 88000, 98000, 95000, 105000],
    "profit": [35000, 43000, 40000, 54000, 53000, 62000]
}

generate_multi_line_chart(performance_data, "quarterly_performance.png")
```

### 예제 4: 다이어그램 자동 생성 (Mermaid 기반)

```python
def generate_flowchart_diagram(description, output_path="flowchart.png"):
    """텍스트 설명을 플로우차트 다이어그램으로 변환"""
    
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # 1단계: Claude가 Mermaid 코드 생성
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": f"""
다음 프로세스 설명을 Mermaid 플로우차트 문법으로 변환해주세요.

설명: {description}

Mermaid 코드만 출력하세요 (```mermaid 태그 포함).
"""
        }]
    )
    
    mermaid_code = message.content[0].text
    
    if "```mermaid" in mermaid_code:
        mermaid_code = mermaid_code.split("```mermaid")[1].split("```")[0].strip()
    
    # 2단계: Mermaid를 이미지로 변환하는 Python 코드 생성
    message2 = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": f"""
다음 Mermaid 코드를 PNG 이미지로 변환하는 Python 코드를 작성해주세요.

Mermaid 코드:
{mermaid_code}

요구사항:
1. mermaid-py 또는 다른 렌더링 라이브러리 사용
2. 출력 파일: {output_path}
3. 고해상도 (DPI 150)
4. 코드만 출력

실행 가능한 완전한 코드를 작성하세요.
"""
        }]
    )
    
    code = message2.content[0].text
    
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()
    
    try:
        exec(code)
        print(f"플로우차트가 생성되었습니다: {output_path}")
    except Exception as e:
        # 대체 방법: 텍스트 기반 다이어그램 저장
        with open(output_path.replace('.png', '.mmd'), 'w') as f:
            f.write(mermaid_code)
        print(f"Mermaid 코드가 저장되었습니다: {output_path.replace('.png', '.mmd')}")
        print(f"https://mermaid.live 에서 시각화할 수 있습니다.")
    
    return output_path

# 사용 예제
process_description = """
사용자 로그인 프로세스:
1. 사용자가 이메일과 비밀번호 입력
2. 입력값 유효성 검사
3. 유효하면 데이터베이스 조회
4. 사용자 정보가 있으면 세션 생성
5. 없으면 에러 메시지 표시
6. 성공 시 대시보드로 리다이렉트
"""

generate_flowchart_diagram(process_description, "login_flow.png")
```

### 예제 5: 히트맵 생성 (상관관계 시각화)

```python
def generate_heatmap(correlation_data, labels, output_path="heatmap.png"):
    """상관관계 매트릭스를 히트맵으로 시각화"""
    
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"""
다음 데이터를 히트맵으로 시각화하는 Python 코드를 작성해주세요.

데이터 (2D 리스트): {correlation_data}
레이블: {labels}

요구사항:
1. seaborn과 matplotlib 사용
2. 숫자 값 표시
3. 색상바 포함
4. 적절한 색상 스케일 (RdYlGn 또는 coolwarm)
5. 파일로 저장: {output_path}
6. 코드만 출력

실행 가능한 완전한 코드를 작성하세요.
"""
        }]
    )
    
    code = message.content[0].text
    
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()
    
    exec(code)
    
    print(f"히트맵이 생성되었습니다: {output_path}")
    return output_path

# 사용 예제
correlation_matrix = [
    [1.0, 0.8, -0.3, 0.5],
    [0.8, 1.0, -0.2, 0.6],
    [-0.3, -0.2, 1.0, -0.7],
    [0.5, 0.6, -0.7, 1.0]
]

feature_labels = ["Revenue", "Marketing", "Support Tickets", "Customer Satisfaction"]

generate_heatmap(correlation_matrix, feature_labels, "correlation_heatmap.png")
```

## 실용적인 사용 시나리오

### 시나리오 1: 대시보드 자동 생성

주간 리포트용 차트 세트를 자동으로 생성:

```python
def create_weekly_dashboard(data_file, output_dir="dashboard"):
    """CSV 데이터에서 여러 차트를 생성하여 대시보드 구성"""
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # 데이터 로드
    with open(data_file, 'r') as f:
        csv_data = f.read()
    
    # 1. 매출 추이 (선 그래프)
    generate_chart_from_csv(csv_data, f"{output_dir}/sales_trend.png")
    
    # 2. 카테고리별 비중 (파이 차트)
    # ... 데이터 변환 로직 ...
    
    # 3. 부서별 성과 (막대 그래프)
    # ... 데이터 변환 로직 ...
    
    print(f"대시보드 차트가 {output_dir}에 생성되었습니다.")
```

### 시나리오 2: 실시간 모니터링 차트

로그 데이터를 실시간으로 시각화:

```python
import time

def monitor_and_visualize(log_file, interval=60):
    """로그 파일을 주기적으로 읽고 차트 업데이트"""
    
    while True:
        # 로그 데이터 파싱
        # ... 로직 ...
        
        # 차트 생성
        generate_chart_from_csv(parsed_data, "monitoring_chart.png")
        
        print(f"차트 업데이트됨: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(interval)
```

### 시나리오 3: A/B 테스트 결과 시각화

```python
def visualize_ab_test_results(test_data):
    """A/B 테스트 결과를 비교 차트로 시각화"""
    
    # 전환율 비교 막대 그래프
    conversion_data = {
        "Variant A": test_data['a_conversion'],
        "Variant B": test_data['b_conversion']
    }
    
    generate_pie_chart(conversion_data, "A/B Test Conversion Rates", "ab_test.png")
    
    # 통계적 유의성 시각화
    # ... 추가 차트 생성 ...
```

## 베스트 프랙티스

1. **데이터 검증**: 시각화 전 데이터 형식과 범위를 검증
2. **에러 처리**: 코드 실행 실패 시 대체 방법 제공
3. **스타일 일관성**: 프로젝트 전체에서 일관된 색상 테마 사용
4. **성능 최적화**: 대용량 데이터는 샘플링 또는 집계 후 시각화
5. **접근성**: 색맹 친화적 색상 팔레트 사용
6. **문서화**: 생성된 차트에 메타데이터(생성 날짜, 데이터 출처) 포함

## 주의사항

- **의존성 관리**: matplotlib, seaborn, pandas 등 필요한 라이브러리 사전 설치 필요
- **메모리 사용**: 고해상도 이미지 생성 시 메모리 사용량 고려
- **코드 실행 보안**: `exec()` 사용 시 신뢰할 수 있는 코드만 실행
- **파일 경로**: 출력 경로의 디렉토리가 존재하는지 확인

## 확장 아이디어

- **인터랙티브 차트**: Plotly 사용하여 HTML 기반 인터랙티브 차트 생성
- **애니메이션**: 시계열 데이터를 GIF 또는 MP4로 애니메이션화
- **3D 시각화**: 3차원 데이터 시각화 지원
- **자동 분석**: Claude가 데이터를 분석하고 최적의 시각화 방법 추천
- **템플릿 시스템**: 재사용 가능한 차트 템플릿 라이브러리 구축

## 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능
```