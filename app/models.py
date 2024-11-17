from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


service_mechanics = db.Table(
    "service_mechanics",
    Base.metadata,
    Column("ticket_id", db.ForeignKey("serviceTickets.id")),
    Column("mechanics_id", db.ForeignKey("mechanics.id"))
)

class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(200), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20))
    password: Mapped[str] = mapped_column(db.String(20), nullable=False)

    # One-to-Many
    serviceTickets: Mapped[List['ServiceTicket']] = relationship(back_populates='customer')

class ServiceTicket(Base):
    __tablename__ = 'serviceTickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(100), nullable=False)
    service_date: Mapped[date] = mapped_column(nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(100), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))
    

    # Many-to-One
    customer: Mapped['Customer'] = relationship(back_populates='serviceTickets')
    # Many-to-Many
    mechanics: Mapped[List['Mechanic']] = relationship(secondary=service_mechanics, back_populates='serviceTickets')

class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(50), nullable=False)
    salary: Mapped[float] = mapped_column( nullable=False)
    password: Mapped[str] = mapped_column(db.String(20), nullable=False)
    role: Mapped[str] = mapped_column(db.String(20), nullable=False)

    serviceTickets: Mapped[List['ServiceTicket']] = relationship(secondary=service_mechanics, back_populates='mechanics')

    # Add query attribute
    query = db.session.query_property()