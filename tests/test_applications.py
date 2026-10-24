def make(client, **overrides):
    payload = {"company": "Acme", "role": "Backend Engineer"} | overrides
    return client.post("/applications", json=payload)


def test_create_and_get(client):
    r = make(client)
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "saved"
    assert client.get(f"/applications/{body['id']}").json()["company"] == "Acme"

def test_patch_updates_status(client):
    created = make(client).json()                      
    r = client.patch(f"/applications/{created['id']}",
                     json={"status": "interview"})     
    assert r.status_code == 200                  
    after = client.get(f"/applications/{created['id']}").json()
    assert after["status"] == "interview"       

def test_patch_only_notes_leaves_other_fields_unchanged(client):
    created = make(client, company="Acme", role="Backend Engineer").json()

    r = client.patch(f"/applications/{created['id']}", json={"notes": "Recruiter called"})
    assert r.status_code == 200

    after = client.get(f"/applications/{created['id']}").json()
    assert after["notes"] == "Recruiter called"        
    assert after["company"] == "Acme"    
    assert after["role"] == "Backend Engineer"

def test_delete_removes_application(client):
    created = make(client).json()
    r = client.delete(f"/applications/{created['id']}")
    assert r.status_code == 204
    after = client.get(f"/applications/{created['id']}")
    assert after.status_code == 404

def test_filter_by_status(client):
    make(client, status="applied")
    make(client, company="Globex")
    r = client.get("/applications", params={"status": "applied"})
    assert [a["company"] for a in r.json()] == ["Acme"]


def test_invalid_status_is_rejected(client):
    assert make(client, status="ghosted").status_code == 422

def test_patch_null_status_is_rejected(client):
    created = make(client).json()
    r = client.patch(f"/applications/{created['id']}", json={"status": None})
    assert r.status_code == 422


def test_get_missing_returns_404(client):
    assert client.get("/applications/999").status_code == 404