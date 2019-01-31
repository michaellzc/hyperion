const express = require('express');
const proxy = require('http-proxy-middleware');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.static(path.join(__dirname, 'build')));

app.get('/*', function(req, res) {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

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

app.listen(PORT, () => console.log(`Listening on :${PORT}`));
