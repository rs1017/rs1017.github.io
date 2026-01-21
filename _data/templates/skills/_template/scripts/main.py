#!/usr/bin/env python3
"""
Skill Name - 메인 실행 스크립트

사용법:
    python main.py --input "입력 데이터"
"""

import argparse
import json
import os
from typing import Any, Dict, Optional


def process(input_data: str, option: bool = False) -> Dict[str, Any]:
    """
    메인 처리 로직

    Args:
        input_data: 입력 데이터
        option: 옵션 플래그

    Returns:
        처리 결과 딕셔너리
    """
    # ┌─────────────────────────────────────┐
    # │  Step 1: 입력 검증                   │
    # └─────────────────────────────────────┘
    if not input_data:
        return {"status": "error", "message": "입력이 비어있습니다"}

    # ┌─────────────────────────────────────┐
    # │  Step 2: 데이터 처리                 │
    # └─────────────────────────────────────┘
    result = {
        "input": input_data,
        "processed": True,
        "option_enabled": option,
    }

    # ┌─────────────────────────────────────┐
    # │  Step 3: 결과 반환                   │
    # └─────────────────────────────────────┘
    return {
        "status": "success",
        "data": result
    }


def main() -> None:
    """메인 엔트리 포인트"""
    parser = argparse.ArgumentParser(description="Skill Name 실행")
    parser.add_argument(
        "--input", "-i",
        type=str,
        required=True,
        help="입력 데이터"
    )
    parser.add_argument(
        "--option", "-o",
        action="store_true",
        help="옵션 활성화"
    )
    parser.add_argument(
        "--output", "-O",
        type=str,
        help="출력 파일 경로 (기본: stdout)"
    )

    args = parser.parse_args()

    # 실행
    result = process(args.input, args.option)

    # 출력
    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"✅ 결과가 {args.output}에 저장되었습니다")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
