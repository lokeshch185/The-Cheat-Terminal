const express = require('express');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const fs = require('fs').promises;
const path = require('path');
const multer = require('multer');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const FILES_DIR = path.join(__dirname, 'files');

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '');

async function ensureFilesDir() {
  try {
    await fs.access(FILES_DIR);
  } catch {
    await fs.mkdir(FILES_DIR, { recursive: true });
  }
}

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    await ensureFilesDir();
    cb(null, FILES_DIR);
  },
  filename: (req, file, cb) => {
    const sanitizedFilename = file.originalname.replace(/[^a-zA-Z0-9._-]/g, '_');
    cb(null, sanitizedFilename);
  }
});

const upload = multer({ 
  storage: storage,
  limits: { fileSize: 10 * 1024 * 1024 } // 10MB limit
});

// Initialize files directory on startup
ensureFilesDir();

// GET endpoint for code solution by filename
app.get('/solution/:filename', async (req, res) => {
  try {
    const { filename } = req.params;
    
    if (filename.includes('..') || filename.includes('/') || filename.includes('\\')) {
      return res.status(400).json({ 
        error: 'Invalid filename',
        message: 'Filename cannot contain path traversal characters'
      });
    }
    
    const filePath = path.join(FILES_DIR, filename);
    
    try {
      const fileContent = await fs.readFile(filePath, 'utf8');
      
      // Determine file extension for content type
      const ext = path.extname(filename).toLowerCase();
      const contentTypes = {
        '.js': 'application/javascript',
        '.ts': 'application/typescript',
        '.py': 'text/x-python',
        '.java': 'text/x-java-source',
        '.cpp': 'text/x-c++src',
        '.c': 'text/x-csrc',
        '.html': 'text/html',
        '.css': 'text/css',
        '.json': 'application/json',
        '.txt': 'text/plain'
      };
      
      const contentType = contentTypes[ext] || 'text/plain';
      
      res.setHeader('Content-Type', contentType);
      res.send(fileContent);
    } catch (fileError) {
      if (fileError.code === 'ENOENT') {
        return res.status(404).json({ 
          error: 'File not found',
          message: `File '${filename}' not found in files directory`
        });
      }
      throw fileError;
    }
  } catch (error) {
    res.status(500).json({ 
      error: 'Internal server error',
      message: error.message 
    });
  }
});

// POST endpoint to upload solution file
app.post('/solution', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ 
        error: 'Bad request',
        message: 'No file uploaded. Please use multipart/form-data with field name "file"' 
      });
    }
    
    const filename = req.file.filename;
    
    res.status(201).json({
      success: true,
      message: 'Solution uploaded successfully',
      filename: filename,
      originalName: req.file.originalname,
      size: req.file.size,
      path: `/solution/${filename}`
    });
  } catch (error) {
    res.status(500).json({ 
      error: 'Internal server error',
      message: error.message 
    });
  }
});

// GET endpoint to query Gemini
app.get('/gemini', async (req, res) => {
  try {
    const { query } = req.query;
    
    if (!query) {
      return res.status(400).json({ 
        error: 'Bad request',
        message: 'Query parameter is required. Use ?query=your question' 
      });
    }
    
    if (!process.env.GEMINI_API_KEY) {
      return res.status(500).json({ 
        error: 'Configuration error',
        message: 'GEMINI_API_KEY is not set in environment variables' 
      });
    }
    
    const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });
    
    const result = await model.generateContent(query);
    const response = await result.response;
    const text = response.text();
    
    res.json({
      success: true,
      query: query,
      response: text,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ 
      error: 'Internal server error',
      message: error.message 
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok',
    timestamp: new Date().toISOString()
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({ 
    message: 'Ace the Test with the Solution APIs packed with Gemini Integration',
    endpoints: {
      'GET /solution/:filename': 'Get a solution file by filename',
      'POST /solution': 'Upload a file directly (multipart/form-data, field: "file")',
      'GET /gemini?query=your question': 'Query Gemini AI',
      'GET /health': 'Health check'
    }
  });
});

// Start server
(async () => {
  await ensureFilesDir();
  app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
    console.log(`Files directory: ${FILES_DIR}`);
  });
})();

