/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

export default {
	async fetch(request, env, ctx) {

		const url = new URL(request.url);

		if (request.method === "GET" && url.pathname === "/readings")
		{
			const results = await env.DB.prepare(`
				SELECT
					g.name AS greenhouse,
					s.device_name,
					r.timestamp,
					r.type,
					r.value
				FROM sensor_readings r
				JOIN sensors s ON r.sensor_id = s.sensor_id
				JOIN greenhouses g ON s.greenhouse_id = g.greenhouse_id
				ORDER BY r.timestamp DESC
			`).all();

			return new Response(JSON.stringify(results.results), {
				headers: {"Content-Type": "application/json"}
			});
		}

		return new Response('Not Found', { status: 404 });
	},
};
