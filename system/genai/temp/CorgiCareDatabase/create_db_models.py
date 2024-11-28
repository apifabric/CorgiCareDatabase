# using resolved_model gpt-4o-2024-08-06# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import date   
from datetime import datetime


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py

from sqlalchemy.dialects.sqlite import *


class Dog(Base):
    """description: Table of dogs admitted to the daycare center"""
    __tablename__ = 'dog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    breed = Column(String)
    birthdate = Column(Date)
    owner_id = Column(Integer, ForeignKey('owner.id'))


class Owner(Base):
    """description: Table of dog owners"""
    __tablename__ = 'owner'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    email = Column(String)


class Booking(Base):
    """description: Table to handle dog daycare bookings"""
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dog_id = Column(Integer, ForeignKey('dog.id'))
    drop_off_date = Column(DateTime)
    pick_up_date = Column(DateTime)
    total_days = Column(Integer)  # derived attribute


class Caregiver(Base):
    """description: Table of caregivers working at the daycare center"""
    __tablename__ = 'caregiver'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    hire_date = Column(Date)


class CareSession(Base):
    """description: Table recording caresession provided to dogs."""
    __tablename__ = 'caresession'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dog_id = Column(Integer, ForeignKey('dog.id'))
    caregiver_id = Column(Integer, ForeignKey('caregiver.id'))
    session_date = Column(Date)
    notes = Column(String)


class SpecialCareNeeds(Base):
    """description: Special care needs of dogs"""
    __tablename__ = 'special_careneeds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dog_id = Column(Integer, ForeignKey('dog.id'))
    condition_name = Column(String)
    care_description = Column(String)


class DietaryRestrictions(Base):
    """description: Dietary restrictions for dogs"""
    __tablename__ = 'dietary_restrictions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dog_id = Column(Integer, ForeignKey('dog.id'))
    restriction_details = Column(String)


class ActivitySchedule(Base):
    """description: Table to schedule activities for dogs."""
    __tablename__ = 'activity_schedule'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dog_id = Column(Integer, ForeignKey('dog.id'))
    activity_date = Column(Date)
    activity_name = Column(String)
    activity_duration = Column(Integer)


class Invoice(Base):
    """description: Invoices for bookings, sessions, and services."""
    __tablename__ = 'invoice'

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey('booking.id'))
    date_issued = Column(Date)
    total_amount = Column(Integer)  # derived attribute
    status = Column(String, default="Pending")


class Payment(Base):
    """description: Payment records for invoices."""
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey('invoice.id'))
    payment_date = Column(Date)
    amount = Column(Integer)


class FacilityService(Base):
    """description: Services provided by the daycare facility."""
    __tablename__ = 'facility_service'

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String)
    service_cost = Column(Integer)


class BookingService(Base):
    """description: Services assigned to a booking."""
    __tablename__ = 'booking_service'

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey('booking.id'))
    service_id = Column(Integer, ForeignKey('facility_service.id'))


# end of model classes


try:
    
    
    
    
    # ALS/GenAI: Create an SQLite database
    
    engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    
    Base.metadata.create_all(engine)
    
    
    
    Session = sessionmaker(bind=engine)
    
    session = Session()
    
    
    
    # ALS/GenAI: Prepare for sample data
    
    
    
    session.commit()
    dog1 = Dog(name="Bella", breed="Welsh Corgi", birthdate=date(2018, 6, 1), owner_id=1)
    dog2 = Dog(name="Charlie", breed="Welsh Corgi", birthdate=date(2019, 5, 14), owner_id=2)
    dog3 = Dog(name="Max", breed="Welsh Corgi", birthdate=date(2020, 7, 10), owner_id=3)
    dog4 = Dog(name="Lucy", breed="Welsh Corgi", birthdate=date(2021, 9, 25), owner_id=4)
    owner1 = Owner(first_name="John", last_name="Doe", phone_number="123-456-7890", email="john.doe@example.com")
    owner2 = Owner(first_name="Jane", last_name="Smith", phone_number="987-654-3210", email="jane.smith@example.com")
    owner3 = Owner(first_name="Alice", last_name="Brown", phone_number="555-123-4567", email="alice.brown@example.com")
    owner4 = Owner(first_name="Bob", last_name="Johnson", phone_number="444-888-6666", email="bob.johnson@example.com")
    
    
    
    session.add_all([dog1, dog2, dog3, dog4, owner1, owner2, owner3, owner4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
