from typing import List, Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from src.config.settings import settings
from src.config.logger import logger
from src.models import Organization, Activity
from src.utils.geo import calculate_distance_km


class OrganizationCRUD:

    async def _get_activity_tree_ids(
            self,
            db: AsyncSession,
            activity_id: int,
            level: int
    ) -> List[int]:
        """Recursively retrieves the ID of an activity and all its descendants up to the specified level"""
        if level < 1:
            return []

        try:
            result = await db.execute(
                select(Activity)
                .where(Activity.id == activity_id)
                .options(selectinload(Activity.children))
            )
            activity = result.scalars().first()

            if not activity:
                return []

            ids = [activity.id]
            if level > 1 and activity.children:
                for child in activity.children:
                    ids.extend(await self._get_activity_tree_ids(db, child.id, level - 1))
            return ids
        except Exception as e:
            logger.error(f"Error getting activity tree: {str(e)}", exc_info=True)
            raise

    async def get_by_building(
            self,
            db: AsyncSession,
            building_id: int
    ) -> Sequence[Organization]:
        """Returns all the organizations in the specified building"""
        try:
            result = await db.execute(
                select(Organization)
                .where(Organization.building_id == building_id)
                .options(
                    selectinload(Organization.activities),
                    selectinload(Organization.phones),
                    joinedload(Organization.building)
                )
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting by building: {str(e)}", exc_info=True)
            raise

    async def get_by_activity(
            self,
            db: AsyncSession,
            activity_id: int
    ) -> Sequence[Organization]:
        """Returns organizations by activity ID (including subsidiaries)"""
        try:
            activity_ids = await self._get_activity_tree_ids(
                db, activity_id, settings.MAX_ACTIVITY_DEPTH
            )
            if not activity_ids:
                logger.warning(f"No activities found for id {activity_id}")
                return []

            result = await db.execute(
                select(Organization)
                .join(Organization.activities)
                .where(Activity.id.in_(activity_ids))
                .options(
                    selectinload(Organization.activities),
                    selectinload(Organization.phones),
                    joinedload(Organization.building)
                )
                .distinct()
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting by activity: {str(e)}", exc_info=True)
            raise

    async def get_by_activity_name(
            self,
            db: AsyncSession,
            activity_name: str
    ) -> Sequence[Organization]:
        """Searches for organizations by type of activity (including subsidiaries)"""
        try:
            result = await db.execute(
                select(Activity)
                .where(Activity.name.ilike(f"%{activity_name}%"))
            )
            activities = result.scalars().all()

            activity_ids = []
            for activity in activities:
                activity_ids.extend(
                    await self._get_activity_tree_ids(
                        db, activity.id, settings.MAX_ACTIVITY_DEPTH
                    )
                )

            if not activity_ids:
                return []

            result = await db.execute(
                select(Organization)
                .join(Organization.activities)
                .where(Activity.id.in_(activity_ids))
                .options(
                    selectinload(Organization.activities),
                    selectinload(Organization.phones),
                    joinedload(Organization.building)
                )
                .distinct()
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting by activity name: {str(e)}", exc_info=True)
            raise

    async def get_by_name(
            self,
            db: AsyncSession,
            name: str
    ) -> Sequence[Organization]:
        """Searches for organizations by name (case-insensitive)"""
        try:
            result = await db.execute(
                select(Organization)
                .where(Organization.name.ilike(f"%{name}%"))
                .options(
                    selectinload(Organization.activities),
                    selectinload(Organization.phones),
                    joinedload(Organization.building)
                )
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error searching by name: {str(e)}", exc_info=True)
            raise

    async def get_by_id(
            self,
            db: AsyncSession,
            org_id: int
    ) -> Optional[Organization]:
        """Returns an organization by ID with all related data"""
        try:
            result = await db.execute(
                select(Organization)
                .where(Organization.id == org_id)
                .options(
                    selectinload(Organization.activities),
                    selectinload(Organization.phones),
                    joinedload(Organization.building)
                )
            )
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error getting organization: {str(e)}", exc_info=True)
            raise

    async def get_in_radius(
            self,
            db: AsyncSession,
            lat: float,
            lng: float,
            radius_km: float,
            limit: Optional[int] = None
    ) -> Sequence[Organization]:
        if radius_km <= 0:
            return []
        """Searches for organizations within the specified coordinates"""
        try:
            result = await db.execute(
                select(Organization)
                .join(Organization.building)
                .options(
                    selectinload(Organization.activities),
                    selectinload(Organization.phones),
                    joinedload(Organization.building)
                )
            )

            orgs_in_radius = []
            for org in result.scalars().all():
                if org.building:
                    distance = calculate_distance_km(
                        lat, lng,
                        org.building.latitude,
                        org.building.longitude
                    )
                    if distance <= radius_km:
                        orgs_in_radius.append(org)
                        if limit and len(orgs_in_radius) >= limit:
                            break

            return orgs_in_radius
        except Exception as e:
            logger.error(f"Error getting in radius: {str(e)}", exc_info=True)
            raise


organization_crud = OrganizationCRUD()
