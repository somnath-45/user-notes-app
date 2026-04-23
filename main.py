from fastapi import FastAPI, Request, status
from Api import UserApi, NotesApi
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from Model.Models import Base
from Core.db import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    friendly_exception = []

    for error in exc.errors():
        where_is_it = " -> ".join(str(loc) for loc in error["loc"])
        what_is_it = error["msg"]

        friendly_exception.append({"field": where_is_it, "message": what_is_it})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"validation_error": friendly_exception},
    )


app.include_router(UserApi.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(NotesApi.router, prefix="/api/v1/notes", tags=["Notes"])


origins= {"http://localhost:5173" "localhost:5173"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)
