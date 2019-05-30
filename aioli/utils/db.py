# -*- coding: utf-8 -*-

from sqlalchemy import asc, desc


def qs_to_sa(value):
    if not value:
        return

    for col_name in value.split(","):
        sort_asc = True
        if col_name.startswith("-"):
            col_name = col_name[1:]
            sort_asc = False

        if self._model_has_attrs(col_name):
            yield asc(col_name) if sort_asc else desc(col_name)
