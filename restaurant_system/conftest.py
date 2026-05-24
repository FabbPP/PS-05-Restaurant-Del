import pytest

from apps.catalog.models import Category, Product
from apps.customers.models import Customer
from apps.dining.models import Table
from apps.inventory.models import StockItem
from apps.orders.models import Order
from apps.delivery.models import Courier
from apps.users.models import User
from apps.core.enums import OrderType


@pytest.fixture
def user_admin(db):
    return User.objects.create_user(username="admin", password="adminpass123", role="ADMIN")


@pytest.fixture
def waiter(db):
    return User.objects.create_user(username="waiter1", password="pass", role="WAITER")


@pytest.fixture
def customer(db):
    return Customer.objects.create(name="Juan Perez", email="juan@example.com", phone="999888777")


@pytest.fixture
def category(db):
    return Category.objects.create(name="Bebidas")


@pytest.fixture
def product(db, category):
    return Product.objects.create(category=category, name="Café", price="5.00")


@pytest.fixture
def stock_item(db, product):
    return StockItem.objects.create(product=product, quantity=10, low_stock_threshold=2)


@pytest.fixture
def product_active(db, category):
    return Product.objects.create(category=category, name="Pizza", price="15.00", is_active=True)


@pytest.fixture
def table(db):
    return Table.objects.create(number=1, capacity=4)


@pytest.fixture
def order_dine_in(db, table):
    return Order.objects.create(order_type=OrderType.DINE_IN, table=table)


@pytest.fixture
def order_delivery(db, customer):
    return Order.objects.create(order_type=OrderType.DELIVERY, customer=customer)


@pytest.fixture
def courier(db):
    user = User.objects.create_user(username="courier1", password="pass", role="COURIER")
    return Courier.objects.create(user=user, is_available=True)


def pytest_collection_modifyitems(config, items):
    for item in items:
        item.add_marker(pytest.mark.django_db)
