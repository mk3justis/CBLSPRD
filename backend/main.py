import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any
# from typing import List

# In case I forget...
# To run the server: uvicorn main:app --reload

class CPU(BaseModel):
    stats: Dict[str, Any]

    def parse(self, stats) :
        lines = stats.split("\n")
        stats_dict = {}
        for line in lines :
            if line.startswith("cpu") :
                parts = line.split()
                cpu_num = parts[0]
                cpu_data = parts[1:]
                stats_dict[cpu_num] = cpu_data
            elif line.startswith("ctxt") :
                stats_dict["context_switches"] = line.split()[1:]
            elif line.startswith("procs_running") :
                stats_dict["procs_running"] = line.split()[1:]
            elif line.startswith("softirq") :
                stats_dict["softirq"] = line.split()[1:]
        return stats_dict


class IO(BaseModel):
    stats: str

class Stat(BaseModel):
    stats: str

class Memory(BaseModel):
    stats: str

class Scheduler(BaseModel):
    stats: str

class Load(BaseModel):
    stats: str

app = FastAPI()

origins = [
    "http://localhost:5176",
    "localhost:5176"
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
    with open("/proc/stat", "r") as file :
        stats = file.read()
    cpu = CPU(stats={})
    parsed_stats = cpu.parse(stats)
    return {"stats":parsed_stats}

@app.get("/io", response_model=IO)
async def read_io():
    with open("/proc/diskstats", "r") as file :
        diskstats = file.read()
    return IO(stats=diskstats)

@app.get("/stat")
async def read_stat():
    with open("/proc/stat", "r") as file :
        stat = file.read()
    return Stat(stats=stat)

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

@app.get("/load")
async def read_load():
    with open("/proc/loadavg", "r") as file :
        loadavg = file.read()
    return Load(stats=loadavg)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)