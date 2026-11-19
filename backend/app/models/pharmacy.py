from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
    func
)

from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Pharmacy(Base):

    __tablename__ = "pharmacies"

    # Composite unique constraint
    __table_args__ = (
        UniqueConstraint(
            "licensing_authority",
            "registration_number",
            name="uq_pharmacy_registration"
        ),
    )

    # Primary key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    #One interview question: Why do we use Mapped[int] instead of simply writing id = mapped_column(Integer, primary_key=True)?
#We use `Mapped[int]` instead of simply writing `id = mapped_column(Integer, primary_key=True)` to provide type hinting and improve code readability. The `Mapped` type indicates that the attribute is a mapped column in the SQLAlchemy ORM model, and it specifies the expected data type (in this case, `int`). This helps developers understand the intended type of the attribute and can also assist with static type checking tools, making the code easier to maintain and less prone to errors.
#

    # Pharmacy information
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    licensing_authority: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    registration_number: Mapped[str] = mapped_column(
        String(80),
        nullable=False
    )

    contact_email: Mapped[str | None] = mapped_column(
        String(254),
        nullable=True
    )

    contact_phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    # Account status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true"
    )

    # Registration timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )