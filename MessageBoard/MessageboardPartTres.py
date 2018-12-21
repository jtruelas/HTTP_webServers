#!/usr/bin/env python3
#
# Step three in building the messageboard server.
#
# Instructions:
#   1. In the do_POST method, send a 303 redirect back to the / page.
#   2. In the do_GET method, put the response together and send it.

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

memory = []

# form variable
form = '''<!DOCTYPE html>
  <title>Message Board</title>
  <form method="POST" action="http://localhost:8000/">
    <textarea name="message"></textarea>
    <br>
    <button type="submit">Post it!</button>
  </form>
  <pre>
  {}
  </pre>
  '''
  
class MessageboardHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # get length of request body
        length = int(self.headers.get('Content-length', 0))

        # read the correct amount of data
        data = self.rfile.read(length).decode()

        # extract message from the request data
        message = parse_qs(data)["message"][0]

        # escape HTML tags in the messag
        message = message.replace("<", "&lt;")

        # store to memory
        memory.append(message)

        # send status code
        self.send_response(303)

        # send headers
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        # send status code
        self.send_response(200)

        # send headers
        self.send_header('Content-type', 'text/html; charset=UTF-8')
        self.end_headers()

        # form a response
        response = form.format("\n".join(memory))

        # send a response body
        self.wfile.write(response.encode())
        


if __name__ == '__main__':
    server_address = ('', 8000) # serves on all addresses through port 8000
    httpd = HTTPServer(server_address, MessageboardHandler)
    httpd.serve_forever()