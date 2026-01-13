---
title: HTML to Markdown 변환 가이드 - 다양한 예제와 팁
author: naksupapa
date: 2023-04-25 09:40:18 +0900
categories: [Development, Markdown]
tags: [html, markdown, converter, guide]
---

# HTML to Markdown 변환 가이드

HTML을 Markdown으로 변환할 때 자주 사용하는 패턴들을 정리했습니다.

## 기본 텍스트 서식

### HTML

```html
<h1>제목 1</h1>
<h2>제목 2</h2>
<h3>제목 3</h3>

<p>일반 단락입니다.</p>

<strong>굵은 글씨</strong>
<b>굵은 글씨 (b 태그)</b>

<em>기울임</em>
<i>기울임 (i 태그)</i>

<del>취소선</del>
<s>취소선 (s 태그)</s>
```

### Markdown

```markdown
# 제목 1
## 제목 2
### 제목 3

일반 단락입니다.

**굵은 글씨**
**굵은 글씨 (b 태그)**

*기울임*
*기울임 (i 태그)*

~~취소선~~
~~취소선 (s 태그)~~
```

## 링크와 이미지

### HTML

```html
<!-- 링크 -->
<a href="https://github.com">GitHub</a>
<a href="https://github.com" title="깃허브 홈페이지">GitHub (타이틀 포함)</a>

<!-- 이미지 -->
<img src="/images/logo.png" alt="로고">
<img src="/images/logo.png" alt="로고" title="회사 로고">

<!-- 이미지 링크 -->
<a href="https://github.com">
  <img src="/images/github-logo.png" alt="GitHub">
</a>
```

### Markdown

```markdown
<!-- 링크 -->
[GitHub](https://github.com)
[GitHub (타이틀 포함)](https://github.com "깃허브 홈페이지")

<!-- 이미지 -->
![로고](/images/logo.png)
![로고](/images/logo.png "회사 로고")

<!-- 이미지 링크 -->
[![GitHub](/images/github-logo.png)](https://github.com)
```

## 목록

### HTML

```html
<!-- 순서 없는 목록 -->
<ul>
  <li>항목 1</li>
  <li>항목 2</li>
  <li>항목 3
    <ul>
      <li>중첩 항목 A</li>
      <li>중첩 항목 B</li>
    </ul>
  </li>
</ul>

<!-- 순서 있는 목록 -->
<ol>
  <li>첫 번째</li>
  <li>두 번째</li>
  <li>세 번째</li>
</ol>
```

### Markdown

```markdown
<!-- 순서 없는 목록 -->
- 항목 1
- 항목 2
- 항목 3
  - 중첩 항목 A
  - 중첩 항목 B

<!-- 순서 있는 목록 -->
1. 첫 번째
2. 두 번째
3. 세 번째
```

## 테이블

### HTML

```html
<table>
  <thead>
    <tr>
      <th>이름</th>
      <th>나이</th>
      <th>직업</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>홍길동</td>
      <td>30</td>
      <td>개발자</td>
    </tr>
    <tr>
      <td>김철수</td>
      <td>25</td>
      <td>디자이너</td>
    </tr>
  </tbody>
</table>
```

### Markdown

```markdown
| 이름 | 나이 | 직업 |
|------|------|------|
| 홍길동 | 30 | 개발자 |
| 김철수 | 25 | 디자이너 |
```

### 정렬이 있는 테이블

```markdown
| 왼쪽 정렬 | 가운데 정렬 | 오른쪽 정렬 |
|:----------|:-----------:|------------:|
| 내용 | 내용 | 내용 |
| 왼쪽 | 가운데 | 오른쪽 |
```

## 코드

### HTML

```html
<!-- 인라인 코드 -->
<code>console.log('Hello')</code>

<!-- 코드 블록 -->
<pre><code>function hello() {
  console.log('Hello, World!');
}
</code></pre>

<!-- 언어 지정 -->
<pre><code class="language-javascript">const greeting = 'Hello';
console.log(greeting);
</code></pre>
```

### Markdown

```markdown
<!-- 인라인 코드 -->
`console.log('Hello')`

<!-- 코드 블록 -->
```
function hello() {
  console.log('Hello, World!');
}
```

<!-- 언어 지정 -->
```javascript
const greeting = 'Hello';
console.log(greeting);
```
```

## 인용문

### HTML

```html
<blockquote>
  <p>인용된 텍스트입니다.</p>
  <p>여러 줄의 인용문도 가능합니다.</p>
</blockquote>

<!-- 중첩 인용 -->
<blockquote>
  <p>첫 번째 레벨</p>
  <blockquote>
    <p>두 번째 레벨</p>
  </blockquote>
</blockquote>
```

### Markdown

```markdown
> 인용된 텍스트입니다.
> 여러 줄의 인용문도 가능합니다.

<!-- 중첩 인용 -->
> 첫 번째 레벨
>> 두 번째 레벨
```

## 수평선

### HTML

```html
<hr>
<hr/>
<hr />
```

### Markdown

```markdown
---

***

___
```

## 체크박스 (GitHub Flavored Markdown)

### HTML

```html
<ul>
  <li><input type="checkbox" checked disabled> 완료된 작업</li>
  <li><input type="checkbox" disabled> 미완료 작업</li>
  <li><input type="checkbox" disabled> 또 다른 작업</li>
</ul>
```

### Markdown

```markdown
- [x] 완료된 작업
- [ ] 미완료 작업
- [ ] 또 다른 작업
```

## 주석

### HTML

```html
<!-- 이것은 HTML 주석입니다 -->
```

### Markdown

```markdown
<!-- 이것은 Markdown 주석입니다 (HTML 주석과 동일) -->

[//]: # (이것도 Markdown 주석 방식입니다)
[comment]: <> (또 다른 주석 방식)
```

## 특수 문자 이스케이프

### HTML

```html
&lt;  <!-- < -->
&gt;  <!-- > -->
&amp; <!-- & -->
&quot; <!-- " -->
&#42; <!-- * -->
```

### Markdown

```markdown
\*   <!-- 별표 -->
\_   <!-- 밑줄 -->
\#   <!-- 해시 -->
\`   <!-- 백틱 -->
\[   <!-- 대괄호 -->
\|   <!-- 파이프 -->
```

## 변환 도구 추천

| 도구 | 특징 | URL |
|------|------|-----|
| **Turndown** | JavaScript 라이브러리 | [turndown](https://github.com/mixmark-io/turndown) |
| **html2text** | Python 라이브러리 | [html2text](https://github.com/Alir3z4/html2text) |
| **Pandoc** | 범용 문서 변환기 | [pandoc.org](https://pandoc.org/) |
| **MarkdownIt** | Markdown 파서/렌더러 | [markdown-it](https://github.com/markdown-it/markdown-it) |

## 변환 시 주의사항

1. **공백 처리**: HTML의 여러 공백은 하나로 합쳐지지만, Markdown은 줄바꿈에 민감합니다
2. **중첩 태그**: 복잡한 중첩 구조는 수동 정리가 필요할 수 있습니다
3. **스타일 손실**: CSS 스타일은 Markdown으로 변환되지 않습니다
4. **테이블 제한**: Markdown 테이블은 셀 병합을 지원하지 않습니다

---

## 참고 자료

- [GitHub Flavored Markdown Spec](https://github.github.com/gfm/)
- [CommonMark Spec](https://spec.commonmark.org/)
- [Markdown Guide](https://www.markdownguide.org/)
