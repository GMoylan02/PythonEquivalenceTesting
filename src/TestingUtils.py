"""
Utils for running the Hobbit test suite/mutation test suite
"""
import os
import signal
import subprocess
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class FuzzResult:
    killed: bool
    elapsed: Optional[float]


def run_hypothesis_fuzz(
    filepath: str,
    log_file: str = "hypofuzz_failures.log",
    timeout_seconds: int = 300,
    project_root: str = None,
    poll_interval: float = 0.5,
    post_kill_grace: float = 0.3,
) -> FuzzResult:
    """
    Run `hypothesis fuzz` on a file, polling the shared log for failures
    """
    if project_root is None:
        project_root = os.path.abspath(os.getcwd())

    initial_failure_count = _count_lines(log_file)

    cmd = ["hypothesis", "fuzz", str(filepath), "--no-dashboard"]
    env = os.environ.copy()
    env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")
    env["MUTANT_UNDER_TEST"] = ""

    elapsed = None
    killed = False
    process = None

    try:
        process = subprocess.Popen(
            cmd, env=env,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid if os.name != 'nt' else None,
        )

        start_time = time.time()
        while True:
            if process.poll() is not None:
                break
            if time.time() - start_time > timeout_seconds:
                break

            if _count_lines(log_file) > initial_failure_count:
                elapsed = time.time() - start_time
                killed = True
                break

            time.sleep(poll_interval)
    except Exception as e:
        print(f"Error: {e}")

    kill_process_tree(process)

    # post-kill check: failure may have been written between
    # last poll and process termination
    if not killed and _count_lines(log_file) > initial_failure_count:
        killed = True

    if post_kill_grace > 0:
        time.sleep(post_kill_grace)

    return FuzzResult(killed=killed, elapsed=elapsed)


def _count_lines(path: str) -> int:
    if not os.path.exists(path):
        return 0
    with open(path, 'rb') as f:
        return sum(1 for _ in f)


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
