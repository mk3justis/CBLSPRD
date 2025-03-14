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

class Filesystem(BaseModel):
    stats: str

class Memory(BaseModel):
    stats: str

class Scheduler(BaseModel):
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

statistics = {
    "cpu": "/proc/cpuinfo",
    "io": "/proc/diskstats",
    "filesystem": "/proc/mounts",
    "memory": "/proc/meminfo",
    "scheduler": "/proc/schedstat"
}

class Home(BaseModel):
    greeting: str

@app.get("/test")
async def testing():
    return {"message": "Server is working!"}

@app.get("/home")
async def read_root():
    return Home(greeting="Hello world!")

@app.get("/cpu", response_model=CPU)
async def read_cpu():
    with open("/proc/cpuinfo", "r") as file :
        cpu_info = file.read()
    # return CPU(stats=cpu_info)
    return CPU(stats="hiya")

@app.get("/io", response_model=IO)
async def read_io():
    with open("/proc/diskstats", "r") as file :
        diskstats = file.read()
    return IO(stats=diskstats)

@app.get("/filesystem")
async def read_filesystem():
    with open("/proc/mounts", "r") as file :
        mounts = file.read()
    return Filesystem(stats=mounts)

@app.get("/memory")
async def read_memory():
    with open("/proc/meminfo", "r") as file :
        meminfo = file.read()
    return Memory(stats=meminfo)

@app.get("/scheduler")
async def read_scheduler():
    with open("/proc/schedstat", "r") as file :
        schedstat = file.read()
    return Scheduler(stats=schedstat)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)