"""Shared SQLAlchemy declarative base.

All models import Base from here so that Alembic autogenerate (and
metadata-driven test setup) sees a unified MetaData object across
packages/models/*.
"""
from sqlalchemy.orm import declarative_base

Base = declarative_base()
