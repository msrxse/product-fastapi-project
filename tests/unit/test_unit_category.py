import pytest
from pydantic import ValidationError

from app.schemas.category_schemas import CategoryCreate


def test_unit_schema_category_validation():
    valid_data = {"name": "test category", "slug": "test-slug"}
    category = CategoryCreate(**valid_data)

    assert category.name == "test category"
    assert category.is_active is False
    assert category.level == 100
    assert category.parent_id is None

    # when doesn't include slug should error
    invalid_data = {
        "name": "test_category",
    }
    with pytest.raises(ValidationError):
        CategoryCreate(**invalid_data)
