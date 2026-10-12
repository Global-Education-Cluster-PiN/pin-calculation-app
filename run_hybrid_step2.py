# Hybrid countries, step 2 (as the platform's second download): extrapolate the PiN of the areas without MSNA data
# from the two step 1 files, recalculate the PiN by severity and write the PiN results, the snapshot and the maps.
# Step 1 is a normal run of run_PiNcalculation_outside_streamlit.py with "hybrid_country": True; this step only needs
# the OCHA file, the step 1 files ("updated_pin_path", "covered_pin_path") and pin2024_cat/<code>_PIN2024.xlsx.
import os, time, importlib
import pandas as pd
import run_config
importlib.reload(run_config)   # pick up edits to run_config.py when re-running in a notebook
from run_config import CASES, ACTIVE_CASE
from src.extrapolation import extrapolate_df_2025_updated
from src.update_re_calculation_for_PiN import UPDATE_calculatePIN
from src.vizualize_PiN import create_output, parameters_to_df, pop_parameters_sheet
from src.snapshot_PiN import create_snapshot_PiN
from src.snapshot_PiN_FR import create_snapshot_PiN_FR
from src.create_map_severity import make_map_severity
from src.local_parameters import case_parameters
from src.output_names import output_name, name_stamp, map_content, newest_file

ACTIVE_CASE = os.environ.get("PIN_CASE") or ACTIVE_CASE   # run_all_cases.py chooses the case through PIN_CASE
cfg = CASES[ACTIVE_CASE]
if not cfg.get("step_2_hpc", False):
    raise ValueError(f"{ACTIVE_CASE} has step_2_hpc = False: run run_PiNcalculation_outside_streamlit.py for step 1")
run_started = time.time()   # used to archive only the files written by this run

country, selected_language, label, admin_var = cfg["country"], cfg["selected_language"], cfg["label"], cfg["admin_var"]
country_code = country.split("--")[-1].strip()
country_label = country.replace(" ", "_").replace("--", "_").replace("/", "_")
out_dir = os.path.join(cfg["output_dir"], country_code, ACTIVE_CASE)
os.makedirs(out_dir, exist_ok=True)
files_stamp = name_stamp()   # result files: same names as the platform downloads, with the run time
def out_name(content, ext):
    return os.path.join(out_dir, output_name(country, content, ext, files_stamp))
# intermediate check files (00_..., 01_...): one folder per run, e.g. checks_20261011-1745
check_dir = os.path.join(out_dir, f"checks_{files_stamp}")
os.makedirs(check_dir, exist_ok=True)

# --- inputs, read as on the platform (pages 1 and 3)
ocha_data = pd.read_excel(cfg["excel_path_ocha"], sheet_name=cfg["sheets"]["ocha"], engine="openpyxl")
# a path with * stands for the newest matching file (step 1 file names include the run time)
updated_2025_pin_file = pd.read_excel(newest_file(cfg["updated_pin_path"]), engine="openpyxl", skiprows=1)
uploaded_covered_2025_pin = pd.read_excel(newest_file(cfg["covered_pin_path"]), engine="openpyxl", sheet_name=None)
step1_parameters_df = pop_parameters_sheet(uploaded_covered_2025_pin)   # not a population group (see page 1)
pin2024_file = os.path.join("pin2024_cat", f"{country_code}_PIN2024.xlsx")
if not os.path.exists(pin2024_file):
    raise FileNotFoundError(f"No 2024 PiN file found: {pin2024_file}")
pin2024_cat = pd.read_excel(pin2024_file, sheet_name=None)

# --- extrapolate with the delta method, then recalculate the PiN by severity
extrapolation_notes = []   # areas that could not be extrapolated as asked: printed and written in the PiN results
merged_df_delta_all, pin_2025_updated = extrapolate_df_2025_updated(updated_2025_pin_file, uploaded_covered_2025_pin, pin2024_cat,
                                                                     notes=extrapolation_notes, selected_language=selected_language)
for note in extrapolation_notes:
    print(f"extrapolation note -- {note['Population group']} {note['Admin Pcode']}: {note['Note']}")
(Tot_PiN_JIAF, Tot_PiN_by_admin, final_overview_df_OCHA, final_overview_df,
 pin_per_admin_status) = UPDATE_calculatePIN(country, pin_2025_updated, ocha_data, label, selected_language)

# --- outputs; the "Parameters Used" sheet is the one of step 1, read from the step 1 file as on the platform
# (files from before this sheet existed: built from the case settings, which step 1 used)
if step1_parameters_df is None:
    step1_parameters_df, _ = parameters_to_df(case_parameters(cfg)[0], selected_language)
ocha_excel = create_output(country_label, Tot_PiN_JIAF, final_overview_df, final_overview_df_OCHA, "PiN TOTAL", admin_var,
                           ocha=True, tot_severity=Tot_PiN_by_admin, selected_language=selected_language,
                           ocha_data=ocha_data, parameters_df=step1_parameters_df, notes=extrapolation_notes)
with open(out_name("step2_results", "xlsx"), "wb") as f:
    f.write(ocha_excel.getvalue())

if selected_language == "French":
    doc_output = create_snapshot_PiN_FR(country_label, final_overview_df, final_overview_df_OCHA, selected_language=selected_language, step1=False)
else:
    doc_output = create_snapshot_PiN(country_label, final_overview_df, final_overview_df_OCHA, selected_language=selected_language)
with open(out_name("step2_snapshot", "docx"), "wb") as f:
    f.write(doc_output.getvalue())

maps = make_map_severity(country, pin_data=Tot_PiN_by_admin, hpc_df=ocha_data)
for layer, buf in maps.items():
    with open(out_name(map_content(layer, "step2_"), "png"), "wb") as f:
        f.write(buf.getvalue())

# --- for checking: the extrapolation of each population group (not in the platform's download)
with pd.ExcelWriter(os.path.join(check_dir, "step2_extrapolation_details.xlsx"), engine="openpyxl") as writer:
    for category, df in merged_df_delta_all.items():
        df.to_excel(writer, sheet_name=str(category)[:31], index=False)

# --- archive this run (single runs only: run_all_cases.py archives batch runs itself, including the log)
if not os.environ.get("PIN_CASE"):
    from src.run_archive import make_run_archive
    zip_path = make_run_archive(ACTIVE_CASE, cfg, "success", run_started, time.time(),
                                archive_inputs=run_config.ARCHIVE_INPUTS)
    print(f"archived: {zip_path}")
