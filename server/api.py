from fastapi import FastAPI, Body # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from pydantic import BaseModel



app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageRequest(BaseModel):
    data: str  # Expect the `data` field as a string


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/image")
def image(request: ImageRequest):
    data = request.data 
    return {"message": "Image received successfully", "data_echo": data}