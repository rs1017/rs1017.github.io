---
layout: post
title: "Claude Code Hook Creator - 훅 생성 가이드"
date: 2026-01-22 10:00:00 +0900
categories: [AI, Skill]
tags: [claude-code, hook, automation, pretooluse, posttooluse]
---

## 개요

Claude Code Hook Creator는 Claude Code의 훅(Hook)을 쉽게 생성하고 구성하는 스킬입니다. 훅을 사용하면 도구 실행 전후에 자동으로 셸 명령을 실행할 수 있습니다.

## 폴더 구조

```
.claude/skills/hook-creator/
├── SKILL.md
└── references/
    ├── hook-events.md
    └── examples.md
```

## 훅 이벤트 종류

| 이벤트 | 설명 |
|--------|------|
| `PreToolUse` | 도구 실행 전 |
| `PostToolUse` | 도구 실행 후 |
| `Notification` | 알림 발생 시 |

## 훅 설정 구조

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' >> ~/.claude/bash-log.txt"
          }
        ]
      }
    ]
  }
}
```

## 구현 예제

### 1. Bash 명령 로깅

```bash
jq -r '"\(.tool_input.command)"' >> ~/.claude/bash-log.txt
```

### 2. TypeScript 자동 포맷팅

```bash
jq -r '.tool_input.file_path' | { read f; [[ "$f" == *.ts ]] && npx prettier --write "$f"; }
```

### 3. .env 파일 수정 차단

```bash
python3 -c "import json,sys; p=json.load(sys.stdin).get('tool_input',{}).get('file_path',''); sys.exit(2 if '.env' in p else 0)"
```

## Exit 코드

- `0`: 도구 실행 허용
- `2`: 도구 실행 차단 (Claude에게 피드백 전달)

## 첨부 파일

> [hook-creator SKILL.md](/assets/downloads/skills/hook-creator/SKILL.md)

## 관련 스킬

- [slash-command-creator](/posts/slash-command-creator/) - Slash Command 생성
- [subagent-creator](/posts/subagent-creator/) - Sub-agent 생성
