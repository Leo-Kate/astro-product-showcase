import { imageMap } from '../../src/generated/image-map';

async function handleImageRequest(params: Record<string, unknown>, request: Request, headOnly = false) {
	const image = String(params.image ?? '');
	const source = imageMap[image];

	if (!source) {
		return new Response('Image not found.', { status: 404 });
	}

	const cache = caches.default;
	const cacheKey = new Request(request.url, { method: 'GET' });
	const cached = await cache.match(cacheKey);
	if (cached) {
		return headOnly ? new Response(null, { status: cached.status, headers: cached.headers }) : cached;
	}

	const upstream = await fetch(source, {
		headers: {
			'User-Agent': 'Mozilla/5.0 Mirck image cache',
			Accept: 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
		},
		cf: {
			cacheEverything: true,
			cacheTtl: 60 * 60 * 24 * 30,
		},
	});

	if (!upstream.ok) {
		return new Response('Image unavailable.', { status: 502 });
	}

	const headers = new Headers(upstream.headers);
	headers.set('Cache-Control', 'public, max-age=31536000, immutable');
	headers.set('X-Robots-Tag', 'noindex');
	headers.delete('Set-Cookie');

	const response = new Response(upstream.body, {
		status: upstream.status,
		headers,
	});

	await cache.put(cacheKey, response.clone());
	return headOnly ? new Response(null, { status: response.status, headers: response.headers }) : response;
}

export const onRequestGet: PagesFunction = async ({ params, request }) => handleImageRequest(params, request);

export const onRequestHead: PagesFunction = async ({ params, request }) => handleImageRequest(params, request, true);
