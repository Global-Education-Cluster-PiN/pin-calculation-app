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
from src.clean_dataset import clean_make_dataset
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

from docx import Document
from docx.shared import Pt, RGBColor
import matplotlib.pyplot as plt
from docx.shared import Inches
import os, glob




################################################
##           input from thee user             ##
################################################



hybrid_country= False
step_2_hpc= False


## BFA 2026
country_code="BFA"
status_var = 'pop_group'
access_var = 'edu_access'
teacher_disruption_var = 'edu_teachers'
idp_disruption_var = 'edu_displaced'
armed_disruption_var = 'no_indicator'#'edu_disrupted_occupation'no_indicator
natural_hazard_var = 'no_indicator'
natural_hazard_var_sev = None
additional_last_var =  'edu_incident_trajet'
additional_last_sev = 4
additional_2_last_var = 'edu_incident_ecol'
additional_2_last_sev = 4
barrier_var = 'edu_barriers'
selected_severity_4_barriers = ["Risques de protection à l’école (tels que le harcèlement physique et verbal, risque de viol, les attaques contre les écoles ou d’autres incidents de protection)",
"Risques de protection pendant le trajet vers l’école (tels que les incidents de harcèlement physique et verbal, risque de viol ou d’autres incidents de protection)",
"L’enfant doit travailler à la maison ou dans la ferme du ménage (c'est-à-dire qu'il ne gagne pas de revenu pour ces activités, mais peut permettre à d'autres membres de la famille de gagner un revenu)",
"L'enfant participe à des activités génératrices de revenus en dehors du ménage",
"Mariage, fiançailles",                                                       
]
selected_severity_5_barriers = ["Grossesse",
"Une interdiction empêche l'enfant d'aller à l'école"
]
#"---> None of the listed barriers <---"
#"Child is associated with armed forces or armed groups "
age_var = 'sne_enfant_ind_age'
gender_var = 'sne_enfant_ind_gender'
start_school = 'September'
country= 'Burkina Faso -- BFA'

# selected_language = 'label::english (en)'
selected_language = 'label::French'

#admin_var = 'Admin_3: Townships'#'Admin_2: Regions'
 
# 'Admin_3: Townships'
admin_var = 'admin2'#'Admin_2: Regions'
 
# 'Admin_3: Townships'
#admin_var = 'Admin_1: States/Regions'#'Admin_2: Regions' 

vector_cycle = [11,15]
single_cycle = (vector_cycle[1] == 0)
primary_start = 6
secondary_end = 17
label = 'label::French'

# Path to your Excel file
excel_path = 'input/BFA/REACH I BFA I 2025 MSNA-eduPlatform.xlsx'
excel_path_ocha = 'input/BFA/BFA_ocha_FINAL__1909.xlsx'
#excel_path_ocha = 'input/test_ocha.xlsx'

# Load the Excel file
xls = pd.ExcelFile(excel_path, engine='openpyxl')
# Print all sheet names (optional)
print(xls.sheet_names)
# Dictionary to hold your dataframes
dfs = {}
# Read each sheet into a dataframe
for sheet_name in xls.sheet_names:
    dfs[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)

# Access specific dataframes
edu_data = dfs['indvidual']
household_data = dfs['main']
survey_data = dfs['survey']
choice_data = dfs['choices']

ocha_xls = pd.ExcelFile(excel_path_ocha, engine='openpyxl')

# Read specific sheets into separate dataframes
ocha_data = pd.read_excel(ocha_xls, sheet_name='ocha')  # 'ocha' sheet
mismatch_ocha_data = pd.read_excel(ocha_xls, sheet_name='scope-fix')  # 'scope-fix' sheet
mismatch_admin = True




##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
#############################################################################        CALCULATION PIN              ################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################
##################################################################################################################################################################################################################

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

status_var = "pop_status_group"
age_var = "ind_age"
gender_var = "ind_gender"
barrier_var = "edu_barrier_final"

edu_data_severity, drop_msg = add_severity(country,
                                edu_data,
                                household_data,
                                choice_data,
                                survey_data,
                                access_var,
                                teacher_disruption_var,
                                idp_disruption_var,
                                armed_disruption_var,
                                natural_hazard_var,
                                natural_hazard_var_sev,
                                additional_last_var,
                                additional_last_sev,
                                additional_2_last_var,
                                additional_2_last_sev,
                                barrier_var,
                                selected_severity_4_barriers,
                                selected_severity_5_barriers,
                                age_var,
                                gender_var,
                                label,
                                admin_var,
                                vector_cycle,
                                start_school,
                                status_var,
                                selected_language=selected_language)



if drop_msg:
    print(drop_msg)

out_dir = os.path.join('output_validation', country_code)
os.makedirs(out_dir, exist_ok=True)
edu_data_severity.to_excel(os.path.join(out_dir, '00_edu_data_with_severity.xlsx'), index=False, engine='openpyxl')


##################################################################################################################################################################################################################
#############################################################################        FINAL OUTPUTS (same steps as page 3)        ################################################################################
##################################################################################################################################################################################################################

# Population-group mapping asked on page 2: values from your status column (None if not present)
host_value, idp_value, returnee_value, refugee_value, other_value = "non_pdi", "pdi", None, None, None

(_, _, _, _, _, _, _, _, _, indicator_per_admin_status, _, _, _, _, _, _, _, _,
 Tot_PiN_JIAF, _, final_overview_df, final_overview_df_OCHA,
 final_overview_dimension_df, final_overview_dimension_df_in_need,
 Tot_PiN_by_admin, country_label) = calculatePIN(
    country, edu_data_severity, household_data, choice_data, survey_data, ocha_data, mismatch_ocha_data,
    access_var, teacher_disruption_var, idp_disruption_var, armed_disruption_var, natural_hazard_var,
    barrier_var, selected_severity_4_barriers, selected_severity_5_barriers,
    age_var, gender_var, label, admin_var, vector_cycle, start_school, status_var,
    host_value, idp_value, returnee_value, refugee_value, other_value,
    mismatch_admin, selected_language, hybrid_country)

if selected_language == "French":
    snapshot = create_snapshot_PiN_FR(country_label, final_overview_df, final_overview_df_OCHA,
                                      final_overview_dimension_df, final_overview_dimension_df_in_need,
                                      selected_language=selected_language, step1=False)
else:
    snapshot = create_snapshot_PiN(country_label, final_overview_df, final_overview_df_OCHA,
                                   final_overview_dimension_df, final_overview_dimension_df_in_need,
                                   selected_language=selected_language)

outputs = {
    f"PiN_results_{country_label}.xlsx": create_output(
        country_label, Tot_PiN_JIAF, final_overview_df, final_overview_df_OCHA, "PiN TOTAL",
        admin_var, ocha=True, tot_severity=Tot_PiN_by_admin, selected_language=selected_language),
    f"PiN_by_indicator_{country_label}.xlsx": create_indicator_output(
        country_label, indicator_per_admin_status, admin_var=admin_var),
    f"PiN_snapshot_{country_label}.docx": snapshot,
}
for layer, buf in make_map_severity(country, pin_data=Tot_PiN_by_admin, hpc_df=ocha_data).items():
    outputs[f"{country_label}_{layer.replace(' ', '_')}.png"] = buf

for name, buf in outputs.items():
    with open(os.path.join(out_dir, name), "wb") as f:
        f.write(buf.getvalue())
    print("saved", os.path.join(out_dir, name))
