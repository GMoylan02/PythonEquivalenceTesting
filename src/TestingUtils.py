"""
Utils for running the Hobbit test suite/mutation test suite
"""
import os
import signal
import subprocess


def clean_directory():
    KEEP_FILES = {"hypofuzz_failures.log", "RunMutationTests.py", "__init__.py"}
    dir_path = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if filename in KEEP_FILES or not os.path.isfile(file_path):
            continue
        os.remove(file_path)


def kill_process_tree(process):
    if process is None or process.poll() is not None:
        return
    try:
        if os.name != 'nt':
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        else:
            subprocess.call(
                ['taskkill', '/F', '/T', '/PID', str(process.pid)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
    except Exception:
        pass

def clear_log(filename="hypofuzz_failures.log"):
    with open(filename, 'w', encoding="utf-8") as f:
        f.write("")
