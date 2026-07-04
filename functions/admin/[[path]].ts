export const onRequest: PagesFunction<{
	ADMIN_USER?: string;
	ADMIN_PASSWORD?: string;
}> = async ({ request, env, next }) => {
	const user = env.ADMIN_USER;
	const password = env.ADMIN_PASSWORD;

	if (!user || !password) {
		return new Response('Admin access is not configured.', { status: 503 });
	}

	const authorization = request.headers.get('Authorization') ?? '';
	const expected = `Basic ${btoa(`${user}:${password}`)}`;

	if (authorization !== expected) {
		return new Response('Authentication required.', {
			status: 401,
			headers: {
				'WWW-Authenticate': 'Basic realm="Mirck Admin"',
				'Cache-Control': 'no-store',
			},
		});
	}

	return next();
};
