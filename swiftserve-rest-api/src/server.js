import http from 'node:http';
import { requestHandler } from './app.js';

const host = process.env.HOST || '127.0.0.1';
const port = Number(process.env.PORT || 3000);

const server = http.createServer(requestHandler);

server.listen(port, host, () => {
  console.log(`SwiftServe API running at http://${host}:${port}`);
});
