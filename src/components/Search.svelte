<script lang="ts">
import I18nKey from "@i18n/i18nKey";
import { i18n } from "@i18n/translation";
import Icon from "@iconify/svelte";
import { searchIcon } from "@/constants/local-icons";
import type { SearchResult } from "@/global";

let keywordDesktop = "";
let keywordMobile = "";
let result: SearchResult[] = [];
let status = "";
let searchVersion = 0;
let mobileInput: HTMLInputElement;
const searchLabel = i18n(I18nKey.search);

function togglePanel() {
	const panel = document.getElementById("search-panel");
	const closed = panel?.classList.toggle("float-panel-closed");
	if (closed === false) {
		mobileInput?.focus();
		void search(keywordMobile, false);
	}
}

async function search(keyword: string, desktop: boolean) {
	const query = keyword.trim();
	const version = ++searchVersion;
	const panel = document.getElementById("search-panel");
	if (desktop) panel?.classList.toggle("float-panel-closed", !query);
	result = [];
	status = query ? "검색 중…" : "";
	if (!query) return;

	try {
		const pagefind = await window.pagefindReady;
		if (!pagefind) {
			if (version === searchVersion) {
				status = import.meta.env.DEV
					? "빌드한 사이트에서 검색할 수 있습니다."
					: "검색을 불러오지 못했습니다.";
			}
			return;
		}
		const response = await pagefind.search(query);
		const matches = await Promise.all(response.results.slice(0, 20).map((item) => item.data()));
		if (version === searchVersion) {
			result = matches;
			status = matches.length ? "" : "검색 결과가 없습니다.";
		}
	} catch {
		if (version === searchVersion) status = "검색을 불러오지 못했습니다.";
	}
}

</script>

<div id="search-bar" class="hidden lg:flex transition-all items-center h-11 mr-2 rounded-lg
	bg-black/[0.04] hover:bg-black/[0.06] focus-within:bg-black/[0.06]
	dark:bg-white/5 dark:hover:bg-white/10 dark:focus-within:bg-white/10">
	<Icon icon={searchIcon} class="absolute text-[1.25rem] pointer-events-none ml-3 transition my-auto text-black/30 dark:text-white/30" />
	<input type="search" aria-label={searchLabel} placeholder={searchLabel} bind:value={keywordDesktop}
		on:input={(event) => search(event.currentTarget.value, true)} on:focus={() => search(keywordDesktop, true)}
		class="transition-all pl-10 text-sm bg-transparent outline-0 h-full w-40 active:w-60 focus:w-60 text-75" />
</div>

<button on:click={togglePanel} aria-label={searchLabel} id="search-switch"
	class="btn-plain scale-animation lg:!hidden rounded-lg w-11 h-11 active:scale-90">
	<Icon icon={searchIcon} class="text-[1.25rem]" />
</button>

<div id="search-panel" class="float-panel float-panel-closed search-panel absolute md:w-[30rem]
	top-20 left-4 md:left-[unset] right-4 shadow-2xl rounded-2xl p-2">
	<div class="flex relative lg:hidden transition-all items-center h-11 rounded-xl
		bg-black/[0.04] focus-within:bg-black/[0.06] dark:bg-white/5 dark:focus-within:bg-white/10">
		<Icon icon={searchIcon} class="absolute text-[1.25rem] pointer-events-none ml-3 transition my-auto text-black/30 dark:text-white/30" />
		<input type="search" aria-label={searchLabel} placeholder={searchLabel} bind:this={mobileInput} bind:value={keywordMobile}
			on:input={(event) => search(event.currentTarget.value, false)}
			class="pl-10 pr-3 absolute inset-0 w-full text-sm bg-transparent outline-0 text-75" />
	</div>

	{#if status}
		<p class="p-3 text-sm text-75" role="status">{status}</p>
	{/if}
	{#each result as item}
		<a href={item.url} class="transition first-of-type:mt-2 lg:first-of-type:mt-0 group block
			rounded-xl text-lg px-3 py-2 hover:bg-[var(--btn-plain-bg-hover)] active:bg-[var(--btn-plain-bg-active)]">
			<div class="transition text-90 inline-flex font-bold group-hover:text-[var(--primary)]">{item.meta.title}</div>
			<div class="transition text-sm text-50">{@html item.excerpt}</div>
		</a>
	{/each}
</div>

<style>
	.search-panel {
		max-height: calc(100vh - 100px);
		overflow-y: auto;
	}
</style>
