import pytest

API_KEY_HEADER = {"X-API-Key": "test-key"}


@pytest.mark.asyncio
class TestOrganizationsAPI:

    async def test_by_building(self, test_client, seed_test_data):
        b1 = seed_test_data["buildings"][0]
        response = await test_client.get(f"/organizations/by_building/{b1.id}", headers=API_KEY_HEADER)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    async def test_by_activity(self, test_client, seed_test_data):
        meat = seed_test_data["activities"]["meat"]
        response = await test_client.get(f"/organizations/by_activity/{meat.id}", headers=API_KEY_HEADER)
        assert response.status_code == 200
        data = response.json()
        assert data[0]["name"] == "ООО Мясоед"

    async def test_by_activity_name(self, test_client, seed_test_data):
        response = await test_client.get("/organizations/by_activity_name/?name=Молоч", headers=API_KEY_HEADER)
        assert response.status_code == 200
        data = response.json()
        assert data[0]["name"] == "ООО Молочник"

    async def test_by_name(self, test_client, seed_test_data):
        response = await test_client.get("/organizations/search/by_name/?name=Грузов", headers=API_KEY_HEADER)
        assert response.status_code == 200
        data = response.json()
        assert data[0]["name"] == "ООО Грузовик"

    async def test_get_in_radius(self, test_client, seed_test_data):
        response = await test_client.get("/organizations/in_radius/?lat=55.76&lng=37.61&radius=1",
                                         headers=API_KEY_HEADER)
        assert response.status_code == 200
        names = {o["name"] for o in response.json()}
        assert "ООО Мясоед" in names

    async def test_organization_detail(self, test_client, seed_test_data):
        org = seed_test_data["orgs"][0]
        response = await test_client.get(f"/organizations/{org.id}", headers=API_KEY_HEADER)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == org.name


@pytest.mark.asyncio
class TestOrganizationsAPIErrors:

    async def test_by_building_not_found(self, test_client):
        response = await test_client.get("/organizations/by_building/9999", headers=API_KEY_HEADER)
        assert response.status_code == 404

    async def test_by_activity_not_found(self, test_client):
        response = await test_client.get("/organizations/by_activity/9999", headers=API_KEY_HEADER)
        assert response.status_code == 404

    async def test_by_activity_name_not_found(self, test_client):
        response = await test_client.get("/organizations/by_activity_name/?name=НеСуществует", headers=API_KEY_HEADER)
        assert response.status_code == 404

    async def test_by_name_not_found(self, test_client):
        response = await test_client.get("/organizations/search/by_name/?name=НеСуществует", headers=API_KEY_HEADER)
        assert response.status_code == 404

    async def test_in_radius_invalid_radius(self, test_client):
        response = await test_client.get("/organizations/in_radius/?lat=55.76&lng=37.61&radius=-1",
                                         headers=API_KEY_HEADER)
        assert response.status_code == 400

    async def test_without_api_key(self, test_client):
        response = await test_client.get("/organizations/by_building/1")
        assert response.status_code == 422

    async def test_invalid_api_key(self, test_client):
        headers = {"X-API-Key": "wrong-key"}
        response = await test_client.get("/organizations/by_building/1", headers=headers)
        assert response.status_code == 403


@pytest.mark.asyncio
class TestBuildingsAPI:

    async def test_list_buildings(self, test_client, seed_test_data):
        response = await test_client.get("/organizations/buildings/", headers=API_KEY_HEADER)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == len(seed_test_data["buildings"])
