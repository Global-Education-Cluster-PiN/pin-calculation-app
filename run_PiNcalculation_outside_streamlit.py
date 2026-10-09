import pandas as pd
#import fuzzywuzzy
from fuzzywuzzy import process
import numpy as np
import datetime
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Border, Side, Font, Alignment
from openpyxl.cell.cell import MergedCell  # Import MergedCell
from io import BytesIO
from src.add_PiN_severity import add_severity
from src.calculation_for_PiN_Dimension import calculatePIN
from src.calculation_for_PiN_Dimension_NO_OCHA import calculatePIN_NO_OCHA
from src.calculation_for_PiN_Dimension_NO_OCHA_2025 import calculatePIN_NO_OCHA_2025
from src.vizualize_PiN import create_output
from src.vizualize_PiN import create_indicator_output
from src.vizualize_PiN import create_indicator_output_no_ocha
from src.vizualize_PiN import create_pin_raw_output
from src.snapshot_PiN import create_snapshot_PiN
from src.snapshot_PiN_FR import create_snapshot_PiN_FR
from src.save_parameter import generate_word_document
from src.save_parameter import generate_parameters
from src.save_parameter_FR import generate_word_document_FR
from src.save_parameter_FR import generate_parameters_FR
from src.create_map_severity import make_map_severity
from src.clean_dataset import clean_make_dataset

from docx import Document
from docx.shared import Pt, RGBColor
import matplotlib.pyplot as plt
from docx.shared import Inches
import os, glob

import importlib
import run_config
importlib.reload(run_config)   # pick up edits to run_config.py when re-running in a notebook
from run_config import CASES, ACTIVE_CASE

ACTIVE_CASE = os.environ.get("PIN_CASE") or ACTIVE_CASE   # run_all_cases.py chooses the case through PIN_CASE
cfg = CASES[ACTIVE_CASE]
import time
run_started = time.time()   # used to archive only the files written by this run

# unpack to the names used in the rest of the script
country, selected_language, label = cfg["country"], cfg["selected_language"], cfg["label"]
start_school, admin_var, vector_cycle = cfg["start_school"], cfg["admin_var"], cfg["vector_cycle"]
hybrid_country, mismatch_admin, no_ocha_data = cfg["hybrid_country"], cfg["mismatch_admin"], cfg["no_ocha_data"]
status_var, access_var = cfg["status_var"], cfg["access_var"]
teacher_disruption_var, idp_disruption_var = cfg["teacher_disruption_var"], cfg["idp_disruption_var"]
armed_disruption_var, natural_hazard_var = cfg["armed_disruption_var"], cfg["natural_hazard_var"]
natural_hazard_var_sev = cfg["natural_hazard_var_sev"]
additional_last_var, additional_last_sev = cfg["additional_last_var"], cfg["additional_last_sev"]
additional_2_last_var, additional_2_last_sev = cfg["additional_2_last_var"], cfg["additional_2_last_sev"]
barrier_var, age_var, gender_var = cfg["barrier_var"], cfg["age_var"], cfg["gender_var"]
selected_severity_4_barriers = cfg["selected_severity_4_barriers"]
selected_severity_5_barriers = cfg["selected_severity_5_barriers"]
single_cycle = (vector_cycle[1] == 0)
# TODO: add later — primary_start, secondary_end, step_2_hpc are commented out in run_config.py (not used yet)
# primary_start, secondary_end = cfg["primary_start"], cfg["secondary_end"]
# step_2_hpc = cfg["step_2_hpc"]
host_value, idp_value, returnee_value = cfg["host_value"], cfg["idp_value"], cfg["returnee_value"]
refugee_value, other_value = cfg["refugee_value"], cfg["other_value"]
if all(v is None for v in (host_value, idp_value, returnee_value, refugee_value, other_value)):
    raise ValueError("Fill in the population-group mapping (host_value, idp_value, ...) in run_config.py")
sheets = cfg["sheets"]
country_code = country.split("--")[-1].strip()
out_dir = os.path.join(cfg["output_dir"], country_code, ACTIVE_CASE)   # one folder per case, so variants don't overwrite each other
os.makedirs(out_dir, exist_ok=True)

# --- checkpoints: save the slow steps once they finish and reuse them while their inputs are unchanged
import hashlib, pickle
use_cache = cfg.get("use_cache", True)          # set "use_cache": False in run_config.py to force a full rerun
cache_dir = os.path.join(out_dir, "cache")
os.makedirs(cache_dir, exist_ok=True)

def file_signature(path):
    """Path, modification time and size: changes whenever the file is edited."""
    return (os.path.abspath(path), os.path.getmtime(path), os.path.getsize(path))

def fingerprint(*parts):
    return hashlib.sha256(repr(parts).encode()).hexdigest()

def load_or_compute(name, key, compute):
    """Return the saved result of `name` if its key matches, otherwise run compute() and save it."""
    path = os.path.join(cache_dir, f"{name}.pkl")
    if use_cache and os.path.exists(path):
        with open(path, "rb") as f:
            saved = pickle.load(f)
        if saved["key"] == key:
            print(f"loaded {name} from cache")
            return saved["result"]
        print(f"{name}: inputs changed, recomputing")
    result = compute()
    with open(path + ".tmp", "wb") as f:
        pickle.dump({"key": key, "result": result}, f)
    os.replace(path + ".tmp", path)          # only a completed step is saved
    print(f"saved {name} to cache")
    return result

# --- load data (checkpoint 01): only the sheets that are used
def load_inputs():
    xls = pd.ExcelFile(cfg["excel_data_path"], engine='openpyxl')
    print(xls.sheet_names)
    needed = [sheets["household"], sheets["edu"], sheets["survey"], sheets["choices"]]
    dfs = {sheet_name: pd.read_excel(xls, sheet_name=sheet_name) for sheet_name in needed}
    ocha_xls = pd.ExcelFile(cfg["excel_path_ocha"], engine='openpyxl')
    ocha_data = pd.read_excel(ocha_xls, sheet_name=sheets["ocha"]) if sheets["ocha"] else None  # None = no OCHA sheet (e.g. LMR_2022)
    mismatch_ocha_data = pd.read_excel(ocha_xls, sheet_name=sheets["scope_fix"])
    return dfs, ocha_data, mismatch_ocha_data

key_loaded = fingerprint(file_signature(cfg["excel_data_path"]), file_signature(cfg["excel_path_ocha"]), sheets)
dfs, ocha_data, mismatch_ocha_data = load_or_compute("01_loaded", key_loaded, load_inputs)
household_data = dfs[sheets["household"]]
edu_data = dfs[sheets["edu"]]
survey_data = dfs[sheets["survey"]]
choice_data = dfs[sheets["choices"]]



#######################################################
#######################################################
##########          CALCULATION PIN          ##########
#######################################################
#######################################################
#######################################################
# Always start from the raw sheets and the column names in run_config.py, so this step can be
# re-run in a notebook even after the standard names below have overwritten status_var, age_var, ...
def run_cleaning():
    return clean_make_dataset (
    country,
    dfs[sheets["edu"]].copy(), dfs[sheets["household"]].copy(),
    dfs[sheets["choices"]].copy(), dfs[sheets["survey"]].copy(),
    access_var, teacher_disruption_var, idp_disruption_var, armed_disruption_var,
    natural_hazard_var,natural_hazard_var_sev,
    additional_last_var,additional_last_sev,
    additional_2_last_var,additional_2_last_sev,
    cfg["barrier_var"], selected_severity_4_barriers, selected_severity_5_barriers,
    cfg["age_var"], cfg["gender_var"],
    label,
    admin_var, vector_cycle, start_school, cfg["status_var"],
    selected_language)

config_for_key = {k: v for k, v in cfg.items() if k not in ("use_cache", "output_dir")}
key_cleaned = fingerprint(key_loaded, config_for_key, file_signature("src/clean_dataset.py"))
edu_data1, household_data, survey_data, choice_data, messages = load_or_compute("02_cleaned", key_cleaned, run_cleaning)

status_var =  "pop_status_group"
age_var = "ind_age"
gender_var =  "ind_gender"
barrier_var = "edu_barrier_final"
file_path000 = os.path.join(out_dir, '000_edu_data.xlsx')
file_path000h = os.path.join(out_dir, '000_hh.xlsx')

# Save the DataFrame to an Excel file
edu_data1.to_excel(file_path000, index=False, engine='openpyxl')
household_data.to_excel(file_path000h, index=False, engine='openpyxl')

def run_severity():
    return add_severity (
    country,
    edu_data1,
    household_data,
    choice_data,
    survey_data,
    access_var, teacher_disruption_var, idp_disruption_var, armed_disruption_var,
    natural_hazard_var,natural_hazard_var_sev,
    additional_last_var,additional_last_sev,
    additional_2_last_var,additional_2_last_sev,
    barrier_var, selected_severity_4_barriers, selected_severity_5_barriers,
    age_var, gender_var,
    label, 
    admin_var, vector_cycle, start_school, status_var,
    selected_language= selected_language)

key_severity = fingerprint(key_cleaned, file_signature("src/add_PiN_severity.py"))
edu_data_severity, drop_msg = load_or_compute("03_severity", key_severity, run_severity)

if drop_msg:
    print(drop_msg)

file_path = os.path.join(out_dir, '00_edu_data_with_severity.xlsx')
# Save the DataFrame to an Excel file
edu_data_severity.to_excel(file_path, index=False, engine='openpyxl')


# Parameters used, as on the platform: "Parameters Used" sheet of the PiN results and Parameters_Input_Document.docx.
# generate_parameters reads the Streamlit session-state names; six of them are named differently in run_config.py.
param_state = {
    **cfg,
    "selected_disruption_natural_hazard_column": natural_hazard_var,
    "natural_hazard_disruption_severity": natural_hazard_var_sev,
    "additional_indicator_last_var": additional_last_var,
    "additional_indicator_last_severity": additional_last_sev,
    "additional_2_indicator_last_var": additional_2_last_var,
    "additional_2_indicator_last_severity": additional_2_last_sev,
}
if selected_language == "French":
    parameters = generate_parameters_FR(param_state)
    doc_parameter_output = generate_word_document_FR(parameters)
else:
    parameters = generate_parameters(param_state)
    doc_parameter_output = generate_word_document(parameters)
with open(os.path.join(out_dir, "Parameters_Input_Document.docx"), "wb") as f:
    f.write(doc_parameter_output.getvalue())


if ocha_data is not None:
    (indicator_barrier4_list,indicator_barrier_list,severity_admin_status_list, dimension_admin_status_list, severity_female_list, severity_male_list, factor_category,  pin_per_admin_status, dimension_per_admin_status,indicator_per_admin_status,
    female_pin_per_admin_status, male_pin_per_admin_status, 
    pin_per_admin_status_girl, pin_per_admin_status_boy,pin_per_admin_status_ece, pin_per_admin_status_primary, pin_per_admin_status_upper_primary, pin_per_admin_status_secondary, 
    Tot_PiN_JIAF, Tot_Dimension_JIAF, final_overview_df,final_overview_df_OCHA, 
    final_overview_dimension_df,final_overview_dimension_df_in_need,
    Tot_PiN_by_admin,
    country_label) = calculatePIN (country, edu_data_severity, household_data, choice_data, survey_data, ocha_data,mismatch_ocha_data,
                                                                                    access_var, teacher_disruption_var, idp_disruption_var, armed_disruption_var,natural_hazard_var,
                                                                                    barrier_var, selected_severity_4_barriers, selected_severity_5_barriers,
                                                                                    age_var, gender_var,
                                                                                    label, 
                                                                                    admin_var, vector_cycle, start_school, status_var,
                                                                                    host_value, idp_value, returnee_value, refugee_value, other_value,
                                                                                    mismatch_admin,
                                                                                    selected_language= selected_language, hybrid_country=hybrid_country)




    print("after calculatePIN")

    # Create the Excel files
    label_total_pin_sheet = "PiN TOTAL"


    if selected_language == "French":
        ocha_excel = create_output(
            country_label,
            Tot_PiN_JIAF,
            final_overview_df,
            final_overview_df_OCHA,
            label_total_pin_sheet,
            admin_var,
            ocha=True,
            tot_severity=Tot_PiN_by_admin,
            selected_language=selected_language,
            parameters=parameters,
            ocha_data=ocha_data
        )
    else:
        ocha_excel = create_output(
            country_label,
            Tot_PiN_JIAF,
            final_overview_df,
            final_overview_df_OCHA,
            label_total_pin_sheet,
            admin_var,
            ocha=True,
            tot_severity=Tot_PiN_by_admin,
            selected_language=selected_language,
            parameters=parameters,
            ocha_data=ocha_data
        )

    print("after create_output")
    
   

    #dimension_jiaf_excel = create_output(Tot_Dimension_JIAF, final_overview_dimension_df, "By dimension TOTAL",   admin_var, dimension= True, ocha= False)
    #dimension_ocha_excel = create_output(Tot_Dimension_JIAF, final_overview_dimension_df, "By dimension TOTAL",  admin_var, dimension= True, ocha= True)
    print('============================================================================================================================================')
    print('============================================================================================================================================')
    print('============================================================================================================================================')
    print('============================================================================================================================================')
    print(final_overview_df)

    if selected_language == 'English':
        doc_output = create_snapshot_PiN(country_label, final_overview_df, final_overview_df_OCHA,final_overview_dimension_df, final_overview_dimension_df_in_need, selected_language=selected_language)

    if selected_language == 'French':
        doc_output = create_snapshot_PiN_FR(country_label, final_overview_df, final_overview_df_OCHA,final_overview_dimension_df, final_overview_dimension_df_in_need,selected_language=selected_language)




        # This returns a dict of BytesIOs keyed by the column name
    maps = make_map_severity(country, Tot_PiN_by_admin, hpc_df=ocha_data)

        # Now write each out to disk (or do whatever you want with the in‐memory PNGs)
    for layer, buf in maps.items():
        fname = os.path.join(out_dir, f"{layer.replace(' ', '_')}.png")
        with open(fname, "wb") as f:
            f.write(buf.getvalue())


    ##   ***********************************    save for intermediate check:
    file_path_pin_test1 = os.path.join(out_dir, '01_pin_sev4.xlsx')
    file_path_pin_test2 = os.path.join(out_dir, '01_pin_barrier.xlsx')



    file_path_pin_1 = os.path.join(out_dir, '01_pin_percentage.xlsx')
    file_path_dimension_1 = os.path.join(out_dir, '01_dimension_percentage.xlsx')
    file_path_pin_female_1 = os.path.join(out_dir, '0a_pin_female_percentage.xlsx')
    file_path_pin_male_1 = os.path.join(out_dir, '0a_pin_male_percentage.xlsx')
    file_path_factor = os.path.join(out_dir, '02_factor_strata.xlsx')
    file_path_pin_2 = os.path.join(out_dir, '03_pin_percentage_total_OCHA.xlsx')
    file_path_pin_female_2a = os.path.join(out_dir, '0b_female_pin_percentage_total_OCHA.xlsx')
    file_path_pin_male_2a = os.path.join(out_dir, '0b_male_pin_percentage_total_OCHA.xlsx')
    file_path_dimension_2 = os.path.join(out_dir, '03_dimension_percentage_total_OCHA.xlsx')
    file_path_indicator_2 = os.path.join(out_dir, '03_indicator_percentage_total_OCHA.xlsx')

    file_path_factor_girl3= os.path.join(out_dir, '04_pin_factor_girl.xlsx')
    file_path_factor_boy3= os.path.join(out_dir, '04_pin_factor_boy.xlsx')
    file_path_factor_ece3= os.path.join(out_dir, '04_pin_factor_ECE.xlsx')
    file_path_factor_primary3= os.path.join(out_dir, '04_pin_factor_primary.xlsx')
    file_path_factor_uprimary3= os.path.join(out_dir, '04_pin_factor_upperprimary.xlsx')
    file_path_factor_secondary3= os.path.join(out_dir, '04_pin_factor_secondary.xlsx')

    file_path_overview= os.path.join(out_dir, '05_pin_overview.xlsx')
    file_path_overview_OCHA= os.path.join(out_dir, '05_pin_overview_OCHA.xlsx')

    file_path_dimension_overview= os.path.join(out_dir, '05_dimension_overview.xlsx')
    file_path_dimension_overview_in_need= os.path.join(out_dir, '05_dimension_overview_in_need.xlsx')


    file_path_pin_tot_by_admin = os.path.join(out_dir, '06_pin_tot_by_admin_area_severity.xlsx')


    # Create an Excel writer object
    with pd.ExcelWriter(file_path_pin_test1) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in indicator_barrier4_list.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)

    # Create an Excel writer object
    with pd.ExcelWriter(file_path_pin_test2) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in indicator_barrier_list.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)


    # Create an Excel writer object
    with pd.ExcelWriter(file_path_pin_1) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in severity_admin_status_list.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)
    with pd.ExcelWriter(file_path_dimension_1) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in dimension_admin_status_list.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)

    with pd.ExcelWriter(file_path_pin_female_1) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in severity_female_list.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)
    with pd.ExcelWriter(file_path_pin_male_1) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in severity_male_list.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)
    with pd.ExcelWriter(file_path_factor) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in factor_category.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)

    with pd.ExcelWriter(file_path_pin_2) as writer:
    # Iterate over each category and DataFrame in the dictionary
        for category, df in pin_per_admin_status.items():
        # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)
    with pd.ExcelWriter(file_path_dimension_2) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in dimension_per_admin_status.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)

    with pd.ExcelWriter(file_path_indicator_2) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in indicator_per_admin_status.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)



    with pd.ExcelWriter(file_path_pin_female_2a) as writer:
    # Iterate over each category and DataFrame in the dictionary
        for category, df in female_pin_per_admin_status.items():
        # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)
    with pd.ExcelWriter(file_path_pin_male_2a) as writer:
    # Iterate over each category and DataFrame in the dictionary
        for category, df in male_pin_per_admin_status.items():
        # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)


    with pd.ExcelWriter(file_path_factor_girl3) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in pin_per_admin_status_girl.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)
    with pd.ExcelWriter(file_path_factor_boy3) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in pin_per_admin_status_boy.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)
    with pd.ExcelWriter(file_path_factor_ece3) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in pin_per_admin_status_ece.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)

    with pd.ExcelWriter(file_path_factor_primary3) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in pin_per_admin_status_primary.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)
    with pd.ExcelWriter(file_path_factor_uprimary3) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in pin_per_admin_status_upper_primary.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)

    with pd.ExcelWriter(file_path_factor_secondary3) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in pin_per_admin_status_secondary.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)


    final_overview_df.to_excel(file_path_overview, index=False, engine='openpyxl')
    final_overview_df_OCHA.to_excel(file_path_overview_OCHA, index=False, engine='openpyxl')
    final_overview_dimension_df.to_excel(file_path_dimension_overview, index=False, engine='openpyxl')
    final_overview_dimension_df_in_need.to_excel(file_path_dimension_overview_in_need, index=False, engine='openpyxl')

    Tot_PiN_by_admin.to_excel(file_path_pin_tot_by_admin, index=False, engine='openpyxl')

    # Save the BytesIO objects to Excel files

    print('before saving')

    # Save ocha_excel
    with open(os.path.join(out_dir, "final__OCHA__platform_output.xlsx"), "wb") as f:
        f.write(ocha_excel.getbuffer())


    indicator_output = create_indicator_output(country_label, indicator_per_admin_status, admin_var=admin_var, ocha_data=ocha_data)
    print("after create_indicator_output")
    with open(os.path.join(out_dir, "final__indicator__platform_output.xlsx"), "wb") as f:
        f.write(indicator_output.getbuffer())    

    # Save dimension_jiaf_excel
    #with open(os.path.join(out_dir, "final__dimension_JIAF__platform_output.xlsx"), "wb") as f:
        #f.write(dimension_jiaf_excel.getbuffer())

    # Save dimension_ocha_excel
    #with open(os.path.join(out_dir, "final__dimension_OCHA__platform_output.xlsx"), "wb") as f:
        #f.write(dimension_ocha_excel.getbuffer())



    # Save the Word document to a file
    file_path = os.path.join(out_dir, "pin_snapshot_with_charts_and_text2.docx")
    with open(file_path, "wb") as f:
        f.write(doc_output.getvalue())





if no_ocha_data:
    (severity_admin_status_list, dimension_admin_status_list,
    indicator_per_admin_status,
    country_label) = calculatePIN_NO_OCHA_2025 (country, edu_data_severity, household_data, choice_data, survey_data,mismatch_ocha_data,
        access_var, teacher_disruption_var, idp_disruption_var, armed_disruption_var,natural_hazard_var,
        barrier_var, selected_severity_4_barriers, selected_severity_5_barriers,
        age_var, gender_var,
        label, 
        admin_var, vector_cycle, start_school, status_var,
        host_value, idp_value, returnee_value, refugee_value, other_value,
        mismatch_admin,
        selected_language= selected_language)
    
    indicator_output = create_indicator_output_no_ocha(country_label, indicator_per_admin_status, admin_var=admin_var, selected_language=selected_language)
    pin_percentage_output    =     create_pin_raw_output(country_label, severity_admin_status_list, admin_var=admin_var, selected_language=selected_language)


    with open(os.path.join(out_dir, "no_ocha__indicator__platform_output.xlsx"), "wb") as f:
        f.write(indicator_output.getbuffer())   
    with open(os.path.join(out_dir, "no_ocha__pin_percentage__platform_output.xlsx"), "wb") as f:
        f.write(pin_percentage_output.getbuffer())      
     
    file_path_pin_no_ocha = os.path.join(out_dir, 'no_ocha_pin_percentage.xlsx')
    file_path_no_ocha_dimension = os.path.join(out_dir, 'no_ocha_dimension_percentage.xlsx')
    file_path_no_ocha_pin_by_indicator = os.path.join(out_dir, 'no_ocha_pin_by_indicator.xlsx')

    with pd.ExcelWriter(file_path_pin_no_ocha) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in severity_admin_status_list.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)

    with pd.ExcelWriter(file_path_no_ocha_dimension) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in dimension_admin_status_list.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)

    with pd.ExcelWriter(file_path_no_ocha_pin_by_indicator) as writer:
        # Iterate over each category and DataFrame in the dictionary
        for category, df in indicator_per_admin_status.items():
            # Write the DataFrame to a sheet named after the category
            df.to_excel(writer, sheet_name=category, index=False)            


# --- archive this run (single runs only: run_all_cases.py archives batch runs itself, including the log)
if not os.environ.get("PIN_CASE"):
    from src.run_archive import make_run_archive
    zip_path = make_run_archive(ACTIVE_CASE, cfg, "success", run_started, time.time(),
                                archive_inputs=run_config.ARCHIVE_INPUTS)
    print(f"archived: {zip_path}")
