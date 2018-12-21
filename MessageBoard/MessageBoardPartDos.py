#!/usr/bin/env python3
#
# Step two in building the messageboard server:
# A server that handles both GET and POST requests.
#
# Instructions:
#
# 1. Add a string variable that contains the form from Messageboard.html.
# 2. Add a do_GET method that returns the form.
#
# You don't need to change the do_POST method in this exercise!
#
# To test your code, run this server and access it at http://localhost:8000/
# in your browser.  You should see the form.  Then put a message into the
# form and submit it.  You should then see the message echoed back to you.

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

# form variable
form = """<!DOCTYPE html>
  <title>Message Board</title>
  <form method="POST" action="http://localhost:8000/">
    <textarea name="message"></textarea>
    <br>
    <button type="submit">Post it!</button>
  </form>
  """
  
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

    def do_GET(self):
        # send status code
        self.send_response(200)

        # send headers
        self.send_header('Content-type', 'text/html; charset=UTF-8')
        self.end_headers()

        # send a response body
        self.wfile.write(form.encode())
        


if __name__ == '__main__':
    server_address = ('', 8000) # serves on all addresses through port 8000
    httpd = HTTPServer(server_address, MessageboardHandler)
    httpd.serve_forever()