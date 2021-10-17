# IBANs

simple IBAN validation API. provides both GET and POST based endpoints

## Limitations

Only the basic IBAN check numbers are validated. but it's possible to add country-based validation

# Installation

`poetry` is required for dependency installation and to run this project

```
% pip install --user poetry
% poetry install
```

# Testing

`poetry` installs everything necessery to run tests with coverage.

```
% poetry run pytest --cov --cov-report=html
```

or use `Makefile`'s target:
```
% make test
```

To inspect code coverage, open `index.html` file located in `htmlcov` folder

# Running

The same `poetry` could be used to launch the server locally
```
% poetry run python ibans

[2021-10-17 12:46:36 +0300] [4264] [INFO] Running on http://127.0.0.1:8000 (CTRL + C to quit)
```

or use `Makefile`'s target:
```
% make run
```

# API Documentation

API documentation available at runtime [http://localhost:8000/docs](http://localhost:8000/docs)

# Deployment

If required, this service may be deployed to any cloud service provider that supports running OCI containers.
For example building and running locally, using `Docker`

```
% docker build -t ibans .
% docker run --rm -it -p 8000:8000 ibans
```

or use `Makefile`'s target:
```
% make docker
```

Ideally, this service should be placed behind a proxy server, configured to cache responses
with respect to query parameters

# Examples

## GET interface
```
% curl "localhost:8000/v1/iban/is_valid?number=EE382200221020145685"

{"is_valid": true}
```

```
% curl "localhost:8000/v1/iban/is_valid?number=EE38%202200%202210%202014%20XXXX"

{"is_valid": false}
```

## POST interface

```
% curl "localhost:8000/v1/iban/validate" -X POST -H 'Content-Type: application/json' -d '{"number": "EE38 2200 2210 2014 5685"}' -i

HTTP/1.1 204
...
```

```
% curl "localhost:8000/v1/iban/validate" -X POST -H 'Content-Type: application/json' -d '{"number": "EE38 2200 2210 2014 XXXX"}' -i

HTTP/1.1 400
...
{"detail":"IBAN check digits mismatch"}
```