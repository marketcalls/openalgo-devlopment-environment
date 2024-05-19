from fastapi import FastAPI
from databases import Database
import redis.asyncio as aioredis

DATABASE_URL = "postgresql://myuser:mypassword@postgres/mydb"
REDIS_URL = "redis://redis:6379"

database = Database(DATABASE_URL)
redis = aioredis.from_url(REDIS_URL)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()
    await redis.ping()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await redis.close()

@app.get("/")
def read_root():
    return {"Hello": "Development Environement"}

@app.get("/postgres")
async def postgres():
    query = "SELECT 1"
    result = await database.fetch_one(query=query)
    return {"PostgreSQL": result[0]}

@app.get("/redis")
async def redis():
    await redis.set("key", "value")
    value = await redis.get("key")
    return {"Redis": value.decode("utf-8")}