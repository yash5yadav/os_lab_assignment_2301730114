# Task 1: Batch Processing Simulation (Python)

import subprocess
import time
import os

scripts = ['script1.py', 'script2.py', 'script3.py']

print("\n===== Batch Processing Started =====\n")

for script in scripts:
    if not os.path.exists(script):
        print(f"❌ {script} not found. Skipping...")
        continue

    print(f"▶ Executing {script} ...")
    start = time.time()

    # Run the script
    result = subprocess.call(['python3', script])

    end = time.time()
    print(f"✔ Completed {script} (Exit Code: {result}) in {end - start:.2f} seconds\n")

print("===== Batch Processing Finished =====")


# Task 2: System Startup and Logging

import multiprocessing
import logging
import time


logging.basicConfig(
    filename='system_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(message)s'
)

def process_task(name):
    """Simulates a system process."""
    logging.info(f"{name} started")
    time.sleep(2)  
    logging.info(f"{name} terminated")

if __name__ == '__main__':
    print("System Booting...")

   
    p1 = multiprocessing.Process(target=process_task, args=("Process-1",))
    p2 = multiprocessing.Process(target=process_task, args=("Process-2",))

    p1.start()
    p2.start()


    p1.join()
    p2.join()

    print("System Shutdown.")

# Task 3: System Calls and IPC (Python - fork, exec, pipe)

import os
import sys

def child_process(read_fd):
    """Child receives message from pipe and executes another program."""
    os.close(write_fd) 
    
    
    message = os.read(read_fd, 1024).decode()
    print(f"Child received: {message}")

    os.close(read_fd)

    
    print("Child executing 'ls -l' using execvp...\n")
    os.execvp("ls", ["ls", "-l"])

def parent_process(write_fd):
    """Parent sends a message and waits for child."""
    os.close(read_fd)  

    message = "Hello from parent process!"
    os.write(write_fd, message.encode())
    os.close(write_fd)

    
    os.wait()
    print("\nParent: Child process finished.")



read_fd, write_fd = os.pipe()


pid = os.fork()

if pid == 0:
    
    child_process(read_fd)

else:
    
    parent_process(write_fd)


# Task 4: VM Detection and Shell Interaction

import subprocess

def get_output(cmd):
    """Run a shell command and return its output."""
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except:
        return ""

def is_vm():
    manufacturer = get_output("cat /sys/class/dmi/id/sys_vendor")
    product_name = get_output("cat /sys/class/dmi/id/product_name")
    hypervisor = get_output("lscpu | grep 'Hypervisor vendor'")

    vm_signatures = [
        "VMware", "VirtualBox", "KVM", "QEMU", "Bochs",
        "Microsoft Corporation", "Xen", "Parallels"
    ]

    data = f"{manufacturer} {product_name} {hypervisor}"

    for sig in vm_signatures:
        if sig.lower() in data.lower():
            return True, sig

    return False, None


if __name__ == "__main__":
    detected, vm_type = is_vm()

    if detected:
        print(f"Virtual Machine Detected: {vm_type}")
    else:
        print("No Virtual Machine Detected (Physical Machine)")


# Task 5: CPU Scheduling Algorithms

def fcfs(processes):
    print("\n===== FCFS Scheduling =====")
    wt = [0] * len(processes)
    tat = [0] * len(processes)

    for i in range(1, len(processes)):
        wt[i] = wt[i-1] + processes[i-1][1]

    for i in range(len(processes)):
        tat[i] = wt[i] + processes[i][1]

    print("PID\tBT\tWT\tTAT")
    total_wt = total_tat = 0
    for i, p in enumerate(processes):
        print(f"{p[0]}\t{p[1]}\t{wt[i]}\t{tat[i]}")
        total_wt += wt[i]
        total_tat += tat[i]

    print("Average WT:", total_wt / len(processes))
    print("Average TAT:", total_tat / len(processes))




def sjf(processes):
    print("\n===== SJF (Non-Preemptive) Scheduling =====")
    processes.sort(key=lambda x: x[1])  

    wt = [0] * len(processes)
    tat = [0] * len(processes)

    for i in range(1, len(processes)):
        wt[i] = wt[i-1] + processes[i-1][1]

    for i in range(len(processes)):
        tat[i] = wt[i] + processes[i][1]

    print("PID\tBT\tWT\tTAT")
    total_wt = total_tat = 0
    for i, p in enumerate(processes):
        print(f"{p[0]}\t{p[1]}\t{wt[i]}\t{tat[i]}")
        total_wt += wt[i]
        total_tat += tat[i]

    print("Average WT:", total_wt / len(processes))
    print("Average TAT:", total_tat / len(processes))

def priority_scheduling(processes):
    print("\n===== Priority Scheduling =====")
    processes.sort(key=lambda x: x[2])  

    wt = [0] * len(processes)
    tat = [0] * len(processes)

    for i in range(1, len(processes)):
        wt[i] = wt[i-1] + processes[i-1][1]

    for i in range(len(processes)):
        tat[i] = wt[i] + processes[i][1]

    print("PID\tBT\tPriority\tWT\tTAT")
    total_wt = total_tat = 0
    for i, p in enumerate(processes):
        print(f"{p[0]}\t{p[1]}\t{p[2]}\t\t{wt[i]}\t{tat[i]}")
        total_wt += wt[i]
        total_tat += tat[i]

    print("Average WT:", total_wt / len(processes))
    print("Average TAT:", total_tat / len(processes))

def round_robin(processes, quantum):
    print("\n===== Round Robin Scheduling =====")

    remaining_bt = [p[1] for p in processes]
    wt = [0] * len(processes)
    tat = [0] * len(processes)
    time = 0

    while True:
        done = True
        for i in range(len(processes)):
            if remaining_bt[i] > 0:
                done = False

                if remaining_bt[i] > quantum:
                    time += quantum
                    remaining_bt[i] -= quantum
                else:
                    time += remaining_bt[i]
                    wt[i] = time - processes[i][1]
                    remaining_bt[i] = 0

        if done:
            break

    for i in range(len(processes)):
        tat[i] = wt[i] + processes[i][1]

    print("PID\tBT\tWT\tTAT")
    total_wt = total_tat = 0
    for i, p in enumerate(processes):
        print(f"{p[0]}\t{p[1]}\t{wt[i]}\t{tat[i]}")
        total_wt += wt[i]
        total_tat += tat[i]

    print("Average WT:", total_wt / len(processes))
    print("Average TAT:", total_tat / len(processes))

if __name__ == "__main__":
    n = int(input("Enter number of processes: "))
    processes_fcfs = []
    processes_sjf = []
    processes_priority = []
    processes_rr = []

    for i in range(n):
        pid = i + 1
        bt = int(input(f"Enter Burst Time for P{pid}: "))
        pr = int(input(f"Enter Priority for P{pid}: "))
        processes_fcfs.append([pid, bt])
        processes_sjf.append([pid, bt])
        processes_priority.append([pid, bt, pr])
        processes_rr.append([pid, bt])

    quantum = int(input("Enter Time Quantum for RR: "))

    fcfs(processes_fcfs)
    sjf(processes_sjf)
    priority_scheduling(processes_priority)
    round_robin(processes_rr, quantum)
