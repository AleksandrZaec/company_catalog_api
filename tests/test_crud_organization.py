import pytest
from src.crud.organization import organization_crud


@pytest.mark.asyncio
class TestOrganizationByBuilding:

    async def test_get_by_building(self, test_session, seed_test_data):
        b1 = seed_test_data["buildings"][0]
        result = await organization_crud.get_by_building(test_session, b1.id)
        assert len(result) == 2
        assert {o.name for o in result} == {"ООО Мясоед", "ООО Молочник"}

    async def test_get_by_building_empty(self, test_session):
        result = await organization_crud.get_by_building(test_session, 9999)
        assert result == []


@pytest.mark.asyncio
class TestOrganizationByActivity:

    async def test_get_by_activity(self, test_session, seed_test_data):
        meat = seed_test_data["activities"]["meat"]
        result = await organization_crud.get_by_activity(test_session, meat.id)
        assert len(result) == 1
        assert result[0].name == "ООО Мясоед"

    async def test_get_by_activity_empty(self, test_session):
        result = await organization_crud.get_by_activity(test_session, 9999)
        assert result == []

    async def test_get_by_activity_name(self, test_session, seed_test_data):
        result = await organization_crud.get_by_activity_name(test_session, "Молоч")
        assert len(result) == 1
        assert result[0].name == "ООО Молочник"

    async def test_get_by_activity_name_empty(self, test_session):
        result = await organization_crud.get_by_activity_name(test_session, "НеСуществует")
        assert result == []


@pytest.mark.asyncio
class TestOrganizationByNameAndID:

    async def test_get_by_name(self, test_session, seed_test_data):
        result = await organization_crud.get_by_name(test_session, "Грузов")
        assert len(result) == 1
        assert result[0].name == "ООО Грузовик"

    async def test_get_by_name_empty(self, test_session):
        result = await organization_crud.get_by_name(test_session, "НеСуществует")
        assert result == []

    async def test_get_by_id(self, test_session, seed_test_data):
        org = seed_test_data["orgs"][0]
        result = await organization_crud.get_by_id(test_session, org.id)
        assert result.name == org.name

    async def test_get_by_id_not_found(self, test_session):
        result = await organization_crud.get_by_id(test_session, 9999)
        assert result is None


@pytest.mark.asyncio
class TestOrganizationInRadius:

    async def test_get_in_radius(self, test_session, seed_test_data):
        lat, lng = 55.76, 37.61
        result = await organization_crud.get_in_radius(test_session, lat, lng, 1.0)
        names = {o.name for o in result}
        assert "ООО Мясоед" in names
        assert "ООО Молочник" in names

    async def test_get_in_radius_zero_radius(self, test_session, seed_test_data):
        lat, lng = 55.76, 37.61
        result = await organization_crud.get_in_radius(test_session, lat, lng, 0)
        assert result == []

    async def test_get_in_radius_with_limit(self, test_session, seed_test_data):
        lat, lng = 55.76, 37.61
        result = await organization_crud.get_in_radius(test_session, lat, lng, 10, limit=1)
        assert len(result) == 1


@pytest.mark.asyncio
class TestActivityTreeIDs:

    async def test_get_activity_tree_ids_root_and_children(self, test_session, seed_test_data):
        root_food = seed_test_data["activities"]["root_food"]
        ids = await organization_crud._get_activity_tree_ids(test_session, root_food.id, 2)
        expected_ids = {root_food.id,
                        seed_test_data["activities"]["meat"].id,
                        seed_test_data["activities"]["milk"].id}
        assert set(ids) == expected_ids

    async def test_get_activity_tree_ids_level_limit(self, test_session, seed_test_data):
        root_food = seed_test_data["activities"]["root_food"]
        ids = await organization_crud._get_activity_tree_ids(test_session, root_food.id, 1)
        assert ids == [root_food.id]
