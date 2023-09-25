#  coding: utf-8 
# from _socket import _RetAddress
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        res = self.handle_route(self.data)
        print(res)
        self.request.sendall(res)

    def handle_route(self, data):        
        lines = str(data).split()
        print(lines)

        # Assuming self.data contains the request
        http_response = "HTTP/1.1 200 OK\r\n"        

        if "GET" in lines[0]:
            try:
                if lines[1].endswith(".html"):
                    http_response += "Content-Type: text/html\r\n"
                    http_response += "\r\n"  # Extra newline to indicate end of headers
                    with open("www/" + lines[1], "r") as f:
                        lines = f.readlines()
                        for line in lines:
                            http_response += line
                
                elif lines[1].endswith(".css/"):
                    http_response += "Content-Type: text/css\r\n"
                    http_response += "\r\n"  # Extra newline to indicate end of headers
                    f_name = lines[1].replace(".css/", ".css")
                    with open("www/" + f_name, "r") as f:
                        lines = f.readlines()
                        for line in lines:
                            http_response += line
                
                elif lines[1].endswith("/"):
                    print("here2")
                    http_response += "Content-Type: text/html\r\n"
                    http_response += "\r\n"  # Extra newline to indicate end of headers
                    with open("www/" + lines[1] + "index.html", "r") as f:
                        lines = f.readlines()
                        for line in lines:
                            http_response += line
                else:
                    redirect_url = "http://127.0.0.1:8080" + lines[1] + "/"
                    http_response = "HTTP/1.1 301 Moved Permanently\r\n"                    
                    http_response += "Content-Type: text/html\r\n"
                    http_response += f"Location: {redirect_url}"

                return bytes(http_response, "utf-8")
            
            except Exception as e:
                print(e)
                http_response = "HTTP/1.1 404 Not Found\r\n" 
                http_response += "Content-Type: text/html\r\n"
                http_response += "\r\n"  # Extra newline to indicate end of headers
                http_response += "<html><body>404 Not Found</body></html>"
   
                return bytes(http_response, "utf-8")
            
        else: # This server can't support any other method
            http_response = b"HTTP/1.1 405 Method Not Allowed\r\n"
            http_response += b"Content-Type: text/html\r\n"
            http_response += b"\r\n"  # Extra newline to indicate end of headers
            http_response += b"<html><body>405 Method Not Allowed</body></html>"

            return http_response
            

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
