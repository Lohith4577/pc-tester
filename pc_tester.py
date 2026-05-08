import psutil
import platform
import socket
import time
from datetime import datetime
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

print("=== PC Tester & Benchmark Tool ===")
print(f"Run at: {datetime.now()}")
print("="*50)

# System Info
def get_system_info():
    print("\n--- System Information ---")
    print(f"OS: {platform.system()} {platform.release()} ({platform.version()})")
    print(f"Computer Name: {socket.gethostname()}")
    print(f"Processor: {platform.processor()}")
    print(f"Machine: {platform.machine()}")
    print(f"Python Version: {platform.python_version()}")

# CPU Info
def get_cpu_info():
    print("\n--- CPU Information ---")
    print(f"Physical cores: {psutil.cpu_count(logical=False)}")
    print(f"Total cores: {psutil.cpu_count(logical=True)}")
    print(f"CPU Frequency: {psutil.cpu_freq().current:.2f} MHz")
    print(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")

# Memory
def get_memory_info():
    print("\n--- Memory Information ---")
    svmem = psutil.virtual_memory()
    print(f"Total: {svmem.total / (1024**3):.2f} GB")
    print(f"Available: {svmem.available / (1024**3):.2f} GB")
    print(f"Used: {svmem.used / (1024**3):.2f} GB")
    print(f"Percentage: {svmem.percent}%")

# Disk
def get_disk_info():
    print("\n--- Disk Information ---")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"Drive {partition.device} ({partition.fstype}): {usage.total / (1024**3):.2f} GB total, {usage.free / (1024**3):.2f} GB free")
        except:
            pass

# GPU
def get_gpu_info():
    print("\n--- GPU Information ---")
    if not GPU_AVAILABLE:
        print("GPUtil not installed. Install with: pip install gputil")
        return
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            for i, gpu in enumerate(gpus):
                print(f"GPU {i}: {gpu.name}")
                print(f"  Memory Total: {gpu.memoryTotal} MB")
                print(f"  Memory Used: {gpu.memoryUsed} MB")
                print(f"  Load: {gpu.load * 100:.1f}%")
        else:
            print("No NVIDIA GPU detected.")
    except:
        print("Error getting GPU info.")

# Simple Benchmarks
def run_benchmarks():
    print("\n--- Running Simple Benchmarks ---")
    # CPU Benchmark - Pi calculation
    print("CPU Benchmark (Pi calculation)...")
    start = time.time()
    def calculate_pi(n):
        pi = 0.0
        for k in range(n):
            pi += 4 * ((-1)**k) / (2*k + 1)
        return pi
    calculate_pi(1000000)
    cpu_time = time.time() - start
    print(f"Time for Pi calc: {cpu_time:.4f} seconds")
    
    # Memory benchmark
    print("Memory Benchmark (list creation)...")
    start = time.time()
    big_list = [i**2 for i in range(10**6)]
    mem_time = time.time() - start
    print(f"Time for 1M list: {mem_time:.4f} seconds")
    
    score = int(1000 / (cpu_time + mem_time + 0.1))
    print(f"\nApproximate Performance Score: {score} (higher is better)")

get_system_info()
get_cpu_info()
get_memory_info()
get_disk_info()
get_gpu_info()
run_benchmarks()
print("\nTest complete!")