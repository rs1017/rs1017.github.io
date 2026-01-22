---

# Markdown TOC Generator

Markdown 문서의 헤딩 구조를 분석하여 자동으로 목차(Table of Contents)를 생성하고 삽입하는 스킬입니다.

## 사용 시점

다음과 같은 상황에서 이 스킬을 사용하세요:

- 사용자가 "마크다운 목차 생성해줘"라고 요청할 때
- 사용자가 "TOC 추가해줘"라고 요청할 때
- 사용자가 README나 문서에 목차가 필요하다고 말할 때
- 긴 마크다운 문서의 네비게이션을 개선하고 싶을 때

## 주요 기능

1. **헤딩 파싱**: H1~H6 헤딩 자동 감지
2. **계층 구조**: 헤딩 레벨에 따른 들여쓰기 목차 생성
3. **앵커 링크**: GitHub 스타일 앵커 자동 생성
4. **유연한 삽입**: 기존 TOC 업데이트 또는 새로 삽입
5. **커스터마이징**: 최대 깊이, 제외 헤딩 설정 가능

## 작동 방식

### 1. 헤딩 추출

```python
import re

def extract_headings(content):
    """마크다운 헤딩 추출"""
    pattern = r'^(#{1,6})\s+(.+)$'
    headings = []
    
    for line in content.split('\n'):
        match = re.match(pattern, line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append({'level': level, 'text': text})
    
    return headings
```

### 2. 앵커 생성

```python
def create_anchor(text):
    """GitHub 스타일 앵커 생성"""
    # 소문자 변환
    anchor = text.lower()
    
    # 특수문자 제거 (하이픈과 공백만 유지)
    anchor = re.sub(r'[^\w\s-]', '', anchor)
    
    # 공백을 하이픈으로 변환
    anchor = re.sub(r'\s+', '-', anchor)
    
    # 연속된 하이픈 제거
    anchor = re.sub(r'-+', '-', anchor)
    
    return anchor.strip('-')
```

### 3. TOC 생성

```python
def generate_toc(headings, max_depth=3, skip_levels=None):
    """계층적 TOC 생성"""
    if skip_levels is None:
        skip_levels = [1]  # H1 기본 제외
    
    toc_lines = ['## Table of Contents\n']
    
    for heading in headings:
        level = heading['level']
        text = heading['text']
        
        # 제외 레벨 체크
        if level in skip_levels or level > max_depth:
            continue
        
        # 들여쓰기 계산
        indent = '  ' * (level - min([h['level'] for h in headings if h['level'] not in skip_levels]))
        
        # 앵커 링크 생성
        anchor = create_anchor(text)
        toc_line = f"{indent}- [{text}](#{anchor})\n"
        
        toc_lines.append(toc_line)
    
    return ''.join(toc_lines)
```

### 4. TOC 삽입

```python
def insert_toc(content, toc, position='auto'):
    """
    TOC를 마크다운 문서에 삽입
    
    Args:
        content: 원본 마크다운 내용
        toc: 생성된 TOC
        position: 삽입 위치 ('auto', 'top', 'after-title', marker)
    """
    lines = content.split('\n')
    
    # 기존 TOC 제거 (<!-- TOC --> 마커 사이)
    toc_start = None
    toc_end = None
    
    for i, line in enumerate(lines):
        if '<!-- TOC -->' in line or '<!-- toc -->' in line:
            if toc_start is None:
                toc_start = i
            else:
                toc_end = i
                break
    
    if toc_start is not None and toc_end is not None:
        # 기존 TOC 교체
        del lines[toc_start:toc_end + 1]
        insert_index = toc_start
    elif position == 'auto':
        # 첫 H1 다음에 삽입
        insert_index = 0
        for i, line in enumerate(lines):
            if re.match(r'^#\s+', line):
                insert_index = i + 1
                break
    elif position == 'top':
        insert_index = 0
    else:
        insert_index = 0
    
    # TOC 삽입
    toc_block = [
        '<!-- TOC -->',
        '',
        toc.strip(),
        '',
        '<!-- /TOC -->',
        ''
    ]
    
    for i, line in enumerate(toc_block):
        lines.insert(insert_index + i, line)
    
    return '\n'.join(lines)
```

## 사용 방법

### 기본 사용

```python
# 마크다운 파일 읽기
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 헤딩 추출
headings = extract_headings(content)

# TOC 생성 (H2~H4만, H1 제외)
toc = generate_toc(headings, max_depth=4, skip_levels=[1])

# TOC 삽입
updated_content = insert_toc(content, toc)

# 파일 저장
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(updated_content)
```

### 고급 옵션

```python
# 모든 레벨 포함 (H1~H6)
toc = generate_toc(headings, max_depth=6, skip_levels=[])

# H2~H3만 포함
toc = generate_toc(headings, max_depth=3, skip_levels=[1, 4, 5, 6])

# 특정 위치에 삽입
updated_content = insert_toc(content, toc, position='top')
```

## 전체 스크립트

```python
#!/usr/bin/env python3
"""
Markdown TOC Generator
자동으로 마크다운 목차를 생성하고 삽입합니다.
"""

import re
import sys
from pathlib import Path


def extract_headings(content):
    """마크다운 헤딩 추출"""
    pattern = r'^(#{1,6})\s+(.+)$'
    headings = []
    
    for line in content.split('\n'):
        match = re.match(pattern, line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            # 코드블록 내부는 제외
            headings.append({'level': level, 'text': text})
    
    return headings


def create_anchor(text):
    """GitHub 스타일 앵커 생성"""
    anchor = text.lower()
    anchor = re.sub(r'[^\w\s-]', '', anchor)
    anchor = re.sub(r'\s+', '-', anchor)
    anchor = re.sub(r'-+', '-', anchor)
    return anchor.strip('-')


def generate_toc(headings, max_depth=3, skip_levels=None):
    """계층적 TOC 생성"""
    if skip_levels is None:
        skip_levels = [1]
    
    if not headings:
        return '## Table of Contents\n\n_(No headings found)_\n'
    
    toc_lines = ['## Table of Contents\n']
    
    # 최소 레벨 찾기 (들여쓰기 기준점)
    valid_levels = [h['level'] for h in headings if h['level'] not in skip_levels and h['level'] <= max_depth]
    
    if not valid_levels:
        return '## Table of Contents\n\n_(No headings found in specified range)_\n'
    
    min_level = min(valid_levels)
    
    for heading in headings:
        level = heading['level']
        text = heading['text']
        
        if level in skip_levels or level > max_depth:
            continue
        
        # 들여쓰기 계산
        indent = '  ' * (level - min_level)
        
        # 앵커 링크 생성
        anchor = create_anchor(text)
        toc_line = f"{indent}- [{text}](#{anchor})\n"
        
        toc_lines.append(toc_line)
    
    return ''.join(toc_lines)


def insert_toc(content, toc, position='auto'):
    """TOC를 마크다운 문서에 삽입"""
    lines = content.split('\n')
    
    # 기존 TOC 제거
    toc_start = None
    toc_end = None
    
    for i, line in enumerate(lines):
        if '<!-- TOC -->' in line or '<!-- toc -->' in line.lower():
            if toc_start is None:
                toc_start = i
            else:
                toc_end = i
                break
    
    if toc_start is not None and toc_end is not None:
        del lines[toc_start:toc_end + 1]
        insert_index = toc_start
    elif position == 'auto':
        # 첫 H1 다음에 삽입
        insert_index = 0
        for i, line in enumerate(lines):
            if re.match(r'^#\s+', line):
                insert_index = i + 1
                # 빈 줄 건너뛰기
                while insert_index < len(lines) and not lines[insert_index].strip():
                    insert_index += 1
                break
    elif position == 'top':
        insert_index = 0
    else:
        insert_index = 0
    
    # TOC 삽입
    toc_block = [
        '<!-- TOC -->',
        '',
        toc.strip(),
        '',
        '<!-- /TOC -->',
        ''
    ]
    
    for i, line in enumerate(toc_block):
        lines.insert(insert_index + i, line)
    
    return '\n'.join(lines)


def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("Usage: python toc_generator.py <markdown_file> [--max-depth N] [--include-h1]")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    # 옵션 파싱
    max_depth = 4
    skip_levels = [1]
    
    if '--max-depth' in sys.argv:
        idx = sys.argv.index('--max-depth')
        if idx + 1 < len(sys.argv):
            max_depth = int(sys.argv[idx + 1])
    
    if '--include-h1' in sys.argv:
        skip_levels = []
    
    # 파일 읽기
    content = file_path.read_text(encoding='utf-8')
    
    # TOC 생성
    headings = extract_headings(content)
    toc = generate_toc(headings, max_depth=max_depth, skip_levels=skip_levels)
    
    # TOC 삽입
    updated_content = insert_toc(content, toc)
    
    # 파일 저장
    file_path.write_text(updated_content, encoding='utf-8')
    
    print(f"✅ TOC generated and inserted into {file_path}")
    print(f"   - Headings found: {len(headings)}")
    print(f"   - Max depth: H{max_depth}")
    print(f"   - H1 included: {'Yes' if not skip_levels else 'No'}")


if __name__ == '__main__':
    main()
```

## 실행 예시

### 기본 실행

```bash
python toc_generator.py README.md
```

### H1 포함

```bash
python toc_generator.py README.md --include-h1
```

### 최대 깊이 지정

```bash
python toc_generator.py README.md --max-depth 6
```

## 생성 예시

**입력 마크다운:**

```markdown
# My Project

## Installation

### Prerequisites

### Setup

## Usage

### Basic Usage

### Advanced Features

## API Reference

### Classes

### Functions
```

**생성된 TOC:**

```markdown
<!-- TOC -->

## Table of Contents

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Advanced Features](#advanced-features)
- [API Reference](#api-reference)
  - [Classes](#classes)
  - [Functions](#functions)

<!-- /TOC -->
```

## 주의사항

1. **앵커 링크**: GitHub, GitLab, Bitbucket 등 플랫폼마다 앵커 생성 규칙이 다를 수 있습니다
2. **중복 헤딩**: 동일한 텍스트의 헤딩이 여러 개 있을 경우 앵커 충돌 가능
3. **특수문자**: 이모지나 특수문자가 포함된 헤딩은 앵커 생성 시 제거됩니다
4. **코드블록**: 코드블록 내부의 `#` 기호는 헤딩으로 인식되지 않도록 주의 필요

## 확장 아이디어

1. **중복 앵커 처리**: 동일 헤딩에 `-1`, `-2` 접미사 추가
2. **플랫폼 별 모드**: GitHub/GitLab/Bitbucket 앵커 스타일 선택
3. **번호 매기기**: `1.`, `1.1.`, `1.1.1.` 형식 목차
4. **제외 패턴**: 특정 텍스트 패턴의 헤딩 제외
5. **GUI 버전**: Tkinter/Qt로 GUI 인터페이스 제공