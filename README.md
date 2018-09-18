# Web-Server

An implementation of a web-server in python

### Usage

```python
from webserver.http.server import HTTPServer
from webserver.http import html

server = HTTPServer(host='localhost', port=5000)

@server.route('/')
def index(request):
    return html('index.html')
    
if __name__ == '__main__':
        server.serve()
```

This will listen on `localhost:5000` and serve the `index.html` file at `/`,
on unregistered paths the server will return a `502 Bad Gateway` response
