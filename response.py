import datetime

class Response: 
  def __init__(self):
    self.http_version   = 'HTTP/1.1'
    self.status         = 500
    self.location       = ''
    self.content_type   = ''
    self.body           = ''
    self.content_length = len(self.body)

  def __str__(self):
    return f'HTTP/1.1 {self.status}\r\nDate: {datetime.datetime.now()}\r\nLocation: {self.location}Content-Length: {self.content_length}\r\nContent-Type:{self.content_type}\r\n\r\n{self.body}'



