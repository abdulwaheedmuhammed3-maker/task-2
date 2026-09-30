import test from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import { requestHandler, resetStore } from '../src/app.js';

function startTestServer() {
  return new Promise((resolve) => {
    const server = http.createServer(requestHandler);
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

async function stopTestServer(server) {
  await new Promise((resolve, reject) => server.close((err) => err ? reject(err) : resolve()));
}

async function request(base, path, options = {}) {
  const response = await fetch(`${base}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    }
  });
  const text = await response.text();
  return { status: response.status, headers: response.headers, body: text ? JSON.parse(text) : null };
}

test.beforeEach(() => resetStore());

test('POST creates a service request and returns 201', async () => {
  const server = await startTestServer();
  const base = `http://127.0.0.1:${server.address().port}`;
  const response = await request(base, '/api/v1/jobs', {
    method: 'POST',
    body: JSON.stringify({ service: 'electrical', description: 'Ceiling light needs repair', area: 'Tanke, Ilorin' })
  });
  assert.equal(response.status, 201);
  assert.equal(response.body.data.service, 'electrical');
  assert.equal(response.body.data.status, 'pending');
  assert.ok(response.body.data.id);
  await stopTestServer(server);
});

test('GET collection and item return 200', async () => {
  const server = await startTestServer();
  const base = `http://127.0.0.1:${server.address().port}`;
  const created = await request(base, '/api/v1/jobs', {
    method: 'POST',
    body: JSON.stringify({ service: 'plumbing', description: 'Kitchen sink is leaking badly', area: 'GRA, Ilorin' })
  });
  const list = await request(base, '/api/v1/jobs');
  const item = await request(base, `/api/v1/jobs/${created.body.data.id}`);
  assert.equal(list.status, 200);
  assert.equal(list.body.count, 1);
  assert.equal(item.status, 200);
  assert.equal(item.body.data.id, created.body.data.id);
  await stopTestServer(server);
});

test('PATCH updates a job and DELETE removes it', async () => {
  const server = await startTestServer();
  const base = `http://127.0.0.1:${server.address().port}`;
  const created = await request(base, '/api/v1/jobs', {
    method: 'POST',
    body: JSON.stringify({ service: 'laundry', description: 'Weekly clothes washing service', area: 'Fate, Ilorin' })
  });
  const id = created.body.data.id;
  const updated = await request(base, `/api/v1/jobs/${id}`, {
    method: 'PATCH',
    body: JSON.stringify({ status: 'accepted' })
  });
  assert.equal(updated.status, 200);
  assert.equal(updated.body.data.status, 'accepted');
  const removed = await request(base, `/api/v1/jobs/${id}`, { method: 'DELETE' });
  assert.equal(removed.status, 204);
  const missing = await request(base, `/api/v1/jobs/${id}`);
  assert.equal(missing.status, 404);
  await stopTestServer(server);
});

test('bad input returns consistent validation errors', async () => {
  const server = await startTestServer();
  const base = `http://127.0.0.1:${server.address().port}`;
  const response = await request(base, '/api/v1/jobs', {
    method: 'POST',
    body: JSON.stringify({ service: 'rocket-launch', description: 'x', area: '' })
  });
  assert.equal(response.status, 422);
  assert.equal(response.body.error.code, 'VALIDATION_ERROR');
  assert.ok(Array.isArray(response.body.error.details));
  await stopTestServer(server);
});

test('malformed JSON returns 400 with the same error shape', async () => {
  const server = await startTestServer();
  const base = `http://127.0.0.1:${server.address().port}`;
  const response = await fetch(`${base}/api/v1/jobs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: '{not-json'
  });
  const body = await response.json();
  assert.equal(response.status, 400);
  assert.equal(body.error.code, 'INVALID_JSON');
  await stopTestServer(server);
});

test('unsupported method returns 405 and Allow header', async () => {
  const server = await startTestServer();
  const base = `http://127.0.0.1:${server.address().port}`;
  const response = await request(base, '/api/v1/jobs', { method: 'PUT', body: JSON.stringify({}) });
  assert.equal(response.status, 405);
  assert.equal(response.headers.get('allow'), 'GET, POST');
  assert.equal(response.body.error.code, 'METHOD_NOT_ALLOWED');
  await stopTestServer(server);
});
