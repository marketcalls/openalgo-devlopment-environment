from fastapi import FastAPI
from databases import Database
import redis.asyncio as redis

DATABASE_URL = "postgresql://myuser:mypassword@postgres/mydb"
REDIS_URL = "redis://redis:6379"

database = Database(DATABASE_URL)
redis_client = redis.from_url(REDIS_URL)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()
    await redis_client.ping()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await redis_client.close()

@app.get("/")
def read_root():
    return {"Hello": "Development Environment"}

@app.get("/postgres")
async def postgres():
    query = "SELECT 1"
    result = await database.fetch_one(query=query)
    return {"PostgreSQL": result[0]}

@app.get("/redis")
async def redis():
    await redis_client.set("key", "value")
    value = await redis_client.get("key")
    return {"Redis": value.decode("utf-8")}