from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Job Tracker API", lifespan=lifespan)


def get_or_404(db: Session, app_id: int) -> models.Application:
    obj = db.get(models.Application, app_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return obj


@app.post("/applications", response_model=schemas.ApplicationOut, status_code=201)
def create_application(payload: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    obj = models.Application(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/applications", response_model=list[schemas.ApplicationOut])
def list_applications(status: schemas.Status | None = None, db: Session = Depends(get_db)):
    query = select(models.Application).order_by(models.Application.id)
    if status is not None:
        query = query.where(models.Application.status == status.value)
    return db.scalars(query).all()


@app.get("/applications/{app_id}", response_model=schemas.ApplicationOut)
def get_application(app_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, app_id)


@app.patch("/applications/{app_id}", response_model=schemas.ApplicationOut)
def update_application(app_id: int, payload: schemas.ApplicationUpdate, db: Session = Depends(get_db)):
    obj = get_or_404(db, app_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/applications/{app_id}", status_code=204)
def delete_application(app_id: int, db: Session = Depends(get_db)):
    obj = get_or_404(db, app_id)
    db.delete(obj)
    db.commit()