import factory
from factory.fuzzy import FuzzyChoice
from service.models import Product, Category

class ProductFactory(factory.Factory):
    """Creates fake products for testing"""
    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(choices=["Hat", "Apple", "Hammer", "iPhone", "Dog Food"])
    description = factory.Faker("text")
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    available = factory.Faker("boolean")
    category = FuzzyChoice(choices=[
        Category.CLOTHS, 
        Category.FOOD, 
        Category.HOUSEWARES, 
        Category.AUTOMOTIVE, 
        Category.TOOLS
    ])
