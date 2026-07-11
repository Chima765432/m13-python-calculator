from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from app.database import Base
from app.operations import get_operation


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(String(20), nullable=False)
    result = Column(Float, nullable=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def compute(self) -> float:
        self.result = get_operation(self.type)(self.a, self.b)
        return self.result
