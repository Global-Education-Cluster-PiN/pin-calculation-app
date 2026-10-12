# Names of the result files, the same on the platform (downloads) and in local runs (output folder):
#   <ISO>_PiN<year>_<content>_<YYYYMMDD-HHMM>.<ext>     e.g. SOM_PiN2026_results_20261011-1745.xlsx
# The time is part of the name so that a new download or run does not replace an earlier one.
import datetime
import glob
import os
import re

PIN_YEAR = 2026   # PiN (HNO) year shown in the names; update with the yearly relabel

# maps: one per layer of make_map_severity (English and French titles)
MAP_CONTENT = {
    "Area severity": "map-area-severity", "Sévérité de la zone": "map-area-severity",
    "% severity level 3": "map-severity-3", "% niveau de sévérité 3": "map-severity-3",
    "% severity level 4": "map-severity-4", "% niveau de sévérité 4": "map-severity-4",
    "% severity level 5": "map-severity-5", "% niveau de sévérité 5": "map-severity-5",
    "% Tot PiN (severity levels 3-5)": "map-total-PiN", "% Tot PiN (niveaux de sévérité 3-5)": "map-total-PiN",
}


def name_stamp():
    """Date and time used in the names (no ':' as Windows does not allow it in file names)."""
    return datetime.datetime.now().strftime("%Y%m%d-%H%M")


def output_name(country, content, ext, stamp):
    """country: "Somalia -- SOM"; content: e.g. "results", "step1_to-fill"; ext: "xlsx", "docx", "png", "zip"."""
    iso = country.split("--")[-1].strip()
    return f"{iso}_PiN{PIN_YEAR}_{content}_{stamp}.{ext}"


def map_content(layer, prefix=""):
    """Content part of a map name, e.g. "map-severity-3" (prefix: "step1_" or "step2_" for the hybrid steps)."""
    content = MAP_CONTENT.get(layer) or "map-" + re.sub(r"[^A-Za-z0-9]+", "-", layer).strip("-")
    return prefix + content


def newest_file(path):
    """Local runs: a path with * (e.g. ..._step1_covered-areas_*.xlsx) stands for the newest matching file."""
    if "*" not in path:
        return path
    matches = glob.glob(path)
    if not matches:
        raise FileNotFoundError(f"No file matches {path}")
    return max(matches, key=os.path.getmtime)
