from apps.core.enums import OrderType


def test_order_create_view(client, table):
    response = client.post("/orders/create/", data={"order_type": OrderType.DINE_IN, "table": table.id})
    assert response.status_code == 201
