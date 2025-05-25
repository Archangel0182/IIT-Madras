from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # Parse query parameters (e.g., ?name=X&name=Y)
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        names = params.get('name', [])
        
        # Handle single/multiple names
        if isinstance(names, str):
            names = [names]
        elif names and isinstance(names[0], list):
            names = names[0]

        # Load marks from JSON
        json_path = os.path.join(os.path.dirname(__file__), 'q-vercel-python.json')
        with open(json_path, 'r') as f:
            data = json.load(f)  # JSON is a LIST of dictionaries
            marks_dict = {item['name']: item['marks'] for item in data}
            marks = [marks_dict.get(name, 0) for name in names]

        # Return JSON response
        self.wfile.write(json.dumps({"marks": marks}).encode())

# For local testing (optional)
if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8000), Handler)
    server.serve_forever()