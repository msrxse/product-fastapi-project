from sqlalchemy import Boolean, CheckConstraint, Column, Integer, String

from .db_connection import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(
        Integer, primary_key=True, nullable=False
    )  # nullable is the default but we add it
    name = Column(String(100), nullable=False)
    slug = Column(String(120), nullable=False)
    is_active = Column(Boolean, nullable=False)
    level = Column(Integer, nullable=False)
    parent_id = Column(Integer, nullable=True)  # nullable is the default but we add it

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="slug_length_check"),
    )
