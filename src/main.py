from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import List, Optional
from . import models, database

app = FastAPI(title="Zoo API")

#1. models and schemas
from pydantic import BaseModel, ConfigDict

class SpeciesCreate(BaseModel):
    name: str
    life_expectancy: int
    family: str
    habitat: str
    extra_info: dict = {}

class SpeciesOut(SpeciesCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class EnclosureCreate(BaseModel):
    complex_name: str
    room_number: int
    has_water: bool
    area: float

class PlacementCreate(BaseModel):
    species_id: int
    enclosure_id: int
    animal_count: int

class EnclosureOut(EnclosureCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

@app.post("/enclosures/", response_model=EnclosureOut)
def create_enclosure(enclosure: EnclosureCreate, db: Session = Depends(database.get_db)):
    db_enclosure = models.Enclosure(**enclosure.model_dump())
    db.add(db_enclosure)
    db.commit()
    db.refresh(db_enclosure)
    return db_enclosure

@app.post("/placements/")
def create_placement(placement: PlacementCreate, db: Session = Depends(database.get_db)):
    db_placement = models.Placement(**placement.model_dump())
    db.add(db_placement)
    db.commit()
    db.refresh(db_placement)
    return db_placement

# 2. CRUD 

@app.post("/species/", response_model=SpeciesOut)
def create_species(species: SpeciesCreate, db: Session = Depends(database.get_db)):
    db_species = models.Species(**species.model_dump())
    db.add(db_species)
    db.commit()
    db.refresh(db_species)
    return db_species

@app.get("/species/{species_id}", response_model=SpeciesOut)
def read_species(species_id: int, db: Session = Depends(database.get_db)):
    res = db.query(models.Species).filter(models.Species.id == species_id).first()
    if not res: raise HTTPException(404, "Not found")
    return res

# 5. queries + 7. pagination + 8. sorting

@app.get("/species/", response_model=List[SpeciesOut])
def get_species_list(
    family: Optional[str] = None,
    min_life: Optional[int] = None,
    sort_by: Optional[str] = "name", # sorting
    skip: int = 0,                   # pagination (offset)
    limit: int = 10,                 # pagination (limit)
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Species)
    
    if family:
        query = query.filter(models.Species.family == family)
    if min_life:
        query = query.filter(models.Species.life_expectancy >= min_life)
    
    if sort_by == "life_expectancy":
        query = query.order_by(models.Species.life_expectancy.desc())
    else:
        query = query.order_by(models.Species.name)
        
    return query.offset(skip).limit(limit).all()

# b. JOIN 
@app.get("/enclosures/{enclosure_id}/animals")
def get_animals_in_enclosure(enclosure_id: int, db: Session = Depends(database.get_db)):
    # JOIN query
    results = db.query(models.Species.name, models.Placement.animal_count)\
        .join(models.Placement, models.Species.id == models.Placement.species_id)\
        .filter(models.Placement.enclosure_id == enclosure_id).all()
    
    return [{"species": r[0], "count": r[1]} for r in results]

# c. UPDATE
@app.put("/enclosures/expand_complex/{complex_name}")
def expand_complex(complex_name: str, db: Session = Depends(database.get_db)):
    stmt = (
        models.Enclosure.__table__.update()
        .where(models.Enclosure.complex_name == complex_name)
        .values(area=models.Enclosure.area * 1.10)
    )
    result = db.execute(stmt)
    db.commit()
    return {"updated_rows": result.rowcount}

# d. GROUP BY 
@app.get("/stats/family_life_expectancy")
def get_stats(db: Session = Depends(database.get_db)):
    results = db.query(
        models.Species.family, 
        func.avg(models.Species.life_expectancy).label("avg_life")
    ).group_by(models.Species.family).all()
    
    return [{"family": r[0], "avg_life": r[1]} for r in results]

# e. SELECT (SQLAlchemy)
@app.get("/species/long_livers/")
def get_long_livers(db: Session = Depends(database.get_db)):
    subquery = db.query(func.avg(models.Species.life_expectancy)).scalar_subquery()
    results = db.query(models.Species).filter(models.Species.life_expectancy > subquery).all()
    return results


@app.get("/search/json/")
def search_json(pattern: str, db: Session = Depends(database.get_db)):
    sql_filter = text("extra_info::text ~ :pattern")
    results = db.query(models.Species).filter(sql_filter).params(pattern=pattern).all()
    return results