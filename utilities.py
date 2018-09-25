def get_view(path):
  with open(f'./views/{path}.html', 'r') as myfile:
        data = myfile.read()
  return data
