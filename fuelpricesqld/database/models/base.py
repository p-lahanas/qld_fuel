import uuid

import sqlalchemy as sql
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class UuidPkMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        sql.Uuid(as_uuid=True, native_uuid=True),
        primary_key=True,
        default_factory=uuid.uuid4,
        server_default=sql.func.newid(),
        init=False,
    )
