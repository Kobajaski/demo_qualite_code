from faker import Faker

__all__ = ["DATA", "FIELDS"]

fake = Faker()
FIELDS = [
    "first_name",
    "last_name",
    "address",
    "country",
    "phone_number",
    "email",
]

DATA = {
    id_number: {
        "id": id_number,
        **{
            method_name: getattr(fake, method_name, lambda: None)()
            for method_name in FIELDS
        },
    }
    for id_number in range(fake.randomize_nb_elements(50))
}
