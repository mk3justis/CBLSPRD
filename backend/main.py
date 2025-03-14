import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from typing import List

# In case I forget...
# To run the server: uvicorn main:app --reload

class CPU(BaseModel):
    stats: str

class IO(BaseModel):
    stats: str

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace /proc filepaths with real filepaths
# I will need to read in from proc somehow
statistics = {
    "cpu": "/proc/cpu",
    "io": "/proc/io",
    "filesystem": "/proc/filesystem",
    "memory": "/proc/memoryj",
    "scheduler": "/proc/scheduler"
}

@app.get("/home")
async def read_root():
    return {"Hello": "World"}

@app.get("/cpu", response_model=CPU)
async def read_cpu():
    return CPU(stats=statistics["cpu"])

@app.get("/io")
async def read_cpu():
    return {}

@app.get("/filesystem")
async def read_cpu():
    return {}

@app.get("/memory")
async def read_cpu():
    return {}

@app.get("/scheduler")
async def read_cpu():
    return {}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)