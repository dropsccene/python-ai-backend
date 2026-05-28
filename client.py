import httpx

r = httpx.get("http://localhost:8000/health")
r.status_code
r.json()
print(r.status_code)
print(r.json())