# EMIS countries (MSNA + EMIS data), run locally from a case of run_config.py, with the same steps as page 3 of the platform:
# cleaning, severity, calculatePIN_with_EMIS, PiN results, snapshot and maps.
# Copy of run_PiNcalculation_outside_streamlit_EMIS.py (kept for reference) that reads its settings from run_config.py.
# Besides the usual keys, the case needs "data_combination" ('emmm', 'eemm' or 'eeem') and "excel_path_other" (EMIS file,
# sheet "sheets"["other"]); see the LMR_2022_EMIS case.
import os, importlib
import pandas as pd
import run_config
importlib.reload(run_config)   # pick up edits to run_config.py when re-running in a notebook
from run_config import CASES, ACTIVE_CASE
from src.clean_dataset import clean_make_dataset
from src.add_PiN_severity import add_severity
from src.calculation_for_PiN_Dimension_with_EMIS import calculatePIN_with_EMIS
from src.vizualize_PiN import create_output
from src.snapshot_PiN import create_snapshot_PiN
from src.snapshot_PiN_FR import create_snapshot_PiN_FR
from src.create_map_severity import make_map_severity

ACTIVE_CASE = os.environ.get("PIN_CASE") or ACTIVE_CASE
cfg = CASES[ACTIVE_CASE]
data_combination = cfg["data_combination"]
if data_combination not in ('emmm', 'eemm', 'eeem'):   # page 3: EMIS for these data combinations
    raise ValueError(f"{ACTIVE_CASE}: data_combination is {data_combination!r}; EMIS needs 'emmm', 'eemm' or 'eeem'")

# unpack to the names used by the platform
country, selected_language, label = cfg["country"], cfg["selected_language"], cfg["label"]
start_school, admin_var, vector_cycle = cfg["start_school"], cfg["admin_var"], cfg["vector_cycle"]
mismatch_admin = cfg["mismatch_admin"]
status_var, access_var = cfg["status_var"], cfg["access_var"]
teacher_disruption_var, idp_disruption_var = cfg["teacher_disruption_var"], cfg["idp_disruption_var"]
armed_disruption_var, natural_hazard_var = cfg["armed_disruption_var"], cfg["natural_hazard_var"]
natural_hazard_var_sev = cfg["natural_hazard_var_sev"]
additional_last_var, additional_last_sev = cfg["additional_last_var"], cfg["additional_last_sev"]
additional_2_last_var, additional_2_last_sev = cfg["additional_2_last_var"], cfg["additional_2_last_sev"]
barrier_var, age_var, gender_var = cfg["barrier_var"], cfg["age_var"], cfg["gender_var"]
selected_severity_4_barriers = cfg["selected_severity_4_barriers"]
selected_severity_5_barriers = cfg["selected_severity_5_barriers"]
host_value, idp_value, returnee_value = cfg["host_value"], cfg["idp_value"], cfg["returnee_value"]
refugee_value, other_value = cfg["refugee_value"], cfg["other_value"]
if all(v is None for v in (host_value, idp_value, returnee_value, refugee_value, other_value)):
    raise ValueError("Fill in the population-group mapping (host_value, idp_value, ...) in run_config.py")
sheets = cfg["sheets"]
country_label = country.replace(" ", "_").replace("--", "_").replace("/", "_")
country_code = country.split("--")[-1].strip()
out_dir = os.path.join(cfg["output_dir"], country_code, ACTIVE_CASE)
os.makedirs(out_dir, exist_ok=True)

# --- inputs
xls = pd.ExcelFile(cfg["excel_data_path"], engine='openpyxl')
household_data = pd.read_excel(xls, sheet_name=sheets["household"])
edu_data = pd.read_excel(xls, sheet_name=sheets["edu"])
survey_data = pd.read_excel(xls, sheet_name=sheets["survey"])
choice_data = pd.read_excel(xls, sheet_name=sheets["choices"])
ocha_xls = pd.ExcelFile(cfg["excel_path_ocha"], engine='openpyxl')
ocha_data = pd.read_excel(ocha_xls, sheet_name=sheets["ocha"])
mismatch_ocha_data = pd.read_excel(ocha_xls, sheet_name=sheets["scope_fix"])
other_data = pd.read_excel(cfg["excel_path_other"], engine='openpyxl', sheet_name=sheets["other"])   # EMIS data

# --- cleaning (as page 3)
edu_data, household_data, survey_data, choice_data, messages = clean_make_dataset(
    country, edu_data, household_data, choice_data, survey_data,
    access_var, teacher_disruption_var, idp_disruption_var, armed_disruption_var,
    natural_hazard_var, natural_hazard_var_sev,
    additional_last_var, additional_last_sev,
    additional_2_last_var, additional_2_last_sev,
    barrier_var, selected_severity_4_barriers, selected_severity_5_barriers,
    age_var, gender_var,
    label,
    admin_var, vector_cycle, start_school, status_var,
    selected_language)
for w in messages.warning:
    print("warning:", w)
for i in messages.info:
    print("info:", i)

# the cleaning step renames these columns
status_var = "pop_status_group"
age_var = "ind_age"
gender_var = "ind_gender"
barrier_var = "edu_barrier_final"

# --- severity
edu_data_severity, drop_msg = add_severity(
    country, edu_data, household_data, choice_data, survey_data,
    access_var, teacher_disruption_var, idp_disruption_var, armed_disruption_var,
    natural_hazard_var, natural_hazard_var_sev,
    additional_last_var, additional_last_sev,
    additional_2_last_var, additional_2_last_sev,
    barrier_var, selected_severity_4_barriers, selected_severity_5_barriers,
    age_var, gender_var,
    label,
    admin_var, vector_cycle, start_school, status_var,
    selected_language,
    full_GEC_compliant=cfg["full_GEC_compliant"])
if drop_msg:
    print("warning:", drop_msg)
edu_data_severity.to_excel(os.path.join(out_dir, '00_edu_data_with_severity.xlsx'), index=False, engine='openpyxl')

# --- PiN with EMIS. calculatePIN_with_EMIS needs the severity columns (severity_category, var.access, ...), so it gets
# edu_data_severity, as the old script did (page 3 passes edu_data).
(pin_by_indicator_status_list, enrollment_df, pop_figures_E_OoS_by_pop_group, severity_by_pop_group,
 pin_by_pop_group, pin_by_dimension_in_need_pop_group, pin_by_indicator_pop_group, test_intermediate_step,
 Tot_PiN_JIAF, final_overview_df_OCHA, final_overview_df, Tot_PiN_by_admin) = calculatePIN_with_EMIS(
    data_combination, country, edu_data_severity, household_data, choice_data, survey_data, ocha_data, mismatch_ocha_data, other_data,
    access_var, teacher_disruption_var, idp_disruption_var, armed_disruption_var, natural_hazard_var,
    barrier_var, selected_severity_4_barriers, selected_severity_5_barriers,
    age_var, gender_var,
    label,
    admin_var, vector_cycle, start_school, status_var, host_value, idp_value, returnee_value, refugee_value, other_value,
    mismatch_admin,
    selected_language)


# --- intermediate files (as the old script)
def write_tables(file_name, tables):
    """A dictionary of tables: one sheet per entry; a single table: one sheet."""
    path = os.path.join(out_dir, file_name)
    if isinstance(tables, dict):
        with pd.ExcelWriter(path) as writer:
            for category, df in tables.items():
                df.to_excel(writer, sheet_name=str(category)[:31], index=False)
    else:
        tables.to_excel(path, index=False, engine='openpyxl')


for file_name, tables in [('E_indicator_results_withright_subset.xlsx', pin_by_indicator_status_list),
                          ('E_enrolment_by_pop_group.xlsx', enrollment_df),
                          ('E_E_OoS_pop_group.xlsx', pop_figures_E_OoS_by_pop_group),
                          ('E_severity_pop_group.xlsx', Tot_PiN_by_admin),
                          ('E_PiN_pop_group.xlsx', Tot_PiN_JIAF),
                          ('E_PiN_by_dimension_in_need.xlsx', pin_by_dimension_in_need_pop_group),
                          ('E_PiN_by_indicator.xlsx', pin_by_indicator_pop_group),
                          ('E_test_all_sev.xlsx', test_intermediate_step)]:
    write_tables(file_name, tables)

# --- outputs (as page 3)
ocha_excel = create_output(country_label, Tot_PiN_JIAF, final_overview_df, final_overview_df_OCHA, "PiN TOTAL", admin_var,
                           ocha=True, tot_severity=Tot_PiN_by_admin, selected_language=selected_language, ocha_data=ocha_data)
with open(os.path.join(out_dir, f'PiN_results_{country_label}.xlsx'), 'wb') as f:
    f.write(ocha_excel.getvalue())
if selected_language == "French":
    doc_output = create_snapshot_PiN_FR(country_label, final_overview_df, final_overview_df_OCHA, selected_language=selected_language, step1=False)
else:
    doc_output = create_snapshot_PiN(country_label, final_overview_df, final_overview_df_OCHA, selected_language=selected_language)
with open(os.path.join(out_dir, f'PiN_snapshot_{country_label}.docx'), 'wb') as f:
    f.write(doc_output.getvalue())
for layer, buf in make_map_severity(country, pin_data=Tot_PiN_by_admin, hpc_df=ocha_data).items():
    with open(os.path.join(out_dir, f'map_{layer}.png'.replace(' ', '_').replace('%', 'pct')), 'wb') as f:
        f.write(buf.getvalue())
print("outputs written to", out_dir)
