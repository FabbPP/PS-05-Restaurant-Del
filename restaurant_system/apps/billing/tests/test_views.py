def test_invoice_create_view(client, order_dine_in):
    order_dine_in.total = 10
    order_dine_in.save()
    response = client.post(
        "/billing/create/",
        data={
            "order": order_dine_in.id,
            "document_type": "RECEIPT",
            "document_number": "B001-3",
            "total_amount": 10,
            "payment_method": "CASH",
            "is_paid": False,
        },
    )
    assert response.status_code == 201
