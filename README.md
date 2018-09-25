# HTTP Server Three

## Release 0 - Facts By Number 
So far our site is pretty boring. You make a get request to `/time` and it returns the time. We basically built a completely unnecessary digital watch. But we learned so much! Still, in order to explore HTTP servers in more depth, we'll need to add some new functionality that is slightly more robust (slightly). 

In this release we are going to add a new route that will allow the client to request a fact from a list of random facts we will have stored server-side in a csv file. The user can request a fact based on a number passed in the url. For example, `/facts/22` will respond with the 22nd fact in our csv file. 

First, we'll add a route to our `controller.py` file. In that route, we write some code that reads the number from the url, looks up the correct fact in the csv file, then creates a response containing that fact. We'll also want to create a new `Jinja2` template to display the fact. 

Let's start with the logic in the controller. 

```Python
#controller.py

@Router.route(r'\/facts\/(\d+)')
def fact(request):
  fact_id = re.match(r'\/facts\/(\d+)', request.path).group(1)

  csv_file = csv.reader(open('facts.csv', "r"), delimiter=",")

  for row in csv_file:
    if row[0] == fact_id:
      fact = row 

  view = Template(get_view('fact'))
  body_response = view.render(fact=fact)

  response = Response()
  response.status = 200
  response.body = body_response

  return response

```
A couple of things to note about this new route. First, we use regex to allow any number to be passed with `/facts`. In our block we use the same pattern to get the number out of the path. Next, we loop through our list of facts to find the one that was requested. From there, we create a response just like we did with our `/time` route. 

All we need to do now is add a new file, `fact.html`,  to our views directory. 


```HTML
<!-- views/fact.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Page Title</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" media="screen" href="main.css" />
    <script src="main.js"></script>
</head>
<body>
    <h1>{{ fact[0] }}. {{ fact[1] }} </h1>
</body>
</html>

```

## Release 1 - params

The last 'feature' we are going to add is the ability to `POST` a new fact. The user will send a `GET` request to our server for an html form. Our server will send back the form. After the user receives the form, they'll fill it out with a random fact and send it back to our server where we'll write the new fact to our `csv` file. 

Before we do any of that, we'll have to add the ability to deal with params to our Request class. 

#### Query Params
Params can be sent in two ways. Query params are sent as part of the url `/users/search?name=thor&city=chicago`. The question mark indicates the start of the params string. From there, key value pairs are matched with `=`. Each individual key value pair is separated by `&`. So we would want to parse the above example out to look something like this:

```Python 
# original string `/users/search?name=thor&city=chicago`

request.params = { 'name': 'thor', 'city': 'chicago' }
```

Grabbing our query params is pretty simple. Let's add some code to our `request.py`. 

Start by adding this line to `__init__` : `self.params  = self.get_params()` Next, you can add the following code inside the `Request` class. 

```Python
# request.py 

def get_params(self):
    if '?' in self.path:
        params = self.parse_params(self.path.split('?')[1])
    return params 

def parse_params(self, params):
    parsed_params = {}
    
    for param in params.split('&'):
      key_and_value = param.split('=')
      
      key = key_and_value[0]
      value = key_and_value[1]
      
      if '+' in value:
        value = value.replace('+',' ')
      
      parsed_params[key] = value 
    
    return parsed_params      

```
First, we have a method that checks to see if any params came in attached to the path. There will always be a `?` so we can check for that and split to get the query string. After that we pass the string to a separate method to be parsed and turned into a dictionary. `parse_params` works similar to our `headers` function, looping through the string, splitting on `=` and making some substitutions where necessary. (params with multiple words are separated by `+` so we have to account for that)

This will cover us when params are passed in the URL with a `GET` request. More commonly, though, params are passed with a `POST` request. In this case they'll appear in the response body instead of the path. 


#### Params In Request Body
 
To get params out of the request body we'll add a new method to our `Request` class. 

```Python
def get_body(self):
    if self.request[-1] != '\r\n':
        return self.request[-1]
    return None 
```
Here we are just checking if anything comes after the carriage return that signals the end of our headers. If so, we return it. If not, we'll return `None`.
Then we can call this method in our `__init__`

The last thing we need to do is set up our Request class to handle the body params. All we should have to do is add a condition to our params method. 

```Python
self.body = self.get_body()
```

Then we can add a condition to our `get_params` function. 
```Python
def get_params(self):
    params = ''
    if '?' in self.path:
      params = self.parse_params(self.path.split('?')[1])
    elif self.body:
      params = self.parse_params(self.body)
    return params 
```
Our new condition checks to see if the body was set to anything. If so, it passes the contents to the `parse_params` function. 

## Release 2 - POSTing New Facts

Now we are finally ready to set up the ability to create new facts. First, let's create a simple HTML form in our `views` directory. 

```HTML
<!-- views/form.html -->
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

```
fact=the+sun+is+enormous
```

If you're not familiar with how HTML forms work, take a look at [this resource](https://www.w3schools.com/html/html_forms.asp).

We'll need to add two new routes to our `controller.py` now. The first will be responsible for delivering the form to the user, and the second will receive the data entered in the form and write it to the `CSV`. 

```Python 
@Router.route(r'\/facts\/new')
def new_fact(request):
  view = Template(get_view('form'))
  body_response = view.render()
  
  response = Response()
  response.status = 200
  response.body = body_response

  return response


@Router.route(r'\/facts', method="post")
def add_fact(request):
  facts = csv.reader(open('facts.csv', "r"), delimiter=",")
  count = sum(1 for row in facts)
  new_fact_number = count + 1
  new_fact = [f'{new_fact_number}', request.params['fact']]
  with open('facts.csv', 'a') as f:
      writer = csv.writer(f)
      writer.writerow(new_fact)

  return f'HTTP/1.1 303 See Other\r\nLocation: http://localhost:8888/facts/{new_fact_number}'
```
The first route is to `/facts/new` and doesn't contain anything we haven't seen already. It simply grabs the HTML form from our views folder and returns it. 

The `POST` route is doing a little more. When the client hits submit on the form, this is the route that will run. Remember, each fact in our file is preceded by a number. When we save the new fact, we need to assign it the next number. (If there are 99 facts, our new fact will be fact 100). We get `number_for_new_fact` by reading the length of the file and adding `1` to it. Then we get the new fact by calling `params['fact']` on our `request` object.

Once we have the fact and the number we write it to the `csv` file. At this point we're done with our logic, but we still need to send back a response. We want our users to be able to get back an HTML page displaying the new fact they created. We've already written the logic to display a fact by its number, so we can send back a redirect that will force the browser to make a new `GET` request to the url that leads to the new fact. 

For now we'll hard code that as a string. When the browser receives a redirect and `Location` header, it knows to make a new get request to the url in the `Location` header. 

Try making a request to `/facts/new`. Fill out the form with a new fact and submit it. You should get redirected to page displaying the fact you just created. 

## Conclusion 

We've really only scratched the surface here. If you want to expand your learning you can look into how to respond with different formats of data (JSON?) depending on the `accepts` header. 

How do servers work with cookies? You can try adding more routes.

The HTML we are sending back isn't styled. How would you serve up a `CSS` style sheet with your HTML? 


