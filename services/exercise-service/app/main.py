from fastapi import FastAPI

from app.routes import router

app = FastAPI(title="Workout Exercise Catalog API")
app.include_router(router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Workout Exercise Catalog API"}
