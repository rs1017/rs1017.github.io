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
	avatar: "",
	name: "NaksuGames",
	bio: "19년차 게임 서버 개발자(현업). 은퇴 후 AI와 함께 인디 게임을 만들고 출시하는 것이 목표입니다.",
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
