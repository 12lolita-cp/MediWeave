from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import Query
from sqlalchemy import select

from app.api.dependencies import get_db
from app.models.pharmacy import Pharmacy
from app.schemas.pharmacy import PharmacyCreate, PharmacyResponse


router = APIRouter(
    prefix="/pharmacies",
    tags=["Pharmacies"]
)


@router.post(
    "/",
    response_model=PharmacyResponse,
    status_code=status.HTTP_201_CREATED
)
def register_pharmacy(
    pharmacy_data: PharmacyCreate,
    db: Session = Depends(get_db)
):
    pharmacy = Pharmacy(
        name=pharmacy_data.name,
        licensing_authority=pharmacy_data.licensing_authority,
        registration_number=pharmacy_data.registration_number,
        contact_email=pharmacy_data.contact_email,
        contact_phone=pharmacy_data.contact_phone
    )

    try:
        db.add(pharmacy)
        db.commit()
        db.refresh(pharmacy)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A pharmacy with this licensing authority and registration number already exists."
        )

    return pharmacy

@router.get("/{pharmacy_id}", response_model=PharmacyResponse)
def get_pharmacy(pharmacy_id: int, db: Session = Depends(get_db)):
    pharmacy = db.get(Pharmacy, pharmacy_id)

    if pharmacy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pharmacy not found"
        )

    return pharmacy


@router.get(
    "/",
    response_model=list[PharmacyResponse]
)
def get_all_pharmacies(
    db: Session = Depends(get_db),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    statement = (
        select(Pharmacy)
        .order_by(Pharmacy.id)
        .offset(offset)
        .limit(limit)
    )

    pharmacies = db.scalars(statement).all()

    return pharmacies