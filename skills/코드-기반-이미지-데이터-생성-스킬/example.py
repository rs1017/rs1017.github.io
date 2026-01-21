#!/usr/bin/env python3
"""
코드 기반 이미지 데이터 생성 스킬

데이터를 입력받아 다양한 형태의 시각화 이미지(차트, 그래프, 다이어그램)를 자동으로 생성합니다.
Claude의 코드 생성 능력과 데이터 분석 능력을 활용하여 복잡한 데이터를 직관적인 시각 자료로 변환합니다.
"""

import os
import sys
import json
import tempfile
from typing import Dict, List, Optional, Any, Literal
from pathlib import Path

import anthropic


class DataVisualizer:
    """데이터 시각화 이미지 생성 클래스"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        DataVisualizer 초기화
        
        Args:
            api_key: Anthropic API 키 (None이면 환경변수 사용)
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def generate_visualization(
        self,
        data_source: str,
        visualization_type: Literal[
            "bar_chart", "line_chart", "pie_chart", "scatter_plot", 
            "heatmap", "flowchart", "sequence_diagram"
        ],
        output_path: str,
        title: Optional[str] = None,
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        color_scheme: Literal["default", "pastel", "vibrant", "monochrome"] = "default",
        width: int = 1200,
        height: int = 800,
        dpi: int = 100,
        format: Literal["png", "svg", "pdf"] = "png",
        style: Literal["minimal", "professional", "academic"] = "professional",
        annotations: Optional[List[str]] = None
    ) -> str:
        """
        데이터 시각화 이미지 생성
        
        Args:
            data_source: 데이터 소스 (CSV, JSON 문자열 또는 파일 경로)
            visualization_type: 시각화 유형
            output_path: 출력 파일 경로
            title: 차트 제목
            x_label: X축 레이블
            y_label: Y축 레이블
            color_scheme: 색상 테마
            width: 이미지 너비
            height: 이미지 높이
            dpi: 해상도
            format: 출력 포맷
            style: 스타일 프리셋
            annotations: 주석 리스트
        
        Returns:
            생성된 파일 경로
        """
        try:
            # 데이터 소스가 파일 경로인지 확인
            if os.path.isfile(data_source):
                with open(data_source, 'r', encoding='utf-8') as f:
                    data_content = f.read()
            else:
                data_content = data_source
            
            # Claude에게 시각화 코드 생성 요청
            prompt = self._build_prompt(
                data_content=data_content,
                visualization_type=visualization_type,
                output_path=output_path,
                title=title,
                x_label=x_label,
                y_label=y_label,
                color_scheme=color_scheme,
                width=width,
                height=height,
                dpi=dpi,
                format=format,
                style=style,
                annotations=annotations
            )
            
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=8192,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # 생성된 코드 추출
            code = message.content[0].text
            code = self._extract_code(code)
            
            # 코드 실행
            self._execute_code(code, output_path)
            
            print(f"✅ 시각화 이미지가 생성되었습니다: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ 이미지 생성 중 오류 발생: {str(e)}", file=sys.stderr)
            raise
    
    def _build_prompt(
        self,
        data_content: str,
        visualization_type: str,
        output_path: str,
        **kwargs
    ) -> str:
        """시각화 코드 생성을 위한 프롬프트 구성"""
        
        viz_type_map = {
            "bar_chart": "막대 그래프",
            "line_chart": "선 그래프",
            "pie_chart": "파이 차트",
            "scatter_plot": "산점도",
            "heatmap": "히트맵",
            "flowchart": "플로우차트",
            "sequence_diagram": "시퀀스 다이어그램"
        }
        
        viz_name = viz_type_map.get(visualization_type, visualization_type)
        
        prompt = f"""다음 데이터를 {viz_name}로 시각화하는 Python 코드를 작성해주세요.

데이터:
{data_content}

출력 파일: {output_path}

요구사항:
1. matplotlib, seaborn, pandas 등 적절한 라이브러리 사용
2. 스타일: {kwargs.get('style', 'professional')}
3. 색상 테마: {kwargs.get('color_scheme', 'default')}
4. 이미지 크기: {kwargs.get('width', 1200)}x{kwargs.get('height', 800)}
5. DPI: {kwargs.get('dpi', 100)}
6. 포맷: {kwargs.get('format', 'png')}
"""
        
        if kwargs.get('title'):
            prompt += f"7. 제목: {kwargs['title']}\n"
        if kwargs.get('x_label'):
            prompt += f"8. X축 레이블: {kwargs['x_label']}\n"
        if kwargs.get('y_label'):
            prompt += f"9. Y축 레이블: {kwargs['y_label']}\n"
        if kwargs.get('annotations'):
            prompt += f"10. 주석: {', '.join(kwargs['annotations'])}\n"
        
        prompt += """
코드 작성 규칙:
- 모든 필요한 import문 포함
- 실행 가능한 완전한 코드
- 에러 핸들링 포함
- 한글 폰트 설정 (나눔고딕 또는 맑은고딕)
- 격자선, 범례 등 시각적 요소 포함
- 코드만 출력 (설명 제외)
- 코드 블록 마커(```) 없이 순수 코드만 출력

코드를 작성해주세요:
"""
        return prompt
    
    def _extract_code(self, response: str) -> str:
        """응답에서 실제 코드만 추출"""
        code = response.strip()
        
        # 코드 블록 제거
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
        
        return code
    
    def _execute_code(self, code: str, output_path: str) -> None:
        """생성된 코드 실행"""
        try:
            # 출력 디렉토리 생성
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 코드 실행 환경 준비
            exec_globals = {
                '__builtins__': __builtins__,
                'output_path': output_path
            }
            
            # 코드 실행
            exec(code, exec_globals)
            
        except Exception as e:
            print(f"코드 실행 중 오류:\n{code}\n", file=sys.stderr)
            raise RuntimeError(f"시각화 코드 실행 실패: {str(e)}")


def main() -> None:
    """메인 함수 - 사용 예제"""
    
    print("🎨 코드 기반 이미지 데이터 생성 스킬 예제\n")
    
    # 예제 1: CSV 데이터로 막대 그래프 생성
    print("=" * 60)
    print("예제 1: 월별 매출 막대 그래프")
    print("=" * 60)
    
    csv_data = """Month,Sales,Expenses
January,45000,32000
February,52000,35000
March,48000,33000
April,61000,38000
May,58000,36000
June,67000,41000"""
    
    visualizer = DataVisualizer()
    
    try:
        visualizer.generate_visualization(
            data_source=csv_data,
            visualization_type="bar_chart",
            output_path="monthly_sales.png",
            title="월별 매출 및 지출 현황",
            x_label="월",
            y_label="금액 (원)",
            color_scheme="vibrant",
            style="professional"
        )
    except Exception as e:
        print(f"예제 1 실패: {e}", file=sys.stderr)
    
    # 예제 2: JSON 데이터로 파이 차트 생성
    print("\n" + "=" * 60)
    print("예제 2: 제품 카테고리별 매출 파이 차트")
    print("=" * 60)
    
    json_data = json.dumps({
        "Electronics": 125000,
        "Clothing": 85000,
        "Food": 62000,
        "Books": 38000,
        "Sports": 45000
    })
    
    try:
        visualizer.generate_visualization(
            data_source=json_data,
            visualization_type="pie_chart",
            output_path="category_sales.png",
            title="카테고리별 매출 비중",
            color_scheme="pastel",
            style="professional"
        )
    except Exception as e:
        print(f"예제 2 실패: {e}", file=sys.stderr)
    
    # 예제 3: 라인 차트 생성
    print("\n" + "=" * 60)
    print("예제 3: 주간 방문자 추이 라인 차트")
    print("=" * 60)
    
    csv_data_line = """Day,Visitors
Monday,1250
Tuesday,1380
Wednesday,1520
Thursday,1680
Friday,2100
Saturday,2450
Sunday,2280"""
    
    try:
        visualizer.generate_visualization(
            data_source=csv_data_line,
            visualization_type="line_chart",
            output_path="weekly_visitors.png",
            title="주간 방문자 추이",
            x_label="요일",
            y_label="방문자 수",
            color_scheme="default",
            style="academic"
        )
    except Exception as e:
        print(f"예제 3 실패: {e}", file=sys.stderr)
    
    print("\n✨ 모든 예제 실행 완료!")
    print("\n생성된 파일:")
    print("  - monthly_sales.png")
    print("  - category_sales.png")
    print("  - weekly_visitors.png")


if __name__ == "__main__":
    main()