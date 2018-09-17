from webserver.http.response import Response


def html(filename: str):
    with open(filename, 'rb') as file:
        data = file.read()
    data.replace(b'\n', b'\r\n')
    headers = {
        'Content-Type': 'text/html',
        'Content-Length': len(data)
    }
    return Response(200, headers=headers, body=data)
