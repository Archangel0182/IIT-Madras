from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.end_headers()

        # Parse query parameters (e.g., ?name=X&name=Y)
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        names = params.get('name', [])

        # Load marks from JSON
        with open('q-vercel-python.json', 'r') as f:
            data = json.load(f)
            marks = [data['students'].get(name, 0) for name in names]

        # Return JSON response
        response = json.dumps({"marks": marks})
        self.wfile.write(response.encode())

# For local testing (optional)
if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8000), Handler)
    server.serve_forever()