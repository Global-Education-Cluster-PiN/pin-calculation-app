import pandas as pd
#import fuzzywuzzy
from fuzzywuzzy import process, fuzz
import numpy as np
import datetime
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Border, Side, Font, Alignment
from openpyxl.cell.cell import MergedCell  # Import MergedCell
import re


int_2 = '2.0'
int_3 = '3.0'
int_4 = '4.0'
int_5 = '5.0'
label_perc2 = '% severity levels 1-2'
label_perc3 = '% severity level 3'
label_perc4 = '% severity level 4'
label_perc5 = '% severity level 5'
label_tot2 = '# severity levels 1-2'
label_tot3 = '# severity level 3'
label_tot4 = '# severity level 4'
label_tot5 = '# severity level 5'
label_perc_tot = '% Tot PiN (severity levels 3-5)'
label_tot = '# Tot PiN (severity levels 3-5)'
label_admin_severity = 'Area severity'
label_tot_population = 'TotN'

int_acc = 'access'
int_agg= 'aggravating circumstances'
int_lc = 'learning condition'
int_penv = 'protected environment'
int_out = 'Not in need'
label_perc_acc = '% Access'
label_perc_agg= '% Aggravating circumstances'
label_perc_lc = '% Learning conditions'
label_perc_penv = '% Protected environment'
label_perc_out = '% Not in need'
label_tot_acc = '# Access'
label_tot_agg= '# Aggravating circumstances'
label_tot_lc = '# Learning conditions'
label_tot_penv = '# Protected environment'
label_tot_out = '# Not in need'
label_dimension_perc_tot = '% Tot in PiN Dimensions'
label_dimension_tot = '# Tot in PiN Dimensions'
label_dimension_tot_population = 'TotN'





##--------------------------------------------------------------------------------------------
def calculate_age_correction(start_month, collection_month):
    # Create a dictionary to map the first three letters of month names to their numeric equivalents
    month_lookup = {datetime.date(2000, i, 1).strftime('%b').lower(): i for i in range(1, 13)}
    
    # Convert month names to their numeric equivalents using the predefined lookup
    start_month_num = month_lookup[start_month.strip()[:3].lower()]
    
    # Adjust the start month number for a school year starting in the previous calendar year
    adjusted_start_month_num = start_month_num - 12 if start_month_num > 6 else start_month_num
    
    # Determine if the age correction should be applied based on the month difference
    age_correction = (collection_month - adjusted_start_month_num) > 6
    return age_correction

##--------------------------------------------------------------------------------------------
def find_matching_choices(choices_df, barriers_list, label_var):
    # List to hold the results
    results = []
    
    # Iterate over each barrier in the list
    for barrier in barriers_list:
        # Filter choices where the label_var matches the current barrier
        matched_choices = choices_df[choices_df[label_var] == barrier]
        
        # If no matches are found, add a 'notfound' entry
        if matched_choices.empty:
            result_entry = {'name': 'notfound', 'label': barrier}
            results.append(result_entry)
        else:
            # For each matched choice, create an entry in the results list
            for _, choice in matched_choices.iterrows():
                result_entry = {'name': choice['name'], 'label': barrier}
                results.append(result_entry)
    
    return results

        

##--------------------------------------------------------------------------------------------
def calculate_severity(country, gender, age, access, barrier,
                       armed_disruption, natural_hazard, additional_ind,additional_2_ind,
                       natural_hazard_severity, additional_ind_severity,additional_2_ind_severity,
                       idp_disruption, teacher_disruption,
                       names_severity_4, names_severity_5, full_GEC_compliant):

    # Helper function to safely normalize string inputs
    def normalize(input_value):
        if isinstance(input_value, str):
            return input_value.lower()
        elif isinstance(input_value, (int, float)):  # Handle numeric values directly
            return input_value
        return ""  # Default to empty string if input is not a string or number

    # Normalize the input to handle different cases and languages
    normalized_age = normalize(age)
    normalized_gender = normalize(gender)
    normalized_access = normalize(access)
    normalized_armed_disruption = normalize(armed_disruption) if armed_disruption is not None else None
    normalized_natural_hazard = normalize(natural_hazard) if natural_hazard is not None else None
    normalized_additional_ind = normalize(additional_ind) if additional_ind is not None else None
    normalized_additional_2_ind = normalize(additional_2_ind) if additional_2_ind is not None else None

    normalized_idp_disruption = normalize(idp_disruption)
    normalized_teacher_disruption = normalize(teacher_disruption)

    # Normalize to handle English and French variations of "yes" and "no"
    yes_answers = ['yes', 'oui', 1, '1', '1. yes', '1. Yes']  # keep lenient
    no_answers  = ['no', 'non', 0, '0', '2. no', '2. No']

    # full_GEC_compliant=True (GEC compliant): out-of-school girls above 12 are in severity 5
    # full_GEC_compliant=False (not GEC compliant): standard rules, as for any other country
    if country == 'Afghanistan -- AFG' and full_GEC_compliant:
        if normalized_access in no_answers:
            if barrier in names_severity_5:
                return 5
            elif normalized_gender == 'female' and (isinstance(normalized_age, (int, float)) and normalized_age > 12):
                return 5
            elif barrier in names_severity_4:
                return 4
            else:
                return 3

        elif normalized_access in yes_answers:
            sev = 2

            if (normalized_armed_disruption is not None) and (normalized_armed_disruption in yes_answers):
                return 5

            if normalized_idp_disruption in yes_answers:
                sev = max(sev, 4)

            if normalized_teacher_disruption in yes_answers:
                sev = max(sev, 3)

            if (normalized_natural_hazard is not None) and (normalized_natural_hazard in yes_answers):
                if isinstance(natural_hazard_severity, int):
                    sev = max(sev, natural_hazard_severity)
                else:
                    sev = max(sev, 3)

            if (normalized_additional_ind is not None) and (normalized_additional_ind in yes_answers):
                if isinstance(additional_ind_severity, int):
                    sev = max(sev, additional_ind_severity)
                else:
                    sev = max(sev, 3)
            # Additional indicator → use its configured severity (3 or 4)
            if (normalized_additional_2_ind is not None) and (normalized_additional_2_ind in yes_answers):
                if isinstance(additional_2_ind_severity, int):
                    sev = max(sev, additional_2_ind_severity)
                else:
                    sev = max(sev, 3)  # conservative default             

            return sev

        return None  # Default fallback

    else:
        # Standard rules
        # Main severity calculation logic
        if normalized_access in no_answers:
            if barrier in names_severity_5:
                return 5
            elif barrier in names_severity_4:
                return 4
            else:
                return 3

        elif normalized_access in yes_answers:
            # Accumulator pattern (start from 2 and raise as triggers fire)
            sev = 2

            # Armed disruption → immediate 5 if yes
            if (normalized_armed_disruption is not None) and (normalized_armed_disruption in yes_answers):
                return 5

            # IDP disruption → at least 4
            if normalized_idp_disruption in yes_answers:
                sev = max(sev, 4)

            # Teacher disruption → at least 3
            if normalized_teacher_disruption in yes_answers:
                sev = max(sev, 3)

            # Natural hazard → use its configured severity (3 or 4)
            if (normalized_natural_hazard is not None) and (normalized_natural_hazard in yes_answers):
                if isinstance(natural_hazard_severity, int):
                    sev = max(sev, natural_hazard_severity)
                else:
                    sev = max(sev, 3)  # conservative default

            # Additional indicator → use its configured severity (3 or 4)
            if (normalized_additional_ind is not None) and (normalized_additional_ind in yes_answers):
                if isinstance(additional_ind_severity, int):
                    sev = max(sev, additional_ind_severity)
                else:
                    sev = max(sev, 3)  # conservative default
            # Additional indicator → use its configured severity (3 or 4)
            if (normalized_additional_2_ind is not None) and (normalized_additional_2_ind in yes_answers):
                if isinstance(additional_2_ind_severity, int):
                    sev = max(sev, additional_2_ind_severity)
                else:
                    sev = max(sev, 3)  # conservative default        

            return sev

        return None  # Default fallback



##--------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------

##--------------------------------------------------------------------------------------------
def add_indicator_columns(data, access_var, teacher_disruption_var, natural_hazard_var, idp_disruption_var, armed_disruption_var, barrier_var, names_severity_4, names_severity_5,
                          natural_hazard_var_sev=None, additional_last_var='no_indicator', additional_last_sev=None,
                          additional_2_last_var='no_indicator', additional_2_last_sev=None):
    """
    Add indicator columns to the dataset and set their values based on conditions,
    taking severity into account.

    Args:
        data (pd.DataFrame): The input DataFrame.
        access_var (str): Column name for access indicator.
        teacher_disruption_var (str): Column name for teacher disruption indicator.
        natural_hazard_var (str): Column name for natural hazard indicator.
        idp_disruption_var (str): Column name for IDP disruption indicator.
        armed_disruption_var (str): Column name for armed disruption indicator.
        barrier_var (str): Column name for barrier indicator.
        names_severity_4 (list): List of barrier names for severity 4.
        names_severity_5 (list): List of barrier names for severity 5.
        natural_hazard_var_sev, additional_last_sev, additional_2_last_sev: severity (3 or 4) of the natural hazard
            and additional indicators, as used in calculate_severity.
        additional_last_var, additional_2_last_var (str): Column names for the additional indicators.

    Returns:
        pd.DataFrame: The updated DataFrame with new indicator columns.
    """

    # Helper function to normalize string inputs
    def normalize(input_value):
        if isinstance(input_value, str):
            return input_value.lower()
        elif isinstance(input_value, (int, float)):  # Handle numeric values directly
            return input_value
        return ""  # Default to empty string if input is not a string or number

    # Define the conditions for yes and no answers
    yes_answers = ['yes', 'oui', 1, '1', '1. yes', '1. Yes']  # keep lenient
    no_answers  = ['no', 'non', 0, '0', '2. no', '2. No']

    no_indicator = 'no_indicator'

    # Initialize new columns with 0
    data['indicator.access'] = 0
    data['indicator.teacher'] = 0
    data['indicator.hazard'] = 0
    data['indicator.idp'] = 0
    data['indicator.occupation'] = 0
    data['indicator.barrier4'] = 0
    data['indicator.barrier5'] = 0

    # Apply conditions with severity filtering
    data['indicator.access'] = data.apply(
        lambda row: 1 if row['severity_category'] == 3 and normalize(row[access_var]) in no_answers else 0, axis=1
    )

    # Severity of the natural hazard and additional indicators, as in calculate_severity (3 when not set)
    hazard_sev = natural_hazard_var_sev if isinstance(natural_hazard_var_sev, int) else 3
    additional_sev = additional_last_sev if isinstance(additional_last_sev, int) else 3
    additional_2_sev = additional_2_last_sev if isinstance(additional_2_last_sev, int) else 3

    def is_yes(row, var):
        return var != no_indicator and normalize(row[var]) in yes_answers

    # In-school children: each child at severity 3 or 4 is counted under exactly one indicator, the first that applies:
    #   severity 3: teacher > hazard > additional > additional2
    #   severity 4: idp shelter > hazard > additional > additional2
    def in_school_indicator(row):
        if normalize(row[access_var]) not in yes_answers:
            return None
        if row['severity_category'] == 3:
            candidates = [
                ('teacher', is_yes(row, teacher_disruption_var)),
                ('hazard', hazard_sev == 3 and is_yes(row, natural_hazard_var)),
                ('additional', additional_sev == 3 and is_yes(row, additional_last_var)),
                ('additional2', additional_2_sev == 3 and is_yes(row, additional_2_last_var)),
            ]
        elif row['severity_category'] == 4:
            candidates = [
                ('idp', is_yes(row, idp_disruption_var)),
                ('hazard4', hazard_sev == 4 and is_yes(row, natural_hazard_var)),
                ('additional4', additional_sev == 4 and is_yes(row, additional_last_var)),
                ('additional2_4', additional_2_sev == 4 and is_yes(row, additional_2_last_var)),
            ]
        else:
            return None
        return next((name for name, applies in candidates if applies), None)

    in_school = data.apply(in_school_indicator, axis=1)
    for name in ['teacher', 'hazard', 'additional', 'additional2', 'idp', 'hazard4', 'additional4', 'additional2_4']:
        data[f'indicator.{name}'] = (in_school == name).astype(int)

    # in-school children only: out-of-school children at severity 5 are counted under their barrier
    if armed_disruption_var != no_indicator:
        data['indicator.occupation'] = data.apply(
            lambda row: 1 if row['severity_category'] == 5 and normalize(row[access_var]) in yes_answers
                             and normalize(row[armed_disruption_var]) in yes_answers else 0, axis=1
        )

    data['indicator.barrier4'] = data.apply(
        lambda row: 1 if row['severity_category'] == 4 and row[barrier_var] in names_severity_4 else 0, axis=1
    )

    data['indicator.barrier5'] = data.apply(
        lambda row: 1 if row['severity_category'] == 5 and row[barrier_var] in names_severity_5 else 0, axis=1
    )

    return data


##--------------------------------------------------------------------------------------------
def add_indicator_columns_for_EMIS(data, access_var, teacher_disruption_var, natural_hazard_var, idp_disruption_var, armed_disruption_var, barrier_var, names_severity_4, names_severity_5):
    # Helper function to normalize string inputs
    def normalize(input_value):
        if isinstance(input_value, str):
            return input_value.lower()
        elif isinstance(input_value, (int, float)):  # Handle numeric values directly
            return input_value
        return ""  # Default to empty string if input is not a string or number

    # Define the conditions for yes and no answers
    yes_answers = ['yes', 'oui', 1, '1', '1. Yes', '1. yes', ]
    no_answers = ['no', 'non', 0, '0','2. No' , '2. no' ]

    no_indicator = 'no_indicator'

    # Initialize new columns with 0
    data['var.access'] = 0
    data['var.teacher'] = 0
    data['var.hazard'] = 0
    data['var.idp'] = 0
    data['var.occupation'] = 0
    data['var.barrier4'] = 0
    data['var.barrier5'] = 0

    # Apply conditions with severity filtering
    data['var.access'] = data.apply(
        lambda row: 1 if normalize(row[access_var]) in yes_answers else 0, axis=1
    )

    if teacher_disruption_var != no_indicator:
        data['var.teacher'] = data.apply(
            lambda row: 1 if row['severity_category'] not in [4, 5] and normalize(row[teacher_disruption_var]) in yes_answers else 0, axis=1
        )

    if natural_hazard_var != no_indicator:
        data['var.hazard'] = data.apply(
            lambda row: 1 if row['severity_category'] not in [4, 5] and (teacher_disruption_var == no_indicator or row[teacher_disruption_var] != 1) and normalize(row[natural_hazard_var]) in yes_answers else 0, axis=1
        )

    if idp_disruption_var != no_indicator:
        data['var.idp'] = data.apply(
            lambda row: 1 if row['severity_category'] == 4 and row['severity_category'] != 5 and normalize(row[idp_disruption_var]) in yes_answers else 0, axis=1
        )

    if armed_disruption_var != no_indicator:
        data['var.occupation'] = data.apply(
            lambda row: 1 if row['severity_category'] == 5 and normalize(row[armed_disruption_var]) in yes_answers else 0, axis=1
        )

    data['var.barrier4'] = data.apply(
        lambda row: 1 if row['severity_category'] == 4 and row[barrier_var] in names_severity_4 else 0, axis=1
    )

    data['var.barrier5'] = data.apply(
        lambda row: 1 if row['severity_category'] == 5 and row[barrier_var] in names_severity_5 else 0, axis=1
    )

    return data
##--------------------------------------------------------------------------------------------
def assign_dimension_pin(access, severity):
    # Normalize access status
    def normalize(input_string):
        if isinstance(input_string, str):
            return input_string.lower()
        return ""  # Default to empty string if input is not a string

    # Normalize the input to handle different cases and languages
    normalized_access = normalize(access)

    # Normalize to handle English and French variations of "yes" and "no"
    yes_answers = ['yes', 'oui', 1, '1', '1. Yes','1. yes']
    no_answers = ['no', 'non', 0, '0','2. No' , '2. no']

    # Mapping severity to dimension labels
    if normalized_access in no_answers:
        if severity in [4, 5]: return 'aggravating circumstances'
        elif severity == 3: return 'access'
    elif normalized_access in yes_answers:
        if severity == 3: return 'learning condition'
        if severity in [4, 5]: return 'protected environment'    
        if severity == 2: return 'Not in need'   
    
    return None  # Default fallback in case none of the conditions are met         

##--------------------------------------------------------------------------------------------
def print_subtables(severity_admin_status, pop_group_var):
    # Get the level number for pop_group_var
    level_number = severity_admin_status.index.names.index(pop_group_var)
    
    # Get unique groups
    unique_groups = severity_admin_status.index.get_level_values(level_number).unique()
    
    # Iterate and print subtables
    for group in unique_groups:
        subtable = severity_admin_status.xs(group, level=level_number)
        print(f"\nSubtable for {pop_group_var} = {group}")
        print(subtable)
        print("\n" + "-"*50 + "\n")


##--------------------------------------------------------------------------------------------
def custom_to_datetime(date_str):
    try:
        # Try the default date parsing first
        return pd.to_datetime(date_str, errors='coerce')
    except:
        try:
            # Handle the 'Y-m-d H:M:S.f+TZ' format
            return pd.to_datetime(date_str, format='%Y-%m-%dT%H:%M:%S.%f%z', errors='coerce')
        except:
            try:
                # Handle the 'Y-m-d H:M:S.f' format without time zone
                return pd.to_datetime(date_str, format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')
            except:
                try:
                    # Handle the 'dd/mm/yyyy' format
                    return pd.to_datetime(date_str, format='%d/%m/%Y', errors='coerce')
                except:
                    # Return NaT if all parsing attempts fail
                    return pd.NaT

##--------------------------------------------------------------------------------------------
def assign_school_cycle(edu_age_corrected, single_cycle=False, lower_primary_start_var=6, lower_primary_end_var=13, upper_primary_end_var=None):

    if lower_primary_start_var == 6: primary_minus_one = 5
    else: primary_minus_one = 6
    if single_cycle:
        # If single cycle is True, handle as a primary to secondary without upper primary
        if lower_primary_start_var <= edu_age_corrected <= lower_primary_end_var:
            return 'primary'
        elif lower_primary_end_var + 1 <= edu_age_corrected <= 18:
            return 'secondary'
        elif edu_age_corrected == primary_minus_one: 
            return 'ECE'
        else:
            return 'out of school range'
    else:
        # If single cycle is False, handle lower primary, upper primary, and secondary phases
        if lower_primary_start_var <= edu_age_corrected <= lower_primary_end_var:
            return 'primary'
        elif upper_primary_end_var and lower_primary_end_var + 1 <= edu_age_corrected <= upper_primary_end_var:
            return 'intermediate level'
        elif upper_primary_end_var and upper_primary_end_var + 1 <= edu_age_corrected <= 18:
            return 'secondary'
        elif edu_age_corrected == primary_minus_one: 
            return 'ECE'
        else:
            return 'out of school range'
        
##--------------------------------------------------------------------------------------------
## finding admin        
def extract_number(col_name: str) -> int|None:
    nums = re.findall(r'\d+', col_name or "")
    return int(nums[-1]) if nums else None

def looks_like_pcode(series, min_fraction=0.8):
    p = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9]+$')
    vals = series.dropna().astype(str)
    if len(vals)==0: return False
    return (vals.str.match(p).sum() / len(vals)) >= min_fraction

def find_best_match(admin_target: str,
                    household_df,
                    similarity_threshold=70,
                    pcode_fraction=0.8,
                    fallback_threshold=50) -> str:
    cols = list(household_df.columns)
    target_num = extract_number(admin_target)

    # — Step 0: All columns that *share* that number in their name
    num_cols = [c for c in cols if extract_number(c)==target_num]

    # — Step 1: Among those, pick any with “code”
    code_cols = [c for c in num_cols if 'code' in c.lower()]
    if code_cols:
        candidates = code_cols
    elif num_cols:
        candidates = num_cols
    else:
        candidates = []

    # — Step 2: If we still have nothing, use your fuzzy + number + code logic:
    if not candidates:
        # fuzzy find “similar” by text
        base = re.sub(r'\d+','', admin_target).lower()
        similar = [c for c in cols
                   if fuzz.partial_ratio(base, re.sub(r'\d+','',c).lower())
                      >= similarity_threshold]

        # among “similar” pick same-number, then code, then rest
        same_num = [c for c in similar if extract_number(c)==target_num]
        code_in_same = [c for c in same_num if 'code' in c.lower()]

        if code_in_same:
            candidates = code_in_same
        elif same_num:
            candidates = same_num
        else:
            candidates = similar

    # — Step 3: fallback global fuzzy if we still have nothing
    if not candidates:
        matches = process.extract(admin_target, cols,
                                  scorer=fuzz.partial_ratio,
                                  limit=len(cols))
        candidates = [m[0] for m in matches if m[1]>=fallback_threshold]

    # — Step 4: If STILL nothing, just take the single best
    if not candidates:
        return process.extractOne(admin_target, cols)[0]

    # Debug print
    print("→ ordered candidates:", candidates)

    # — Step 5: pick first whose values *look* like P-codes
    for c in candidates:
        if looks_like_pcode(household_df[c], min_fraction=pcode_fraction):
            print(f"→ picking {c} (passed P-code check)")
            return c

    # — Step 6: fallback to single best fuzzy match
    print("→ none passed P-code check; falling back")
    return process.extractOne(admin_target, cols,
                              scorer=fuzz.partial_ratio)[0]
########################################################################################################################################
########################################################################################################################################
##############################################    PIN CALCULATION FUNCTION    ##########################################################
########################################################################################################################################
########################################################################################################################################
def add_severity(country,
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
                selected_language,
                full_GEC_compliant,
                barrier_match="label",
                stop_if_barrier_missing=False):
    # barrier_match: column of the choices sheet the severity 4/5 barriers are matched on: "label" (the `label`
    # column, as listed on the platform) or "name" (the choice names, local runs). stop_if_barrier_missing: stop
    # when a barrier is not found in that column (local runs), instead of leaving it out

    admin_target = admin_var
    pop_group_var = status_var


    # --------------------------------------------------------------------------------------------
    admin_levels_per_country = {
        'Afghanistan -- AFG': ['Admin_1: Region', 'Admin_2: Province', 'Admin_3: Districts'],
        'Burkina Faso -- BFA': ['Admin_1: Regions (Région)', 'Admin_2: Province', 'Admin_3: Department (Département)'],
        'Cameroon -- CMR': ['Admin_1', 'Admin_2', 'Admin_3'],
        'Central African Republic -- CAR': ['Admin_1: Prefectures (préfectures)', 'Admin_2: Sub-prefectures (sous-préfectures)', 'Admin_3: Communes'],
        'Democratic Republic of the Congo -- DRC': ['Admin_1: Provinces', 'Admin_2: Territories', 'Admin_3: Sectors/chiefdoms/communes'],
        'Haiti -- HTI': ['Admin_1: Departments (départements)', 'Admin_2: Arrondissements', 'Admin_3: Communes'],
        'Iraq -- IRQ': ['Admin_1: Governorates', 'Admin_2: Districts (aqḍyat)', 'Admin_3: Sub-districts (naḥiyat)'],
        'Kenya -- KEN': ['Admin_1: Counties', 'Admin_2: Sub-counties (kaunti ndogo)', 'Admin_3: Wards (mtaa)'],
        'Bangladesh -- BGD': ['Admin_1: Divisions (bibhag)', 'Admin_2: Districts (zila)', 'Admin_3: Upazilas'],
        'Lebanon -- LBN': ['Admin_1: Governorates', 'Admin_2: Districts (qaḍya)', 'Admin_3: Municipalities'],
        'Moldova -- MDA': ['Admin_1: Districts', 'Admin_2: Cities', 'Admin_3: Communes'],
        'Mali -- MLI': ['Admin_1: Régions', 'Admin_2: Cercles', 'Admin_3: Arrondissements'],
        'Mozambique -- MOZ': ['Admin_1: Provinces (provincias)', 'Admin_2: Districts (distritos)', 'Admin_3: Postos'],
        'Myanmar -- MMR': ['Admin_1: States/Regions', 'Admin_2: Districts', 'Admin_3: Townships'],
        'Niger -- NER': ['Admin_1: Régions ', 'Admin_2: Départements', 'Admin_3: Communes'],
        'Syria -- SYR': ['Admin_1: Governorates', 'Admin_2: Districts (mintaqah)', 'Admin_3: Subdistricts (nawaḥi)'],
        'Ukraine -- UKR': ['Admin_1: Oblasts', 'Admin_2: Raions', 'Admin_3: Hromadas'],
        'Somalia -- SOM': ['Admin_1: States', 'Admin_2: Regions', 'Admin_3: Districts']
    }



    ####### ** 1 **       ------------------------------ manipulation and join between H and edu data   ------------------------------------------     #######
    edu_uuid_column = "uuid"
    household_uuid_column =  "uuid"
    admin_var = "admin_hno"
    weight_column = "weights"


    # Get the admin levels for the specified country
    admin_levels = admin_levels_per_country.get(country, [])
    # Flatten the admin levels to extract just the terms (like 'Region', 'District', etc.)
    admin_keywords = [term.split(": ")[-1].lower() for term in admin_levels]
    # Create a list of all household data columns that contain 'admin' or any of the admin keywords
    admin_columns_from_household = [col for col in household_data.columns if 'admin' in col.lower() or any(keyword in col.lower() for keyword in admin_keywords)]
    # Make sure admin_var is not duplicated
    if admin_var in admin_columns_from_household:
        admin_columns_from_household.remove(admin_var)
    # Now add the admin columns to the columns to include, without duplicating
    columns_to_include = [household_uuid_column, admin_var, pop_group_var, 'month', 'weights'] + admin_columns_from_household
    # Ensure there are no duplicate column names in columns_to_include
    columns_to_include = list(set(columns_to_include))


    columns_to_drop = [col for col in columns_to_include if col in edu_data.columns and col != edu_uuid_column and col != household_uuid_column]
    edu_data = edu_data.drop(columns=columns_to_drop, errors='ignore')

    # ----> Perform the joint_by
    edu_data = pd.merge(edu_data, household_data[columns_to_include], left_on=edu_uuid_column, right_on=household_uuid_column, how='left')

    # --- Myanmar special case: create edu_ind_age_corrected = age_var - 1
    if country == "Myanmar -- MMR":
        # create/overwrite corrected age
        edu_data["edu_ind_age_corrected"] = pd.to_numeric(edu_data[age_var], errors="coerce") - 1
        # use corrected age going forward
        age_var = "edu_ind_age_corrected"


    edu_data['edu_age_corrected'] = edu_data.apply(lambda row: row[age_var] - 1 if calculate_age_correction(start_school, row['month']) else row[age_var], axis=1)

    single_cycle = (vector_cycle[1] == 0)
    if country != 'Afghanistan -- AFG': primary_start = 6
    else: primary_start = 7

    edu_data['school_cycle'] = edu_data['edu_age_corrected'].apply(
        lambda x: assign_school_cycle(
            x, 
            single_cycle=single_cycle, 
            lower_primary_start_var=primary_start, 
            lower_primary_end_var=vector_cycle[0], 
            upper_primary_end_var=vector_cycle[1] if not single_cycle else None
        )
    )
   
    if country != 'Afghanistan -- AFG':
        edu_data = edu_data[(edu_data['edu_age_corrected'] >= 5) & (edu_data['edu_age_corrected'] <= 17)]
    #elif    country == 'Haiti -- HTI':
        #edu_data = edu_data[(edu_data['edu_age_corrected'] >= 3) & (edu_data['edu_age_corrected'] <= 17)]          
    else:
        edu_data = edu_data[(edu_data['edu_age_corrected'] >= 6) & (edu_data['edu_age_corrected'] <= 17)]

    # full_GEC_compliant=False: girls keep their reported barrier
    if country == "Afghanistan -- AFG" and full_GEC_compliant:
        female_vals = {"female", "femme", "woman_girl", "feminin"}
        no_access_vals = {"no", "non", "0", 0}

        # ensure age is numeric for the comparison (> 12)
        age_num = pd.to_numeric(edu_data[age_var], errors="coerce")

        edu_data.loc[
            (edu_data[gender_var].astype(str).str.strip().str.lower().isin(female_vals)) &
            (age_num > 12) &
            (edu_data[access_var].isin(no_access_vals)),
            barrier_var
        ] = "ban"



    ####### ** 2 **       ------------------------------ severity definition and calculation ------------------------------------------     #######
   
    if barrier_match not in ("label", "name"):
        raise ValueError(f"barrier_match must be 'label' or 'name', not {barrier_match!r}")
    match_column = label if barrier_match == "label" else "name"
    severity_4_matches = find_matching_choices(choice_data, selected_severity_4_barriers, label_var=match_column)
    severity_5_matches = find_matching_choices(choice_data, selected_severity_5_barriers, label_var=match_column)
    missing_barriers = [entry['label'] for entry in severity_4_matches + severity_5_matches if entry['name'] == 'notfound']
    if missing_barriers and stop_if_barrier_missing:
        raise ValueError(
            f"Severity 4/5 barriers not found in the column '{match_column}' of the choices sheet: "
            + ", ".join(repr(b) for b in missing_barriers)
            + ". Check their spelling, or set \"barrier_match\" ('label' or 'name') in run_config.py.")
    print('severity_4_matches =======> ')
    print(selected_severity_4_barriers)
    print(severity_4_matches)

    names_severity_4 = [entry['name'] for entry in severity_4_matches]
    names_severity_5 = [entry['name'] for entry in severity_5_matches]

    print('access_var ' + access_var + " gender_var " , gender_var)

    edu_data['severity_category'] = edu_data.apply(lambda row: calculate_severity(
        country = country,
        gender = row[gender_var],
        age = row ['edu_age_corrected'],
        access=row[access_var], 
        barrier=row[barrier_var], 
        armed_disruption=row[armed_disruption_var] if armed_disruption_var != 'no_indicator' else None, 
        natural_hazard=row[natural_hazard_var] if natural_hazard_var != 'no_indicator' else None, 
        additional_ind=row[additional_last_var] if additional_last_var != 'no_indicator' else None, 
        additional_2_ind=row[additional_2_last_var] if additional_2_last_var != 'no_indicator' else None, 
        natural_hazard_severity= natural_hazard_var_sev if natural_hazard_var != 'no_indicator' else None, 
        additional_ind_severity=additional_last_sev if additional_last_var != 'no_indicator' else None,
        additional_2_ind_severity=additional_2_last_sev if additional_2_last_var != 'no_indicator' else None, 
        idp_disruption=row[idp_disruption_var] if idp_disruption_var != 'no_indicator' else None,
        teacher_disruption=row[teacher_disruption_var] if teacher_disruption_var != 'no_indicator' else None,
        #protection_at_school=row['e_incident_ecol'] if country == 'Burkina Faso -- BFA'  else None,
        #protection_to_school=row['e_incident_trajet'] if country == 'Burkina Faso -- BFA'  else None,
        names_severity_4=names_severity_4, 
        names_severity_5=names_severity_5,
        full_GEC_compliant=full_GEC_compliant

    ), axis=1)

    # Add the new column 'dimension_pin' to edu_data
    edu_data['dimension_pin'] = edu_data.apply(lambda row: assign_dimension_pin(
        access=row[access_var],
        severity= row['severity_category']
        ), axis=1)

    edu_data = add_indicator_columns(
        data=edu_data,
        access_var=access_var,
        teacher_disruption_var=teacher_disruption_var,
        natural_hazard_var=natural_hazard_var,
        idp_disruption_var=idp_disruption_var,
        armed_disruption_var=armed_disruption_var,
        barrier_var=barrier_var,
        names_severity_4=names_severity_4,
        names_severity_5=names_severity_5,
        natural_hazard_var_sev=natural_hazard_var_sev,
        additional_last_var=additional_last_var,
        additional_last_sev=additional_last_sev,
        additional_2_last_var=additional_2_last_var,
        additional_2_last_sev=additional_2_last_sev
    )

    edu_data = add_indicator_columns_for_EMIS(
        data=edu_data,
        access_var=access_var,
        teacher_disruption_var=teacher_disruption_var,
        natural_hazard_var=natural_hazard_var,
        idp_disruption_var=idp_disruption_var,
        armed_disruption_var=armed_disruption_var,
        barrier_var=barrier_var,
        names_severity_4=names_severity_4,
        names_severity_5=names_severity_5
    )
    # --- Drop rows where severity_category is missing AND edu_age_corrected == 17 ---
    age17 = pd.to_numeric(edu_data["edu_age_corrected"], errors="coerce").eq(17)

    sev_missing = (
        edu_data["severity_category"].isna()
        | edu_data["severity_category"].astype(str).str.strip().isin(["", "None", "nan"])
    )

    to_drop = age17 & sev_missing
    n_drop = int(to_drop.sum())

    drop_msg = None

    if n_drop > 50:
        edu_data = edu_data.loc[~to_drop].copy()
        drop_msg = (f"Dropped {to_drop.sum()} Rows with an empty severity_category and edu_age_corrected == 17 likely indicate cases where education indicators were not collected for individuals aged 18")


    return edu_data, drop_msg


