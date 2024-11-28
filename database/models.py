# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  November 28, 2024 23:54:29
# Database: sqlite:////tmp/tmp.E1aVtvgWFx-01JDTK3YN54J85QCZQ7QYGWJW1/CorgiCareDatabase/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Caregiver(SAFRSBaseX, Base):
    """
    description: Table of caregivers working at the daycare center
    """
    __tablename__ = 'caregiver'
    _s_collection_name = 'Caregiver'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    hire_date = Column(Date)

    # parent relationships (access parent)

    # child relationships (access children)
    CaresessionList : Mapped[List["Caresession"]] = relationship(back_populates="caregiver")



class FacilityService(SAFRSBaseX, Base):
    """
    description: Services provided by the daycare facility.
    """
    __tablename__ = 'facility_service'
    _s_collection_name = 'FacilityService'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    service_name = Column(String)
    service_cost = Column(Integer)

    # parent relationships (access parent)

    # child relationships (access children)
    BookingServiceList : Mapped[List["BookingService"]] = relationship(back_populates="service")



class Owner(SAFRSBaseX, Base):
    """
    description: Table of dog owners
    """
    __tablename__ = 'owner'
    _s_collection_name = 'Owner'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    email = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    DogList : Mapped[List["Dog"]] = relationship(back_populates="owner")



class Dog(SAFRSBaseX, Base):
    """
    description: Table of dogs admitted to the daycare center
    """
    __tablename__ = 'dog'
    _s_collection_name = 'Dog'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    breed = Column(String)
    birthdate = Column(Date)
    owner_id = Column(ForeignKey('owner.id'))

    # parent relationships (access parent)
    owner : Mapped["Owner"] = relationship(back_populates=("DogList"))

    # child relationships (access children)
    ActivityScheduleList : Mapped[List["ActivitySchedule"]] = relationship(back_populates="dog")
    BookingList : Mapped[List["Booking"]] = relationship(back_populates="dog")
    CaresessionList : Mapped[List["Caresession"]] = relationship(back_populates="dog")
    DietaryRestrictionList : Mapped[List["DietaryRestriction"]] = relationship(back_populates="dog")
    SpecialCareneedList : Mapped[List["SpecialCareneed"]] = relationship(back_populates="dog")



class ActivitySchedule(SAFRSBaseX, Base):
    """
    description: Table to schedule activities for dogs.
    """
    __tablename__ = 'activity_schedule'
    _s_collection_name = 'ActivitySchedule'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    dog_id = Column(ForeignKey('dog.id'))
    activity_date = Column(Date)
    activity_name = Column(String)
    activity_duration = Column(Integer)

    # parent relationships (access parent)
    dog : Mapped["Dog"] = relationship(back_populates=("ActivityScheduleList"))

    # child relationships (access children)



class Booking(SAFRSBaseX, Base):
    """
    description: Table to handle dog daycare bookings
    """
    __tablename__ = 'booking'
    _s_collection_name = 'Booking'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    dog_id = Column(ForeignKey('dog.id'))
    drop_off_date = Column(DateTime)
    pick_up_date = Column(DateTime)
    total_days = Column(Integer)

    # parent relationships (access parent)
    dog : Mapped["Dog"] = relationship(back_populates=("BookingList"))

    # child relationships (access children)
    BookingServiceList : Mapped[List["BookingService"]] = relationship(back_populates="booking")
    InvoiceList : Mapped[List["Invoice"]] = relationship(back_populates="booking")



class Caresession(SAFRSBaseX, Base):
    """
    description: Table recording caresession provided to dogs.
    """
    __tablename__ = 'caresession'
    _s_collection_name = 'Caresession'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    dog_id = Column(ForeignKey('dog.id'))
    caregiver_id = Column(ForeignKey('caregiver.id'))
    session_date = Column(Date)
    notes = Column(String)

    # parent relationships (access parent)
    caregiver : Mapped["Caregiver"] = relationship(back_populates=("CaresessionList"))
    dog : Mapped["Dog"] = relationship(back_populates=("CaresessionList"))

    # child relationships (access children)



class DietaryRestriction(SAFRSBaseX, Base):
    """
    description: Dietary restrictions for dogs
    """
    __tablename__ = 'dietary_restrictions'
    _s_collection_name = 'DietaryRestriction'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    dog_id = Column(ForeignKey('dog.id'))
    restriction_details = Column(String)

    # parent relationships (access parent)
    dog : Mapped["Dog"] = relationship(back_populates=("DietaryRestrictionList"))

    # child relationships (access children)



class SpecialCareneed(SAFRSBaseX, Base):
    """
    description: Special care needs of dogs
    """
    __tablename__ = 'special_careneeds'
    _s_collection_name = 'SpecialCareneed'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    dog_id = Column(ForeignKey('dog.id'))
    condition_name = Column(String)
    care_description = Column(String)

    # parent relationships (access parent)
    dog : Mapped["Dog"] = relationship(back_populates=("SpecialCareneedList"))

    # child relationships (access children)



class BookingService(SAFRSBaseX, Base):
    """
    description: Services assigned to a booking.
    """
    __tablename__ = 'booking_service'
    _s_collection_name = 'BookingService'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    booking_id = Column(ForeignKey('booking.id'))
    service_id = Column(ForeignKey('facility_service.id'))

    # parent relationships (access parent)
    booking : Mapped["Booking"] = relationship(back_populates=("BookingServiceList"))
    service : Mapped["FacilityService"] = relationship(back_populates=("BookingServiceList"))

    # child relationships (access children)



class Invoice(SAFRSBaseX, Base):
    """
    description: Invoices for bookings, sessions, and services.
    """
    __tablename__ = 'invoice'
    _s_collection_name = 'Invoice'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    booking_id = Column(ForeignKey('booking.id'))
    date_issued = Column(Date)
    total_amount = Column(Integer)
    status = Column(String)

    # parent relationships (access parent)
    booking : Mapped["Booking"] = relationship(back_populates=("InvoiceList"))

    # child relationships (access children)
    PaymentList : Mapped[List["Payment"]] = relationship(back_populates="invoice")



class Payment(SAFRSBaseX, Base):
    """
    description: Payment records for invoices.
    """
    __tablename__ = 'payment'
    _s_collection_name = 'Payment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    invoice_id = Column(ForeignKey('invoice.id'))
    payment_date = Column(Date)
    amount = Column(Integer)

    # parent relationships (access parent)
    invoice : Mapped["Invoice"] = relationship(back_populates=("PaymentList"))

    # child relationships (access children)
