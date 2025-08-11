from src.config.logger import logger
from typing import Any, List, Type
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel


class BaseCRUD:
    def __init__(
            self,
            model: Type[Any],
            create_schema: Type[BaseModel],
            update_schema: Type[BaseModel],
            read_schema: Type[BaseModel],
    ) -> None:
        self.model = model
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.read_schema = read_schema

    async def get_by_id(self, db: AsyncSession, obj_id: int) -> BaseModel:
        result = await db.execute(select(self.model).where(self.model.id == obj_id))
        obj = result.scalar_one_or_none()
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return self.read_schema.model_validate(obj)

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[BaseModel]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        objs = result.scalars().all()
        return [self.read_schema.model_validate(obj) for obj in objs]

    async def create(self, db: AsyncSession, obj_in: BaseModel) -> BaseModel:
        obj_data = obj_in.model_dump(exclude_unset=True)
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        try:
            await db.commit()
            await db.refresh(db_obj)
        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating {self.model.__name__}: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
        return self.read_schema.model_validate(db_obj)

    async def update(self, db: AsyncSession, obj_id: int, obj_in: BaseModel) -> BaseModel:
        result = await db.execute(select(self.model).where(self.model.id == obj_id))
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Object not found")

        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)

        try:
            await db.commit()
            await db.refresh(db_obj)
        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating {self.model.__name__} id={obj_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        return self.read_schema.model_validate(db_obj)

    async def delete(self, db: AsyncSession, obj_id: int) -> None:
        result = await db.execute(select(self.model).where(self.model.id == obj_id))
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Object not found")

        try:
            await db.delete(db_obj)
            await db.commit()
        except Exception as e:
            await db.rollback()
            logger.error(f"Error deleting {self.model.__name__} id={obj_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
