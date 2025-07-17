from faker import Faker
from pytest import fixture


@fixture(scope="session")
def faker() -> Faker:
    return Faker()
