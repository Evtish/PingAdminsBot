from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship
)


# базовая модель
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


# модель сообщения
class Message(Base):
    thread: Mapped["Thread"] = relationship(back_populates='messages')
    text: Mapped[str]
    authod_is_admin: Mapped[bool]


# модель диалога
class Thread(Base):
    messages: Mapped[list["Message"]] = relationship(back_populates='thread')
    user_id: Mapped[int]
    admin_id: Mapped[int]
    active: Mapped[bool]
