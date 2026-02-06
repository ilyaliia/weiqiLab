from sqlalchemy.orm import Mapped, mapped_column

from database import Base


# Database model (SQLAlchemy)
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]  # TODO hash

