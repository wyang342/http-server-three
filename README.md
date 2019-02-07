# HTTP Server Three
So far our site is pretty boring. It returns 'Hello World' when you make a GET request to `/` and when you make a GET request to `/time`, it returns the time. We basically built an unnecessary digital watch. But we learned so much! Still, in order to explore HTTP servers in more depth, we'll need to add some new functionality that is slightly more robust. 

In this challenge, we are going to create some more functionality on our site to teach us about HTTP servers and give us a precursor to Django! Specifically, we're going to create 4 routes:
- `/facts` (GET) -> this will return all the facts on our `facts.csv` file in bullet form with URLs to lead us to...
- `/facts/:id` -> this will find the fact with the ID number in the CSV file and put it out to the screen
- `/facts/new` -> this will take us to a form to create a new fact in the database
- `/facts` (POST) -> this will save the contents of the form into the database

## Release 0 - All Facts
Our routes are following [RESTful Routing](https://medium.com/@atingenkay/restful-routes-what-are-they-8fe221521bb) patterns. Right now we are focusing on creating a `/facts` page that will give me a list of all the facts with a URL link to each individual fact. 

The data we've got in the CSV file needs to be read into a `Fact` class and displayed out to the page. Let's start with creating an HTML template for all these facts:

```html
# templates/all_facts.html
<!DOCTYPE html>
<html>

<head>
	<meta charset="utf-8" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>All Facts</title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body>
  <h1> All Facts </h1>
  <ul>
  {% for fact in facts %} 
    <li> <a href="/facts/{{fact.id}}"> Fact #{{fact.id}} </a> </li>
  {% endfor %}
  </ul>
</body>

</html>
```
The `{% %}` is when you want to run Python code but not interpolate it. `{{ }}` is for interpolating Python code. Next, let's register the URL in our controller:

```python
# controller.py
@Router.route('/facts')
def facts(_request):
    response = Response('all_facts', {'facts': Fact.all_facts()})
    return response
```

And let's update `router.py`:

```python
import re
class Router:
  routes = []

  @classmethod
  def route(self, path, method='get'):
    def add_to_routes(function):
      route = {'path': path, 'function': function, 'method': method}
      self.routes.append(route)
    return add_to_routes

  @classmethod
  def process(self, request):
    parsed_request = request.parsed_request
    for route in self.routes:
      if re.search(route['path'], parsed_request['uri'])  and route['method'].lower() == parsed_request['method'].lower():
        return route['function'](parsed_request)
    return 'HTTP/1.1 404 Not Found \r\n'
```


Finally, create a `Fact` class on your own. Here are the specs:
- It must take in an ID and fact as instance variables
- It that has a class method called `all_facts` which returns an array of `Fact` objects.
- You've done this before in School Interface. You can figure this out!

By the end of this, you should be able to go to `/facts` and see a list of facts with URLs to individual facts. We'll build this next.

## Release 1: GET-ing individual facts
We are going to add a new route that will allow the client to request a fact from a list of random facts we will have stored in a CSV file. The user can request a fact based on a number passed in the url. For example, `/facts/22` will respond with the 22nd fact in our CSV file. 

First, we'll add a route to our `controller.py` file. In that route, we write some code that reads the number from the URL, looks up the correct fact in the CSV file, then creates a response containing that fact. We'll also want to create a new `Jinja2` template to display the fact.

Let's start with the logic in the controller:

```Python
#controller.py
...
@Router.route(r'\/facts\/(\d+)')
def fact(request):
    fact_id = re.match(r'\/facts\/(\d+)', request['uri']).group(1)
    csv_file = csv.reader(open('facts.csv', "r"))
    for row in csv_file:
        if row[0] == fact_id:
            fact = row 
    response = Response('fact', {'fact': fact})
    return response
```

We've added a bunch of regex into our code. The thing we need to pay attention to most is finding `fact_id`: we want to grab the fact id from the URL and match it with a record in the database. We create a `Response` object from there and then feed it into a `fact` template with a dictionary of variables to be interpolated.

Create a new `templates/fact.html` to display our fact. By the end of this, you should be able to go to and see the following:
- http://localhost:8888/ -> Hello!
- http://localhost:8888/time -> The current time is INSERT_CURRENT_TIME
- http://localhost:8888/facts -> A list of all the facts with links to those individual facts
- http://localhost:8888/facts/:id -> The fact with the id you pass in the URL


## Release 2 - POSTing New Facts

The last 'feature' we are going to add is the ability to `POST` a new fact. Here's the workflow:
- The user will send a `GET` request to our server for an HTML form
- Our server will send back the form
- The user receives the form and fills it out with a random fact
- Our server will write the new fact to our CSV file

Before we do any of that, we'll have to add the ability to deal with params to our `Request` class. 

#### Query Params
Params can be sent in two ways: via a GET request and via a POST request. Query params are sent as part of the url `/users/search?name=thor&city=chicago` in GET requests. The question mark indicates the start of the params string. From there, key/value pairs are matched with `=`. Each individual key value pair is separated by `&`.

More often, params are sent via POST requests. We're going to create a route containing a form and collect the params upon submission.

First, let's create a simple HTML form in our `templates` directory. If you're not familiar with how HTML forms work, take a look at [this resource](https://www.w3schools.com/html/html_forms.asp).

```HTML
<!-- templates/form.html -->
<!DOCTYPE html>
<html>
  <body>
    <h2>New Fact</h2>
    <form action="/facts" method="POST">
      Create a new fact:<br>
      <input type="text" name="fact">
      <br>
      <input type="submit" value="Submit">
    </form> 
  </body>
</html>
```
We set our form up with an input for a new fact and a submit button. We set the action attribute to `/facts` and the http method to `POST`. Notice that we set the `name` attribute on our input to `fact`. This is what the key will get set to when the new fact gets passed in the request body. 

We'll need to add a new route to our `controller.py` for delivering the form to the user.

```python 
@Router.route(r'\/facts\/new')
def new_fact(_request):
  response = Response('form')
```

Ensure you are about to view the form before moving forward.

Next, we want to fill out the form and have our data POST to `controller.py`. The `controller.py` will hit a route specific to `/facts` POST (not GET) and parse the data you get in. We'll get you started and it's your job to save it into the CSV file. Make sure you keep track of the last ID number and increment it each time. By the end of this, you should be able to create new records into your CSV file.

```python
# controller.py
@Router.route(r'\/facts', 'POST')
def add_fact(request):
	all_facts = csv.reader(open('facts.csv', 'r'))
  # your code here
	return f'HTTP/1.1 303 See Other\r\nLocation: http://localhost:8888/facts/{new_fact_number}'
```

## Conclusion 
We've really only scratched the surface - if you found this HTTP project tedious, that's okay! We are just learning how to combine all of our skills into this small project. Django, React, and most frameworks take care of all of this for you!
