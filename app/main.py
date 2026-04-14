from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import redis
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI(title="Talha's CI/CD Project")


def get_db_connection():
    try:
        conn = psycopg2.connect(
            os.getenv(
                "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/test_db"
            )
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


def get_redis_connection():
    try:
        r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        return r
    except Exception as e:
        print(f"Redis connection error: {e}")
        return None


@app.get("/")
async def root():
    return {
        "message": "You're looking at Talha's CI/CD project. The app is live and running."
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/ready")
async def readiness_check():
    db_status = "connected" if get_db_connection() else "disconnected"
    redis_status = "connected" if get_redis_connection() else "disconnected"

    return {
        "status": (
            "ready"
            if db_status == "connected" and redis_status == "connected"
            else "not_ready"
        ),
        "database": db_status,
        "redis": redis_status,
    }


@app.get("/metrics")
async def metrics():
    try:
        redis_conn = get_redis_connection()
        visits = redis_conn.incr("visits") if redis_conn else 0
    except Exception:
        visits = 0

    return {"visits": visits, "status": "ok"}


class User(BaseModel):
    name: str
    email: str


@app.post("/users")
async def create_user(user: User):
    conn = get_db_connection()
    if not conn:
        return JSONResponse(status_code=503, content={"error": "Database unavailable"})

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id, name, email, created_at",
                (user.name, user.email),
            )
            result = cur.fetchone()
            conn.commit()
            return {"user": dict(result)}
    except Exception as e:
        conn.rollback()
        return JSONResponse(
            status_code=500, content={"error": f"Failed to create user: {str(e)}"}
        )
    finally:
        conn.close()


@app.get("/users")
async def get_users():
    conn = get_db_connection()
    if not conn:
        return JSONResponse(status_code=503, content={"error": "Database unavailable"})

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, name, email, created_at FROM users ORDER BY created_at DESC"
            )
            users = cur.fetchall()
            return {"users": [dict(u) for u in users]}
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"error": f"Failed to fetch users: {str(e)}"}
        )
    finally:
        conn.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
