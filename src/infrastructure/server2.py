from http.server import HTTPServer, SimpleHTTPRequestHandler
from src.domain.config import settings


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        print("ERROR_LOG_RECEIVED:", post_data.decode("utf-8"))
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    HTTPServer(("localhost", settings.server_port + 1), CORSRequestHandler).serve_forever()
