const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    createProxyMiddleware("/api", {
      proxyTimeout: 3 * 60 * 1e3,
      target: process.env.REACT_APP_API_PROXY,
      changeOrigin: true,
    })
  );
};
