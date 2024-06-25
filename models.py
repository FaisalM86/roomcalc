# models.py

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    access_level = Column(Integer, nullable=False)  # Add this line to define access_level

class Project(Base):
    __tablename__ = 'projects'
    ProjectID = Column(Integer, primary_key=True)
    ProjectName = Column(String, nullable=False)
    Client = Column(String)
    Contract = Column(String)
    SubContractor = Column(String)
    DocumentNumber = Column(String)
    Revision = Column(String)
    RevisionDate = Column(String)
    AmbientTempSummer = Column(Float)
    AmbientTempWinter = Column(Float)
    DefaultUValue = Column(Float)
    Density = Column(Float)
    HeatCapacity = Column(Float)
    rooms = relationship("Room", back_populates="project")
    supply_systems = relationship("SupplySystem", back_populates="project")

class Room(Base):
    __tablename__ = 'rooms'
    RoomID = Column(Integer, primary_key=True)
    ProjectID = Column(Integer, ForeignKey('projects.ProjectID'))
    LocationNo = Column(String)
    RoomName = Column(String, nullable=False)
    MinAirChangeRate = Column(Float)
    MinVentilationPerArea = Column(Float)
    MinVentilationPerPerson = Column(Float)
    Elevation = Column(Float)
    Height = Column(Float)
    Remarks = Column(Text)
    Volume = Column(Float)
    FloorArea = Column(Float)
    Occupancy = Column(Integer)
    RequiredAirflow = Column(Float)

    project = relationship("Project", back_populates="rooms")
    surfaces = relationship("Surface", back_populates="room")
    room_supply_systems = relationship("RoomSupplySystem", back_populates="room")
    lights = relationship("Light", back_populates="room")
    personnels = relationship("Personnel", back_populates="room")
    equipments = relationship("Equipment", back_populates="room")
    walls = relationship("WallData", back_populates="room", cascade="all, delete-orphan")


class WallData(Base):
    __tablename__ = 'wall_data'

    WallID = Column(Integer, primary_key=True, autoincrement=True)
    RoomID = Column(Integer, ForeignKey('rooms.RoomID'), nullable=False)
    Length = Column(Float, nullable=False)
    Angle = Column(Float, nullable=False)
    room = relationship("Room", back_populates="walls")
class Surface(Base):
    __tablename__ = 'surfaces'
    SurfaceID = Column(Integer, primary_key=True)
    RoomID = Column(Integer, ForeignKey('rooms.RoomID'))
    SurfaceType = Column(String, nullable=False)
    Area = Column(Float)
    UValue = Column(Float)
    TemperatureOther = Column(Float)
    room = relationship("Room", back_populates="surfaces")

class SupplySystem(Base):
    __tablename__ = 'supply_systems'
    SupplySystemID = Column(Integer, primary_key=True)
    ProjectID = Column(Integer, ForeignKey('projects.ProjectID'))
    SystemNo = Column(String)
    SystemName = Column(String)
    TempSupplyWinter = Column(Float)
    TempSupplySummer = Column(Float)
    CoolingEnthalpy = Column(Float)
    FanHeat = Column(Float)
    project = relationship("Project", back_populates="supply_systems")
    room_supply_systems = relationship("RoomSupplySystem", back_populates="supply_system")

class RoomSupplySystem(Base):
    __tablename__ = 'room_supply_systems'
    RoomID = Column(Integer, ForeignKey('rooms.RoomID'), primary_key=True)
    SupplySystemID = Column(Integer, ForeignKey('supply_systems.SupplySystemID'), primary_key=True)
    IncreaseDecrease = Column(String)
    RecircSystemName = Column(String)
    ExtractSystemName = Column(String)
    CoolAirTempSummer = Column(Float)
    CoolAirTempWinter = Column(Float)
    room = relationship("Room", back_populates="room_supply_systems")
    supply_system = relationship("SupplySystem", back_populates="room_supply_systems")

class Light(Base):
    __tablename__ = 'lights'
    LightID = Column(Integer, primary_key=True)
    RoomID = Column(Integer, ForeignKey('rooms.RoomID'))
    LightDescription = Column(String)
    HeatLoadSummer = Column(Float)
    HeatLoadWinter = Column(Float)
    ApplySummer = Column(Integer)
    ApplyWinter = Column(Integer)
    room = relationship("Room", back_populates="lights")

class Personnel(Base):
    __tablename__ = 'personnels'
    PersonnelID = Column(Integer, primary_key=True)
    RoomID = Column(Integer, ForeignKey('rooms.RoomID'))
    Quantity = Column(Integer)
    HeatLoadPerPersonSummer = Column(Float)
    HeatLoadPerPersonWinter = Column(Float)
    ApplySummer = Column(Integer)
    ApplyWinter = Column(Integer)
    room = relationship("Room", back_populates="personnels")

class Equipment(Base):
    __tablename__ = 'equipments'
    EquipmentID = Column(Integer, primary_key=True)
    RoomID = Column(Integer, ForeignKey('rooms.RoomID'))
    EquipmentDescription = Column(String)
    HeatLoadSummer = Column(Float)
    HeatLoadWinter = Column(Float)
    ApplySummer = Column(Integer)
    ApplyWinter = Column(Integer)
    room = relationship("Room", back_populates="equipments")
