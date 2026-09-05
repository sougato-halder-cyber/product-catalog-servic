"""Factory for creating fake Product objects for tests."""
import factory
from faker import Faker
from service.models import Product

fake = Faker()


class ProductFactory(factory.Factory):
    """Creates fake products for testing"""

    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("word")
    category = factory.Faker("random_element", elements=[
        "electronics", "clothing", "grocery", "furniture", "toys"
    ])
    availability = factory.Faker("boolean")
    price = factory.Faker("pyfloat", left_digits=3, right_digits=2, positive=True)
