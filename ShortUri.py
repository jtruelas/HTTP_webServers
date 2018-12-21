#!/usr/bin/env python3
#
# This server is intended to serve three kinds of requests:
#
#   * A GET request to the / (root) path.  The server returns a form allowing
#     the user to submit a new name/URI pairing.  The form also includes a
#     listing of all the known pairings.
#   * A POST request containing "longuri" and "shortname" fields.  The server
#     checks that the URI is valid (by requesting it), and if so, stores the
#     mapping from shortname to longuri in its dictionary.  The server then
#     redirects back to the root path.
#   * A GET request whose path contains a short name.  The server looks up
#     that short name in its dictionary and redirects to the corresponding
#     long URI.

import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote

memory = {}

htmlForm = '''<!DOCTYPE html>
<html>
<head>
	<title>Short Uri</title>
</head>
<form method="POST" action="http://localhost:8000">
	<label>Long URI:
        <input name="long_url">
    </label>
    <br>
    <label>Short name:
        <input name="short_url">
    </label>
    <br>
    <button type="submit" name="submit">Save</button>
</form>
<br>
<p>URLs I know of:</p>
<pre>
{}
</pre>
</html>
'''

def check_Uri(Uri, timeout=2):
	try:
		# sets varible to status code
		uri = requests.get(Uri, timeout=timeout)
		return uri.status_code == 200
	except requests.RequestException:
		# if GET request raised an exception uri is bad
		return False


class shortUri(BaseHTTPRequestHandler):

	def do_POST(self):
		# find length of response body
		length = int(self.headers.get('Content-length', 0))
		# read data
		data = self.rfile.read(length).decode()
		# extract text input
		params = parse_qs(data)

		# check if fields are filled
		if "long_url" not in params or "short_url" not in params:
			# send response code
			self.send_response(400)
			# send headers
			self.send_header('Content-type', 'text/plain; charset=utf-8')
			self.end_headers()
			# send error message
			self.wfile.write("error 400: All fields not empty.".encode())
			return

		longurl = params["long_url"][0]
		shorturl = params["short_url"][0]
		# check longurl validity
		if check_Uri(longurl):
			# save entry
			memory[shorturl] = longurl
			# send response code
			self.send_response(303)
			# send headers
			self.send_header('Location', '/')
			self.end_headers()
		else:
			# send response code
			self.send_response(404)
			# send headers
			self.send_header('Content-type', 'text/plain; charset=utf-8')
			self.end_headers()
			# send error message
			self.wfile.write(
				"error 404: Invalid URL entry. Make sure to enter full address.".encode())

	def do_GET(self):
		# assign path to variable
		short_uri = unquote(self.path[1:])

		# check if short_uri was entered
		if short_uri:
			if short_uri in memory:
				# send a response code
				self.send_response(303)
				# send headers
				self.send_header('Location', memory[short_uri])
				self.end_headers()
			else:
				# send a response code
				self.send_response(404)
				# send headers
				self.send_header('Content-type', 'text/plain; charset=utf-8')
				self.end_headers()
				# display error message
				self.wfile.write("error 404: I do not know {}.".format(short_uri).encode())
		else:
			# send a response code
			self.send_response(200)
			# send headers
			self.send_header('Content-type', 'text/html; charset=utf-8')
			self.end_headers()
			# display form and update with saved uri(s)
			savedUri = "\n".join("{} : {}".format(key, memory[key])
				for key in sorted(memory.keys()))
			self.wfile.write(htmlForm.format(savedUri).encode())

if __name__ == '__main__':
	server_address = ('', 8000)
	httpd = HTTPServer(server_address, shortUri)
	httpd.serve_forever()