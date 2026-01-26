# GPSA Publicity API Server

REST API for processing SDIF swim meet results files. Designed for integration with n8n and other automation tools.

## Quick Start

### Local Development

```bash
cd publicity-server
npm install
npm start
```

Server runs at `http://localhost:3000`

### Docker

```bash
cd publicity-server
docker-compose up
```

No build step required - uses official Node.js image with volume mounts for instant code sync.

## API Endpoints

### Health Check

```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.2",
  "timestamp": "2025-06-16T12:00:00.000Z"
}
```

### API Information

```
GET /api
```

**Response:**
```json
{
  "name": "GPSA Publicity API",
  "version": "1.2",
  "endpoints": { ... },
  "limits": {
    "maxFileSize": "256KB",
    "allowedExtensions": [".sd3", ".txt", ".zip"]
  }
}
```

### Process SDIF File

```
POST /api/process
Content-Type: multipart/form-data
```

**Request Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | File | Yes | SDIF file (.sd3, .txt, or .zip) |
| `override` | JSON string | No | Override configuration (see below) |

**Override Configuration:**
```json
{
  "enabled": true,
  "winnerCode": "GG",
  "reason": "Team forfeited due to insufficient swimmers"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "filename": "2025-06-16_GG_v_WW.html",
  "html": "<!DOCTYPE html>...",
  "metadata": {
    "meetName": "2025 Great Oaks v. Westfield",
    "meetDate": "2025-06-16",
    "teams": [
      {"code": "GG", "name": "Great Oaks", "score": 245.0},
      {"code": "WW", "name": "Westfield", "score": 198.0}
    ],
    "eventCount": 42
  }
}
```

## Error Responses

| HTTP Code | Condition | Example Response |
|-----------|-----------|------------------|
| 400 | No file uploaded | `{"success": false, "error": "No file uploaded"}` |
| 400 | Invalid file type | `{"success": false, "error": "Invalid file type. Allowed: .sd3, .txt, .zip"}` |
| 413 | File too large | `{"success": false, "error": "File too large. Maximum size is 256KB"}` |
| 422 | Invalid SDIF format | `{"success": false, "error": "Invalid SDIF format: Missing B1 (Meet) record"}` |
| 500 | Server error | `{"success": false, "error": "Internal server error"}` |

## Usage Examples

### cURL

```bash
# Basic usage
curl -X POST http://localhost:3000/api/process \
  -F "file=@meet_results.sd3"

# With override
curl -X POST http://localhost:3000/api/process \
  -F "file=@meet_results.sd3" \
  -F 'override={"enabled":true,"winnerCode":"GG","reason":"Forfeit"}'

# Save HTML output
curl -X POST http://localhost:3000/api/process \
  -F "file=@meet_results.sd3" \
  | jq -r '.html' > results.html
```

### n8n Integration

1. **HTTP Request Node:**
   - Method: `POST`
   - URL: `http://your-server:3000/api/process`
   - Body Content Type: `Form-Data/Multipart`

2. **Form Fields:**
   - `file`: Binary data from previous node (e.g., email attachment, webhook upload)
   - `override`: (Optional) JSON string for forfeit handling

3. **Response Processing:**
   - Access `$json.html` for the generated HTML
   - Access `$json.filename` for the suggested filename
   - Access `$json.metadata` for meet information

**Example n8n Workflow:**
```
Email Trigger → Extract Attachment → HTTP Request (API) → Write File → Send Notification
```

### JavaScript/Node.js

```javascript
const FormData = require('form-data');
const fs = require('fs');

const form = new FormData();
form.append('file', fs.createReadStream('meet_results.sd3'));

const response = await fetch('http://localhost:3000/api/process', {
  method: 'POST',
  body: form
});

const result = await response.json();
console.log(result.filename);
fs.writeFileSync(result.filename, result.html);
```

## Architecture

The API server uses the shared `publicity-core.js` module, ensuring identical parsing logic between the browser tool and API:

```
publicity-server/
├── server.mjs          # Express API server
├── package.json        # Dependencies
├── docker-compose.yml  # Docker configuration
└── README.md           # This file

lib/
└── publicity-core.js  # Shared parsing logic (mounted in Docker)
```

### Volume Mounts (Docker)

The Docker setup uses volume mounts instead of a Dockerfile:
- `./` → `/app` - Server code
- `../lib` → `/app/lib` - Shared module

**Benefits:**
- Changes to `lib/publicity-core.js` sync instantly (no rebuild needed)
- Same code used by browser and API
- Simpler deployment

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3000 | Server port |
| `NODE_ENV` | development | Environment mode |

## Troubleshooting

### "Cannot find module './lib/publicity-core.js'"

Ensure you're running from the `publicity-server` directory and the `lib` folder exists at the repository root:

```bash
ls ../lib/publicity-core.js  # Should exist
```

### Docker volume mount issues

On Windows, ensure Docker Desktop has access to the repository directory in Settings → Resources → File Sharing.

### File size errors

The API limits file uploads to 256KB. For larger files, extract the SDIF content before uploading.
