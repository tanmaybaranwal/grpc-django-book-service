# grpc_book_service_backend

gRPC Integration with Django.

This project uses internal automation and build tools. The
concerned files and folders in project are:

- grpc_protos
- grpc_utils
- grpc_rest

The Django Application in this project is basic skeleton without
serializers, urls and build files. It contains `views` and it's implementation
which we will be using in `grpc_services`.


## Setup virtualenv

```sh
pip install virtualenv
virtualenv .venv
```

## Install requirements

```bash
$ pip install -r requirements.txt
$ pip install googleapis-common-protos
# if you ran into any issue with kerbrose package install below system dependencies
$ sudo apt-get install krb5-config libkrb5-dev libssl-dev libsasl2-dev libsasl2-modules-gssapi-mit

```

## Running django management commands & usage

```sh
$ source .venv/bin/activate
$ export DJANGO_SETTINGS_MODULE=grpc_book_service_backend.settings.local
$ python manage.py build -a grpc_book_service
$ python manage.py build -p # generate protobuf
$ python manage.py makemigrations
$ python manage.py migrate
```

## Running gRPC Server:

```sh
$ python manage.py generate_grpc_stubs grpc_book_service/grpc_protos app.proto

# If importing google.api.annotations:
$ python -m grpc_tools.protoc -I grpc_book_service/grpc_protos --python_out=./grpc_book_service/grpc_protos --grpc_python_out=./grpc_book_service/grpc_protos -I$GOPATH/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis grpc_book_service/grpc_protos/app.proto

# Start gRPC Server
$ python manage.py run_grpc_server grpc_book_service

```

## Running REST Server with gRPC:

```sh

# GoLang Gateway out: <https://github.com/grpc-ecosystem/grpc-gateway>
# This is a way which I couldn't figure out.
$ protoc -I/usr/local/include -I. -I./grpc_book_service/grpc_protos -I$GOPATH/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis --grpc-gateway_out=logtostderr=true:. ./grpc_book_service/grpc_protos/app.proto

# Another way using <https://github.com/RussellLuo/grpc-pytools/>

# Generate AST File
$ python -m grpc_tools.protoc -I. --pytools-ast_out=grpc_book_service/grpc_rest/app_ast.json grpc_book_service/grpc_protos/app.proto

# Generate Pythonic Services based on Flask
$ python -m grpc_pytools.pythonic --proto-ast-file=grpc_book_service/grpc_protos/app_ast.json --pb2-module-name=grpc_book_service/grpc_protos/app_pb2 > grpc_book_service/grpc_rest/services.py

# Generate Marshmallow Schemas
$ python -m grpc_pytools.marshmallow --proto-ast-file=grpc_book_service/grpc_protos/app_ast.json --pb2-module-name=grpc_book_service/grpc_protos/app_pb2 > grpc_book_service/grpc_rest/schemas.py

# Generate RESTart APIs
$ python -m grpc_pytools.restart --proto-ast-file=grpc_book_service/grpc_protos/app_ast.json --pb2-module-name=grpc_book_service/grpc_protos/app_pb2 --grpc-server=localhost:50051 > grpc_book_service/grpc_rest/apis.py
# Modify the api path in <grpc_book_service/grpc_rest/apis.py> as per OpenAPI Spec

# Run the HTTP/1.1 server
$ restart grpc_book_service.grpc_rest.apis:api -p 60066

# Try cURL
$ curl -i -H 'Content-Type: application/json' -X POST http://localhost:60066/grpc_book_service/get_book_post -d '{"isbn": 1}'
```

## Connecting to GRPC Using ServiceClient

```python
from grpc_book_service.grpc_protos import app_pb2, app_pb2_grpc
from grpc_book_service.grpc_utils.service_client import ServiceClient
books_service_client = ServiceClient(app_pb2_grpc, 'GRPCBookServiceStub', 'localhost', 50051)
response = books_service_client.GetBookPost(app_pb2.GetBookRequest(isbn=1))

# <response:>
# isbn: 1
# name: "NW-Novel"
# author: "Hiroko Murakami"
# title: "Norwegian Wood"
# codes: 1.0
# codes: 2.5
# codes: 5.5
```

The project also has helper modules from following repos, packages and blogs:

- https://pypi.org/project/grpc-django/
- http://flagzeta.org/blog/using-grpc-with-django/