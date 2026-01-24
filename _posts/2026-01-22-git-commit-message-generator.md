-
---
layout: post
title: "Git 커밋 메시지 자동 생성 스킬"
date: 2026-01-22 12:00:00 +0900
categories: [AI, Skill]
tags: [git, commit, conventional-commits, automation, workflow]
---

## 개요

좋은 커밋 메시지를 작성하는 것은 프로젝트 히스토리를 이해하는 데 필수적입니다. 하지만 매번 일관된 형식으로 의미 있는 메시지를 작성하는 것은 쉽지 않습니다.

`git-commit-message-generator` 스킬은 스테이징된 변경사항을 분석하여 Conventional Commits 형식의 커밋 메시지를 자동으로 생성합니다.

## 파일 위치

| 구분 | 경로 |
|------|------|
| 정의 파일 | `/assets/downloads/skills/git-commit-message-generator/SKILL.md` |
| 설치 위치 | `~/.claude/skills/git-commit-message-generator/SKILL.md` |

## 스킬 구조

```
.claude/skills/git-commit-message-generator/
└── SKILL.md              # 스킬 정의 파일
```

## 주요 기능

### 1. Conventional Commits 형식

표준화된 커밋 타입을 자동으로 식별:

- **feat**: 새로운 기능 추가
- **fix**: 버그 수정
- **docs**: 문서 변경
- **style**: 코드 스타일 변경 (포맷팅, 세미콜론 등)
- **refactor**: 기능 변경 없는 리팩토링
- **test**: 테스트 추가/수정
- **chore**: 빌드, 의존성, 도구 변경
- **perf**: 성능 개선
- **ci**: CI/CD 설정 변경

### 2. 스마트 분석

변경사항을 분석하여:
- 변경 타입 자동 감지
- 영향받은 모듈/파일 식별 (scope)
- 명확하고 간결한 설명 생성
- 복잡한 변경사항에 대한 본문 제공

### 3. 일관성 보장

팀 전체가 동일한 커밋 메시지 스타일을 유지할 수 있습니다.

## 사용 방법

### 설치

```bash
# 스킬 디렉토리 생성
mkdir -p ~/.claude/skills/git-commit-message-generator

# SKILL.md 파일 다운로드 및 저장
```

### 실행

```bash
# 1. 변경사항 스테이징
git add src/auth/login.js
git add tests/auth.test.js

# 2. Claude Code에서 스킬 실행
# "Generate a commit message for staged changes"

# 3. 생성된 메시지 검토 및 커밋
git commit -m "feat(auth): implement JWT-based authentication"
```

## 실행 예시

### 예시 1: 새 기능 추가

**변경사항**:
```diff
+ function authenticateUser(token) {
+   return jwt.verify(token, SECRET_KEY);
+ }
+ 
+ function generateToken(userId) {
+   return jwt.sign({ userId }, SECRET_KEY);
+ }
```

**생성된 메시지**:
```
feat(auth): implement JWT-based authentication

- Add token generation and validation functions
- Implement JWT middleware for protected routes
```

### 예시 2: 버그 수정

**변경사항**:
```diff
- if (user.age > 18) {
+ if (user.age >= 18) {
    allowAccess();
  }
```

**생성된 메시지**:
```
fix(auth): correct age validation logic

Change age check from > 18 to >= 18 to include 18-year-olds
```

### 예시 3: 리팩토링

**변경사항**:
```diff
- const data = fetchData();
- const processed = processData(data);
- const result = transformData(processed);
+ const result = pipe(
+   fetchData,
+   processData,
+   transformData
+ )();
```

**생성된 메시지**:
```
refactor(data): replace sequential calls with function composition

Improve code readability using pipe pattern
```

## 전체 코드

```markdown
---
name: git-commit-message-generator
description: Analyzes staged changes and generates conventional commit messages. Use when the user needs to create a git commit and wants help writing a good commit message following best practices.
---

# git-commit-message-generator

A skill that analyzes staged changes and generates conventional commit messages following best practices.

## Overview

This skill helps developers write consistent, meaningful commit messages by analyzing git diff output and following conventional commit format (type(scope): description).

## When to Use

Use this skill when:
- You have staged changes ready to commit
- You want to follow conventional commit format
- You need help describing what changed and why
- You want consistent commit message style across your team

## How It Works

1. Analyzes `git diff --staged` to understand changes
2. Identifies the type of change (feat, fix, docs, etc.)
3. Determines the scope (affected module/file)
4. Generates a clear, concise commit message
5. Provides optional body text for complex changes

## Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, semicolons, etc.)
- `refactor`: Code refactoring without feature changes
- `test`: Adding or updating tests
- `chore`: Build process, dependencies, or tooling changes
- `perf`: Performance improvements
- `ci`: CI/CD configuration changes

## Usage

```bash
# Stage your changes
git add .

# Generate commit message
claude /commit-msg

# Review and commit
git commit -m "feat(auth): add OAuth2 login flow"
```

## Example Output

For a change adding user authentication:

```
feat(auth): implement JWT-based authentication

- Add JWT token generation and validation
- Create middleware for protected routes
- Implement refresh token mechanism
- Add user session management
```

## Best Practices

1. **Be specific**: Describe what changed, not how
2. **Use imperative mood**: "add feature" not "added feature"
3. **Keep subject line under 72 characters**
4. **Add body for complex changes**
5. **Reference issues**: Add "Closes #123" when applicable

## Integration

Works seamlessly with:
- Git hooks (pre-commit, prepare-commit-msg)
- CI/CD pipelines
- Pull request workflows
- Changelog generators

## Customization

You can customize the skill to:
- Follow your team's commit conventions
- Add custom commit types
- Include ticket numbers automatically
- Enforce specific message patterns
```

## 장점

### 1. 생산성 향상
커밋 메시지 작성 시간을 단축하고 코딩에 집중할 수 있습니다.

### 2. 일관성
팀 전체가 동일한 형식의 커밋 메시지를 작성합니다.

### 3. 히스토리 품질
명확한 커밋 히스토리로 코드 변경 추적이 쉬워집니다.

### 4. 자동화 지원
Changelog 자동 생성, 시맨틱 버저닝 등과 연동 가능합니다.

## 활용 팁

### Git Hook 연동

`.git/hooks/prepare-commit-msg` 파일 생성:

```bash
#!/bin/bash
# 스테이징된 변경사항이 있으면 자동으로 메시지 생성
if [ -n "$(git diff --staged)" ]; then
  claude "Generate commit message for staged changes" > .git/COMMIT_EDITMSG
fi
```

### CI/CD 통합

커밋 메시지 형식을 자동으로 검증:

```yaml
- name: Validate commit message
  run: |
    if ! echo "$COMMIT_MSG" | grep -Eq '^(feat|fix|docs|style|refactor|test|chore|perf|ci)(\(.+\))?: .+'; then
      echo "Invalid commit message format"
      exit 1
    fi
```

## 관련 스킬

- **git-commit-analyzer**: 기존 커밋 히스토리 분석
- **changelog-generator**: 커밋 메시지에서 체인지로그 생성
- **code-reviewer**: 코드 변경사항 자동 리뷰

---

## 마치며

좋은 커밋 메시지는 미래의 자신과 팀원을 위한 선물입니다. `git-commit-message-generator` 스킬로 일관되고 의미 있는 커밋 히스토리를 만들어보세요.