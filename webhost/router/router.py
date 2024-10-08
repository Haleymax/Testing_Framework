from pymongo import hello

from webhost.api.app import hello_world
from webhost.app import app

app.add_url_rule('/hello', 'hello', hello_world)
