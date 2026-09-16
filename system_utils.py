"""
System Utilities Module

This module provides comprehensive system and OS utilities including:
- System information gathering
- File and directory operations
- Process management
- Environment variable handling
- System monitoring
- Network system utilities
- User and group management
- System resource monitoring
- Cross-platform compatibility
- System performance utilities

All functions include comprehensive docstrings and type hints.
"""

import os
import sys
import platform
import subprocess
import shutil
import time
import tempfile
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


@dataclass
class SystemInfo:
    """Container for system information."""
    system: str
    node_name: str
    release: str
    version: str
    machine: str
    processor: str
    python_version: str
    python_implementation: str


@dataclass
class ProcessInfo:
    """Container for process information."""
    pid: int
    name: str
    status: str
    cpu_percent: float
    memory_percent: float
    create_time: float
    num_threads: int


@dataclass
class DiskUsage:
    """Container for disk usage information."""
    total: int
    used: int
    free: int
    percent: float


@dataclass
class NetworkInfo:
    """Container for network information."""
    bytes_sent: int
    bytes_recv: int
    packets_sent: int
    packets_recv: int


class SystemInformation:
    """System information gathering utilities."""
    
    @staticmethod
    get_system_info() -> SystemInfo:
        """Get comprehensive system information."""
        return SystemInfo(
            system=platform.system(),
            node_name=platform.node(),
            release=platform.release(),
            version=platform.version(),
            machine=platform.machine(),
            processor=platform.processor(),
            python_version=platform.python_version(),
            python_implementation=platform.python_implementation()
        )
    
    @staticmethod
    get_platform_details() -> Dict[str, str]:
        """Get detailed platform information."""
        return {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": sys.version,
            "python_executable": sys.executable,
            "platform": platform.platform(),
            "architecture": platform.architecture()
        }
    
    @staticmethod
    get_environment_variables() -> Dict[str, str]:
        """Get all environment variables."""
        return dict(os.environ)
    
    @staticmethod
    get_environment_variable(key: str, default: Optional[str] = None) -> Optional[str]:
        """Get specific environment variable."""
        return os.environ.get(key, default)
    
    @staticmethod
    set_environment_variable(key: str, value: str) -> None:
        """Set environment variable."""
        os.environ[key] = value
    
    @staticmethod
    get_python_path() -> List[str]:
        """Get Python sys.path."""
        return sys.path
    
    @staticmethod
    get_current_working_directory() -> str:
        """Get current working directory."""
        return os.getcwd()
    
    @staticmethod
    get_home_directory() -> str:
        """Get user home directory."""
        return os.path.expanduser("~")
    
    @staticmethod
    get_temp_directory() -> str:
        """Get system temporary directory."""
        return tempfile.gettempdir() if 'tempfile' in sys.modules else "/tmp"
    
    @staticmethod
    is_admin() -> bool:
        """Check if running with admin/root privileges."""
        try:
            if platform.system() == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except:
            return False


class ProcessManager:
    """Process management utilities."""
    
    @staticmethod
    def get_current_process_id() -> int:
        """Get current process ID."""
        return os.getpid()
    
    @staticmethod
    def get_parent_process_id() -> int:
        """Get parent process ID."""
        return os.getppid()
    
    @staticmethod
    def get_process_info(pid: int) -> Optional[ProcessInfo]:
        """Get information about a specific process."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        
        try:
            process = psutil.Process(pid)
            return ProcessInfo(
                pid=process.pid,
                name=process.name(),
                status=process.status(),
                cpu_percent=process.cpu_percent(),
                memory_percent=process.memory_percent(),
                create_time=process.create_time(),
                num_threads=process.num_threads()
            )
        except psutil.NoSuchProcess:
            return None
    
    @staticmethod
    def get_all_processes() -> List[ProcessInfo]:
        """Get information about all running processes."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 
                                        'memory_percent', 'create_time', 'num_threads']):
            try:
                processes.append(ProcessInfo(
                    pid=proc.info['pid'],
                    name=proc.info['name'],
                    status=proc.info['status'],
                    cpu_percent=proc.info['cpu_percent'] or 0,
                    memory_percent=proc.info['memory_percent'] or 0,
                    create_time=proc.info['create_time'] or 0,
                    num_threads=proc.info['num_threads'] or 0
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return processes
    
    @staticmethod
    def kill_process(pid: int) -> bool:
        """Kill a process by PID."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        
        try:
            process = psutil.Process(pid)
            process.kill()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    
    @staticmethod
    def terminate_process(pid: int) -> bool:
        """Terminate a process by PID."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        
        try:
            process = psutil.Process(pid)
            process.terminate()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    
    @staticmethod
    def run_command(command: str, 
                   capture_output: bool = True,
                   shell: bool = True,
                   timeout: Optional[int] = None) -> Tuple[int, str, str]:
        """Run a system command."""
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=capture_output,
                text=True,
                timeout=timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)
    
    @staticmethod
    def run_command_async(command: str, 
                         shell: bool = True) -> subprocess.Popen:
        """Run a command asynchronously."""
        return subprocess.Popen(command, shell=True)


class SystemMonitor:
    """System monitoring utilities."""
    
    @staticmethod
    def get_cpu_usage(interval: float = 1.0) -> float:
        """Get current CPU usage percentage."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        return psutil.cpu_percent(interval=interval)
    
    @staticmethod
    def get_cpu_usage_per_cpu() -> List[float]:
        """Get CPU usage per core."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        return psutil.cpu_percent(interval=1.0, percpu=True)
    
    @staticmethod
    def get_cpu_count() -> int:
        """Get number of CPU cores."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        return psutil.cpu_count()
    
    @staticmethod
    def get_memory_usage() -> Dict[str, float]:
        """Get memory usage information."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "free": mem.free,
            "percent": mem.percent
        }
    
    @staticmethod
    def get_swap_usage() -> Dict[str, float]:
        """Get swap memory usage."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        
        swap = psutil.swap_memory()
        return {
            "total": swap.total,
            "used": swap.used,
            "free": swap.free,
            "percent": swap.percent
        }
    
    @staticmethod
    def get_disk_usage(path: str = "/") -> DiskUsage:
        """Get disk usage for specified path."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        
        usage = psutil.disk_usage(path)
        return DiskUsage(
            total=usage.total,
            used=usage.used,
            free=usage.free,
            percent=usage.percent
        )
    
    @staticmethod
    def get_disk_partitions() -> List[Dict[str, Any]]:
        """Get all disk partitions."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        
        partitions = []
        for partition in psutil.disk_partitions():
            partitions.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "opts": partition.opts
            })
        return partitions
    
    @staticmethod
    def get_network_io_counters() -> NetworkInfo:
        """Get network I/O counters."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        
        net_io = psutil.net_io_counters()
        return NetworkInfo(
            bytes_sent=net_io.bytes_sent,
            bytes_recv=net_io.bytes_recv,
            packets_sent=net_io.packets_sent,
            packets_recv=net_io.packets_recv
        )
    
    @staticmethod
    def get_boot_time() -> float:
        """Get system boot time."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        return psutil.boot_time()
    
    @staticmethod
    def get_uptime() -> float:
        """Get system uptime in seconds."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        return time.time() - psutil.boot_time()


class FileSystem:
    """File system operations."""
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes."""
        return os.path.getsize(file_path)
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """Get comprehensive file information."""
        stat = os.stat(file_path)
        return {
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "accessed": stat.st_atime,
            "mode": stat.st_mode,
            "inode": stat.st_ino,
            "device": stat.st_dev,
            "nlinks": stat.st_nlink
        }
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if file exists."""
        return os.path.isfile(file_path)
    
    @staticmethod
    def directory_exists(dir_path: str) -> bool:
        """Check if directory exists."""
        return os.path.isdir(dir_path)
    
    @staticmethod
    def create_directory(dir_path: str, parents: bool = False) -> bool:
        """Create directory."""
        try:
            if parents:
                os.makedirs(dir_path, exist_ok=True)
            else:
                os.mkdir(dir_path)
            return True
        except OSError:
            return False
    
    @staticmethod
    def delete_directory(dir_path: str) -> bool:
        """Delete directory."""
        try:
            shutil.rmtree(dir_path)
            return True
        except OSError:
            return False
    
    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """Copy file."""
        try:
            shutil.copy2(source, destination)
            return True
        except OSError:
            return False
    
    @staticmethod
    def move_file(source: str, destination: str) -> bool:
        """Move file."""
        try:
            shutil.move(source, destination)
            return True
        except OSError:
            return False
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Delete file."""
        try:
            os.remove(file_path)
            return True
        except OSError:
            return False
    
    @staticmethod
    def list_directory(dir_path: str, 
                     include_hidden: bool = False) -> List[str]:
        """List contents of directory."""
        items = os.listdir(dir_path)
        
        if not include_hidden:
            items = [item for item in items if not item.startswith('.')]
        
        return items
    
    @staticmethod
    def list_files(dir_path: str, 
                  pattern: str = "*",
                  recursive: bool = False) -> List[str]:
        """List files matching pattern."""
        from glob import glob
        
        if recursive:
            pattern = os.path.join(dir_path, "**", pattern)
            return glob(pattern, recursive=True)
        else:
            pattern = os.path.join(dir_path, pattern)
            return glob(pattern)
    
    @staticmethod
    def get_directory_size(dir_path: str) -> int:
        """Get total size of directory in bytes."""
        total_size = 0
        
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(file_path)
                except OSError:
                    continue
        
        return total_size
    
    @staticmethod
    def find_files_by_name(dir_path: str, 
                          name: str,
                          recursive: bool = True) -> List[str]:
        """Find files by name."""
        matches = []
        
        if recursive:
            for dirpath, dirnames, filenames in os.walk(dir_path):
                for filename in filenames:
                    if name in filename:
                        matches.append(os.path.join(dirpath, filename))
        else:
            for filename in os.listdir(dir_path):
                if name in filename:
                    matches.append(os.path.join(dir_path, filename))
        
        return matches
    
    @staticmethod
    def find_files_by_extension(dir_path: str,
                               extension: str,
                               recursive: bool = True) -> List[str]:
        """Find files by extension."""
        if not extension.startswith('.'):
            extension = '.' + extension
        
        matches = []
        
        if recursive:
            for dirpath, dirnames, filenames in os.walk(dir_path):
                for filename in filenames:
                    if filename.endswith(extension):
                        matches.append(os.path.join(dirpath, filename))
        else:
            for filename in os.listdir(dir_path):
                if filename.endswith(extension):
                    matches.append(os.path.join(dir_path, filename))
        
        return matches
    
    @staticmethod
    def create_temp_file(suffix: str = "", 
                        prefix: str = "tmp",
                        directory: Optional[str] = None) -> str:
        """Create a temporary file."""
        import tempfile
        fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=directory)
        os.close(fd)
        return path
    
    @staticmethod
    def create_temp_directory(suffix: str = "",
                             prefix: str = "tmp",
                             directory: Optional[str] = None) -> str:
        """Create a temporary directory."""
        import tempfile
        return tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=directory)


class PathUtilities:
    """Path manipulation utilities."""
    
    @staticmethod
    def join_paths(*paths: str) -> str:
        """Join path components."""
        return os.path.join(*paths)
    
    @staticmethod
    def normalize_path(path: str) -> str:
        """Normalize path."""
        return os.path.normpath(path)
    
    @staticmethod
    def absolute_path(path: str) -> str:
        """Get absolute path."""
        return os.path.abspath(path)
    
    @staticmethod
    def relative_path(path: str, start: str) -> str:
        """Get relative path."""
        return os.path.relpath(path, start)
    
    @staticmethod
    def split_path(path: str) -> Tuple[str, str]:
        """Split path into head and tail."""
        return os.path.split(path)
    
    @staticmethod
    def split_extension(path: str) -> Tuple[str, str]:
        """Split path into root and extension."""
        return os.path.splitext(path)
    
    @staticmethod
    def get_basename(path: str) -> str:
        """Get basename of path."""
        return os.path.basename(path)
    
    @staticmethod
    def get_dirname(path: str) -> str:
        """Get directory name of path."""
        return os.path.dirname(path)
    
    @staticmethod
    def expand_user(path: str) -> str:
        """Expand user home directory."""
        return os.path.expanduser(path)
    
    @staticmethod
    def expand_vars(path: str) -> str:
        """Expand environment variables."""
        return os.path.expandvars(path)


class NetworkUtilities:
    """Network-related system utilities."""
    
    @staticmethod
    def get_hostname() -> str:
        """Get system hostname."""
        return platform.node()
    
    @staticmethod
    def get_local_ip() -> Optional[str]:
        """Get local IP address."""
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return None
    
    @staticmethod
    def get_public_ip() -> Optional[str]:
        """Get public IP address."""
        try:
            import requests
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            return response.json()['ip']
        except:
            return None
    
    @staticmethod
    def check_port(host: str, port: int, timeout: float = 1.0) -> bool:
        """Check if port is open on host."""
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            s.close()
            return result == 0
        except:
            return False
    
    @staticmethod
    def ping_host(host: str, timeout: float = 2.0) -> bool:
        """Ping a host to check connectivity."""
        try:
            if platform.system() == "Windows":
                command = f"ping -n 1 -w {int(timeout * 1000)} {host}"
            else:
                command = f"ping -c 1 -W {int(timeout)} {host}"
            
            result = subprocess.run(command, shell=True, capture_output=True, timeout=timeout + 1)
            return result.returncode == 0
        except:
            return False
    
    @staticmethod
    def get_mac_address() -> Optional[str]:
        """Get MAC address of first network interface."""
        try:
            import uuid
            mac = uuid.getnode()
            return ':'.join(['{:02x}'.format((mac >> elements) & 0xff) 
                            for elements in range(0, 8*6, 8)][::-1])
        except:
            return None


class PerformanceMonitor:
    """Performance monitoring utilities."""
    
    @staticmethod
    def measure_execution_time(func: callable) -> callable:
        """Decorator to measure function execution time."""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time:.4f} seconds")
            return result
        return wrapper
    
    @staticmethod
    def memory_usage() -> Dict[str, float]:
        """Get current memory usage of Python process."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        
        process = psutil.Process()
        mem_info = process.memory_info()
        
        return {
            "rss": mem_info.rss,  # Resident Set Size
            "vms": mem_info.vms,  # Virtual Memory Size
            "percent": process.memory_percent()
        }
    
    @staticmethod
    def cpu_usage(interval: float = 1.0) -> float:
        """Get current CPU usage of Python process."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        
        process = psutil.Process()
        return process.cpu_percent(interval=interval)
    
    @staticmethod
    def thread_count() -> int:
        """Get number of threads in current process."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        
        process = psutil.Process()
        return process.num_threads()
    
    @staticmethod
    def open_files() -> List[str]:
        """Get list of open files by current process."""
        if not PSUTIL_AVAILABLE:
            raise ImportError("psutil library is required. Install with: pip install psutil")
        
        process = psutil.Process()
        return [f.path for f in process.open_files()]


class CrossPlatform:
    """Cross-platform compatibility utilities."""
    
    @staticmethod
    def is_windows() -> bool:
        """Check if running on Windows."""
        return platform.system() == "Windows"
    
    @staticmethod
    def is_linux() -> bool:
        """Check if running on Linux."""
        return platform.system() == "Linux"
    
    @staticmethod
    def is_macos() -> bool:
        """Check if running on macOS."""
        return platform.system() == "Darwin"
    
    @staticmethod
    def get_path_separator() -> str:
        """Get the path separator for current platform."""
        return os.sep
    
    @staticmethod
    def get_line_separator() -> str:
        """Get the line separator for current platform."""
        return os.linesep
    
    @staticmethod
    def get_newline() -> str:
        """Get newline character for current platform."""
        return "\r\n" if CrossPlatform.is_windows() else "\n"
    
    @staticmethod
    def open_file(file_path: str) -> bool:
        """Open file with default application."""
        try:
            if CrossPlatform.is_windows():
                os.startfile(file_path)
            elif CrossPlatform.is_macos():
                subprocess.run(["open", file_path])
            else:  # Linux
                subprocess.run(["xdg-open", file_path])
            return True
        except:
            return False
    
    @staticmethod
    def open_url(url: str) -> bool:
        """Open URL in default browser."""
        try:
            import webbrowser
            webbrowser.open(url)
            return True
        except:
            return False
    
    @staticmethod
    def clear_screen() -> None:
        """Clear terminal screen."""
        if CrossPlatform.is_windows():
            os.system('cls')
        else:
            os.system('clear')


def demonstrate_system_utils():
    """Demonstrate system utilities functionality."""
    print("=== System Utilities Demonstration ===\n")
    
    # System Information
    print("1. System Information:")
    sys_info = SystemInformation.get_system_info()
    print(f"   System: {sys_info.system}")
    print(f"   Node: {sys_info.node_name}")
    print(f"   Release: {sys_info.release}")
    print(f"   Machine: {sys_info.machine}")
    print(f"   Python: {sys_info.python_version}")
    
    # Environment
    print("\n2. Environment Variables:")
    print(f"   Home: {SystemInformation.get_home_directory()}")
    print(f"   Current dir: {SystemInformation.get_current_working_directory()}")
    print(f"   PATH: {SystemInformation.get_environment_variable('PATH', 'Not set')[:50]}...")
    
    # Process Management
    print("\n3. Process Management:")
    print(f"   Current PID: {ProcessManager.get_current_process_id()}")
    print(f"   Parent PID: {ProcessManager.get_parent_process_id()}")
    
    # System Monitoring (if psutil available)
    if PSUTIL_AVAILABLE:
        print("\n4. System Monitoring:")
        print(f"   CPU usage: {SystemMonitor.get_cpu_usage():.1f}%")
        print(f"   CPU cores: {SystemMonitor.get_cpu_count()}")
        
        mem = SystemMonitor.get_memory_usage()
        print(f"   Memory: {mem['used'] / (1024**3):.2f}GB / {mem['total'] / (1024**3):.2f}GB ({mem['percent']:.1f}%)")
        
        disk = SystemMonitor.get_disk_usage("/")
        print(f"   Disk: {disk['used'] / (1024**3):.2f}GB / {disk['total'] / (1024**3):.2f}GB ({disk['percent']:.1f}%)")
        
        print(f"   Uptime: {SystemMonitor.get_uptime() / 3600:.1f} hours")
    else:
        print("\n4. System Monitoring:")
        print("   psutil not available - install with: pip install psutil")
    
    # File System
    print("\n5. File System:")
    current_dir = SystemInformation.get_current_working_directory()
    print(f"   Current directory: {current_dir}")
    print(f"   Directory exists: {FileSystem.directory_exists(current_dir)}")
    
    files = FileSystem.list_directory(current_dir)[:5]  # First 5 items
    print(f"   Directory contents (first 5): {files}")
    
    # Path Utilities
    print("\n6. Path Utilities:")
    test_path = "/home/user/documents/file.txt"
    print(f"   Basename: {PathUtilities.get_basename(test_path)}")
    print(f"   Dirname: {PathUtilities.get_dirname(test_path)}")
    print(f"   Extension: {PathUtilities.split_extension(test_path)[1]}")
    
    # Network Utilities
    print("\n7. Network Utilities:")
    print(f"   Hostname: {NetworkUtilities.get_hostname()}")
    print(f"   Local IP: {NetworkUtilities.get_local_ip()}")
    print(f"   MAC address: {NetworkUtilities.get_mac_address()}")
    
    # Cross-platform
    print("\n8. Cross-platform:")
    print(f"   Platform: {platform.system()}")
    print(f"   Is Windows: {CrossPlatform.is_windows()}")
    print(f"   Is Linux: {CrossPlatform.is_linux()}")
    print(f"   Is macOS: {CrossPlatform.is_macos()}")
    print(f"   Path separator: {CrossPlatform.get_path_separator()}")
    
    # Performance
    print("\n9. Performance Monitoring:")
    if PSUTIL_AVAILABLE:
        perf = PerformanceMonitor.memory_usage()
        print(f"   Memory RSS: {perf['rss'] / (1024**2):.2f}MB")
        print(f"   Memory percent: {perf['percent']:.1f}%")
        print(f"   Thread count: {PerformanceMonitor.thread_count()}")
    else:
        print("   psutil not available")
    
    # Command execution
    print("\n10. Command Execution:")
    returncode, stdout, stderr = ProcessManager.run_command("echo 'Hello from shell'")
    print(f"   Command output: {stdout.strip()}")
    
    print("\n=== Demonstration Complete ===")


if __name__ == "__main__":
    demonstrate_system_utils()