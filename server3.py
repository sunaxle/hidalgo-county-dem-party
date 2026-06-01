from http.server import HTTPServer, BaseHTTPRequestHandler
class LogHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print("ERROR_LOG_RECEIVED:", post_data.decode('utf-8'))
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.end_headers()

if __name__ == '__main__':
    HTTPServer(('localhost', 8003), LogHandler).serve_forever()
