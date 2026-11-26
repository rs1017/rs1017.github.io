# 프린터블 플레이룸

유아와 초등 저학년을 위한 출력 활동지 사이트입니다. [Astro](https://astro.build/)와 [Fuwari](https://github.com/saicaca/fuwari)를 사용합니다. 운영 주소는 https://rs1017.github.io/ 입니다.

## 로컬 실행

Node.js 24와 `package.json`에 고정된 pnpm을 사용합니다.

```sh
pnpm install --frozen-lockfile
pnpm check
pnpm build
pnpm preview
```

검색 인덱스는 빌드에서 생성됩니다. 검색을 확인하려면 `pnpm preview`로 빌드 결과를 엽니다.

## 게시와 배포

`pnpm new-post 글-이름`으로 활동지 게시글을 만듭니다. 게시글은 `src/content/posts/`에 둡니다. 활동지 제작 기준은 [AGENTS.md](AGENTS.md)를 참고하세요.

GitHub Pages의 게시 방식은 GitHub Actions입니다. 개발 브랜치와 PR에서도 빌드를 검증하며 `main`에서만 배포합니다. Jekyll 시기의 파일과 이력은 `backup/jekyll-before-fuwari`에서 확인할 수 있습니다.

## 광고와 분석

기존 공개 AdSense 게시자 ID와 `ads.txt`를 유지했습니다. 기존 사이트는 자동 광고를 사용했고 개별 광고 단위 ID는 없었습니다. Google Analytics 측정 ID와 유효한 Google Search Console 확인 값은 없었습니다.

새 사이트는 기본값에서 광고와 분석 스크립트를 호출하지 않습니다. 광고를 시작하기 전에 GitHub Pages 및 AdSense 정책, 아동 대상 콘텐츠의 광고 설정, 해당 지역의 동의 요건을 검토하고 개인정보처리방침을 갱신합니다. 게시글용 광고 단위를 사용하려면 GitHub Actions 저장소 변수에 `PUBLIC_ADSENSE_ENABLED=true`와 `PUBLIC_ADSENSE_POST_SLOT`을 설정합니다.

Fuwari 원본은 `6d39b0dec41282e7852e23e032998a5789abee28`입니다. MIT 고지는 [LICENSE](LICENSE)에 있습니다. UI 아이콘은 [Google Material Symbols](https://github.com/google/material-design-icons)와 Dave Gandy의 [Font Awesome](https://fontawesome.com/license/free)에서 가져왔습니다.
