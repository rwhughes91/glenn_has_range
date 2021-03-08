from typing import List


def get_col_name_from_enum(enums: List[str]) -> List[str]:
    """
    Takes sort enum produced by graphene-sqlalchemy' relay interface
    and converts to model column names
    """

    cols = []
    for enum in enums:
        col = "_".join(enum.split("_")[0:-1]).lower()
        cols.append(col)

    return cols
