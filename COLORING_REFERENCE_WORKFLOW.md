# Coloring Reference Workflow

이 문서는 유아용 색칠 컨텐츠를 만들 때 `아이들이 좋아하는 인기 속성`을 반영하되, `공식 캐릭터를 그대로 복제하지 않는` 안전한 제작 기준입니다.

## 1. 레퍼런스 축

실제 검색 기준으로 강한 축은 다음과 같습니다.

- 여아 취향:
  - 티니핑 계열의 `반짝임`, `공주`, `리본`, `하트`, `작은 요정`, `핑크-퍼플 무드`
  - 티티체리 계열의 `소녀 팀`, `마법 아이템`, `귀여운 동물 동료`
  - 아이돌/변신소녀 계열의 `무대`, `마이크`, `별`, `헤어 액세서리`, `우정`

- 남아 취향:
  - 메탈카드봇/또봇 계열의 `변신 로봇`, `탈것`, `경찰/소방/구조`, `기계 디테일`
  - 공룡 계열의 `티라노`, `트리케라톱스`, `스테고사우루스`, `화산`, `정글`
  - 바다/탈것 계열의 `잠수함`, `기차`, `비행기`, `우주선`

- 공통 취향:
  - 토끼, 고양이, 강아지, 오리 같은 친숙한 동물
  - 큰 눈, 둥근 얼굴, 단순한 실루엣
  - 장식 요소: 별, 구름, 꽃, 하트, 리본, 번개, 톱니

## 2. 금지선

- 공식 캐릭터 이름, 공식 로고, 공식 상징을 그대로 쓰지 않음
- 특정 캐릭터 복장/헤어/색 배합을 그대로 복제하지 않음
- “티니핑 하츄핑 그려줘” 같은 직접 복제 프롬프트 금지
- “메탈카드봇 블루캅 그대로” 같은 직접 복제 프롬프트 금지

## 3. 안전한 대체 방식

- `공식 IP 그대로`가 아니라 `속성 조합`으로 재설계

예시:

- 티니핑 느낌:
  - `반짝 요정 공주`, `하트 머리장식`, `리본 드레스`, `작은 별봉`

- 티티체리 느낌:
  - `마법소녀 탐험대`, `귀여운 동물 파트너`, `장난감 무전기`, `팀 배지`

- 메탈카드봇 느낌:
  - `경찰차 변신 로봇`, `소방차 변신 로봇`, `드릴 팔 구조 로봇`

- 공룡메카/공룡물 느낌:
  - `친근한 아기 공룡`, `기계 장갑 공룡`, `화산 배경 공룡 친구`

## 4. 색칠 페이지 기준

- 배경은 기본적으로 흰색
- 넓은 면을 아이가 직접 칠할 수 있게 비워둠
- 굵은 외곽선 + 얇은 내부선 조합
- 검은 면채움 최소화
- 검은 바이저, 검은 갑옷 패널, 검은 실루엣 면은 금지에 가깝게 본다
- 한 페이지에 주제 하나만

## 5. 추천 페이지 라인업

### 여아 축

- 반짝 공주 요정 10장
- 마이크 든 무대 소녀 10장
- 리본 고양이 마법친구 10장
- 별봉 든 변신소녀 10장

### 남아 축

- 구조 로봇 10장
- 경찰 로봇 10장
- 공룡 로봇 10장
- 잠수함/기차/우주선 10장

### 공통 축

- 공룡 친구 10장
- 토끼/고양이/오리 친구 10장
- 바다 친구 10장
- 날씨 친구 10장

## 6. 고퀄 워크플로우

1. 한 포스트 주제를 1개 고른다.
2. 10장 샷리스트를 먼저 쓴다.
3. 각 장은 `1장 생성 -> 중복/구도 확인 -> 통과 시 다음 장` 순서로 진행한다.
4. 프롬프트는 항상 `white background`, `coloring page`, `black and white line art`, `large open spaces`를 포함한다.
5. 비슷한 구도/실루엣이 나오면 즉시 폐기하고 다시 뽑는다.
6. 10장이 다 모이면 그때 포스트를 갱신한다.

## 6-1. 웹 레퍼런스에서 확인한 공통점

- 로봇 색칠 페이지는 `정면 또는 3/4 정면` 단독 캐릭터 구도가 많다.
- 배경이 있더라도 `작은 구름`, `땅선`, `별`, `꽃` 정도로 제한된다.
- 얼굴은 크고 단순하다. 눈과 입이 바로 읽혀야 한다.
- 외곽선은 굵고, 내부 디테일은 적다.
- 큰 검은 면채움 대신 `빈 면적`을 남긴다.
- 공룡/로봇/요정 모두 `주인공 1명 + 작은 보조 장식` 구도가 가장 안정적이다.
- robot coloring pages 레퍼런스는 `cute cartoon robot`, `simple background`, `bold outline`이 가장 많다.
- anime coloring pages도 `캐릭터 시트`보다 `한 장면 한 인물`이 인쇄 적합성이 높다.

## 6-2. 강제 품질 게이트

- 한 페이지에 메인 주인공은 1명만 둔다.
- 메인 주인공은 페이지 폭의 최소 45% 이상을 차지해야 한다.
- 순수 장식 요소는 최대 4개까지만 둔다.
- 검은 실루엣 면채움은 금지한다.
- 배경 건물, 실내, 복잡한 풍경이 메인을 잡아먹으면 폐기한다.
- tracing, maze, English, counting 페이지에는 장식 캐릭터를 과하게 넣지 않는다.
- `multiple characters`, `character sheet`, `model sheet`, `collage`, `panel layout` 결과가 나오면 바로 폐기한다.
- 색이 조금이라도 남거나 회색 면이 넓게 깔리면 바로 폐기한다.
- 검은 면이 색칠 공간을 먹어버리면 바로 폐기한다.

## 6-3. 실패 시 전환 규칙

- 텍스트만으로 생성했는데 `그리드`, `패널`, `콜라주`, `반복 오브젝트`가 나오면 같은 방식으로 계속 밀지 않는다.
- 그런 경우에는 `고퀄 컬러 캐릭터 원본 생성 -> 선화 변환 -> 후정리` 파이프라인으로 즉시 전환한다.
- 여아풍 고퀄 색칠도안은 특히 `원본 캐릭터 퀄리티`를 먼저 확보한 뒤 선화화하는 쪽이 더 안정적이다.

## 7. 프롬프트 템플릿

## 7-1. 선호 키워드

- `drawing`
- `line drawing`
- `outline drawing`
- `black ink drawing`
- `clean monochrome drawing`
- `coloring book drawing`

## 7-2. 피해야 할 키워드

- `render`
- `cinematic`
- `glossy`
- `shaded`
- `colored`
- `panel`
- `character sheet`

### 공주/요정

`original magical fairy princess coloring page, black and white line art, big eyes, ribbon accessories, star wand, white background, large open spaces, printable worksheet`

### 로봇

`original rescue robot coloring page, black and white line art, vehicle inspired robot, simple mechanical details, white background, large open spaces, printable worksheet`

### 로봇 강화 템플릿

`original cute rescue robot hero coloring book drawing, single full body character only, centered composition, front view or 3/4 front view, clean outline drawing, black ink line drawing, monochrome, pure white background, no scenery, no floor, large open coloring spaces, simple mechanical details, printable worksheet`

### 로봇 네거티브 강화

`multiple characters, character sheet, collage, lineup, panel, comic page, color, colored fill, gray shading, background room, garage, city, heavy shadows`

### 공룡

`original friendly dinosaur coloring page, black and white line art, rounded cute face, simple scales, white background, large open spaces, printable worksheet`

### 아이돌/무대

`original stage performer girl coloring page, black and white line art, microphone, star accessories, cheerful pose, white background, large open spaces, printable worksheet`
