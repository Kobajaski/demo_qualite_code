from faker import Faker
from pydantic import BaseModel

__all__ = ["DATA", "FIELDS", "BaseItem", "Item"]
fake = Faker()


class BaseItem(BaseModel):
    first_name: str
    last_name: str
    address: str
    country: str
    phone_number: str
    email: str


class Item(BaseItem):
    id: int


FIELDS = [
    "first_name",
    "last_name",
    "address",
    "country",
    "phone_number",
    "email",
]

DATA = {
    id_number: Item(id=id_number, **{method_name: getattr(fake, method_name, lambda: None)() for method_name in FIELDS})
    for id_number in range(fake.randomize_nb_elements(50))
}
