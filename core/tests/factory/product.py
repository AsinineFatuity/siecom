import factory
from factory.django import DjangoModelFactory
from core.models import Product, Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: f"Category{n}")
    description = factory.Faker("sentence")
    parent = factory.SubFactory(
        "core.tests.factory.product.CategoryFactory", parent=None
    )


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: f"Product{n}")
    description = factory.Faker("text")
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    stock = factory.Faker("pyint", min_value=0, max_value=100)
    category = factory.SubFactory(CategoryFactory)
