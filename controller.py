from router import Router
from jinja2 import Template
from utilities import get_view
from response import Response
import csv
import datetime

@Router.route(r'\/hello')
def index():
  view = Template(get_view('index'))
  body_response = view.render()

  response = Response()
  response.status = 200
  response.body = body_response

  return response


@Router.route(r'\/time')
def time():
  view = Template(get_view('time'))
  body_response = view.render(date=datetime.datetime.now())

  response = Response()
  response.status = 200
  response.body = body_response

  return response
