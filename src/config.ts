import type {
	ExpressiveCodeConfig,
	LicenseConfig,
	NavBarConfig,
	ProfileConfig,
	SiteConfig,
} from "./types/config";
import { LinkPreset } from "./types/config";

export const siteConfig: SiteConfig = {
	title: "NaksuGames",
	subtitle: "1인 개발 게임 · 나키온의 모험 개발기",
	lang: "ko",
	themeColor: { hue: 250, fixed: false },
	banner: {
		enable: false,
		src: "",
		position: "center",
		credit: { enable: false, text: "", url: "" },
	},
	toc: { enable: true, depth: 2 },
	favicon: [],
};

export const navBarConfig: NavBarConfig = {
	links: [LinkPreset.Home, LinkPreset.Archive, LinkPreset.About],
};

export const profileConfig: ProfileConfig = {
	avatar: "assets/images/avatar.jpg",
	name: "NaksuGames",
	bio: "배운짓이 게임쪽 서버 개발만 거진 20년 했어요\n나이는 먹어가고 은퇴 하면 1인 개발 하고 싶어서\n준비 해 가는 과정을 블로그로 남겨요\n죽을때까지 게임 개발만 하려고요",
	links: [
		{
			name: "YouTube",
			icon: "fa6-brands:youtube",
			url: "https://www.youtube.com/@naksupapa",
		},
		{
			name: "GitHub",
			icon: "fa6-brands:github",
			url: "https://github.com/rs1017",
		},
	],
};

export const licenseConfig: LicenseConfig = {
	enable: false,
	name: "",
	url: "",
};

export const expressiveCodeConfig: ExpressiveCodeConfig = {
	theme: "github-dark",
};
