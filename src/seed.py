import asyncio
from faker import Faker
from sqlalchemy import select
from src.config.db import AsyncSessionLocal
from src.models import Building, Activity, Organization, Phone
import random

fake = Faker('ru_RU')


async def seed_database():
    async with AsyncSessionLocal() as session:

        root_activities = [
            Activity(name="Еда"),
            Activity(name="Автомобили"),
        ]
        session.add_all(root_activities)
        await session.commit()

        child_activities = [
            Activity(name="Мясная продукция", parent_id=root_activities[0].id),
            Activity(name="Молочная продукция", parent_id=root_activities[0].id),
            Activity(name="Грузовые", parent_id=root_activities[1].id),
            Activity(name="Легковые", parent_id=root_activities[1].id),
            Activity(name="Запчасти", parent_id=None),
            Activity(name="Аксессуары", parent_id=None),
        ]
        session.add_all(child_activities)
        await session.commit()

        buildings = []
        for _ in range(50):
            buildings.append(Building(
                address=f"{fake.city()}, {fake.street_address()}",
                latitude=random.uniform(55.55, 55.90),
                longitude=random.uniform(37.35, 37.85)
            ))
        session.add_all(buildings)
        await session.commit()

        all_activities = (await session.execute(select(Activity))).scalars().all()

        for _ in range(200):
            org = Organization(
                name=f"ООО {fake.company()}",
                building_id=fake.random_element(buildings).id
            )

            selected_activities = fake.random_elements(
                elements=all_activities,
                unique=True,
                length=fake.random_int(1, 3)
            )
            org.activities.extend(selected_activities)

            for _ in range(fake.random_int(1, 3)):
                org.phones.append(Phone(
                    number=fake.phone_number()
                ))

            session.add(org)

        await session.commit()
        print("The test data has been created successfully!")


if __name__ == "__main__":
    asyncio.run(seed_database())
