from apps.kitchen.forms import KitchenTicketForm


def test_kitchen_ticket_form_missing_order():
    form = KitchenTicketForm(data={"status": "QUEUED"})
    assert not form.is_valid()
    assert "order" in form.errors
