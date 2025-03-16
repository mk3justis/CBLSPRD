import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any

class CPU(BaseModel):
    cpu_stats: Dict[str, Any]

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
    io_stats: Dict[str, Any]

    def parse(self, stats):
        lines = stats.split("\n")
        stats_dict = {}
        for line in lines:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) > 2:
                device = parts[2]
                if device == 'sda' or device == 'sda1':
                    device_data = parts[3:]
                    stats_dict[device] = device_data
        return stats_dict

class Memory(BaseModel):
    memory_stats: Dict[str, Any]

class Scheduler(BaseModel):
    scheduler_stats: Dict[str, Any]

class Load(BaseModel):
    load_stats: Dict[str, Any]

app = FastAPI()

origins = [
    "http://localhost:5177",
    "localhost:5177"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    cpu = CPU(cpu_stats={})
    parsed_stats = cpu.parse(stats)
    return {"cpu_stats":parsed_stats}

@app.get("/io", response_model=IO)
async def read_io():
    with open("/proc/diskstats", "r") as file :
        diskstats = file.read()
    io = IO(io_stats={})
    parsed_stats = io.parse(diskstats)
    return {"io_stats":parsed_stats}

@app.get("/memory")
async def read_memory():
    with open("/proc/meminfo", "r") as file :
        meminfo = file.read()
    memory = Memory(memory_stats={})
    return {"memory_stats":meminfo}

@app.get("/scheduler")
async def read_scheduler():
    with open("/proc/schedstat", "r") as file :
        schedstat = file.read()
    scheduler = Scheduler(scheduler_stats={})
    return {"scheduler_stats": schedstat}

@app.get("/load")
async def read_load():
    with open("/proc/loadavg", "r") as file :
        loadavg = file.read()
    load = Load(load_stats={})
    return {"load_stats": loadavg}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)