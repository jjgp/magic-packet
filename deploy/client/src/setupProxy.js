const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    createProxyMiddleware("/api", {
      target: process.env.CLIENT_API_PROXY,
      changeOrigin: true,
    })
  );

  app.use(
    createProxyMiddleware("/api/train", {
      target: process.env.CLIENT_API_PROXY,
      changeOrigin: true,
      proxyTimeout: 3 * 60 * 1e3,
      timeout: 3 * 60 * 1e3,
      ws: true,
    })
  );
};
