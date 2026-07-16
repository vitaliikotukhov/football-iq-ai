from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models import Competition, Country, Fixture, Manager, Referee, Season, Stadium, Team, Transfer
from app.schemas.country import CountryCreate, CountryRead
from app.schemas.team import TeamCreate, TeamRead
router=APIRouter(prefix="/knowledge", tags=["knowledge"])
@router.get("/summary")
def knowledge_summary(db:Session=Depends(get_db))->dict[str,int]:
    models={"countries":Country,"competitions":Competition,"seasons":Season,"teams":Team,"stadiums":Stadium,"managers":Manager,"referees":Referee,"fixtures":Fixture,"transfers":Transfer}
    return {name: db.scalar(select(func.count()).select_from(model)) or 0 for name,model in models.items()}
@router.post("/countries",response_model=CountryRead,status_code=status.HTTP_201_CREATED)
def create_country(payload:CountryCreate,db:Session=Depends(get_db))->Country:
    country=Country(name=payload.name,code=payload.code)
    db.add(country)
    try: db.commit()
    except IntegrityError as exc:
        db.rollback(); raise HTTPException(status_code=409,detail="Country name or code already exists.") from exc
    db.refresh(country); return country
@router.get("/countries",response_model=list[CountryRead])
def list_countries(db:Session=Depends(get_db))->list[Country]:
    return list(db.scalars(select(Country).order_by(Country.name)).all())
@router.post("/teams",response_model=TeamRead,status_code=status.HTTP_201_CREATED)
def create_team(payload:TeamCreate,db:Session=Depends(get_db))->Team:
    team=Team(**payload.model_dump()); db.add(team)
    try: db.commit()
    except IntegrityError as exc:
        db.rollback(); raise HTTPException(status_code=409,detail="Team could not be created. Check related IDs and api_id.") from exc
    db.refresh(team); return team
@router.get("/teams",response_model=list[TeamRead])
def list_teams(db:Session=Depends(get_db))->list[Team]:
    return list(db.scalars(select(Team).order_by(Team.name)).all())
