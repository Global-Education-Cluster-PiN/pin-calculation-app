# Run run_PiNcalculation_outside_streamlit.py once for each case in RUN_CASES (run_config.py).
# Each case runs in its own Python process, so all its memory is released when it finishes
# and a failing case does not affect the next one. The output of each case is also saved in logs/<case>.log,
# and each run is archived in output_dir/<country>/archives/<case>_<timestamp>.zip (see src/run_archive.py).
import os, sys, subprocess, time
import importlib
import run_config
importlib.reload(run_config)   # pick up edits to run_config.py when re-running in a notebook
from src.run_archive import make_run_archive

os.makedirs("logs", exist_ok=True)
failed = []
for case in run_config.RUN_CASES:
    print(f"\n===== {case} =====", flush=True)
    log_path = os.path.join("logs", f"{case}.log")
    started = time.time()
    with open(log_path, "w", encoding="utf-8") as log:
        proc = subprocess.Popen(
            [sys.executable, "run_PiNcalculation_outside_streamlit.py"],
            env={**os.environ, "PIN_CASE": case, "PYTHONUNBUFFERED": "1"},   # unbuffered: lines appear as they are printed
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
        for line in proc.stdout:          # show progress live and keep a log per case
            print(line, end="")
            log.write(line)
        status = "success" if proc.wait() == 0 else "failed"
    if status == "failed":
        failed.append(case)

    try:
        zip_path = make_run_archive(case, run_config.CASES[case], status, started, time.time(),
                                    log_path=log_path, archive_inputs=run_config.ARCHIVE_INPUTS)
        print(f"archived ({status}): {zip_path}")
    except Exception as e:                # an archiving problem must not stop the other cases
        print(f"archive failed for {case}: {e}")

print("\ndone. failed:", failed or "none")
