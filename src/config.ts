import type {
	ExpressiveCodeConfig,
	LicenseConfig,
	NavBarConfig,
	ProfileConfig,
	SiteConfig,
} from "./types/config";
import { LinkPreset } from "./types/config";

export const siteConfig: SiteConfig = {
	title: "프린터블 플레이룸",
	subtitle: "유아와 초등 저학년을 위한 출력 활동지",
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
	name: "Printable Playroom",
	bio: "집과 교실에서 바로 출력해 쓰는 활동지",
	links: [
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
