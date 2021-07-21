# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import re
import os.path

defaultHostName = "localhost"
defaultServerPort = 8080
configFileName = "config.json"
configHostKey = "hostname"
configPortKey = "port"
feedFileName = "feed.xml"
imageFileName = "image.png"

class MyServer(BaseHTTPRequestHandler):

    # Handle GET request
    def do_GET(self):
        if self.path == "/" + feedFileName:
            self.handle_Feed()
        elif re.search("/episode/", self.path):
            self.handle_Episode()
        elif self.path == "/" + imageFileName:
            self.handle_Image()
        else:
            self.handle_Not_Found("Not Found")
    
    # Handle request for RSS feed
    def handle_Feed(self):
        # Make sure feed file exists
        if not os.path.isfile(feedFileName):
            self.handle_Not_Found("No feed found!")
            return
        
        self.send_response(200)
        self.send_header("Content-type", "text/xml")
        self.end_headers()
        self.wfile.write(load_binary(feedFileName))
    
    # Handle request for podcast image
    def handle_Image(self):
        # Make sure the image file exists
        if not os.path.isfile(imageFileName):
            self.handle_Not_Found("No image found!")
            return
        
        self.send_response(200)
        self.send_header("Content-type", "image/png")
        self.end_headers()
        self.wfile.write(load_binary(imageFileName))

    # Handle episode request
    def handle_Episode(self):
        # Check if an mp3 file was requested
        m = re.search("[^/]+\.mp3", self.path)
        if not m:
            self.handle_Not_Found("No episode found for: " + self.path)
            return
        
        # Check if the requested file exists
        filename = "./episodes/" + m.group()
        if not os.path.isfile(filename):
            self.handle_Not_Found("No file found for episode: " + self.path)
            return
        
        self.send_response(200)
        self.send_header("Content-type", "audio/mpeg")
        self.end_headers()
        self.wfile.write(load_binary(filename))

    # Generic 404 handling
    def handle_Not_Found(self, message):
        self.send_error(404, message)
        self.end_headers()


def load_binary(file):
    with open(file, 'rb') as file:
        return file.read()
    


if __name__ == "__main__":

    hostName = defaultHostName
    serverPort = defaultServerPort

    if os.path.exists(configFileName):
        print("Found config! loading...")
        config = json.load(open(configFileName))
        if configHostKey in config:
            hostName = config[configHostKey]
        if configPortKey in config:
            serverPort = config[configPortKey]
    else:
        print("No config given! Using defaults...")  

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")