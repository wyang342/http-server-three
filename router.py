
class Router:
 
  routes = []

  @classmethod 
  def route(self, route, method='get'):
    def add_to_routes(f):
      r = {'path': route, 'process': f, 'method': method}
      self.routes.append(r)
      
    return add_to_routes

  @classmethod
  def process(self, request):
    for route in self.routes:
      if route['path'] == request.path and route['method'].lower() == request.method.lower():
        return route['process']()


