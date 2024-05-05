from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from db import get_session, engine
from models import User, UserSchema, Base
import redis
import json
import logging 
logger = logging.getLogger(__name__)

from functools import wraps
import tracemalloc
tracemalloc.start()


app = FastAPI()

async def get_db():
    db = get_session()
    try:
        yield db
    finally:
        await db.close()
        
# ------------------------------------------
#           Connexion Redis
# ------------------------------------------

redis = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/users/cache/{user_id}")
def get_user_with_cache(user_id: int, db: Session = Depends(get_db)):
    try:
        cached_data = redis.get(f"user:{user_id}")
        if cached_data is not None:
            cached_data_str = cached_data.decode('utf-8')
            cached_data_json = cached_data_str.replace("'", '"')
            try:
                return json.loads(cached_data_json)
            except json.JSONDecodeError as e:
                cached_data = None

        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

        user_data = {"id": db_user.id, "username": db_user.username, "email": db_user.email}
        redis.set(f"user:{user_id}", json.dumps(user_data), ex=60)

        return user_data

    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")



# ------------------------------------------
#             API routes
# ------------------------------------------

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
    
    await redis.delete(f"/users/{user_id}")
    
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
    
    await redis.delete(f"/users/{user_id}")
    
    return db_user
