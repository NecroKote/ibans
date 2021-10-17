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

# Running

The same `poetry` could be used to launch the server locally
```
% poetry run python ibans

[2021-10-17 12:46:36 +0300] [4264] [INFO] Running on http://127.0.0.1:8000 (CTRL + C to quit)
```

# API Documentation

API documentation available at runtime [http://localhost:8000/docs](http://localhost:8000/docs)