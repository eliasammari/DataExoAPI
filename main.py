from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from db import get_session, engine
from models import User, UserSchema, Base
import aioredis
from functools import wraps
import tracemalloc
tracemalloc.start()


app = FastAPI()


# ------------------------------------------
#           Connexion Redis
# ------------------------------------------

redis_pool = None

async def get_redis_pool():
    global redis_pool
    if not redis_pool:
        redis_pool = await aioredis.create_redis_pool("redis://localhost")
    return redis_pool

# Middleware pour le cache avec Redis
async def cache_middleware(request, call_next, redis_pool=Depends(get_redis_pool)):
    key = request.url.path
    cached_response = await redis_pool.get(key)
    if cached_response:
        return cached_response
    response = await call_next(request)
    await redis_pool.set(key, response, expire=60)  # Cache valide pendant 60 secondes
    return response

app.middleware("http")(cache_middleware)


# ------------------------------------------
#             API routes
# ------------------------------------------

async def get_db():
    db = get_session()
    try:
        yield db
    finally:
        await db.close()


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.post("/users")
async def index(user: UserSchema, db: AsyncSession = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
    
# Define a GET endpoint for /users
@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(User))
    users = results.scalars().all()
    return {'users':users}

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        async with engine.connect() as connection:
            db_user = await db.get(User, user_id)
            if db_user is None:
                raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

            return db_user
    finally:
        try:
            await db.close()
        except Exception as e:
                print(f"Error occurred while closing AsyncSession: {e}")


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await db.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    await db.delete(db_user)
    await db.commit()
    return {"message": "Utilisateur supprimé avec succès"}

@app.delete("/users")
async def delete_all_users(db: AsyncSession = Depends(get_db)):
    try:
        # Get all users from the database
        users = await db.execute(User.__table__.delete())

        # Commit the deletion operation
        await db.commit()

        # Return success message
        return {"message": f"All {users.rowcount} users deleted successfully"}

    except Exception as e:
        # Rollback changes if an error occurs
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserSchema, db: AsyncSession = Depends(get_db)):
    db_user = await db.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    db_user.username = user.username
    db_user.email = user.email
    await db.commit()
    await db.refresh(db_user)
    return db_user
