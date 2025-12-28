from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from .database import Base

class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)          
    life_expectancy = Column(Integer)         
    family = Column(String)                   
    habitat = Column(String)   

    placements = relationship("Placement", back_populates="species")               
    

class Enclosure(Base):
    __tablename__ = "enclosures"

    id = Column(Integer, primary_key=True, index=True)
    complex_name = Column(String)            
    room_number = Column(Integer)            
    has_water = Column(Boolean, default=False)
    area = Column(Float)                       

    placements = relationship("Placement", back_populates="enclosure")

class Placement(Base):
    __tablename__ = "placements"

    id = Column(Integer, primary_key=True, index=True)
    species_id = Column(Integer, ForeignKey("species.id"))
    enclosure_id = Column(Integer, ForeignKey("enclosures.id"))
    animal_count = Column(Integer)             # Количество животных

    species = relationship("Species", back_populates="placements")
    enclosure = relationship("Enclosure", back_populates="placements")