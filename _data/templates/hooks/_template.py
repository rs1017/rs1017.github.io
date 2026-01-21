#!/usr/bin/env python3
"""
Hook Name - Claude Code Hook 템플릿

이 훅은 특정 이벤트 발생 시 자동으로 실행됩니다.

Hook Types:
- PreToolUse: 도구 실행 전
- PostToolUse: 도구 실행 후
- Notification: 알림 발생 시

사용법:
    .claude/settings.json에 등록:
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Bash",
            "hooks": ["python .claude/hooks/hook_name.py"]
          }
        ]
      }
    }
"""

import json
import os
import sys
from typing import Any, Dict, Optional


# ┌─────────────────────────────────────────────────────────┐
# │  Hook Configuration                                      │
# └─────────────────────────────────────────────────────────┘

HOOK_CONFIG = {
    "name": "hook-name",
    "type": "PreToolUse",  # PreToolUse, PostToolUse, Notification
    "matcher": "Bash",      # 매칭할 도구 이름
    "description": "훅 설명",
}


# ┌─────────────────────────────────────────────────────────┐
# │  Main Hook Logic                                         │
# └─────────────────────────────────────────────────────────┘

def process_hook(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    훅 메인 로직

    Args:
        event_data: Claude Code에서 전달된 이벤트 데이터

    Returns:
        처리 결과 (continue, block, 또는 modify)
    """
    tool_name = event_data.get("tool_name", "")
    tool_input = event_data.get("tool_input", {})

    # ── Step 1: 조건 확인 ──
    # 특정 조건에서만 처리
    if not should_process(tool_name, tool_input):
        return {"action": "continue"}

    # ── Step 2: 처리 로직 ──
    result = execute_hook_logic(tool_input)

    # ── Step 3: 결과 반환 ──
    if result.get("block"):
        return {
            "action": "block",
            "message": result.get("message", "Hook blocked the action")
        }

    return {"action": "continue"}


def should_process(tool_name: str, tool_input: Dict[str, Any]) -> bool:
    """처리 여부 결정"""
    # 여기에 조건 로직 추가
    return True


def execute_hook_logic(tool_input: Dict[str, Any]) -> Dict[str, Any]:
    """실제 훅 로직 실행"""
    # 여기에 실제 로직 추가
    return {"block": False}


# ┌─────────────────────────────────────────────────────────┐
# │  Entry Point                                             │
# └─────────────────────────────────────────────────────────┘

def main() -> None:
    """메인 엔트리 포인트"""
    # stdin에서 이벤트 데이터 읽기
    try:
        input_data = sys.stdin.read()
        event_data = json.loads(input_data) if input_data else {}
    except json.JSONDecodeError:
        event_data = {}

    # 훅 실행
    result = process_hook(event_data)

    # 결과 출력 (stdout)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
