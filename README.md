# API

### Installation

```sh
$ virtualenv auth
$ cd auth
$ source bin/active
$ git clone https://github.com/LSDkk5/auth
$ pip install -r src/REQUIREMENTS.txt
```

### Db config
#### database.json

```json
{
    "host": "yourhost",
    "port": 5432,
    "database": "database",
    "user": "user",
    "password": "password"
}
```

### Init database

```sh
$ python initdb.py
```

### Run development server

```sh
$ python src/run.py
```

```python
 * Serving Flask app "api" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
