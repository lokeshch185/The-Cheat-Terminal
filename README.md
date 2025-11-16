# The-Cheating-Terminal

Ace the labs, pre-upload and read files directly from your terminal using https endpoint, packed along with Gemini endpoint for the unseen. Run it locally or globally based on internet access.


## Features

- **GET /solution/:filename** - Retrieve a solution file by filename from the `files` folder
- **POST /solution** - Upload a new solution file directly to the `files` folder
- **POST /gemini/query** - Query Google Gemini AI (gemini-2.5-flash model)

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file in the root directory:
```
PORT=3000
GEMINI_API_KEY=your_gemini_api_key_here
```

3. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

4. Start the server:
```bash
npm start
```

## API Endpoints

### GET /solution/:filename
Retrieve a solution file by its filename from the `files` folder.

**Parameters:**
- `filename` - The name of the file to retrieve (e.g., `solution.js`, `mycode.py`)

**Response:**
Returns the file content with appropriate Content-Type header based on file extension.

**Example:**
```
GET /solution/solution.js
```

Returns the JavaScript file content.

### POST /solution
Upload a new solution file directly to the `files` folder.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Field name: `file`

**Note:** The file will be saved with its original filename (sanitized for security). No need to provide code, filename, or language in the request body.

**Response:**
```json
{
  "success": true,
  "message": "Solution uploaded successfully",
  "filename": "solution.js",
  "originalName": "solution.js",
  "size": 1024,
  "path": "/solution/solution.js"
}
```

### POST /gemini/query
Query Gemini AI (using gemini-2.5-flash model) with a question.

**Request Body:**
```json
{
  "query": "What is JavaScript?"
}
```

**Response:**
```json
{
  "success": true,
  "query": "What is JavaScript?",
  "response": "Gemini AI response...",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

## Example Usage

### Upload a solution file:

**Mac / Linux:**
```bash
curl -X POST http://localhost:3000/solution \
  -F "file=@/path/to/your/file.js"
```

**Windows PowerShell:**
```powershell
curl -X POST http://localhost:3000/solution `
  -F "file=@C:\path\to\your\file.js"
```

**Windows CMD:**
```cmd
curl -X POST http://localhost:3000/solution ^
  -F "file=@C:\path\to\your\file.js"
```

Or using a form in HTML:
```html
<form action="http://localhost:3000/solution" method="POST" enctype="multipart/form-data">
  <input type="file" name="file" />
  <button type="submit">Upload</button>
</form>
```

### Get a solution file:

**Mac / Linux:**
```bash
# Display file content in terminal
curl http://localhost:3000/solution/hello.js

# Save file to disk (recommended for complete file retrieval)
curl http://localhost:3000/solution/hello.js -o hello.js

# Or use --no-buffer to disable buffering
curl --no-buffer http://localhost:3000/solution/hello.js
```

**Windows PowerShell:**
```powershell
# Display file content in terminal
curl http://localhost:3000/solution/hello.js

# Save file to disk (recommended for complete file retrieval)
curl http://localhost:3000/solution/hello.js -o hello.js

# Or use --no-buffer to disable buffering
curl --no-buffer http://localhost:3000/solution/hello.js
```

**Windows CMD:**
```cmd
REM Display file content in terminal
curl http://localhost:3000/solution/hello.js

REM Save file to disk (recommended for complete file retrieval)
curl http://localhost:3000/solution/hello.js -o hello.js

REM Or use --no-buffer to disable buffering
curl --no-buffer http://localhost:3000/solution/hello.js
```

### Query Gemini:

**Mac / Linux:**
```bash
curl -X POST http://localhost:3000/gemini/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is JavaScript?"}'
```

**Windows PowerShell:**
```powershell
curl -Method POST "http://localhost:3000/gemini/query" `
-Headers @{ "Content-Type" = "application/json" } `
-Body '{ "query": "What is JavaScript?" }' -o filename.txt
```

**Windows CMD:**
```cmd
curl -X POST http://localhost:3000/gemini/query ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"What is JavaScript?\"}"
```

