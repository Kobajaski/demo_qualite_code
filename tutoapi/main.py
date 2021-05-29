from typing import Optional
from functools import wraps

from fastapi import FastAPI
from .data import DATA, FIELDS


app = FastAPI()

def verify_filter(default={}):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, filters, **kwargs):
            return (
                function(*args, filters=filters, **kwargs)
                if not filters or all(f in FIELDS for f in filters.split(','))
                else default
            )
        return wrapper
    return decorator


def filtering(dict_data, filters):
    return {
        key: value for key, value in dict_data.items()
        if not filters or key in filters
    }


@app.get("/list")
@verify_filter(default=[])
def read_root(filters: Optional[str] = ""):
    return list(map(lambda x: filtering(x, filters), DATA.values()))


@app.get("/items/{item_id}")
@verify_filter()
def read_item(item_id: int, filters: Optional[str] = ""):
    return filtering(DATA.get(item_id, {}), filters)