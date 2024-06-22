const http = require('http');
const fs = require('fs');
const path = require('path');

// Function to serve static files
function serveStaticFile(res, filePath, contentType) {
    fs.readFile(filePath, (err, data) => {
        if (err) {
            // If an error occurs, send a 500 Internal Server Error response
            res.writeHead(500, { 'Content-Type': 'text/plain' });
            res.end('Internal Server Error');
        } else {
            // If successful, send the file content with the specified content type
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(data);
        }
    });
}

// Create an HTTP server
const server = http.createServer((req, res) => {
    // Determine the file path based on the request URL
    let filePath = '.' + req.url;
    if (filePath === './') {
        filePath = './events.html'; // Default to events.html if no specific file is requested
    }

    // Determine the content type based on the file extension
    let contentType = 'text/html';
    const extname = path.extname(filePath);
    if (extname === '.css') {
        contentType = 'text/css';
    }

    // Serve the static file
    serveStaticFile(res, filePath, contentType);
});

// Set the port number
const PORT = process.env.PORT || 3000;

// Start the server
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
