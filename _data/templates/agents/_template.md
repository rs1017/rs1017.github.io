---
name: agent-name
description: Agent 설명
version: "1.0.0"
---

# Agent Name

## 🎯 목적

이 에이전트의 목적을 설명합니다.

## 📋 역할

- 역할 1
- 역할 2
- 역할 3

## 🔧 설정

```yaml
model: sonnet
temperature: 0.7
max_tokens: 4096
```

## 💬 시스템 프롬프트

```
당신은 [역할]을 수행하는 AI 에이전트입니다.

## 주요 임무
1. 임무 1
2. 임무 2

## 제약 사항
- 제약 1
- 제약 2
```

## 📎 사용 예시

```python
# 에이전트 호출 예시
response = agent.run(prompt="사용자 요청")
```
