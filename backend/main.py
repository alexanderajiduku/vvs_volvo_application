import logging.config
from fastapi import FastAPI 
from app.database.database import get_db
from api.v1.api import api_router  
from app.core.cors import setup_cors
from fastapi.staticfiles import StaticFiles


def create_application() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router, prefix="/api/v1")
    setup_cors(app)
    
    UPLOAD_DIR = "annotated_results"
    app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

    return app


app = create_application()


@app.get("/")
async def home():
    return {"message": "Welcome to the home page!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
