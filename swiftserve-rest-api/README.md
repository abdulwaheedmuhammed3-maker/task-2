# SwiftServe Service Requests REST API

A small, stranger-friendly REST API for a SwiftServe pilot. It manages **service requests** such as electrical repairs, plumbing, cleaning, laundry and errands.

## Design choices

- **Runtime:** Node.js 20+
- **Storage:** in-memory `Map` only. No database, file storage, authentication or real personal data.
- **API style:** JSON over HTTP using standard REST methods.
- **Specification:** `openapi.yaml` (OpenAPI 3.0.3)
- **Tests:** built-in Node test runner; no test dependency required.

## Run in five minutes

```bash
cd swiftserve-rest-api
node src/server.js
```

The API starts at `http://127.0.0.1:3000`.

In another terminal:

```bash
npm test
```

You should see all tests pass.

## Endpoints

| Method | Endpoint | Purpose | Success |
|---|---|---|---|
| `POST` | `/api/v1/jobs` | Create a service request | `201 Created` |
| `GET` | `/api/v1/jobs` | List service requests | `200 OK` |
| `GET` | `/api/v1/jobs/:id` | Read one request | `200 OK` |
| `PATCH` | `/api/v1/jobs/:id` | Update fields | `200 OK` |
| `DELETE` | `/api/v1/jobs/:id` | Delete request | `204 No Content` |

Optional filter: `GET /api/v1/jobs?status=pending`

## Example requests and responses

### Create

```bash
curl -X POST http://127.0.0.1:3000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{"service":"electrical","description":"Ceiling light needs repair","area":"Tanke, Ilorin"}'
```

Example response (`201`):

```json
{
  "data": {
    "id": "2f4cfaa0-3b3c-4d92-b8a6-5c8c5d553e7d",
    "service": "electrical",
    "description": "Ceiling light needs repair",
    "area": "Tanke, Ilorin",
    "status": "pending",
    "createdAt": "2026-09-30T12:00:00.000Z",
    "updatedAt": "2026-09-30T12:00:00.000Z"
  }
}
```

### List

```bash
curl http://127.0.0.1:3000/api/v1/jobs
```

Example (`200`):

```json
{
  "data": [],
  "count": 0
}
```

### Update

```bash
curl -X PATCH http://127.0.0.1:3000/api/v1/jobs/2f4cfaa0-3b3c-4d92-b8a6-5c8c5d553e7d \
  -H "Content-Type: application/json" \
  -d '{"status":"accepted"}'
```

### Delete

```bash
curl -i -X DELETE http://127.0.0.1:3000/api/v1/jobs/2f4cfaa0-3b3c-4d92-b8a6-5c8c5d553e7d
```

Response: `204 No Content` with an empty body.

## Validation and consistent errors

`POST` requires `service`, `description` and `area`. `service` must be one of:

`cleaning`, `laundry`, `electrical`, `plumbing`, `ac-repair`, `appliance-repair`, `errand`

Descriptions must be 10–500 characters and areas 2–80 characters.

`PATCH` allows any subset of those fields plus `status`, which must be `pending`, `accepted`, `completed` or `cancelled`.

Bad input uses the same envelope:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "details": [
      "description must be a string between 10 and 500 characters."
    ]
  }
}
```

## Status code choices

- **200 OK** — successful reads, lists and updates.
- **201 Created** — a new service request was created.
- **204 No Content** — deletion succeeded and there is intentionally no response body.
- **400 Bad Request** — request syntax is invalid, such as malformed JSON or an invalid query parameter.
- **404 Not Found** — the route or requested job does not exist.
- **405 Method Not Allowed** — the HTTP method is not supported; the response includes an `Allow` header.
- **422 Unprocessable Content** — the JSON is syntactically valid but fails business/input validation.
- **500 Internal Server Error** — unexpected server-side failure; implementation details are not exposed.

## Privacy and data handling

The API accepts only a service category, short job description, area label and status. It does **not** require names, phone numbers, email addresses, payment-card information or precise home addresses. Records exist only in RAM and disappear when the process stops.

## Files

- `src/server.js` — starts the HTTP server.
- `src/app.js` — routes, validation and in-memory store.
- `test/api.test.js` — automated API tests.
- `openapi.yaml` — machine-readable API specification.
