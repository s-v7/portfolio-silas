export default {
  async fetch(req, env, ctx) {
    const url = new URL(req.url);

    if(req.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
	  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
	  "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
      });
    }

    const BACKEND_URL = "https://api.backend.sv7-dev.com";
    const targetUrl = `${BACKEND_URL}${url.pathname}${url.serach}`;

    const modifiedRequest = new Request(targetUrl, {
      method: req.method,
      headers: req.headers,
      body: req.body,
      redirect: "follow"
    });

    try {
      const res = await fetch(modifiedRequest);
      const nHeaders = new Headers(res.headers);
      nHeaders.set("Access-Controll-Allow-Origin", "*");
      nHeaders.set("X-Powered-By", "Atlas-AI-Edge-Worker");

      return new Response(res.body, {
        status: res.status,
	statustext: res.statusText,
	headers: nHeaders
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: "Edge Proxy Error", details: err.message }), {
        status: 502,
	headers: {"Content-Type": "application/json" },
      });
    }
  }
};
      
