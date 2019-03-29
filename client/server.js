const express = require('express');
const proxy = require('http-proxy-middleware');
const path = require('path');
const compression = require('compression');

const app = express();
const PORT = process.env.PORT || 5000;

// Gzip
app.use(compression());

// Proxy api request
app.use(
  '/api',
  proxy({
    target: process.env.API_ROOT_URL,
    changeOrigin: true,
    ws: true,
    pathRewrite: {
      '^/api': '',
    },
  })
);

app.use(express.static(path.join(__dirname, 'build')));

// eslint-disable-next-line no-unused-vars
app.get('*', function(req, res) {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

// eslint-disable-next-line no-console
app.listen(PORT, () => console.log(`Listening on :${PORT}`));
