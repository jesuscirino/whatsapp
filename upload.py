import os
import cgi
from http.server import SimpleHTTPRequestHandler, HTTPServer

class FileUploadRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'

        return super().do_GET()

    def do_POST(self):
        if self.path == '/upload':
            content_type, pdict = cgi.parse_header(self.headers['content-type'])
            if content_type == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                pdict['CONTENT-LENGTH'] = int(self.headers['content-length'])
                files = cgi.parse_multipart(self.rfile, pdict)
                

                for file in files['file']:
                    filename = 'uploaded_file.bin'
                    with open(filename, 'wb') as f:
                        f.write(file)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'File uploaded successfully')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Not Found')

def run(server_class=HTTPServer, handler_class=FileUploadRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
