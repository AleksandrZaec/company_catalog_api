from src.config.logger import logger
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.config.db import get_db
from src.crud.organization import organization_crud
from src.models import Building
from src.schemas.organization import OrganizationRead
from src.schemas.building import BuildingBase
from sqlalchemy import select
from src.utils.security import verify_api_key
from src.config.settings import settings

router = APIRouter()


@router.get(
    "/organizations/by_building/{building_id}",
    response_model=List[OrganizationRead],
    summary="Get organizations by building ID",
    description="Returns all organizations located in the specified building",
    dependencies=[Depends(verify_api_key)]
)
async def organizations_by_building(
        building_id: int,
        db: AsyncSession = Depends(get_db)
) -> List[OrganizationRead]:
    orgs = await organization_crud.get_by_building(db, building_id)
    if not orgs:
        logger.warning(f"No organizations found for building {building_id}")
        raise HTTPException(
            status_code=404,
            detail="No organizations found in this building or building doesn't exist"
        )
    return orgs


@router.get(
    "/organizations/by_activity/{activity_id}",
    response_model=List[OrganizationRead],
    summary="Get organizations by activity ID",
    description=f"Returns all organizations related to the specified activity and its children (up to {settings.MAX_ACTIVITY_DEPTH} levels deep)",
    dependencies=[Depends(verify_api_key)]
)
async def organizations_by_activity(
        activity_id: int,
        db: AsyncSession = Depends(get_db)
) -> List[OrganizationRead]:
    orgs = await organization_crud.get_by_activity(db, activity_id)
    if not orgs:
        logger.warning(f"No organizations found for activity {activity_id}")
        raise HTTPException(
            status_code=404,
            detail="No organizations found for this activity or activity doesn't exist"
        )
    return orgs


@router.get(
    "/organizations/by_activity_name/",
    response_model=List[OrganizationRead],
    summary="Search organizations by activity name",
    description=f"Returns all organizations related to activities with matching name and their children (up to {settings.MAX_ACTIVITY_DEPTH} levels deep)",
    dependencies=[Depends(verify_api_key)]
)
async def organizations_by_activity_name(
        name: str = Query(..., description="Activity name to search for"),
        db: AsyncSession = Depends(get_db)
) -> List[OrganizationRead]:
    orgs = await organization_crud.get_by_activity_name(db, name)
    if not orgs:
        logger.warning(f"No organizations found for activity name '{name}'")
        raise HTTPException(
            status_code=404,
            detail=f"No organizations found for activity name '{name}'"
        )
    return orgs


@router.get(
    "/organizations/{org_id}",
    response_model=OrganizationRead,
    summary="Get organization by ID",
    description="Returns detailed information about a specific organization",
    dependencies=[Depends(verify_api_key)]
)
async def organization_detail(
        org_id: int,
        db: AsyncSession = Depends(get_db)
) -> OrganizationRead:
    org = await organization_crud.get_by_id(db, org_id)
    if not org:
        logger.warning(f"Organization {org_id} not found")
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )
    return org


@router.get(
    "/organizations/search/by_name/",
    response_model=List[OrganizationRead],
    summary="Search organizations by name",
    description="Returns organizations with names containing the search string",
    dependencies=[Depends(verify_api_key)]
)
async def organization_search(
        name: str = Query(..., description="Partial organization name to search for"),
        db: AsyncSession = Depends(get_db)
) -> List[OrganizationRead]:
    orgs = await organization_crud.get_by_name(db, name)
    if not orgs:
        logger.warning(f"No organizations found for name '{name}'")
        raise HTTPException(
            status_code=404,
            detail=f"No organizations found matching '{name}'"
        )
    return orgs


@router.get(
    "/organizations/in_radius/",
    response_model=List[OrganizationRead],
    summary="Get organizations in geographic radius",
    description="Returns organizations located within specified radius (in km) from given coordinates",
    dependencies=[Depends(verify_api_key)]
)
async def organizations_in_radius(
        lat: float = Query(..., example=55.751244, description="Latitude of center point"),
        lng: float = Query(..., example=37.618423, description="Longitude of center point"),
        radius: float = Query(..., example=5.0, description="Search radius in kilometers"),
        db: AsyncSession = Depends(get_db)
) -> List[OrganizationRead]:
    if radius <= 0:
        logger.warning(f"Invalid radius value: {radius}")
        raise HTTPException(
            status_code=400,
            detail="Radius must be positive"
        )

    orgs = await organization_crud.get_in_radius(db, lat, lng, radius)
    if not orgs:
        logger.warning(f"No organizations found in {radius}km radius from {lat},{lng}")
        raise HTTPException(
            status_code=404,
            detail=f"No organizations found within {radius}km of specified location"
        )
    return orgs


@router.get(
    "/buildings/",
    response_model=List[BuildingBase],
    summary="List all buildings",
    description="Returns basic information about all buildings in the system",
    dependencies=[Depends(verify_api_key)]
)
async def list_buildings(db: AsyncSession = Depends(get_db)) -> List[BuildingBase]:
    try:
        result = await db.execute(select(Building))
        buildings = result.scalars().all()
        logger.info(f"Retrieved {len(buildings)} buildings")
        return buildings
    except Exception as e:
        logger.error(f"Error listing buildings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving buildings list"
        )
