class Request: 
  
  def __init__(self, request_text):
    self.request      = request_text.split('\r\n')
    self.request_line = self.request.pop(0).split(' ')
    self.headers      = self.parse_headers()
    self.method       = self.request_line[0]
    self.path         = self.request_line[1]
    self.url          = self.headers['host']

  
  def parse_headers(self):
    request = self.request
    headers = {}

    for header in request:
      seperated_header_value = header.split(': ')
      if len(seperated_header_value) > 1:
        headers[seperated_header_value[0].lower()] = seperated_header_value[1]
    return headers 

get_req = [
    "GET /favicon.ico HTTP/1.1\r\n",
    "Host: localhost:9292\r\n",
    "Connection: keep-alive\r\n",
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36\r\n",
    "Accept: image/webp,image/apng,image/*,*/*;q=0.8\r\n",
    "Referer: http://localhost:9292/\r\n",
    "Accept-Encoding: gzip, deflate, br\r\n",
    "Accept-Language: en-US,en;q=0.9,es;q=0.8\r\n",
    "\r\n"
]


