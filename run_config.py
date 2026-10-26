# Settings for run_PiNcalculation_outside_streamlit*.py
# Pick the case to run with ACTIVE_CASE; add new countries/years as new keyed entries.
# To run several cases in a row, list them in RUN_CASES and run run_all_cases.py.
# Optional in a case: "overall_country": True/False calculates the rates for all the population groups
# together (True) or per group (False); without it, OVERALL_COUNTRIES of src/calculation_for_PiN_Dimension.py decides.
# Optional in a case: "ece_3_4_ratio" (3-4 population / 5-17 population) and "students_per_teacher" add the
# children aged 3-4 (5-17 figures x ratio) and the teachers ((5-17 + 3-4) / students per teacher) to the
# results Excel: rows in "PiN TOTAL" and "PiN 3-4 -- ..." / "PiN teachers -- ..." sheets (src/add_ece_teachers.py).

ACTIVE_CASE = "CMR_2026"                       # single run
RUN_CASES = ["HTI_2026_Departement", "HTI_2026_ZMPAP"] #,"COD_2023","COD_2026","COD_2025"]    # batch run (run_all_cases.py)
ARCHIVE_INPUTS = True    # True: copy the Assessment dataset and the OCHA file into each successful run's archive zip; False: store only their checksums

CASES = {

    "CMR_2026": {
        # --- general
        "country": "Cameroon -- CMR",
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": "English",
        "label": "label::english (en)",
        "start_school": "September",  # data collection 24 June - 28 August 2026
        "admin_var": "Admin_2: Departments",
        "vector_cycle": [11, 16],  # anglophone system: primary 6-11, secondary 12-16, high school 17-18
        "hybrid_country": False,           # True = hybrid country: French labels are not translated in calculatePIN
        "mismatch_admin": True,    # scope-fix: Ndian takes the results of South-West; Far North without MSNA yet (no PiN)
        "no_ocha_data": False,
        # Children 3-4: the baseline's "1. Children" are 0-17 (18 years): 3-4 = 2 years, 5-17 = 13 years
        "ece_3_4_ratio": 2 / 13,
        "students_per_teacher": 45,

        # --- input files (country_support/CMR/09_code: 01_prepare_pop.R, 02_msna_NWSW_prep.R)
        # MSNA 2026 NWSW, representative at admin2 (department); the population file has the 19
        # departments of the baseline (Far North, North-West, South-West)
        "excel_data_path": "input/CMR/CMR_NWSW_MSNA_2026_edu_data_v1.xlsx",
        "excel_path_ocha": "input/CMR/CMR_Population_figures_v1.xlsx",

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
        "host_value": "host",
        "idp_value": "idp",
        "returnee_value": "retourne",
        "refugee_value": None,     # no refugee group in the baseline (refugees left empty in the population file)
        "other_value": None,

        # --- Assessment variables (names of country_support/CMR/09_code/02_msna_NWSW_prep.R)
        "status_var": "pop_group",
        "access_var": "edu_access",
        "teacher_disruption_var": "edu_disrupted_teacher",
        "idp_disruption_var": "edu_disrupted_displaced",
        "armed_disruption_var": "edu_disrupted_attack",
        "natural_hazard_var": "edu_disrupted_hazards",
        "natural_hazard_var_sev": 4,  
        "additional_last_var": "no_indicator",
        "additional_last_sev": None,
        "additional_2_last_var": "no_indicator",
        "additional_2_last_sev": None,
        "barrier_var": "edu_barrier",
        "age_var": "ind_age",
        "gender_var": "ind_gender",

        # --- barrier severity (choice names of l_edu_barrier, recoded by label in 02_msna_NWSW_prep.R)
        "barrier_match": "name",
        "selected_severity_4_barriers": [
            "school_closed",              # School has been closed due to damage, natural disaster, conflict
            "protection_at_school",       # Protection risks whilst at the school
            "protection_travel_school",   # Protection risks whilst travelling to the school
            "child_work_home",            # Child needs to work at home or on the household's own farm
            "child_work_outside",         # Child participating in income generating activities outside of the home
            "child_marriage",             # Marriage or engagement
        ],
        "selected_severity_5_barriers": [
            "child_armed_group",          # Child is associated with armed forces or armed groups
            "child_pregnancy",            # Pregnancy
            "ban",                        # There is a ban preventing child from attending
        ],
    },

    "SSD_2026": {
        # --- general
        "country": "South Sudan -- SSD",
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": "English",
        "label": "label::English",
        "start_school": "February",  # school year February-December (ISNA: "2026 school year")
        "admin_var": "Admin_2: Counties",
        "vector_cycle": [13, 0],  # primary P1-P8 6-13, secondary S1-S4 14-17 (two levels)
        # TODO: add later — not used by the run script yet
        # "primary_start": 7,
        # "secondary_end": 17,
        # "step_2_hpc": False,
        "hybrid_country": False,           # True = hybrid country: French labels are not translated in calculatePIN
        "mismatch_admin": True,    # scope-fix: Ayod and Budi take the results of their state
        "no_ocha_data": False,
        # Children 3-4 (to add the 3-4 y.o. and teacher rows, uncomment both keys): 3-4 = 5-17 x 7.4 / 35.
        # Origin: ICCG endorsed 2027 baseline (country_support/SSD/10_PiN supporting files), sheet
        # "2027 Population Baseline", shares of the affected population, the same in all counties:
        # under 5 = 9.6% male + 8.9% female = 18.5%, so 3-4 (2 of the 5 years) = 18.5% x 2/5 = 7.4%;
        # 5-17 = 17.7% male + 17.3% female = 35%. Both are shares of the same population, so the
        # 3-4 / 5-17 ratio is 7.4 / 35 (about 0.211). Check the shares of the new baseline every year
        # "ece_3_4_ratio": 7.4 / 35,
        # "students_per_teacher": 45,

        # --- input files (country_support/SSD/09_code: 00_pcode_dictionary.R, 01_prepare_pop.R, 02_isna_prep.R)
        "excel_data_path": "input/SSD/SSD_ISNA_2026_edu_data_v1.xlsx",
        "excel_path_ocha": "input/SSD/SSD_Population_figures_v1.xlsx",

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
        "host_value": "hc",
        "idp_value": "idp",
        "returnee_value": "ret",
        "refugee_value": None,     # no refugee group in the ISNA (refugees left empty in the population file)
        "other_value": None,

        # --- Assessment variables
        "status_var": "pop_group",
        "access_var": "edu_access",
        "teacher_disruption_var": "edu_disrupted_teacher",
        "idp_disruption_var": "edu_disrupted_displaced",
        "armed_disruption_var": "edu_disrupted_attack",
        "natural_hazard_var": "edu_disrupted_hazards",
        "natural_hazard_var_sev": 3,
        "additional_last_var": "insecurity_armed_conflict_violence_threats",  # G.3.3 insecurity, armed conflict, violence, threats
        "additional_last_sev": 4,
        "additional_2_last_var": "school_temporarily_permanently_closed",  # G.3.7 school temporarily or permanently closed
        "additional_2_last_sev": 3,
        "barrier_var": "edu_barrier",
        "age_var": "ind_age",
        "gender_var": "ind_gender",

        # --- barrier severity: labels of the choices sheet; the only lists of severities: 02_isna_prep.R
        # (country_support/SSD) reads them to keep one barrier per child
        "barrier_match": "label",
        "selected_severity_4_barriers": [
            "8. Insecurity, conflict or violence",
            "11. Child is working or engaged in household/livelihood activities",
            "17. Protection or safety concerns on the way to or at school",
            "18. School occupied or used for other purposes",
            "21. Marriage, engagement",
            "23. Discrimination, stigma or social exclusion",
            "24. Lack of required documentation or difficulty enrolling",
            "25. Child recently arrived through displacement/return and could not enroll",
            "26. School admission/enrolment restrictions",
        ],
        "selected_severity_5_barriers": [
            "20. Pregnancy",
        ],
    },

    "NER_2026": {
        # --- general
        "country": 'Niger -- NER',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": 'French',
        "label": 'label::french (fr)',
        "start_school": 'October',
        "admin_var": 'Admin_2: Départements',
        "vector_cycle": [11, 15],  # end of level1, end of level2 for 3 level system
        "hybrid_country": False,
        "mismatch_admin": True,    # scope-fix: departments without MSNA take the results of their region
        "no_ocha_data": False,

        # --- input files (country_support/NER/09_code: 01_prepare_pop.R, 02_msna_prep.R)
        # MSNA 2026, representative at admin2 (department); only the departments of the analysis
        # scope ("Portée d'analyse" = oui) in the population file
        "excel_data_path": 'input/NER/NER_MSNA_2026_edu_data_v1.xlsx',
        "excel_path_ocha": 'input/NER/NER_Population_figures_v1.xlsx',
        "sheets": {
            "household": 'main',
            "edu": 'edu_ind',
            "survey": 'survey',
            "choices": 'choices',
            "ocha": 'ocha',
            "scope_fix": 'scope-fix',
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if
        "host_value": "host",
        "idp_value": "idp",
        "returnee_value": None,     # "retourne" in the MSNA (110 hh), no population figure yet
        "refugee_value": "refugie",
        "other_value": None,        # migrants: population in Other, no group in the MSNA

        # --- Assessment variables (names of country_support/NER/09_code/02_msna_prep.R)
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'edu_disrupted_attack',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": 4,
        "additional_last_var": 'no_indicator',
        "additional_last_sev": None,
        "additional_2_last_var": 'no_indicator',
        "additional_2_last_sev": None,
        "barrier_var": 'edu_barrier',
        "barrier_match": "name",  # severity 4/5 barriers below are choice names: "name": "label" (default)
        "age_var": 'ind_age',
        "gender_var": 'ind_gender',

        # --- barrier severity (choice names of l_edu_barrier in the MSNA 2026 tool)
        "selected_severity_4_barriers": [
            "school_closed",              # 8. L'école a été fermée en raison de dommagee ou d'un conflit
            "protection_at_school",       # 11. Risques de protection à l'école
            "protection_travel_school",   # 12. Risques de protection pendant le trajet
            "child_work_home",            # 13. L'enfant doit travailler à la maison ou dans la ferme du ménage
            "child_work_outside",         # 14. L'enfant participe à des activités générdu ménage
            "child_marriage",             # 16. Mariage ou fiançailles
        ],
        "selected_severity_5_barriers": [
            "child_armed_group",          # 15. L'enfant est associé à des forces armées
            "child_pregnancy",            # 17. Grossesse
            "ban",                        # 20. Une interdiction empêche l'enfant d'alle
        ],
    },

    "HTI_2026_Departement": {
        # --- general
        "country": 'Haiti -- HTI',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": 'French',
        "label": 'label::french (fr)',
        "start_school": 'September',
        "admin_var": 'Admin_1: Departments (départements)',
        "vector_cycle": [11, 14],  # fondamental 1st-2nd cycle 6-11, 3rd cycle 12-14, secondary 15-17
        "hybrid_country": False,
        "mismatch_admin": False,
        "no_ocha_data": False,

        # --- input files (country_support/HTI/09_code: 01_prepare_pop.R, 02_msna_prep.R)
        # MSNA 2026, survey "Departement": representative at admin1 (department). Ouest includes the
        # ZMPAP, as in the OCHA template (the ZMPAP is reported in addition, HTI_2026_ZMPAP)
        "excel_data_path": 'input/HTI/HTI_MSNA_2026_Departement_edu_data_v1.xlsx',
        "excel_path_ocha": 'input/HTI/HTI_Population_figures_Departement_v1.xlsx',
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
        "host_value": "host_community",
        "idp_value": "idp",
        "returnee_value": "returnee",
        "refugee_value": None,
        "other_value": None,

        # --- Assessment variables (names of country_support/HTI/09_code/02_msna_prep.R)
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'edu_disrupted_attack',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": 3,
        "additional_last_var": 'no_indicator',
        "additional_last_sev": None,
        "additional_2_last_var": 'no_indicator',
        "additional_2_last_sev": None,
        "barrier_var": 'edu_barrier',
        "barrier_match": "name",  # severity 4/5 barriers below are choice names: "name"; labels (as on the platform): "label" (default)
        "age_var": 'ind_age',
        "gender_var": 'ind_gender',

        # --- barrier severity (choice names of l_edu_barrier in the MSNA 2026 tool)
        "selected_severity_4_barriers": [
            "school_closed",              # 1. L'école a été fermée en raison de dommages, d'une catastrophe naturelle ou d'un conflit
            "protection_at_school",       # 4. Risques de protection à l'école
            "protection_travel_school",   # 5. Risques de protection pendant le trajet vers l'école
            "child_work_home",            # 6. L'enfant doit travailler à la maison ou dans la ferme du ménage
            "child_work_outside",         # 7. L'enfant participe à des activités génératrices de revenus en dehors du foyer
            "child_marriage",             # 9. Mariage ou fiançailles
            "child_pregnancy",            # 9. Grossesse
            "ban",                        # 12. Une interdiction empêche l'enfant d'aller à l'école
            "enroll_lack_documentation",  # 14. Impossibilité de s'inscrire à l'école en raison d'un manque de documents
            "enroll_displacement",        # 15. Impossibilité de s'inscrire à l'école en raison d'un déplacement/retour récent
        ],
        "selected_severity_5_barriers": [
            "child_armed_group",          # 8. L'enfant est associé à des forces armées ou à des groupes armés
        ],
    },

    "HTI_2026_ZMPAP": {
        # --- general
        "country": 'Haiti -- HTI',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": 'French',
        "label": 'label::french (fr)',
        "start_school": 'September',
        "admin_var": 'Admin_2: Communes',  # admin2 of the MSNA is the commune (the app lists Admin_2 as arrondissements for HTI)
        "vector_cycle": [11, 14],  # fondamental 1st-2nd cycle 6-11, 3rd cycle 12-14, secondary 15-17
        "hybrid_country": False,
        "mismatch_admin": False,
        "no_ocha_data": False,

        # --- input files (country_support/HTI/09_code: 01_prepare_pop.R, 02_msna_prep.R)
        # MSNA 2026, survey "ZMPAP": representative at admin2 (the 7 communes of the zone metropolitaine
        # de Port-au-Prince); reported in addition to the departments (HTI_2026_Departement), not summed
        "excel_data_path": 'input/HTI/HTI_MSNA_2026_ZMPAP_edu_data_v1.xlsx',
        "excel_path_ocha": 'input/HTI/HTI_Population_figures_ZMPAP_v1.xlsx',
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
        "host_value": "host_community",
        "idp_value": "idp",
        "returnee_value": "returnee",
        "refugee_value": None,
        "other_value": None,

        # --- Assessment variables (names of country_support/HTI/09_code/02_msna_prep.R)
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'edu_disrupted_attack',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": 3,
        "additional_last_var": 'no_indicator',
        "additional_last_sev": None,
        "additional_2_last_var": 'no_indicator',
        "additional_2_last_sev": None,
        "barrier_var": 'edu_barrier',
        "barrier_match": "name",  # severity 4/5 barriers below are choice names: "name"; labels (as on the platform): "label" (default)
        "age_var": 'ind_age',
        "gender_var": 'ind_gender',

        # --- barrier severity (choice names of l_edu_barrier in the MSNA 2026 tool)
        "selected_severity_4_barriers": [
            "school_closed",              # 1. L'école a été fermée en raison de dommages, d'une catastrophe naturelle ou d'un conflit
            "protection_at_school",       # 4. Risques de protection à l'école
            "protection_travel_school",   # 5. Risques de protection pendant le trajet vers l'école
            "child_work_home",            # 6. L'enfant doit travailler à la maison ou dans la ferme du ménage
            "child_work_outside",         # 7. L'enfant participe à des activités génératrices de revenus en dehors du foyer
            "child_marriage",             # 9. Mariage ou fiançailles
            "child_pregnancy",            # 9. Grossesse
            "ban",                        # 12. Une interdiction empêche l'enfant d'aller à l'école
            "enroll_lack_documentation",  # 14. Impossibilité de s'inscrire à l'école en raison d'un manque de documents
            "enroll_displacement",        # 15. Impossibilité de s'inscrire à l'école en raison d'un déplacement/retour récent
        ],
        "selected_severity_5_barriers": [
            "child_armed_group",          # 8. L'enfant est associé à des forces armées ou à des groupes armés
        ],
    },

    "COD_2026": {
        # from cases_coutry_helpers.py lines 406-469 ("## DRC")
        # --- general
        "country": 'Democratic Republic of the Congo -- DRC',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": 'French',
        "label": 'label::french (fr)',
        "start_school": 'September',
        "admin_var": 'Admin_3: Sectors/chiefdoms/communes',
        "vector_cycle": [11, 13],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/COD/COD_MSNA_2026_edu_data.xlsx',
        "excel_path_ocha": 'input/COD/COD_Population_figures_no_pop_groups.xlsx',
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
        "host_value": 'host', #Host
        "idp_value": None, #IDP in sites
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None, #IDP dans des Famille d'acueille

        # --- Assessment variables
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'edu_disrupted_attack',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": 3,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'edu_barrier',
        "barrier_match": "name",  # severity 4/5 barriers below are choice names: "name"; labels (as on the platform): "label" (default)
        "age_var": 'edu_ind_age',
        "gender_var": 'edu_ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            "child_work_home",
            "child_work_outside",
            "protection_at_school",
            "protection_travel_school",
            "child_marriage",
            "enroll_lack_documentation",
            "enroll_displacement",
            "discrimination",
            "school_closed",
        ],
        "selected_severity_5_barriers": [
            "child_pregnancy",
            "child_armed_group",
            "ban",
        ],
    },

    "COD_2025": {
        # from cases_coutry_helpers.py lines 406-469 ("## DRC")
        # --- general
        "country": 'Democratic Republic of the Congo -- DRC',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": 'French',
        "label": 'label',
        "start_school": 'September',
        "admin_var": 'Admin_3: Sectors/chiefdoms/communes',
        "vector_cycle": [11, 13],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/COD/COD_MSNA_2025_edu_data.xlsx',
        "excel_path_ocha": 'input/COD/COD_Population_figures_with_pop_groups.xlsx',
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
        "host_value": 'Hote', #Host
        "idp_value": 'PDI_Site', #IDP in sites
        "returnee_value": 'Retourne',
        "refugee_value": None,
        "other_value": 'PDI_FA', #IDP dans des Famille d'acueille

        # --- Assessment variables
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'edu_disrupted_attack',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": 3,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'edu_barrier',
        "barrier_match": "name",  # severity 4/5 barriers below are choice names: "name"; labels (as on the platform): "label" (default)
        "age_var": 'edu_ind_age',
        "gender_var": 'edu_ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            "discrimination",
            "enroll_displacement",
            "enroll_lack_documentation",
            "school_closed_natural",
            "school_closed_conflict",
            "school_closed_other",
            "child_work_home",
            "child_work_outside",
            "child_marriage",
            "protection_at_school",
            "protection_travel_school",
        ],
        "selected_severity_5_barriers": [
            "child_pregnancy",
            "child_armed_group",
            "ban",
        ],
    },

    "COD_2024": {
        # from cases_coutry_helpers.py lines 406-469 ("## DRC")
        # --- general
        "country": 'Democratic Republic of the Congo -- DRC',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": 'French',
        "label": 'label',
        "start_school": 'September',
        "admin_var": 'Admin_3: Sectors/chiefdoms/communes',
        "vector_cycle": [11, 13],
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

        # --- Assessment variables
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

    "COD_2023": {
        # from cases_coutry_helpers.py lines 470-535 ("## DRC-2")
        # '## DRC-2' block: Assessment 2023 data with DRC_ocha_2025
        # --- general
        "country": 'Democratic Republic of the Congo -- DRC',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": 'French',
        "label": 'label',
        "start_school": 'September',
        "admin_var": 'Admin_3: Sectors/chiefdoms/communes',
        "vector_cycle": [11, 13],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/COD/COD_MSNA_2023_edu_data.xlsx',
        "excel_path_ocha": 'input/COD/COD_Population_figures_with_pop_groups.xlsx',
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
        "host_value": 'Hote', #Host
        "idp_value": 'PDI_Site', #IDP in sites
        "returnee_value": 'Retourne',
        "refugee_value": None,
        "other_value": 'PDI_FA', #IDP dans des Famille d'acueille

        # --- Assessment variables
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disruption_teacher',
        "idp_disruption_var": 'no_indicator', # The code 'edu_disruption_displaced' is used, but the questions is about safe displacement towards or form the school: "l'enfant a pu se rendre à l'école en toute sécurité et apprendre dans des conditions sûres à l'école ?"
        "armed_disruption_var": 'no_indicator',
        "natural_hazard_var": 'edu_disruption_hazard',
        "natural_hazard_var_sev": 3,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'edu_barrier',
        "barrier_match": "name",  # severity 4/5 barriers below are choice names: "name"; labels (as on the platform): "label" (default)
        "age_var": 'age_years',
        "gender_var": 'ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
            "risque_pro_trajet",
            "risque_pro",
            "enfant_maison",
            "impossible_inscri",
            "mariage_grossesse",
        ],
        "selected_severity_5_barriers": [
            'recrutement_ga',
        ],
    },

    "BFA_2025": {
        # from cases_coutry_helpers.py lines 148-209 ("## BFA")
        # --- general
        "country": 'Burkina Faso -- BFA',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": 'French',
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

        # --- input files (country_support/BFA/09_code: 01_prepare_pop.R, 02_msna_prep.R; scope-fix by hand)
        # MSNA 2025: all its provinces (31)
        "excel_data_path": 'input/BFA/BFA_MSNA_2025_edu_data_v1.xlsx',
        "excel_path_ocha": 'input/BFA/BFA_Population_figures_PiN2026MSNA2025.xlsx',
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
        "host_value": "non_pdi",
        "idp_value": "pdi",  # IDPs + returnees (one group in the MSNA)
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- Assessment variables (standard names of country_support/BFA/09_code/02_msna_prep.R)
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'no_indicator',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": 3,
        "additional_last_var": 'edu_incident_trajet',
        "additional_last_sev": 4,
        "additional_2_last_var": 'edu_incident_ecol',
        "additional_2_last_sev": 4,
        "barrier_var": 'edu_barrier',
        "barrier_match": "name",  # severity 4/5 barriers below are choice names: "name"; labels (as on the platform): "label" (default)
        "age_var": 'ind_age',
        "gender_var": 'ind_gender',

        # --- barrier severity (choice names of l_raison_pas_educ_formel in the MSNA 2025 tool)
        "selected_severity_4_barriers": [
            "fermeture_ecole",
            "risque_protection",
            "risque_protection_trajet",
            "travail_domestiq",
            "participation_agr",
            "mariage",
            "grossesse",
        ],
        "selected_severity_5_barriers": [
            "interdiction",
        ],
    },

    "BFA_2024": {
        # from cases_coutry_helpers.py lines 148-209 ("## BFA")
        # --- general
        "country": 'Burkina Faso -- BFA',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": 'French',
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

        # --- input files (country_support/BFA/09_code: 01_prepare_pop.R, 02_msna_prep.R; scope-fix by hand)
        # MSNA 2024: only the provinces not covered by the MSNA 2025 (BF4702, BF5303)
        "excel_data_path": 'input/BFA/BFA_MSNA_2024_edu_data_v1.xlsx',
        "excel_path_ocha": 'input/BFA/BFA_Population_figures_PiN2026MSNA2024.xlsx',
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
        "host_value": "non_pdi",
        "idp_value": "pdi",  # IDPs + returnees (one group in the MSNA)
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- Assessment variables (standard names of country_support/BFA/09_code/02_msna_prep.R)
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'no_indicator',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": 3,
        "additional_last_var": 'edu_incident_trajet',
        "additional_last_sev": 4,
        "additional_2_last_var": 'edu_incident_ecol',
        "additional_2_last_sev": 4,
        "barrier_var": 'edu_barrier',
        "barrier_match": "name",  # severity 4/5 barriers below are choice names: "name"; labels (as on the platform): "label" (default)
        "age_var": 'ind_age',
        "gender_var": 'ind_gender',

        # --- barrier severity (choice names of l_raison_pas_educ_formel in the MSNA 2024 tool)
        "selected_severity_4_barriers": [
            "fermeture_ecole",
            "risque_protection",
            "risque_protection_trajet",
            "travail_domestiq",
            "participation_agr",
            "mariage",
        ],
        "selected_severity_5_barriers": [
            "interdiction",
            "enft_recrute",
        ],
    },

    "BFA_2024_regions": {
        # --- general
        "country": 'Burkina Faso -- BFA',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": 'French',
        "label": 'label',
        "start_school": 'September',
        "admin_var": 'Admin_3: Department (Département)',
        "vector_cycle": [10, 14],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": False,
        "mismatch_admin": True,
        "no_ocha_data": False,

        # --- input files (country_support/BFA/09_code: 01_prepare_pop.R, 02_msna_prep.R; scope-fix by hand)
        # MSNA 2024: households only representative at admin1, regions BF13, BF50, BF51, BF55, BF57.
        # Scope-fix: the 102 communes of their provinces not covered by the MSNA 2025 (not Poni, BF5704)
        "excel_data_path": 'input/BFA/BFA_MSNA_2024_regions_edu_data_v1.xlsx',
        "excel_path_ocha": 'input/BFA/BFA_Population_figures_PiN2026MSNA2024_regions.xlsx',
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
        "host_value": "non_pdi",
        "idp_value": "pdi",  # IDPs + returnees (one group in the MSNA)
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- Assessment variables (standard names of country_support/BFA/09_code/02_msna_prep.R)
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'no_indicator',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": 3,
        "additional_last_var": 'edu_incident_trajet',
        "additional_last_sev": 4,
        "additional_2_last_var": 'edu_incident_ecol',
        "additional_2_last_sev": 4,
        "barrier_var": 'edu_barrier',
        "barrier_match": "name",  # severity 4/5 barriers below are choice names: "name"; labels (as on the platform): "label" (default)
        "age_var": 'ind_age',
        "gender_var": 'ind_gender',

        # --- barrier severity (choice names of l_raison_pas_educ_formel in the MSNA 2024 tool)
        "selected_severity_4_barriers": [
            "fermeture_ecole",
            "risque_protection",
            "risque_protection_trajet",
            "travail_domestiq",
            "participation_agr",
            "mariage",
        ],
        "selected_severity_5_barriers": [
            "interdiction",
            "enft_recrute",
        ],
    },

    "MOZ_IOM_2026": {
        # --- general
        "country": "Mozambique -- MOZ",
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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
        "excel_data_path": "input/LBN/REACH_LBN_Dataset_MSNA_2026_edu.xlsx",
        "excel_path_ocha": "input/LBN/LBN_MSNA_pop.xlsx",
        
        "sheets": {
            "household": "clean_main",
            "edu": "clean_edu",
            "survey": "survey",
            "choices": "choices",
            "ocha": "ocha",
            "scope_fix": "scope-fix",
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        "host_value": "lebanese",
        "idp_value": None,
        "returnee_value": None ,
        "refugee_value": "palestinian",
        "other_value": "migrant",

        # --- Assessment variables
        "status_var": "pop_group",
        "age_var": "edu_ind_age",
        "gender_var": "edu_ind_gender",
        "access_var": "edu_access",
        "teacher_disruption_var": "edu_disrupted_teacher",
        "idp_disruption_var": "edu_disrupted_displaced",
        "natural_hazard_var": "edu_disrupted_hazards",
        "natural_hazard_var_sev": 4,
        "armed_disruption_var": 'edu_disrupted_attack',
        "additional_last_var": "edu_disrupted_occupied_armed_forces",
        "additional_last_sev": 4,
        "additional_2_last_var": "no_indicator",
        "additional_2_last_sev": None,
        "barrier_var": "edu_barrier",

        # --- barrier severity
        "selected_severity_4_barriers": ['The child needs to work at home or on the household’s farm without earning an income, including to allow other household members to undertake income-generating activities',
                'The child is engaged in income-generating activities outside the home',
                'The child faces protection risks at school',
                'The child faces protection risks while travelling to or from school',
                'The child is married or engaged',
                'The school is closed due to damage, a natural disaster, or conflict',
                'The child is experiencing discrimination or stigmatisation',
                'A restriction or ban will prevent the child from attending school'],

        "selected_severity_5_barriers": ['The child is associated with armed forces or armed groups',
                'The child is pregnant',
                'The child can not enrol due to a lack of documentation'],
    },

     "CAR_2026_fr_admin1": {
        # from cases_coutry_helpers.py lines 660-725 ("## CAR")
        # second '## CAR' block
        # --- general
        "country": 'Central African Republic -- CAR',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": 'French',
        "label": 'label::Français (fr)',
        "start_school": 'September',
        "admin_var": 'Admin_1: Prefectures (préfectures)',
        "vector_cycle": [12, 16],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": True,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/CAF/CAF_MSNA_edu_data.xlsx',
        "excel_path_ocha": 'input/CAF/CAF_Population_figures_admin1.xlsx',
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
        "host_value": 'hote',
        "idp_value": 'idp_site',
        "returnee_value": 'retourne',
        "refugee_value": None,
        "other_value": 'idp_host' ,

        # --- Assessment variables
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'edu_disrupted_attack',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": 3,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'edu_barrier',
        "barrier_match": "name",  # severity 4/5 barriers below are choice names: "name"; labels (as on the platform): "label" (default)
        "age_var": 'edu_ind_age',
        "gender_var": 'edu_ind_gender',

        # --- barrier severity
        "selected_severity_4_barriers": [
                "child_work_home",
                "child_work_outside",
                "protection_at_school",
                "protection_travel_school",
                "child_marriage",
                "school_closed",
        ],
        "selected_severity_5_barriers": [
            "child_armed_group",
            "child_pregnancy",
        ],
    },

     "CAR_2026_fr_admin2": {
        # from cases_coutry_helpers.py lines 660-725 ("## CAR")
        # second '## CAR' block

        "step_2_hpc": True,              # True = step 2 (run_hybrid_step2.py)
        "updated_pin_path": "input/CAF/CAR_PiN2026_step1_to-fill_filled.xlsx",
        "covered_pin_path": "output_validation/CAR/CAR_2026_fr_admin2/CAR_PiN2026_step1_covered-areas_*.xlsx",


        "country": 'Central African Republic -- CAR',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": 'French',
        "label": 'label::Français (fr)',
        "start_school": 'September',
        "admin_var": 'Admin_2: Sub-prefectures (sous-préfectures)',
        "vector_cycle": [12, 16],
        # TODO: add later — not used by the run script yet
        # "primary_start": 6,
        # "secondary_end": 17,
        "hybrid_country": True,  # not set in original: default
        "mismatch_admin": False,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/CAF/CFA_MSNA_edu_data.xlsx',
        "excel_path_ocha": 'input/CAF/CAF_Population_figures_admin2.xlsx',
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
        "host_value": 'hote',
        "idp_value": 'idp_site',
        "returnee_value": 'retourne',
        "refugee_value": None,
        "other_value": 'idp_host' ,

        # --- Assessment variables
        "status_var": 'pop_group',
        "access_var": 'edu_access',
        "teacher_disruption_var": 'edu_disrupted_teacher',
        "idp_disruption_var": 'edu_disrupted_displaced',
        "armed_disruption_var": 'edu_disrupted_attack',
        "natural_hazard_var": 'edu_disrupted_hazards',
        "natural_hazard_var_sev": 3,  # not set in original: default
        "additional_last_var": 'no_indicator',  # not set in original: default
        "additional_last_sev": None,  # not set in original: default
        "additional_2_last_var": 'no_indicator',  # not set in original: default
        "additional_2_last_sev": None,  # not set in original: default
        "barrier_var": 'edu_barrier',
        "barrier_match": "name",  # severity 4/5 barriers below are choice names: "name"; labels (as on the platform): "label" (default)
        "age_var": 'edu_ind_age',
        "gender_var": 'edu_ind_gender',

         # --- barrier severity
        "selected_severity_4_barriers": [
                "child_work_home",
                "child_work_outside",
                "protection_at_school",
                "protection_travel_school",
                "child_marriage",
                "school_closed",
        ],
        "selected_severity_5_barriers": [
            "child_armed_group",
            "child_pregnancy",
        ],
    },

    "AFG_2026_no_ban_admin1-2": {
        
        # --- general
        "country": 'Afghanistan -- AFG',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": 'English',
        "label": 'label::English',
        "start_school": 'November',
        "admin_var": 'Admin_2: Province',
        "vector_cycle": [14, 16],
        # TODO: add later — not used by the run script yet
        # "primary_start": 7,
        # "secondary_end": 17,
        "hybrid_country": False,  # not set in original: default
        "mismatch_admin": True,
        "no_ocha_data": False,  # not set in original: default

        # --- input files
        "excel_data_path": 'input/AFG/00_Datasets/AFG_MSNA_edu_data.xlsx',
        "excel_path_ocha": 'input/AFG/10_PiN supporting files/AFG_Population_figures_filled_v4.xlsx',
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

        # --- Assessment variables
        "status_var": "pop_group",
        "age_var": "edu_ind_age",
        "gender_var": "edu_ind_gender",
        "access_var": "edu_access",
        "teacher_disruption_var": "edu_disrupted_teacher",
        "idp_disruption_var": "edu_disrupted_displaced",
        "natural_hazard_var": "no_indicator",
        "natural_hazard_var_sev": None,
        "armed_disruption_var": "no_indicator",
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

    "AFG_2026_no_ban_admin2": {
        
        # --- general
        "country": 'Afghanistan -- AFG',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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
        "excel_path_ocha": 'input/AFG/10_PiN supporting files/AFG_Population_figures_filled_v3.xlsx',
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

        # --- Assessment variables
        "status_var": "pop_group",
        "age_var": "edu_ind_age",
        "gender_var": "edu_ind_gender",
        "access_var": "edu_access",
        "teacher_disruption_var": "edu_disrupted_teacher",
        "idp_disruption_var": "edu_disrupted_displaced",
        "natural_hazard_var": "no_indicator",
        "natural_hazard_var_sev": None,
        "armed_disruption_var": "no_indicator",
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

    "AFG_2026_limited_ban": {
        
        # --- general
        "country": 'Afghanistan -- AFG',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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

        # --- Assessment variables
        "status_var": "pop_group",
        "age_var": "edu_ind_age",
        "gender_var": "edu_ind_gender",
        "access_var": "edu_access",
        "teacher_disruption_var": "edu_disrupted_teacher",
        "idp_disruption_var": "edu_disrupted_displaced",
        "natural_hazard_var": "no_indicator",
        "natural_hazard_var_sev": None,
        "armed_disruption_var": "no_indicator",
        "additional_last_var": "no_indicator",
        "additional_last_sev": None,
        "additional_2_last_var": "no_indicator",
        "additional_2_last_sev": None,
        "barrier_var": "edu_orig_barrier",

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

    "AFG_2026_full_ban": {
        
        # --- general
        "country": 'Afghanistan -- AFG',
        "full_GEC_compliant": True,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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

        # --- Assessment variables
        "status_var": "pop_group",
        "age_var": "edu_ind_age",
        "gender_var": "edu_ind_gender",
        "access_var": "edu_access",
        "teacher_disruption_var": "edu_disrupted_teacher",
        "idp_disruption_var": "edu_disrupted_displaced",
        "natural_hazard_var": "no_indicator",
        "natural_hazard_var_sev": None,
        "armed_disruption_var": "no_indicator",
        "additional_last_var": "no_indicator",
        "additional_last_sev": None,
        "additional_2_last_var": "no_indicator",
        "additional_2_last_sev": None,
        "barrier_var": "edu_orig_barrier",

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

    "LBN_MSNA_2026": {
        # --- general
        "country": "Lebanon -- LBN",
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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
        "excel_data_path": "input/LBN/REACH_LBN_Dataset_MSNA_2026_edu.xlsx",
        "excel_path_ocha": "input/LBN/LBN_MSNA_pop.xlsx",
        
        "sheets": {
            "household": "clean_main",
            "edu": "clean_edu",
            "survey": "survey",
            "choices": "choices",
            "ocha": "ocha",
            "scope_fix": "scope-fix",
        },
        "output_dir": "output_validation",

        # --- population-group mapping (page 2): values from your status column, None if the group is not present
        "host_value": "lebanese",
        "idp_value": None,
        "returnee_value": None ,
        "refugee_value": "palestinian",
        "other_value": "migrant",

        # --- Assessment variables
        "status_var": "pop_group",
        "age_var": "edu_ind_age",
        "gender_var": "edu_ind_gender",
        "access_var": "edu_access",
        "teacher_disruption_var": "edu_disrupted_teacher",
        "idp_disruption_var": "edu_disrupted_displaced",
        "natural_hazard_var": "edu_disrupted_hazards",
        "natural_hazard_var_sev": 4,
        "armed_disruption_var": 'edu_disrupted_attack',
        "additional_last_var": "edu_disrupted_occupied_armed_forces",
        "additional_last_sev": 4,
        "additional_2_last_var": "no_indicator",
        "additional_2_last_sev": None,
        "barrier_var": "edu_barrier",

        # --- barrier severity
        "selected_severity_4_barriers": ['The child needs to work at home or on the household’s farm without earning an income, including to allow other household members to undertake income-generating activities',
                'The child is engaged in income-generating activities outside the home',
                'The child faces protection risks at school',
                'The child faces protection risks while travelling to or from school',
                'The child is married or engaged',
                'The school is closed due to damage, a natural disaster, or conflict',
                'The child is experiencing discrimination or stigmatisation',
                'A restriction or ban will prevent the child from attending school'],

        "selected_severity_5_barriers": ['The child is associated with armed forces or armed groups',
                'The child is pregnant',
                'The child can not enrol due to a lack of documentation'],
    },

    "VaSYR_2026": {
        # --- general
        "country": "Lebanon -- LBN",
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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

        # --- Assessment variables
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
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
        "selected_language": "English",
        "label": "label::english",
        "start_school": "September",
        "admin_var": "Admin_2: Districts",
        "vector_cycle": [13, 0],
        # TODO: add later — not used by the run script yet
        # "primary_start": 7,
        # "secondary_end": 17,
        "hybrid_country": False,           # True = hybrid country: French labels are not translated in calculatePIN
        "step_2_hpc": False,              # hybrid countries: False = step 1 (run_PiNcalculation_outside_streamlit.py); True = step 2 (run_hybrid_step2.py)
        "mismatch_admin": False,
        "no_ocha_data": False,

        # --- input files
        "excel_data_path": "input/SOM/SOM_MSNA_ALL_edu_data.xlsx",
        "excel_path_ocha": "input/SOM/SOM_Population_figures_filled_v2.xlsx",
        # step 2 inputs: the step 1 "step1_to-fill" file once filled (copy it to input/ first, so that it stays with the
        # inputs) and the step 1 "step1_covered-areas" file; a * stands for the newest matching file
        "updated_pin_path": "input/SOM/SOM_PiN2026_step1_to-fill_filled.xlsx",
        "covered_pin_path": "output_validation/SOM/SOM_2026/SOM_PiN2026_step1_covered-areas_*.xlsx",
        
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

        # --- Assessment variables
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
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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

        # --- Assessment variables
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
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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

        # --- Assessment variables
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
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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

        # --- Assessment variables
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

    "AFG_2024": {
        # from cases_coutry_helpers.py lines 210-275 ("## AFG")
        # --- general
        "country": 'Afghanistan -- AFG',
        "full_GEC_compliant": True,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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

        # --- Assessment variables
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
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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

        # --- Assessment variables
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
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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

        # --- Assessment variables
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

    "MLI_2024": {
        # from cases_coutry_helpers.py lines 599-659 ("## MLI")
        # --- general
        "country": 'Mali -- MLI',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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

        # --- Assessment variables
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

    "CAR_2024_a": {
        # from cases_coutry_helpers.py lines 536-598 ("## CAR")
        # first '## CAR' block (different barriers/indicators from CAR_2024_b)
        # --- general
        "country": 'Central African Republic -- CAR',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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

        # --- Assessment variables
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

    "CAR_2024_b": {
        # from cases_coutry_helpers.py lines 660-725 ("## CAR")
        # second '## CAR' block
        # --- general
        "country": 'Central African Republic -- CAR',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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

        # --- Assessment variables
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
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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
        "excel_data_path": 'input/Assessment Mozambique 2025.xlsx',
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

        # --- Assessment variables
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
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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

        # --- Assessment variables
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
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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

        # --- Assessment variables
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

    "BFA_2025-old": {
        # from the former run_PiNcalculation_outside_streamlit2.py (deleted), "## BFA (run2)"
        # --- general
        "country": 'Burkina Faso -- BFA',
        "full_GEC_compliant": False,  # True: GEC compliant (all out-of-school girls above 12 in severity 5); False: not GEC compliant (standard rules)
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
        "excel_data_path": 'input/BFA/REACH I BFA I 2025 Assessment-eduPlatform.xlsx',
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
        "host_value": 'non_pdi',  # from the former run_PiNcalculation_outside_streamlit2.py
        "idp_value": 'pdi',
        "returnee_value": None,
        "refugee_value": None,
        "other_value": None,

        # --- Assessment variables
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


# --- JENA and EMIS countries: cases for run_PiNcalculation_outside_streamlit_JENA_config.py / _EMIS_config.py.
# Derived from NER_2024 and LMR_2022 with the settings of the old run_PiNcalculation_outside_streamlit_JENA.py / _EMIS.py
# (kept for reference). Extra keys, as on page 1 of the platform:
#   "data_combination": JENA when 'mjjm'; EMIS when 'emmm', 'eemm' or 'eeem'
#   "excel_path_other": the JENA or EMIS file, read from the sheet "sheets"["other"] (page 1 reads 'indicator';
#                       the old scripts read the first sheet)
# TODO: fill in the population-group mapping (host_value, ...) before running: the old scripts predate it.
CASES["NER_2024_JENA"] = {
    **CASES["NER_2024"],
    "data_combination": 'mjjm',
    "excel_path_other": 'input/Niger_JENA_PTR_protection.xlsx',
    "sheets": {**CASES["NER_2024"]["sheets"], "other": 'indicator'},
    "status_var": 'd_statut_deplacement',
    "access_var": 'edu_access',
    "teacher_disruption_var": 'edu_disrupted_teacher',
    "idp_disruption_var": 'edu_disrupted_displaced',
    "armed_disruption_var": 'edu_disrupted_occupation',
    "natural_hazard_var": 'no_indicator',
    "natural_hazard_var_sev": None,
    "additional_last_var": 'no_indicator',
    "additional_last_sev": None,
    "additional_2_last_var": 'no_indicator',
    "additional_2_last_sev": None,
    "barrier_var": 'edu_barrier',
    "age_var": 'ind_age',
    "gender_var": 'ind_gender',
    "selected_severity_4_barriers": [
        "L'école a été fermée en raison de dommages, d'une catastrophe naturelle ou d'un conflit.",
        "Mariage, fiançailles et/ou grossesse",
        "Risques de protection à l'école",
        "Risques de protection pendant le trajet vers l'école",
        "L'enfant doit travailler à la maison ou dans la ferme du ménage (c'est-à-dire qu'il ne gagne pas de revenu pour ces activités, mais peut permettre à d'autres membres de la famille de gagner un revenu)",
        "L'enfant participe à des activités génératrices de revenus en dehors du foyer",
    ],
    "selected_severity_5_barriers": [
        "L'enfant est associé à des forces armées ou à des groupes armés",
    ],
}

CASES["LMR_2022_EMIS"] = {
    **CASES["LMR_2022"],
    "data_combination": 'eemm',
    "excel_path_other": 'input/emis_LMR_eemm.xlsx',
    "no_ocha_data": False,     # EMIS needs the OCHA figures (LMR_2022 runs without them)
    "sheets": {**CASES["LMR_2022"]["sheets"], "ocha": 'ocha', "other": 'indicator'},
}
