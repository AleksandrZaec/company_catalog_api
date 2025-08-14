import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config.db import Base, get_db
from src.config.settings import settings
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.models import Activity, Building, Organization, Phone


@pytest.fixture(scope="session", autouse=True)
def ensure_test_env():
    """Ensure tests run only in the TEST environment."""
    assert settings.MODE == "TEST", f"Expected MODE=TEST, got {settings.MODE}"


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Create a fresh test database engine and recreate schema per test."""
    engine = create_async_engine(settings.DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_session(test_engine):
    """Provide a new async DB session for each test."""
    sessionmaker_ = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)
    async with sessionmaker_() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def test_client(test_session):
    """Override get_db dependency and provide an async test client."""

    async def override_get_db():
        yield test_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
            transport=transport,
            base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def seed_test_data(test_session):
    """Siding test data"""
    db_session = test_session

    root_food = Activity(name="Еда")
    root_auto = Activity(name="Автомобили")
    db_session.add_all([root_food, root_auto])
    await db_session.commit()

    meat = Activity(name="Мясная продукция", parent_id=root_food.id)
    milk = Activity(name="Молочная продукция", parent_id=root_food.id)
    cargo = Activity(name="Грузовые", parent_id=root_auto.id)
    db_session.add_all([meat, milk, cargo])
    await db_session.commit()

    b1 = Building(address="Москва, Тверская 1", latitude=55.76, longitude=37.61)
    b2 = Building(address="Москва, Арбат 10", latitude=55.75, longitude=37.59)
    db_session.add_all([b1, b2])
    await db_session.commit()

    o1 = Organization(name="ООО Мясоед", building_id=b1.id, activities=[meat])
    o1.phones.append(Phone(number="+7 999 111-22-33"))

    o2 = Organization(name="ООО Молочник", building_id=b1.id, activities=[milk])
    o2.phones.append(Phone(number="+7 999 444-55-66"))

    o3 = Organization(name="ООО Грузовик", building_id=b2.id, activities=[cargo])
    o3.phones.append(Phone(number="+7 999 777-88-99"))

    db_session.add_all([o1, o2, o3])
    await db_session.commit()

    yield {
        "activities": {
            "root_food": root_food,
            "root_auto": root_auto,
            "meat": meat,
            "milk": milk,
            "cargo": cargo
        },
        "buildings": [b1, b2],
        "orgs": [o1, o2, o3]
    }
