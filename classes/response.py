from jinja2 import Template

class Response:
    def __init__(self, filename, template_variables={}):
        self.build_html_response(filename, template_variables)
    
    def __str__(self):
        return self.html_response
    
    def build_html_response(self, filename, template_variables):
        jina_template = y = self.get_template(filename)
        html_body = jina_template.render(template_variables)
        self.html_response = f"HTTP/1.1 200 OK\r\nContent-Type:text/html\r\nContent-Length:{len(html_body)}\r\n\r\n{html_body}"
    
    def get_template(self, filename):
        with open(f'./templates/{filename}.html', 'r') as myfile:
            return Template(myfile.read())
