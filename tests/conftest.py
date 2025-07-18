from pytest import fixture
from faker import Faker


@fixture(scope='function')
def faker() -> Faker:
    return Faker()
