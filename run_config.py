# Settings for run_PiNcalculation_outside_streamlit*.py
# Pick the case to run with ACTIVE_CASE; add new countries/years as new keyed entries.

ACTIVE_CASE = "AFG_2026"

CASES = {
    "AFG_2026": {
        
        # --- general
        "country": 'Afghanistan -- AFG',
        "selected_language": 'English',
        "label": 'label::English',
        "start_school": 'November',
        "admin_var": 'Admin_2: Province',
        "vector_cycle": [14, 16],
        # TODO: add later — not used by the run script yet
        # "primary_start": 7,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/AFG/00_Datasets/AFG_MSNA_edu_data.xlsx',
        "excel_path_ocha": 'input/AFG/10_PiN supporting files/AFG_Population_figures_filled_v2.xlsx',
        "sheets": {
            "household": 'hh_main_data',
            "edu": 'edu_clean_data',
            "survey": 'survey',
            "choices": 'choices',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in before running (the script stops if all five are None)
        "host_value": 'general_pop',
        "idp_value": 'idp',
        "returnee_value": 'cb_returnee',
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": "pop_group",
        "age_var": "edu_ind_age",
        "gender_var": "edu_ind_gender",
        "access_var": "edu_access",
        "teacher_disruption_var": "edu_disrupted_teachers",
        "idp_disruption_var": "edu_disrupted_displaced",
        "natural_hazard_var": "no_indicator",
        "natural_hazard_var_sev": None,
        "armed_disruption_var": 'edu_disrupted_man_made',
        "additional_last_var": "no_indicator",
        "additional_last_sev": None,
        "additional_2_last_var": "no_indicator",
        "additional_2_last_sev": None,
        "barrier_var": "edu_barrier",

        # --- barrier severity
        "selected_severity_4_barriers": ['Protection risks whilst at the school',
                    'Protection risks whilst travelling to the school',
                    "Child needs to work at home or on the household's own farm, i.e. is not earning an income for these activities, but may allow other family members to earn an income",
                    'Child participating in income generating activities outside of the home',
                    'Marriage or engagement'],

        "selected_severity_5_barriers": ['There is a ban preventing child from attending',
                    'Child is associated with armed forces or armed groups',
                    'Pregnancy'],
    },

    "VaSYR_2026": {
        # --- general
        "country": "Lebanon -- LBN",
        "selected_language": "English",
        "label": "label::English",
        "start_school": "September",
        "admin_var": "Admin_2: Districts (qaḍya)",   
        "vector_cycle": [11, 14],
        # TODO: add later — not used by the run script yet
        # "primary_start": 7,
        # "secondary_end": 17,
        # "step_2_hpc": False,
        "hybrid_country": False,           # True = hybrid country: French labels are not translated in calculatePIN
        "mismatch_admin": False,
        "no_ocha_data": False,

        # --- input files
        "excel_data_path": "input/LBN/LBN_VaSYR_edu_data.xlsx",
        "excel_path_ocha": "input/LBN/LBN_SYR_pop.xlsx",
        
        "sheets": {
            "household": "main",
            "edu": "edu_ind",
            "survey": "survey",
            "choices": "choices",
            "ocha": "ocha",
            "scope_fix": "scope-fix",
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        "host_value": "vasyr",
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": "pop_group",
        "age_var": "ind_age",
        "gender_var": "ind_gender",
        "access_var": "edu_access",
        "teacher_disruption_var": "edu_disrupted_teachers",
        "idp_disruption_var": "edu_disrupted_displaced",
        "natural_hazard_var": "edu_disrupted_hazards",
        "natural_hazard_var_sev": 4,
        "armed_disruption_var": 'edu_disrupted_man_made',
        "additional_last_var": "no_indicator",
        "additional_last_sev": None,
        "additional_2_last_var": "no_indicator",
        "additional_2_last_sev": None,
        "barrier_var": "edu_barrier",

        # --- barrier severity
        "selected_severity_4_barriers": [
            "h. Not attending due to marriage",
            "i. Not attending due to work",
            "m. School closed due to emergency/conflict",
            "n. School damaged or unsafe due to emergency/conflict",
            "o. School being used as a shelter for displaced households",
            "r. Safety concerns on the way to school due to emergency/conflict",
            "s. Safety concerns for girls, including lack of safe transport, unsafe routes, or fear of harassment",
            "u. Children need to stay at home to take care of the home and/or siblings",
            "u. Children need to stay at home to take care of the home and/or siblings",
            "v. Not attending due to fear of violence in school from school personnel",
            "v. Not attending due to fear of violence in school from school personnel",
            "w. Not attending due to fear of violence in school from other children",
            "x. Fear of violence on the way to school",
        ],
        "selected_severity_5_barriers": [
            "w. Lack of documentation",
        ],
        
    },
    "SOM_2026": {
        # --- general
        "country": "Somalia -- SOM",
        "selected_language": "English",
        "label": "label::english",
        "start_school": "October",
        "admin_var": "Admin_2: Districts",   
        "vector_cycle": [13, 0],
        # TODO: add later — not used by the run script yet
        # "primary_start": 7,
        # "secondary_end": 17,
        # "step_2_hpc": False,
        "hybrid_country": True,           # True = hybrid country: French labels are not translated in calculatePIN
        "mismatch_admin": False,
        "no_ocha_data": False,

        # --- input files
        "excel_data_path": "input/SOM/SOM_MSNA_ALL_edu_data.xlsx",
        "excel_path_ocha": "input/SOM/SOM_Population_figures_filled.xlsx",
        
        "sheets": {
            "household": "hh clean data",
            "edu": "edu clean data",
            "survey": "survey",
            "choices": "choices",
            "ocha": "ocha",
            "scope_fix": "scope-fix",
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        "host_value": "affected_population",
        "idp_value": "idp",
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": "pop_group",
        "age_var": "edu_ind_age",
        "gender_var": "edu_ind_gender",
        "access_var": "edu_access",
        "teacher_disruption_var": "edu_disrupted_teacher",
        "idp_disruption_var": "edu_disrupted_displaced",
        "natural_hazard_var": "edu_disrupted_hazards",
        "natural_hazard_var_sev": 4,
        "armed_disruption_var": 'no_indicator',
        "additional_last_var": "no_indicator",
        "additional_last_sev": None,
        "additional_2_last_var": "no_indicator",
        "additional_2_last_sev": None,
        "barrier_var": "edu_barrier",

        # --- barrier severity
        "selected_severity_4_barriers": [
            "School has been closed due to damage, natural disaster, conflict",
            "Protection risks whilst at the school",
            "Protection risks whilst travelling to the school",
            "Child needs to work at home or on the household's own farm",
            "Child participating in income generating activities outside of the home",
            "Marriage or engagement",
            "The child's disability or health issues prevent access to school",
            "Unable to enroll in school due to lack of documentation",
            "Unable to enroll in school due to recent displacement/return",
            "The school is not providing adequate support to my child with a disability or health issues",
        ],
        "selected_severity_5_barriers": [
            "Child is associated with armed forces or armed groups",
            "Pregnancy",
            "There is a ban preventing the child from attending",
            "Discrimination or stigmatization of the child",
        ],
        
    },

    "SSD_2025": {
        # --- general
        "country": "South Sudan -- SSD",
        "selected_language": "English",
        "label": "label",
        "start_school": "October",
        "admin_var": "Admin_2: Cercles",   # 'Admin_3: Townships' / 'Admin_2: Regions'
        "vector_cycle": [11, 0],
        # TODO: add later — not used by the run script yet
        # "primary_start": 7,
        # "secondary_end": 17,
        # "step_2_hpc": False,
        "hybrid_country": False,           # True = hybrid country: French labels are not translated in calculatePIN
        "mismatch_admin": False,
        "no_ocha_data": False,

        # --- input files
        "excel_data_path": "input/ISNA.xlsx",
        "excel_path_ocha": "input/ocha_SSD_2025.xlsx",
        
        "sheets": {
            "household": "Cleaned household data",
            "edu": "indv_data",
            "survey": "Questionnaire",
            "choices": "Choices",
            "ocha": "ocha",
            "scope_fix": "scope-fix",
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in for SSD before running (the script stops if all five are None)
        "host_value": None,
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": "pop_group",
        "access_var": "edu_access",
        "teacher_disruption_var": "edu_disrupted_teacher",
        "idp_disruption_var": "edu_disrupted_displaced",
        "armed_disruption_var": "edu_disrupted_attack",
        "natural_hazard_var": "edu_disrupted_hazards",
        "natural_hazard_var_sev": None,
        "additional_last_var": "no_indicator",
        "additional_last_sev": None,
        "additional_2_last_var": "no_indicator",
        "additional_2_last_sev": None,
        "barrier_var": "edu_barrier",
        "age_var": "b_8_1_years",
        "gender_var": "b_8_3_sex_of_household_member",

        # --- barrier severity
        "selected_severity_4_barriers": [
            "1. Cannot afford the direct costs of education (e.g. tuition, supplies, transportation)",
            "2. There is a lack of interest for formal education",
            "3. Education is not a priority either for the child or the household",
            "4. Lack of appropriate and accessible school",
            "5. The child is too young",
        ],
        "selected_severity_5_barriers": [
            "10. Curriculum and/or the certificates issued by school are not perceived to be useful for the household",
            "14. Pregnancy",
            "11. Protection risks whilst at the school",
            "12. Marriage, engagement",
            "13. The child's disability or health issues prevents them from accessing school",
        ],
        # "---> None of the listed barriers <---"
        # "Child is associated with armed forces or armed groups "
    },

    "LMR_2022": {
        # from cases_coutry_helpers.py lines 2-82 ("## Lemuria")
        # --- general
        "country": 'Lemuria -- LMR',
        "selected_language": 'English',
        "label": 'label::English',
        "start_school": 'September',
        "admin_var": 'Admin_2: District',
        "vector_cycle": [12, 16],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": True,

        # --- input files
        "excel_data_path": 'input/Lemuria_MSNA_2022.xlsx',
        "excel_path_ocha": 'input/OCHA_pop_LMR.xlsx',
        "sheets": {
            "household": '01_clean_data_main',
            "edu": '02_clean_data_indiv',
            "survey": 'survey',
            "choices": 'choices',
            "ocha": None,
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in before running (the script stops if all five are None)
        "host_value": None,
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'edu_disrupted_occupation',
        "natural_hazard_var": 'no_indicator',
        "natural_hazard_var_sev": None,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'edu_barrier',
        "age_var": 'ind_age',
        "gender_var": 'ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            'Cannot afford education-related costs (e.g. tuition, supplies, transportation)',
            'There is a lack of interest/Education is not a priority either for the child or the household',
        ],
        "selected_severity_5_barriers": [
            'School has been closed due to natural disaster',
            'School has been closed due to conflict',
            'Lack of or poor quality of teachers',
            'Protection/safety risks while commuting to school',
            'Protection/safety risks while at school',
            'Child marriage, engagement or pregnancies',
        ],
    },

    "MMR_2024": {
        # from cases_coutry_helpers.py lines 83-147 ("## MMR")
        # --- general
        "country": 'Myanmar -- MMR',
        "selected_language": 'English',  # not set in original: default — check
        "label": 'label::English',
        "start_school": 'September',
        "admin_var": 'Admin_1: States/Regions',
        "vector_cycle": [10, 14],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/REACH_MMR_MMR2402_MSNA_Dataset_VALIDATED.xlsx',
        "excel_path_ocha": 'input/ocha_pop_MMR.xlsx',
        "sheets": {
            "household": '01_clean_data_main',
            "edu": '02_clean_data_indiv',
            "survey": 'survey',
            "choices": 'choices',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in before running (the script stops if all five are None)
        "host_value": None,
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'edu_disrupted_occupation',
        "natural_hazard_var": 'no_indicator',  # not set in original: default
        "natural_hazard_var_sev": None,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'edu_barrier',
        "age_var": 'ind_age',
        "gender_var": 'ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            'Protection/safety risks while commuting to school',
            'Protection/safety risks while at school',
            "Child needs to work at home or on the household's own farm (i.e. is not earning an income for these activities, but may allow other family members to earn an income)",
            'Child participating in income generating activities outside of the home',
            'Child marriage, engagement or pregnancies',
            'Discrimination or stigmatization of the child for any reason',
            'Unable to enroll in school due to lack of documentation',
        ],
        "selected_severity_5_barriers": [
            'Child is associated with armed forces or armed groups ',
        ],
    },

    "BFA_2024": {
        # from cases_coutry_helpers.py lines 148-209 ("## BFA")
        # --- general
        "country": 'Burkina Faso -- BFA',
        "selected_language": 'English',  # not set in original: default — check
        "label": 'label',
        "start_school": 'September',
        "admin_var": 'Admin_3: Department (Département)',
        "vector_cycle": [10, 14],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": True,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/BFA2402_MSNA_2024_DATA_CLEANED_VF.xlsx',
        "excel_path_ocha": 'input/ocha_pop_BFA.xlsx',
        "sheets": {
            "household": 'main_cleaned',
            "edu": 'loop_sne_cleaned',
            "survey": 'survey',
            "choices": 'choices',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in before running (the script stops if all five are None)
        "host_value": None,
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": 'i_type_pop',
        "access_var": 'e_enfant_scolarise_formel',
        "teacher_disruption_var": 'e_absence_enseignant',
        "idp_disruption_var": 'e_ecole_abris',
        "armed_disruption_var": 'no_indicator',
        "natural_hazard_var": 'no_indicator',  # not set in original: default
        "natural_hazard_var_sev": None,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'e_raison_pas_educ_formel',
        "age_var": 'sne_enfant_ind_age',
        "gender_var": 'sne_enfant_ind_genre',

        # --- barrier severity
        "selected_severity_4_barriers": [
            'Risques de protection à l’école (tels que le harcèlement physique et verbal, risque de viol, les attaques contre les écoles ou d’autres incidents de protection)',
            'Risques de protection pendant le trajet vers l’école (tels que les incidents de harcèlement physique et verbal, risque de viol ou d’autres incidents de protection)',
        ],
        "selected_severity_5_barriers": [
            "L'enfant est associé à des forces armées ou à des groupes armés",
        ],
    },

    "AFG_2024": {
        # from cases_coutry_helpers.py lines 210-275 ("## AFG")
        # --- general
        "country": 'Afghanistan -- AFG',
        "selected_language": 'English',
        "label": 'label::English',
        "start_school": 'November',
        "admin_var": 'Admin_2',
        "vector_cycle": [14, 16],
        # TODO: add later — not used by the run script yet
        # "primary_start": 7,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/AFG_WoAA_2024_data.xlsx',
        "excel_path_ocha": 'input/AFG_ocha_admin2.xlsx',
        "sheets": {
            "household": 'AFG_WoAA_2024_data_main_recoded',
            "edu": 'AFG_WoAA_2024_edu_loop',
            "survey": 'survey',
            "choices": 'choices',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in before running (the script stops if all five are None)
        "host_value": None,
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": 'urbanity',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'no_indicator',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": None,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'resn_no_access',
        "age_var": 'ind_age',
        "gender_var": 'edu_ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            'Protection risks whilst at the school ',
            'Protection risks whilst travelling to the school ',
            "Child needs to work at home or on the household's own farm (i.e. is not earning an income for these activities, but may allow other family members to earn an income) ",
            'Child participating in income generating activities outside of the home',
        ],
        "selected_severity_5_barriers": [
            'Child is associated with armed forces or armed groups ',
        ],
    },

    "SOM_2024": {
        # from cases_coutry_helpers.py lines 276-340 ("## SOM")
        # --- general
        "country": 'Somalia -- SOM',
        "selected_language": 'English',
        "label": 'label::english',
        "start_school": 'September',
        "admin_var": 'Admin_2: Districts',
        "vector_cycle": [12, 16],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/REACH_MSNA_2024_FINAL_Cleaned_Weights.xlsx',
        "excel_path_ocha": 'input/ocha.xlsx',
        "sheets": {
            "household": 'main',
            "edu": 'edu_ind',
            "survey": 'survey',
            "choices": 'choices',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in before running (the script stops if all five are None)
        "host_value": None,
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": 'population_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'edu_disrupted_hazards',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": None,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'edu_barrier',
        "age_var": 'edu_ind_age',
        "gender_var": 'edu_ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            'Protection risks whilst at the school ',
            'Protection risks whilst travelling to the school ',
        ],
        "selected_severity_5_barriers": [
            'Child is associated with armed forces or armed groups ',
        ],
    },

    "NER_2024": {
        # from cases_coutry_helpers.py lines 341-405 ("## NER")
        # year inferred from position in cases_coutry_helpers.py (file name has no year)
        # --- general
        "country": 'Niger -- NER',
        "selected_language": 'French',
        "label": 'label::french',
        "start_school": 'September',
        "admin_var": 'Admin_2: Départements',
        "vector_cycle": [12, 16],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/ner_msna_clean_data_FINAL.xlsx',
        "excel_path_ocha": 'input/ocha_NER_update.xlsx',
        "sheets": {
            "household": 'raw_data_clean',
            "edu": 'loop_data_clean',
            "survey": 'kobo_survey',
            "choices": 'kobo_choices',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in before running (the script stops if all five are None)
        "host_value": None,
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": 'd_statut_deplacement',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'edu_disrupted_hazards',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": None,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'edu_barrier',
        "age_var": 'edu_age',
        "gender_var": 'edu_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            'Risques de protection à l’école (tels que le harcèlement physique et verbal, risque de viol, les attaques contre les écoles ou d’autres incidents de protection)',
            'Risques de protection pendant le trajet vers l’école (tels que les incidents de harcèlement physique et verbal, risque de viol ou d’autres incidents de protection)',
        ],
        "selected_severity_5_barriers": [
            "L'enfant est associé à des forces armées ou à des groupes armés",
        ],
    },

    "DRC_2024": {
        # from cases_coutry_helpers.py lines 406-469 ("## DRC")
        # --- general
        "country": 'Democratic Republic of the Congo -- DRC',
        "selected_language": 'French',
        "label": 'label::french',
        "start_school": 'September',
        "admin_var": 'Admin_3: Sectors/chiefdoms/communes',
        "vector_cycle": [12, 16],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/REACH_DRC2404_MSNA2024_Clean-Data.xlsx',
        "excel_path_ocha": 'input/DRC_ocha.xlsx',
        "sheets": {
            "household": 'hh_data',
            "edu": 'edu_data',
            "survey": 'survey',
            "choices": 'choices',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in before running (the script stops if all five are None)
        "host_value": None,
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": 'hoh_dis',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'edu_disrupted_hazards',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": None,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'edu_barrier',
        "age_var": 'edu_ind_age',
        "gender_var": 'edu_ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            'Risques de protection à l’école (tels que le harcèlement physique et verbal, risque de viol, les attaques contre les écoles ou d’autres incidents de protection)',
            'Risques de protection pendant le trajet vers l’école (tels que les incidents de harcèlement physique et verbal, risque de viol ou d’autres incidents de protection)',
        ],
        "selected_severity_5_barriers": [
            "L'enfant est associé à des forces armées ou à des groupes armés",
        ],
    },

    "DRC_2023": {
        # from cases_coutry_helpers.py lines 470-535 ("## DRC-2")
        # '## DRC-2' block: MSNA 2023 data with DRC_ocha_2025
        # --- general
        "country": 'Democratic Republic of the Congo -- DRC',
        "selected_language": 'French',
        "label": 'label',
        "start_school": 'September',
        "admin_var": 'Admin_3',
        "vector_cycle": [11, 0],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": False,

        # --- input files
        "excel_data_path": 'input/REACH_MSNA_2023_DRC_clean dataset_v2.xlsx',
        "excel_path_ocha": 'input/DRC_ocha_2025.xlsx',
        "sheets": {
            "household": 'BDD nettoyée',
            "edu": 'HH roster',
            "survey": 'Questionnaire',
            "choices": 'Options',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in before running (the script stops if all five are None)
        "host_value": None,
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disruption_teacher',
        "idp_disruption_var": 'edu_disruption_displaced',
        "armed_disruption_var": 'no_indicator',
        "natural_hazard_var": 'no_indicator',
        "natural_hazard_var_sev": None,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'edu_barrier',
        "age_var": 'age_years',
        "gender_var": 'ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            "Risques de protection pendant le trajet vers l'école",
            "Risques de protection à l'école",
            'Enfant aidant à la maison / à la ferme',
            "Impossibilité d'enregistrer ou d'inscrire l'enfant à l'école",
            'Mariage et/ou grossesse',
        ],
        "selected_severity_5_barriers": [
            'Les enfants rejoignent ou sont recrutés par des groupes armés',
        ],
    },

    "CAR_2024_a": {
        # from cases_coutry_helpers.py lines 536-598 ("## CAR")
        # first '## CAR' block (different barriers/indicators from CAR_2024_b)
        # --- general
        "country": 'Central African Republic -- CAR',
        "selected_language": 'English',  # not set in original: default — check
        "label": 'label::french',
        "start_school": 'September',
        "admin_var": 'Admin_2: Sub-prefectures (sous-préfectures)',
        "vector_cycle": [12, 16],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/CAR2402_REACH_MSNA_Base-de-donnees-nettoyees_septembre-2024-1.xlsx',
        "excel_path_ocha": 'input/Ocha_pop_CAR.xlsx',
        "sheets": {
            "household": 'menage',
            "edu": 'Education',
            "survey": 'survey',
            "choices": 'choices',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in before running (the script stops if all five are None)
        "host_value": None,
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": 'type_population',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'edu_disrupted_hazards',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": None,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'edu_barrier',
        "age_var": 'edu_ind_age',
        "gender_var": 'edu_ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            "Absence d'école appropriée et accessible",
        ],
        "selected_severity_5_barriers": [
            "Le handicap ou les problèmes de santé de l'enfant l'empêchent d'aller à l'école",
        ],
    },

    "MLI_2024": {
        # from cases_coutry_helpers.py lines 599-659 ("## MLI")
        # --- general
        "country": 'Mali -- MLI',
        "selected_language": 'English',
        "label": 'label::french',
        "start_school": 'October',
        "admin_var": 'Admin_2: Cercles',
        "vector_cycle": [11, 0],
        # TODO: add later — not used by the run script yet
        # "primary_start": 7,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/REACH_MLI2402__Clean-Dataset_final.xlsx',
        "excel_path_ocha": 'input/Template_Population_figures_final_1510.xlsx',
        "sheets": {
            "household": 'Ménages',
            "edu": 'Ménages',
            "survey": 'Survey',
            "choices": 'Choices',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in before running (the script stops if all five are None)
        "host_value": None,
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'no_indicator',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": None,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'edu_barrier',
        "age_var": 'edu_ind_age',
        "gender_var": 'edu_ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            'Mariage, fiançailles et/ou grossesse',
        ],
        "selected_severity_5_barriers": [
            "L'enfant est associé à des forces armées ou à des groupes armés ",
        ],
    },

    "CAR_2024_b": {
        # from cases_coutry_helpers.py lines 660-725 ("## CAR")
        # second '## CAR' block
        # --- general
        "country": 'Central African Republic -- CAR',
        "selected_language": 'French',
        "label": 'label::french',
        "start_school": 'September',
        "admin_var": 'Admin_2: Sub-prefectures (sous-préfectures)',
        "vector_cycle": [12, 16],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/CAR2402_REACH_MSNA_Base-de-donnees-nettoyees_septembre-2024-1.xlsx',
        "excel_path_ocha": 'input/Ocha_pop_CAR.xlsx',
        "sheets": {
            "household": 'menage',
            "edu": 'Education',
            "survey": 'survey',
            "choices": 'choices',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in before running (the script stops if all five are None)
        "host_value": None,
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": 'type_population',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'edu_disrupted_occupation',
        "natural_hazard_var": 'no_indicator',
        "natural_hazard_var_sev": None,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'edu_barrier',
        "age_var": 'edu_ind_age',
        "gender_var": 'edu_ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            "Risques de protection à l'école ",
            "Risques de protection pendant le trajet vers l'école ",
            "L'enfant doit travailler à la maison ou dans la ferme du ménage (c'est-à-dire qu'il ne gagne pas de revenu pour ces activités, mais peut permettre à d'autres membres de la famille de gagner un revenu)",
            "L'enfant participe à des activités génératrices de revenus en dehors du foyer",
            'Mariage, fiançailles et/ou grossesse',
            "Impossibilité de s'inscrire à l'école en raison d'un manque de documents",
            "Impossibilité de s'inscrire à l'école en raison d'un déplacement/retour récent (déplacement après le début de l'année scolaire)",
        ],
        "selected_severity_5_barriers": [
            "L'enfant est associé à des forces armées ou à des groupes armés ",
        ],
    },

    "MOZ_2025": {
        # from cases_coutry_helpers.py lines 726-801 ("## MOZ")
        # --- general
        "country": 'Mozambique -- MOZ',
        "selected_language": 'English',
        "label": 'label::english',
        "start_school": 'June',
        "admin_var": 'Admin_3',
        "vector_cycle": [10, 14],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": True,
        "no_ocha_data": False,

        # --- input files
        "excel_data_path": 'input/MSNA Mozambique 2025.xlsx',
        "excel_path_ocha": 'input/ocha_MOZ.xlsx',
        "sheets": {
            "household": 'main',
            "edu": 'edu_ind',
            "survey": 'survey',
            "choices": 'choices',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in before running (the script stops if all five are None)
        "host_value": None,
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": 'pop_group',
        "access_var": 'Did child of age: ${edu_ind_age} and gender: ${edu_ind_gender} attend school or any early childhood education program at any time during the 2025 school year?',
        "teacher_disruption_var": 'In the past 12 months, was the education child of age: ${edu_ind_age} and gender: ${edu_ind_gender} disrupted by any of the following events:/Teacher’s absence',
        "idp_disruption_var": 'In the past 12 months, was the education child of age: ${edu_ind_age} and gender: ${edu_ind_gender} disrupted by any of the following events:/School used as a shelter by displaced persons',
        "armed_disruption_var": 'In the past 12 months, was the education child of age: ${edu_ind_age} and gender: ${edu_ind_gender} disrupted by any of the following events:/Direct attack on education (e.g. school occupied by armed actors, damaged by munitions/fire, looted)',
        "natural_hazard_var": 'no_indicator',
        "natural_hazard_var_sev": 4,
        "additional_last_var": 'no_indicator',
        "additional_last_sev": None,
        "additional_2_last_var": 'no_indicator',
        "additional_2_last_sev": None,
        "barrier_var": 'edu_barrier',
        "age_var": 'edu_ind_age',
        "gender_var": 'edu_ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            'Protection risks whilst at the school',
            'Protection risks whilst travelling to the school',
            'Not enough food for the family and school doesn´t provide school feeding',
            "Child needs to work at home or on the household's own farm (i.e. is not earning an income for these activities, but may allow other family members to earn an income)",
            'Child participating in income generating activities outside of the home',
        ],
        "selected_severity_5_barriers": [
            'Child is associated with armed forces or armed groups',
        ],
    },

    "MMR_2025": {
        # from cases_coutry_helpers.py lines 802-874 ("## MMR")
        # --- general
        "country": 'Myanmar -- MMR',
        "selected_language": 'English',
        "label": 'label::English',
        "start_school": 'June',
        "admin_var": 'Admin_3: Townships',
        "vector_cycle": [10, 14],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": True,
        "no_ocha_data": False,

        # --- input files
        "excel_data_path": 'input/REACH_MMR_MMR2503_MSNA_Dataset_V2_1.xlsx',
        "excel_path_ocha": 'input/Template_Population_figures - Final.xlsx',
        "sheets": {
            "household": '01_clean_data_main',
            "edu": '02_clean_data_indiv',
            "survey": 'survey',
            "choices": 'choices',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in before running (the script stops if all five are None)
        "host_value": None,
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'edu_disrupted_attack',
        "natural_hazard_var": 'no_indicator',
        "natural_hazard_var_sev": None,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'edu_barrier',
        "age_var": 'ind_age',
        "gender_var": 'ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            'Protection/safety risks while commuting to school',
            'Protection/safety risks while at school',
            "Child needs to work at home or on the household's own farm (i.e. is not earning an income for these activities, but may allow other family members to earn an income)",
            'Child participating in income generating activities outside of the home',
            'Child marriage, engagement or pregnancies',
            'Discrimination or stigmatization of the child for any reason',
            'Unable to enroll in school due to lack of documentation',
        ],
        "selected_severity_5_barriers": [
            'Child is associated with armed forces or armed groups',
            'Pregnancy',
        ],
    },

    "MLI_2025": {
        # from cases_coutry_helpers.py lines 875-942 ("## MLI")
        # --- general
        "country": 'Mali -- MLI',
        "selected_language": 'French',
        "label": 'label::french',
        "start_school": 'October',
        "admin_var": 'Admin_2: Cercles',
        "vector_cycle": [11, 0],
        # TODO: add later — not used by the run script yet
        # "primary_start": 7,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": True,
        "no_ocha_data": False,

        # --- input files
        "excel_data_path": 'input/MSNA_2025_MLI_South_and_North.xlsx',
        "excel_path_ocha": 'input/MLI_ocha.xlsx',
        "sheets": {
            "household": 'hh data',
            "edu": 'edu data',
            "survey": 'survey',
            "choices": 'choices',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        # TODO: fill in before running (the script stops if all five are None)
        "host_value": None,
        "idp_value": None,
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'no_indicator',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": 4,
        "additional_last_var": 'no_indicator',
        "additional_last_sev": None,
        "additional_2_last_var": 'no_indicator',
        "additional_2_last_sev": None,
        "barrier_var": 'edu_barrier',
        "age_var": 'edu_ind_age',
        "gender_var": 'edu_ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            "L'enfant doit travailler à la maison ou dans la ferme du ménage (c'est-à-dire qu'il ne gagne pas de revenu pour ces activités, mais peut permettre à d'autres membres de la famille de gagner un revenu)",
            "Risques de protection à l'école ",
            "Risques de protection pendant le trajet vers l'école ",
        ],
        "selected_severity_5_barriers": [
            "L'enfant est associé à des forces armées ou à des groupes armés ",
            'Grossesse',
        ],
    },

    "BFA_2025": {
        # from run_PiNcalculation_outside_streamlit2.py lines 42-119 ("## BFA (run2)")
        # --- general
        "country": 'Burkina Faso -- BFA',
        "selected_language": 'French',  # original was 'label::French', which made outputs English
        "label": 'label::French',
        "start_school": 'September',
        "admin_var": 'admin2',
        "vector_cycle": [11, 15],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        # "step_2_hpc": False,
        "hybrid_country": False,
        "mismatch_admin": True,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/BFA/REACH I BFA I 2025 MSNA-eduPlatform.xlsx',
        "excel_path_ocha": 'input/BFA/BFA_ocha_FINAL__1909.xlsx',
        "sheets": {
            "household": 'main',
            "edu": 'indvidual',
            "survey": 'survey',
            "choices": 'choices',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        "host_value": 'non_pdi',  # from run_PiNcalculation_outside_streamlit2.py line 190
        "idp_value": 'pdi',
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- MSNA variables
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_teachers',
        "idp_disruption_var": 'edu_displaced',
        "armed_disruption_var": 'no_indicator',
        "natural_hazard_var": 'no_indicator',
        "natural_hazard_var_sev": None,
        "additional_last_var": 'edu_incident_trajet',
        "additional_last_sev": 4,
        "additional_2_last_var": 'edu_incident_ecol',
        "additional_2_last_sev": 4,
        "barrier_var": 'edu_barriers',
        "age_var": 'sne_enfant_ind_age',
        "gender_var": 'sne_enfant_ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            'Risques de protection à l’école (tels que le harcèlement physique et verbal, risque de viol, les attaques contre les écoles ou d’autres incidents de protection)',
            'Risques de protection pendant le trajet vers l’école (tels que les incidents de harcèlement physique et verbal, risque de viol ou d’autres incidents de protection)',
            "L’enfant doit travailler à la maison ou dans la ferme du ménage (c'est-à-dire qu'il ne gagne pas de revenu pour ces activités, mais peut permettre à d'autres membres de la famille de gagner un revenu)",
            "L'enfant participe à des activités génératrices de revenus en dehors du ménage",
            'Mariage, fiançailles',
        ],
        "selected_severity_5_barriers": [
            'Grossesse',
            "Une interdiction empêche l'enfant d'aller à l'école",
        ],
    },
}
