from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.routes import auth, tags, photo, users
import os
from pathlib import Path
from dependencies import get_redis_client
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
<<<<<<< HEAD
from src.repository.cloudinary_tr import apply_transformation 
=======
import uvicorn
>>>>>>> ace5f721a994fac01726a5d5a8d720d7f1d42078

app = FastAPI()
app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)


app.include_router(auth.router, prefix="/api")
app.include_router(tags.router, prefix="/api")
app.include_router(photo.router, prefix="/api")
app.include_router(users.router, prefix="/api")

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """
    Initialize FastAPI requests limiter
    """
    await FastAPILimiter.init(get_redis_client())


@app.get("/")
def read_root():
    """
    root level endpoint

    :return: Hello world message.
    :rtype: dict
    """

    return {"message": "Hello world"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Endpoint to serve the favicon.

    :return: The favicon file.
    :rtype: FileResponse
    """
    file_name = "favicon.png"
    file_path = os.path.join(app.root_path, "static", file_name)
    return FileResponse(
        path=file_path,
        headers={"Content-Disposition": "attachment; filename=" + file_name},
    )

<<<<<<< HEAD
@app.get("/apply_transformation")  
async def apply_transformation_endpoint(photo_id: int, transformation_choice: int):
    if transformation_choice == 1:
        transformation = {"width": 300, "height": 200}
    elif transformation_choice == 2:
        transformation = {"crop": "fill"}
    elif transformation_choice == 3:
        transformation = {"effect": "grayscale"}
    elif transformation_choice == 4:
        transformation = {"angle": 90}
    elif transformation_choice == 5:
        transformation = {"blur": 500}
    else:
        return {"message": "Niepoprawny numer transformacji."}

    with get_db_session() as db_session:
        transformed_url = apply_transformation(db_session, photo_id, transformation)
        if transformed_url:
            return {"message": "Zdjęcie po zastosowaniu transformacji:", "transformed_url": transformed_url}
        else:
            return {"message": "Nie znaleziono zdjęcia o podanym ID."}
=======

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
>>>>>>> ace5f721a994fac01726a5d5a8d720d7f1d42078
