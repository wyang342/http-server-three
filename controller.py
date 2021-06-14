from classes.router import Router
from classes.response import Response
import datetime
import re
import csv
from classes.fact import Fact


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
            fact = Fact(row[0], row[1])
    response = Response('fact', {'fact': fact})
    return response


@Router.route(r'\/facts\/new')
def new_fact(_request):
    response = Response('form')
    return response


@Router.route(r'\/facts', 'POST')
def add_fact(request):
    new_fact_number = len(Fact.all_facts()) + 1

    with open('facts.csv', 'a') as csvfile:
        fieldnames = ['id', 'fact']
        writer = csv.DictWriter(csvfile, fieldnames=['id', 'fact'])
        writer.writerow({'id': new_fact_number, 'fact': str(request['fact'])})

    return f'HTTP/1.1 303 See Other\r\nLocation: http://localhost:8888/facts/{new_fact_number}'
