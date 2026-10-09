# Traceability: one zip per run with the case settings, the code version, the inputs, the results and the log.
# A successful run stores everything; a failed run stores only what helps to debug it (log, settings, code version,
# input checksums and the list of files written before the failure).
import datetime
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import zipfile


def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def file_info(path):
    return {"path": path, "size_bytes": os.path.getsize(path), "sha256": sha256(path),
            "modified": datetime.datetime.fromtimestamp(os.path.getmtime(path)).isoformat(timespec="seconds")}


def git(*args):
    try:
        return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return ""


def case_out_dir(cfg, case):
    """Same folder as the run script: output_dir/<country code>/<case>."""
    country_code = cfg["country"].split("--")[-1].strip()
    return os.path.join(cfg["output_dir"], country_code, case)


def make_run_archive(case, cfg, status, started, finished, log_path=None, archive_inputs=True):
    """Write output_dir/<country>/archives/<case>_<timestamp>.zip and return its path.

    started / finished are time.time() values; status is "success" or "failed".
    Only result files written during this run (modified after `started`) are stored.
    """
    out_dir = case_out_dir(cfg, case)
    archive_dir = os.path.join(os.path.dirname(out_dir), "archives")
    os.makedirs(archive_dir, exist_ok=True)
    stamp = datetime.datetime.fromtimestamp(started).strftime("%Y%m%d-%H%M%S")
    zip_path = os.path.join(archive_dir, f"{case}_{stamp}.zip")

    # result files of this run (the cache is left out: large and rebuilt automatically)
    written, not_updated = [], []
    if os.path.isdir(out_dir):
        for root, dirs, files in os.walk(out_dir):
            dirs[:] = [d for d in dirs if d != "cache"]
            for name in sorted(files):
                path = os.path.join(root, name)
                # 1 s margin: file modification times can be slightly coarser than time.time()
                (written if os.path.getmtime(path) >= started - 1 else not_updated).append(path)

    manifest = {
        "case": case,
        "status": status,
        "started": datetime.datetime.fromtimestamp(started).isoformat(timespec="seconds"),
        "finished": datetime.datetime.fromtimestamp(finished).isoformat(timespec="seconds"),
        "duration_seconds": round(finished - started, 1),
        "archive_inputs": archive_inputs,
        "code": {
            "commit": git("rev-parse", "HEAD").strip(),
            "branch": git("rev-parse", "--abbrev-ref", "HEAD").strip(),
            "uncommitted_python_changes": bool(git("diff", "HEAD", "--name-only", "--", "*.py").strip()),
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "inputs": {},
        "results": [],
        "files_written_before_failure": [],
        "results_folder_not_updated_by_this_run": [],
    }
    for role, key in (("msna", "excel_data_path"), ("ocha", "excel_path_ocha")):
        path = cfg.get(key)
        manifest["inputs"][role] = file_info(path) if path and os.path.exists(path) else {"path": path, "missing": True}

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("config/case_config.json", json.dumps({case: cfg}, indent=2, ensure_ascii=False, default=str))
        z.writestr("code/git_diff_python.txt", git("diff", "HEAD", "--", "*.py") or "no uncommitted changes in .py files\n")
        z.writestr("code/packages.txt", "\n".join(sorted(
            f"{d.metadata['Name']}=={d.version}" for d in importlib.metadata.distributions())) + "\n")
        if log_path and os.path.exists(log_path):
            z.write(log_path, "log/" + os.path.basename(log_path))

        if status == "success":
            if archive_inputs:
                for role in ("msna", "ocha"):
                    if not manifest["inputs"][role].get("missing"):
                        z.write(manifest["inputs"][role]["path"], f"inputs/{role}/" + os.path.basename(manifest["inputs"][role]["path"]))
            for path in written:
                z.write(path, "results/" + os.path.relpath(path, out_dir))
                manifest["results"].append(file_info(path))
        else:
            # failed run: no inputs or results, only the names of the files it managed to write
            manifest["files_written_before_failure"] = [os.path.relpath(p, out_dir) for p in written]
        manifest["results_folder_not_updated_by_this_run"] = [os.path.relpath(p, out_dir) for p in not_updated]

        z.writestr("MANIFEST.json", json.dumps(manifest, indent=2, ensure_ascii=False))
    return zip_path
