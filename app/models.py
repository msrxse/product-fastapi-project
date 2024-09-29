import sqlalchemy
from sqlalchemy import (
    DECIMAL,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID

from .db_connection import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(
        Integer, primary_key=True, nullable=False
    )  # nullable is the default but we add it
    name = Column(String(100), nullable=False)
    slug = Column(String(120), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    level = Column(Integer, nullable=False, default="100", server_default="100")
    parent_id = Column(
        Integer, ForeignKey("category.id"), nullable=True
    )  # nullable is the default but we add it

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="category_name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="category_slug_length_check"),
        UniqueConstraint("name", "level", name="uq_category_name_level"),
        UniqueConstraint("slug", name="uq_category_slug"),
    )


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, nullable=False)
    pid = Column(  # we manually specify uniqueness with a constraint, see uq_product_pid, so we dont add unique=True here
        UUID(as_uuid=True),
        nullable=False,
        server_default=text("uuid_generate_v4()"),
    )
    name = Column(String(200), nullable=False)
    slug = Column(String(220), nullable=False)
    description = Column(Text, nullable=True)
    is_digital = Column(Boolean, nullable=False, default=False, server_default="False")
    created_at = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=sqlalchemy.func.now(),
        nullable=False,
    )
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    stock_status = Column(
        Enum(
            "oos", "is", "obo", name="status_enum"
        ),  # out of stock, in stock, on back order
        nullable=False,
        server_default="oos",
    )
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    seasonal_id = Column(Integer, ForeignKey("seasonal_event.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="product_name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="product_slug_length_check"),
        UniqueConstraint("name", name="uq_product_name"),
        UniqueConstraint("slug", name="uq_product_slug"),
        UniqueConstraint("pid", name="uq_product_pid"),
    )


class ProductLine(Base):
    __tablename__ = "product_line"

    id = Column(Integer, primary_key=True, nullable=False)
    price = Column(DECIMAL(5, 2), nullable=False)
    sku = Column(  # we manually specify uniqueness with a constraint, see uq_product_line_sku, so we dont add unique=True here
        UUID(as_uuid=True),
        nullable=False,
        server_default=text("uuid_generate_v4()"),
    )
    stock_qty = Column(Integer, nullable=False, default=0, server_default="0")
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    order = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    created_at = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "price >= 0 AND price <= 999.99", name="product_line_max_value"
        ),
        CheckConstraint(
            '"order" >= 1 AND "order" <= 20', name="product_order_line_range"
        ),  # order in quotes since it is a reserved word
        UniqueConstraint(
            "order", "product_id", name="uq_product_line_order_product_id"
        ),
        UniqueConstraint("sku", name="uq_product_line_sku"),
    )


class ProductImage(Base):
    __tablename__ = "product_image"

    id = Column(Integer, primary_key=True, nullable=False)
    alternative_text = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    order = Column(Integer, nullable=False)
    product_line_id = Column(Integer, ForeignKey("product_line.id"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            '"order" >= 0 AND "order" <= 20', name="product_image_order_range"
        ),
        CheckConstraint(
            "LENGTH(alternative_text) > 0",
            name="product_image_alternative_text_length_check",
        ),
        CheckConstraint("LENGTH(url) > 0", name="product_image_url_length_check"),
        UniqueConstraint(
            "order", "product_line_id", name="uq_product_image_order_product_line_id"
        ),
    )


class SeasonalEvents(Base):
    __tablename__ = "seasonal_event"

    id = Column(Integer, primary_key=True, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    name = Column(String(100), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "LENGTH(name) > 0",
            name="seasonal_event_name_length_check",
        ),
        UniqueConstraint("name", name="uq_seasonal_event_name"),
    )


class Attribute(Base):
    __tablename__ = "attribute"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(100), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "LENGTH(name) > 0",
            name="attribute_name_length_check",
        ),
        UniqueConstraint("name", name="uq_attribute_name"),
    )


class ProductType(Base):
    __tablename__ = "product_type"

    id = Column(
        Integer, primary_key=True, nullable=False
    )  # nullable is the default but we add it
    name = Column(String(100), nullable=False)
    level = Column(Integer, nullable=False)
    parent_id = Column(
        Integer, ForeignKey("product_type.id"), nullable=True
    )  # nullable is the default but we add it

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="product_type_name_length_check"),
        UniqueConstraint("name", "level", name="uq_product_type_name_level"),
    )


class AttributeValue(Base):
    __tablename__ = "attribute_value"

    id = Column(
        Integer, primary_key=True, nullable=False
    )  # nullable is the default but we add it
    attribute_value = Column(String(100), nullable=False)
    attribute_id = Column(
        Integer, ForeignKey("attribute_value.id"), nullable=False
    )  # nullable is the default but we add it

    __table_args__ = (
        CheckConstraint(
            "LENGTH(attribute_value) > 0", name="attribute_value_name_length_check"
        ),
        UniqueConstraint(
            "attribute_value", "attribute_id", name="uq_attribute_value_attribute_id"
        ),
    )


class ProductLineAttributeValue(Base):
    __tablename__ = "product_line_attribute_value"

    id = Column(
        Integer, primary_key=True, nullable=False
    )  # nullable is the default but we add it
    product_line_id = Column(
        Integer, ForeignKey("product_line.id"), nullable=False
    )  # nullable is the default but we add it
    attribute_value_id = Column(
        Integer, ForeignKey("attribute_value.id"), nullable=False
    )  # nullable is the default but we add it

    __table_args__ = (
        UniqueConstraint(
            "attribute_value_id",
            "product_line_id",
            name="uq_product_line_attribute_value",
        ),
    )
