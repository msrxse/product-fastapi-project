from sqlalchemy import Integer

"""
## Table and Column Validation
"""

"""
- [ ] Confirm the presence of all required tables within the database schema.
"""


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("product_product_type")


"""
- [ ] Validate the existence of expected columns in each table, ensuring correct data types.
"""


def test_model_structure_column_data_types(db_inspector):
    table = "product_product_type"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}
    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["product_id"]["type"], Integer)
    assert isinstance(columns["product_type_id"]["type"], Integer)


"""
- [ ] Ensure that column foreign keys correctly defined.
"""


def test_model_structure_column_foreign_key(db_inspector):
    table = "product_product_type"
    foreign_keys = db_inspector.get_foreign_keys(table)

    product_product_type_foreign_key = next(
        (
            fk
            for fk in foreign_keys
            if set(fk["constrained_columns"]) == {"product_id"}
            or set(fk["constrained_columns"]) == {"product_type_id"}
        ),
        None,
    )
    assert product_product_type_foreign_key is not None


"""
- [ ] Verify nullable or not nullable fields
"""


def test_model_structure_nullable_constrains(db_inspector):
    table = "product_product_type"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "product_id": False,
        "product_type_id": False,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(
            column_name
        ), f"column '{column_name}' is not nullable as expected"


"""
- [ ] Test columns with specific constraints to ensure they are accurately defined.
"""


"""
- [ ] Verify the correctness of default values for relevant columns.
"""


"""
- [ ] Ensure that column lengths align with defined requirements.
"""


"""
- [ ]  Validate the enforcement of unique constraints for columns requiring unique values.
"""


def test_model_structure_unique_constraints(db_inspector):
    table = "product_product_type"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(
        constraint["name"] == "uq_product_id_product_type_id"
        for constraint in constraints
    )
