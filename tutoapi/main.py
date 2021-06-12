from functools import wraps
from typing import Any, Callable, Dict, List, Optional

from fastapi import FastAPI

from .data import DATA, FIELDS, BaseItem, Item

app = FastAPI()


def verify_filter(default: Any = {}):
    """
    Decorator to verify if filters are appliable, else return a default value
    instead of call given function.

    :param default: default value to return
    :type default: object
    :rtype: object
    """

    def decorator(function: Callable):
        @wraps(function)
        def wrapper(*args, filters: Optional[str], **kwargs):
            return (
                function(*args, filters=filters, **kwargs)
                if not filters or all(f in FIELDS for f in filters.split(","))
                else default
            )

        return wrapper

    return decorator


def filtering(dict_data: Dict, filters: Optional[str]):
    """
    Filter the input dictionnary with the given filters key values

    :param dict_data: dictionnary to filter
    :param filters: filters values
    :type dict_data: dict
    :type filters: list
    :rtype: dict
    """

    return {key: value for key, value in dict_data.items() if not filters or key in filters or key == "id"}


@app.post("/items/append")
def write_item(item: BaseItem):
    new_id = len(DATA)
    DATA[new_id] = Item(
        id=new_id,
        **item.dict(),
    )
    return {"state": "success", "count": 1}


@app.post("/list/append")
def write_list(items: List[BaseItem]):
    new_id = len(DATA)
    DATA.update(
        {
            (new_id + counter): Item(
                id=new_id + counter,
                **item.dict(),
            )
            for counter, item in enumerate(items)
        }
    )
    return {"state": "success", "count": len(items)}


@app.get("/list")
@verify_filter(default=[])
def read_list(filters: Optional[str] = ""):
    """
    List all items

    :param filters: filtering return key for each object
    :type filters: str
    :rtype: list
    """

    return list(map(lambda x: filtering(x, filters), map(Item.dict, DATA.values())))


@app.get("/items/{item_id}")
@verify_filter()
def read_item(item_id: int, filters: Optional[str] = ""):
    """
    Get a specific item

    :param item_id: identifier of the item ('id' key)
    :param filters: filtering return key
    :type item_id: int
    :type filters: list
    :rtype: dict
    """

    return filtering(DATA[item_id].dict() if item_id in DATA else {}, filters)
