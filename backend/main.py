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
        cpu_usage = {}
        stats_dict = {}
        for line in lines :
            if line.startswith("cpu") and not line.startswith("cpu0") and not line.startswith("cpu1"):
                parts = line.split()
                cpu_usage["cpu"] = parts[0]
                cpu_usage["user"] = int(parts[1])
                cpu_usage["nice"] = int(parts[2])
                cpu_usage["system"] = int(parts[3])
                cpu_usage["idle"] = int(parts[4])
                cpu_usage["iowait"] = int(parts[5])
                cpu_usage["irq"] = int(parts[6])
                cpu_usage["softirq"] = int(parts[7])
                cpu_usage["steal"] = int(parts[8])
                cpu_usage["guest"] = int(parts[9])
                cpu_usage["guest_nice"] = int(parts[10])
                usage = ((cpu_usage["user"] + cpu_usage["system"]) / (cpu_usage["user"] + cpu_usage["nice"] + cpu_usage["system"] + cpu_usage["idle"] + cpu_usage["iowait"] + cpu_usage["irq"] + cpu_usage["softirq"] + cpu_usage["steal"]))
                stats_dict["cpu usage"] = str(round(usage, 5)*100)
                break
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
            device = parts[2]
            if device.startswith("sda") :
                stats_dict["reads"] = parts[3]
                stats_dict["writes"] = parts[7]
                stats_dict["I/Os "] = parts[11]
        return stats_dict

class Memory(BaseModel):
    memory_stats: Dict[str, Any]

    def parse(self, stats):
        lines = stats.split("\n")
        stats_dict = {}
        for line in lines:
            parts = line.split()
            if line.startswith("MemFree") :
                entry = parts[1]
                stats_dict["MemFree"] = entry
        return stats_dict

class Scheduler(BaseModel):
    scheduler_stats: Dict[str, Any]

    def parse(self, stats):
        lines = stats.split("\n")
        stats_dict = {}
        for line in lines:
            if line.startswith("cpu") :
                parts = line.split()
                stats_dict["cpu_runtime"] = parts[7]
                stats_dict["cpu_waittime"] = parts[8]
        return stats_dict

class Load(BaseModel):
    load_stats: Dict[str, Any]

    def parse(self, stats):
        stats_dict = {}
        parts = stats.split(" ")
        stats_dict["one"] = parts[0]
        stats_dict["five"] = parts[1]
        stats_dict["fifteen"] = parts[2]
        return stats_dict

app = FastAPI()

origins = [
    "http://localhost:5174",
    "localhost:5174"
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
    parsed_stats = memory.parse(meminfo)
    return {"memory_stats":parsed_stats}

@app.get("/scheduler")
async def read_scheduler():
    with open("/proc/schedstat", "r") as file :
        schedstat = file.read()
    scheduler = Scheduler(scheduler_stats={})
    parsed_stats = scheduler.parse(schedstat)
    return {"scheduler_stats": parsed_stats}

@app.get("/load")
async def read_load():
    with open("/proc/loadavg", "r") as file :
        loadavg = file.read()
    load = Load(load_stats={})
    parsed_stats = load.parse(loadavg)
    return {"load_stats": parsed_stats}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)