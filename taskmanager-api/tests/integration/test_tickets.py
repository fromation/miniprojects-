import pytest

@pytest.mark.asyncio
async def test_ticket_flow(client):
        await client.post("/auth/register", json={
            "email": "ticketuser@example.com",
            "password": "password123",
            "username": "ticketuser"
        })

        login_response = await client.post("/auth/login", data={
            "username": "ticketuser@example.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        ticket_response = await client.post("/tickets/", json={
            "title": "Test Ticket",
            "description": "Testing ticket creation"
        }, headers=headers)
        assert ticket_response.status_code == 201

        get_response = await client.get("/tickets/", headers=headers)
        assert get_response.status_code == 200
        tickets = get_response.json()
        assert any(t["title"] == "Test Ticket" for t in tickets)
