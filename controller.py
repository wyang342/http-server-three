from classes.router import Router
from classes.response import Response
from classes.fact import Fact
import datetime
import re
import csv
import cgi, cgitb

@Router.route('/')
def index(_request):
    response = Response('index')
    return response

@Router.route('/time')
def time(_request):
    response = Response('time', {'time': datetime.datetime.now()})
    return response

@Router.route('/facts')
def facts(_request):
    response = Response('all_facts', {'facts': Fact.all_facts()})
    return response

@Router.route(r'\/facts\/(\d+)')
def fact(request):
    fact_id = re.match(r'\/facts\/(\d+)', request['uri']).group(1)
    csv_file = csv.reader(open('facts.csv', "r"))
    for row in csv_file:
        if row[0] == fact_id:
            fact = row
    response = Response('fact', {'fact': fact})
    return response

@Router.route(r'\/facts\/new')
def new_fact(_request):
  response = Response('form')
  return response

@Router.route(r'\/facts', 'POST')
def add_fact(request):
  last_row_id = 0
  all_facts = csv.reader(open('facts.csv', 'r'))
  for row in all_facts:
    if row[0] == 'id':
      continue
    if int(row[0]) > last_row_id:
      last_row_id = int(row[0])
  new_fact_number = last_row_id + 1
  if '+' in request['fact']:
    new_fact = request['fact'].replace('+', ' ')
  else:
    new_fact = request['fact']
  new_row = [new_fact_number, new_fact]
  with open('facts.csv', 'a') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(new_row)

  return f'HTTP/1.1 303 See Other\r\nLocation: http://localhost:8888/facts/{new_fact_number}'
