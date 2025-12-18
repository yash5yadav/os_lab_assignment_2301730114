import os
import subprocess
import time
import sys

# Task 1: Create N child processes
def task1_create_children(n):
    print(f"Creating {n} child processes...")
    children = []
    for i in range(n):
        pid = os.fork()
        if pid == 0:
            # Child process
            print(f"Child {i}: PID={os.getpid()}, PPID={os.getppid()}, Custom Message: Hello from child {i}")
            os._exit(0)
        else:
            # Parent process
            children.append(pid)
            print(f"Parent created child {pid}")

    # Parent waits for children
    for _ in range(len(children)):
        os.wait()
    print("All children finished.\n")

# Task 2: Each child executes a Linux command
def task2_exec_children(n, cmd):
    print(f"Creating {n} children to execute command: {cmd}")
    children = []
    for i in range(n):
        pid = os.fork()
        if pid == 0:
            # Child process runs command
            print(f"Child {i}: running command '{cmd}'")
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                print(f"Output from child {i}:\n{result.stdout}")
                if result.stderr:
                    print(f"Errors from child {i}:\n{result.stderr}")
            except Exception as e:
                print(f"Error executing command: {e}")
            os._exit(0)
        else:
            children.append(pid)
            print(f"Parent created child {pid} for Task 2")

    # Parent waits
    for _ in range(len(children)):
        os.wait()
    print("All children finished (Task 2).\n")

# Task 3a: Zombie Process
def task3_zombie():
    print("Creating zombie process...")
    pid = os.fork()
    if pid == 0:
        print(f"[Zombie Demo] Child PID={os.getpid()} exiting now")
        os._exit(0)
    else:
        print(f"[Zombie Demo] Parent PID={os.getpid()} created child {pid}")
        print("[Zombie Demo] Child should become zombie for ~10 seconds...")
        print("👉 Open another terminal and run: ps -el | grep defunct")
        print("👉 Or run: ps aux | grep Z")
        time.sleep(10)
        os.wait()
        print("[Zombie Demo] Parent has reaped child, zombie cleared.\n")

# Task 3b: Orphan Process
def task3_orphan():
    print("Creating orphan process...")
    pid = os.fork()
    if pid == 0:
        print(f"[Orphan Demo] Child PID={os.getpid()}, PPID={os.getppid()} - sleeping for 5 seconds")
        time.sleep(5)
        print(f"[Orphan Demo] Child PID={os.getpid()} woke up, new PPID={os.getppid()} (should be 1 - init)")
        os._exit(0)
    else:
        print(f"[Orphan Demo] Parent PID={os.getpid()} created child {pid}, exiting immediately")
        os._exit(0)

# Task 4: Inspect Process Info from /proc
def task4_inspect_proc(pid=None):
    if pid is None:
        pid = os.getpid()
    
    print(f"Inspecting process {pid} from /proc filesystem...")
    
    try:
        # Check if /proc exists
        if not os.path.exists('/proc'):
            print("/proc filesystem not available")
            return
        
        # Read process status
        status_path = f"/proc/{pid}/status"
        if os.path.exists(status_path):
            print(f"\n=== Process {pid} Status ===")
            with open(status_path, 'r') as f:
                for line in f:
                    if any(key in line for key in ['Name', 'State', 'VmRSS', 'VmSize']):
                        print(line.strip())
        else:
            print(f"Process {pid} does not exist")
            return
        
        # Read executable path
        exe_path = f"/proc/{pid}/exe"
        if os.path.exists(exe_path):
            try:
                real_path = os.readlink(exe_path)
                print(f"\nExecutable path: {real_path}")
            except OSError:
                print("\nExecutable path: [Permission denied]")
        
        # Read file descriptors
        fd_dir = f"/proc/{pid}/fd"
        if os.path.exists(fd_dir):
            try:
                fds = os.listdir(fd_dir)
                print(f"\nOpen file descriptors: {len(fds)} files")
                # Show first few for brevity
                for fd in sorted(fds)[:5]:
                    fd_path = f"{fd_dir}/{fd}"
                    try:
                        target = os.readlink(fd_path)
                        print(f"  {fd} -> {target}")
                    except OSError:
                        print(f"  {fd} -> [Permission denied]")
                if len(fds) > 5:
                    print(f"  ... and {len(fds) - 5} more")
            except PermissionError:
                print("\nFile descriptors: [Permission denied]")
                
    except Exception as e:
        print(f"Error reading /proc info: {e}")
    
    print()

# Task 5: Process Prioritization with nice values
def task5_priority_demo():
    print("Demonstrating process prioritization with nice values...")
    
    children = []
    nice_values = [0, 10, 19]  # Different nice values (0=normal, 19=lowest priority)
    
    for i, nice_val in enumerate(nice_values):
        pid = os.fork()
        if pid == 0:
            # Child process - set nice value and do CPU-intensive work
            try:
                os.nice(nice_val)
                actual_nice = os.nice(0)  # Get current nice value
                print(f"Child {i} with nice value {actual_nice} starting CPU work")
                
                # CPU-intensive task (calculate primes)
                start_time = time.time()
                primes = []
                num = 2
                while time.time() - start_time < 3:  # Run for 3 seconds
                    is_prime = True
                    for prime in primes:
                        if prime * prime > num:
                            break
                        if num % prime == 0:
                            is_prime = False
                            break
                    if is_prime:
                        primes.append(num)
                    num += 1
                
                print(f"Child {i} with nice {actual_nice} found {len(primes)} primes in 3 seconds")
            except Exception as e:
                print(f"Error in child {i}: {e}")
            os._exit(0)
        else:
            children.append(pid)
            print(f"Created child {pid} with target nice value {nice_val}")
    
    # Parent waits for all children
    for _ in children:
        os.wait()
    print("All priority demo children finished\n")

def main():
    print("=" * 50)
    print("Process Management Demonstration")
    print("=" * 50)
    
    # Task 1
    print("TASK 1: Process Creation Utility")
    task1_create_children(3)
    
    # Task 2
    print("TASK 2: Command Execution Using exec()")
    task2_exec_children(2, "date")
    task2_exec_children(2, "ls -la")
    
    # Task 3
    print("TASK 3: Zombie & Orphan Processes")
    task3_zombie()
    
    # For orphan, we need to handle the parent exit
    orphan_pid = os.fork()
    if orphan_pid == 0:
        # This is the orphan demo process
        task3_orphan()
        sys.exit(0)
    else:
        # Wait a bit for orphan to finish
        time.sleep(8)
    
    # Task 4
    print("TASK 4: Inspecting Process Info from /proc")
    task4_inspect_proc(os.getpid())  # Inspect current process
    task4_inspect_proc(1)           # Try to inspect init process (usually pid 1)
    
    # Task 5
    print("TASK 5: Process Prioritization")
    task5_priority_demo()
    
    print("All tasks completed!")

if __name__ == "__main__":
    main()
