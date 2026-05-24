from apps.dining.services import update_table_status


def test_update_table_status(table):
    update_table_status(table, "OCCUPIED")
    table.refresh_from_db()
    assert table.status == "OCCUPIED"
