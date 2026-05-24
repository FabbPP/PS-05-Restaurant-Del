import factory
from django.contrib.auth import get_user_model
from apps.catalog.models import Category, Product
from apps.dining.models import Table
from apps.orders.models import Order
from apps.core.enums import OrderType, TableStatus

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    role = "WAITER"
    is_active = True

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    name = factory.Faker("word")

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    category = factory.SubFactory(CategoryFactory)
    name = factory.Faker("word")
    price = "15.00"
    is_active = True

class TableFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Table
    number = factory.Sequence(lambda n: n + 1)
    capacity = 4
    status = TableStatus.FREE

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
    order_type = OrderType.DINE_IN
    table = factory.SubFactory(TableFactory)
    waiter = factory.SubFactory(UserFactory)