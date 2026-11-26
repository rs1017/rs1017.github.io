// Keep this URL so browsers can replace the old Jekyll service worker.
self.addEventListener("install", (event) => {
	event.waitUntil(self.skipWaiting());
});

self.addEventListener("activate", (event) => {
	event.waitUntil(retireLegacyWorker());
});

async function retireLegacyWorker() {
	try {
		const legacyCaches = (await caches.keys()).filter((name) =>
			name.startsWith("chirpy-"),
		);
		await Promise.all(legacyCaches.map((name) => caches.delete(name)));
	} finally {
		await self.registration.unregister();
	}
}
