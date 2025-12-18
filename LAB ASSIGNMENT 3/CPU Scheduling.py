# Task 1: CPU Scheduling with Gantt Chart

# ==========================================================
# CPU Scheduling Simulation with Priority + Round Robin
# Includes:
# - Priority Scheduling (Non-Preemptive)
# - Round Robin Scheduling
# - Gantt Chart for both algorithms
# - Average WT & TAT calculation
# ==========================================================

def print_gantt_chart(gantt):
    """Print Gantt Chart visually"""
    print("\nGantt Chart:")
    for p in gantt:
        print(f"| P{p} ", end="")
    print("|")

    print("0", end="")
    for _ in gantt:
        print("----", end="")
    print()



def priority_scheduling():
    processes = []
    n = int(input("Enter number of processes: "))

    for i in range(n):
        bt = int(input(f"Enter Burst Time for P{i+1}: "))
        pr = int(input(f"Enter Priority (lower number = higher priority) for P{i+1}: "))
        processes.append((i+1, bt, pr))

    processes.sort(key=lambda x: x[2])

    gantt = []
    wt = 0
    total_wt = 0
    total_tat = 0

    print("\nPriority Scheduling:")
    print("PID\tBT\tPriority\tWT\tTAT")

    for pid, bt, pr in processes:
        tat = wt + bt
        print(f"{pid}\t{bt}\t{pr}\t\t{wt}\t{tat}")

        total_wt += wt
        total_tat += tat
        wt += bt

       
        gantt.extend([pid] * bt)

    print_gantt_chart(gantt)

    print(f"\nAverage Waiting Time: {total_wt / n:.2f}")
    print(f"Average Turnaround Time: {total_tat / n:.2f}")



def round_robin():
    processes = []
    n = int(input("\nEnter number of processes: "))
    tq = int(input("Enter Time Quantum: "))

    for i in range(n):
        bt = int(input(f"Enter Burst Time for P{i+1}: "))
        processes.append([i+1, bt, bt])  # [PID, BT, Remaining]

    time = 0
    gantt = []
    wt = [0] * n
    tat = [0] * n

    queue = processes.copy()

    while True:
        done = True
        for p in queue:
            pid, bt, rem = p
            if rem > 0:
                done = False

                
                run_time = min(tq, rem)
                time += run_time
                p[2] -= run_time

                gantt.extend([pid] * run_time)

                if p[2] == 0:
                    tat[pid - 1] = time
                    wt[pid - 1] = tat[pid - 1] - bt

        if done:
            break

    print("\nRound Robin Scheduling:")
    print("PID\tBT\tWT\tTAT")
    for i in range(n):
        print(f"{i+1}\t{processes[i][1]}\t{wt[i]}\t{tat[i]}")

    print_gantt_chart(gantt)

    print(f"\nAverage Waiting Time: {sum(wt)/n:.2f}")
    print(f"Average Turnaround Time: {sum(tat)/n:.2f}")

print("======== CPU Scheduling Simulation (With Gantt Chart) ========")
print("1. Priority Scheduling")
print("2. Round Robin Scheduling")

choice = int(input("Enter choice: "))

if choice == 1:
    priority_scheduling()
elif choice == 2:
    round_robin()
else:
    print("Invalid option!")


# Task 2: Sequential File Allocation

total_blocks = int(input("Enter total number of blocks: "))
block_status = [0] * total_blocks   # 0 = free, 1 = allocated


n = int(input("Enter number of files: "))

for i in range(n):
    print(f"\n--- File {i+1} ---")
    start = int(input(f"Enter starting block for file {i+1}: "))
    length = int(input(f"Enter length of file {i+1}: "))

    allocated = True

    for j in range(start, start + length):
        if j >= total_blocks:       # Out of disk range
            allocated = False
            break
        if block_status[j] == 1:    # Already allocated
            allocated = False
            break

    if allocated:
        for j in range(start, start + length):
            block_status[j] = 1
        print(f"File {i+1} allocated from block {start} to {start + length - 1}")
    else:
        print(f"File {i+1} cannot be allocated.")

# Final block allocation map
print("\nFinal Block Allocation:")
for i in range(total_blocks):
    print(f"Block {i} → {'Allocated' if block_status[i] == 1 else 'Free'}")


# Task 3: Indexed File Allocation

total_blocks = int(input("Enter total number of blocks: "))
block_status = [0] * total_blocks    


n = int(input("Enter number of files: "))

for i in range(n):
    print(f"\n--- File {i+1} ---")


    index = int(input(f"Enter index block for file {i+1}: "))

    if index >= total_blocks or index < 0:
        print("Invalid index block number!")
        continue

    if block_status[index] == 1:
        print("Index block already allocated.")
        continue

    count = int(input("Enter number of data blocks: "))
    data_blocks = list(map(int, input("Enter block numbers: ").split()))

    if len(data_blocks) != count:
        print("Error: Number of data blocks does not match input count.")
        continue

    if any(blk >= total_blocks or blk < 0 for blk in data_blocks):
        print("Invalid block number(s).")
        continue

    if any(block_status[blk] == 1 for blk in data_blocks):
        print("Error: One or more data blocks already allocated.")
        continue

    block_status[index] = 1
    for blk in data_blocks:
        block_status[blk] = 1

    print(f"File {i+1} allocated successfully.")
    print(f"Index Block: {index}")
    print(f"Data Blocks: {data_blocks}")


print("\nFinal Block Allocation Status:")
for i in range(total_blocks):
    print(f"Block {i} -> {'Allocated' if block_status[i] == 1 else 'Free'}")


# Task 4: Contiguous Memory Allocation

def allocate_memory(strategy):
    print(f"\n--- {strategy.upper()} FIT MEMORY ALLOCATION ---")

    
    partitions = list(map(int, input("Enter partition sizes: ").split()))
    processes = list(map(int, input("Enter process sizes: ").split()))

    allocation = [-1] * len(processes)  

    for i, psize in enumerate(processes):
        idx = -1  

        if strategy == "first":
           
            for j, part in enumerate(partitions):
                if part >= psize:
                    idx = j
                    break

        elif strategy == "best":
         
            best = float("inf")
            for j, part in enumerate(partitions):
                if part >= psize and part < best:
                    best = part
                    idx = j

        elif strategy == "worst":
          
            worst = -1
            for j, part in enumerate(partitions):
                if part >= psize and part > worst:
                    worst = part
                    idx = j

        
        if idx != -1:
            allocation[i] = idx
            partitions[idx] -= psize  

   
    print("\nAllocation Result:")
    for i, a in enumerate(allocation):
        if a != -1:
            print(f"Process {i+1} ({processes[i]} KB) → Partition {a+1}")
        else:
            print(f"Process {i+1} ({processes[i]} KB) → Not Allocated")

    print("\nRemaining Partition Sizes:", partitions)

allocate_memory("first")
allocate_memory("best")
allocate_memory("worst")

# Task 5: MFT & MVT Memory Management

def MFT():
    print("\n===== MFT (Fixed Partition) Memory Management =====")
    
    mem_size = int(input("Enter total memory size: "))
    part_size = int(input("Enter fixed partition size: "))
    n = int(input("Enter number of processes: "))

    partitions = mem_size // part_size
    print(f"\nTotal Memory Divided into {partitions} Fixed Partitions of {part_size} KB each.")

    internal_frag = 0

    for i in range(n):
        psize = int(input(f"\nEnter size of Process {i+1}: "))

        if psize <= part_size:
            waste = part_size - psize
            internal_frag += waste
            print(f"Process {i+1} allocated. (Internal Fragmentation = {waste} KB)")
        else:
            print(f"Process {i+1} NOT allocated — too large for fixed partition.")

    print(f"\nTotal Internal Fragmentation: {internal_frag} KB")



def MVT():
    print("\n===== MVT (Variable Partition) Memory Management =====")
    
    mem_size = int(input("Enter total memory size: "))
    n = int(input("Enter number of processes: "))

    external_frag = 0

    for i in range(n):
        psize = int(input(f"\nEnter size of Process {i+1}: "))

        if psize <= mem_size:
            print(f"Process {i+1} allocated.")
            mem_size -= psize
        else:
            print(f"Process {i+1} cannot be allocated — Not enough memory.")
            external_frag = mem_size  
            break

    print(f"\nRemaining Free Memory: {mem_size} KB")
    print(f"External Fragmentation: {external_frag} KB")

print("=== MFT Simulation ===")
MFT()

print("\n=== MVT Simulation ===")
MVT()


