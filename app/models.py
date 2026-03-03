from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    habits = relationship("Habit", back_populates="owner")


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="habits")
    completions = relationship("Completion", back_populates="habit")


class Completion(Base):
    __tablename__ = "completions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    habit_id = Column(Integer, ForeignKey("habits.id"))

    habit = relationship("Habit", back_populates="completions")

    __table_args__ = (
        UniqueConstraint("habit_id", "date", name="unique_completion_per_day"),
    )