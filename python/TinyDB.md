# TinyDB Reference

from tinydb import TinyDB, Query

db = TinyDB('path/to/db.json')
User = Query()

db.insert({'name': 'John', 'age': 22})
db.search(User.name == 'John')

# [{'name': 'John', 'age': 22}]

Example Code
from tinydb import TinyDB, Query
db = TinyDB('/path/to/db.json')
db.insert({'int': 1, 'char': 'a'})
db.insert({'int': 1, 'char': 'b'})
Query Language
User = Query()
# Search for a field value
db.search(User.name == 'John')
[{'name': 'John', 'age': 22}, {'name': 'John', 'age': 37}]

# Combine two queries with logical and
db.search((User.name == 'John') & (User.age <= 30))
[{'name': 'John', 'age': 22}]

# Combine two queries with logical or
db.search((User.name == 'John') | (User.name == 'Bob'))
[{'name': 'John', 'age': 22}, {'name': 'John', 'age': 37}, {'name': 'Bob', 'age': 42}]

# Negate a query with logical not
db.search(~(User.name == 'John'))
[{'name': 'Megan', 'age': 27}, {'name': 'Bob', 'age': 42}]

# Apply transformation to field with `map`
db.search((User.age.map(lambda x: x + x) == 44))
[{'name': 'John', 'age': 22}]

# More possible comparisons:  !=  <  >  <=  >=
# More possible checks: where(...).matches(regex), where(...).test(your_test_func)
Tables
table = db.table('name')
table.insert({'value': True})
table.all()
[{'value': True}]
Using Middlewares
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
db = TinyDB('/path/to/db.json', storage=CachingMiddleware(JSONStorage))