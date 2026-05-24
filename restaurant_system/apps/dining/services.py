from __future__ import annotations

from apps.dining.models import Table


def update_table_status(table: Table, status: str) -> Table:
    table.status = status
    table.save()
    return table
