# Run run_PiNcalculation_outside_streamlit.py once for each case in RUN_CASES (run_config.py).
# Each case runs in its own Python process, so all its memory is released when it finishes
# and a failing case does not affect the next one. The output of each case is also saved in logs/<case>.log.
import os, sys, subprocess
import importlib
import run_config
importlib.reload(run_config)   # pick up edits to run_config.py when re-running in a notebook

os.makedirs("logs", exist_ok=True)
failed = []
for case in run_config.RUN_CASES:
    print(f"\n===== {case} =====", flush=True)
    with open(os.path.join("logs", f"{case}.log"), "w", encoding="utf-8") as log:
        proc = subprocess.Popen(
            [sys.executable, "run_PiNcalculation_outside_streamlit.py"],
            env={**os.environ, "PIN_CASE": case, "PYTHONUNBUFFERED": "1"},   # unbuffered: lines appear as they are printed
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
        for line in proc.stdout:          # show progress live and keep a log per case
            print(line, end="")
            log.write(line)
        if proc.wait() != 0:
            failed.append(case)

print("\ndone. failed:", failed or "none")
