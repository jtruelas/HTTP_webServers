# Find the length of the POST request data
#
# Read the correct amount of request data
#
# Run the MessageboardPartUno.py server
#
# Open the MessageboardPartUno.html file in browser
#
# Run test.py with the server running

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

class MessageboardHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # get length of request body
        length = int(self.headers.get('Content-length', 0))

        # read the correct amount of data
        data = self.rfile.read(length).decode()

        # extract message from the request data
        message = parse_qs(data)["message"][0]

        # send status code
        self.send_response(200)

        # send headers
        self.send_header('Content-type', 'text/plain; charset=UTF-8')
        self.end_headers()

        # send a response body
        self.wfile.write(message.encode())

if __name__ == '__main__':
	server_address = ('', 8000) # serves on all addresses through port 8000
	httpd = HTTPServer(server_address, MessageboardHandler)
	httpd.serve_forever()