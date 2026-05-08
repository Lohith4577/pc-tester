import psutil
import platform
import time
import math
from datetime import datetime

print("="*60)
print("PC TESTER - System Information & Benchmark")
print("="*60)
print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# OS Info
def get_os_info():
    return {
        'OS': platform.system() + ' ' + platform.release(),
        'Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor()
    }

# CPU Info
def get_cpu_info():
    cpu = {
        'Physical cores': psutil.cpu_count(logical=False),
        'Total cores': psutil.cpu_count(logical=True),
        'Max Frequency': f"{psutil.cpu_freq().max:.2f} MHz" if psutil.cpu_freq() else 'N/A',
        'Current Frequency': f"{psutil.cpu_freq().current:.2f} MHz" if psutil.cpu_freq() else 'N/A',
        'CPU Usage': f"{psutil.cpu_percent(interval=1)}%"
    }
    return cpu

# Memory Info
def get_memory_info():
    mem = psutil.virtual_memory()
    return {
        'Total RAM': f"{mem.total / (1024**3):.2f} GB",
        'Available RAM': f"{mem.available / (1024**3):.2f} GB",
        'Used RAM': f"{mem.used / (1024**3):.2f} GB",
        'Usage %': f"{mem.percent}%"
    }

# Disk Info
def get_disk_info():
    disks = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disks.append({
                'Device': partition.device,
                'Mountpoint': partition.mountpoint,
                'Total': f"{usage.total / (1024**3):.2f} GB",
                'Free': f"{usage.free / (1024**3):.2f} GB",
                'Used': f"{usage.used / (1024**3):.2f} GB",
                'Usage %': f"{usage.percent}%"
            })
        except:
            pass
    return disks

# Simple CPU Benchmark
def cpu_benchmark():
    print("Running CPU benchmark (Pi calculation)...")
    start = time.time()
    x = 0
    for i in range(1, 5000000):
        x += math.sin(i) * math.cos(i)
    end = time.time()
    duration = end - start
    score = int(1000 / (duration + 0.1))
    return duration, score

# Memory Benchmark
def memory_benchmark():
    print("Running Memory benchmark...")
    start = time.time()
    data = [i * i for i in range(10_000_000)]
    del data
    end = time.time()
    duration = end - start
    return duration

print("Fetching system information...\n")

os_info = get_os_info()
cpu_info = get_cpu_info()
mem_info = get_memory_info()
disks = get_disk_info()

print("Operating System:")
for k, v in os_info.items():
    print(f"  {k}: {v}")
print()

print("CPU:")
for k, v in cpu_info.items():
    print(f"  {k}: {v}")
print()

print("Memory:")
for k, v in mem_info.items():
    print(f"  {k}: {v}")
print()

print("Disks:")
for disk in disks:
    print(f"  Device: {disk['Device']} ({disk['Mountpoint']})")
    print(f"    Total: {disk['Total']} | Free: {disk['Free']} | Usage: {disk['Usage %']}")
    print()

# Benchmarks
cpu_time, cpu_score = cpu_benchmark()
mem_time = memory_benchmark()

print("\nBenchmarks:")
print(f"CPU Benchmark time: {cpu_time:.2f} seconds")
print(f"Memory Benchmark time: {mem_time:.2f} seconds")
print(f"\nOverall Performance Score: {cpu_score}/1000")
print("(Higher is better - rough estimate)")

print("\n" + "="*60)
print("Test completed!")
print("="*60)