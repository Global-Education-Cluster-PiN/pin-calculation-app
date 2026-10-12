# Parameters used in local runs, as on the platform: "Parameters Used" sheet of the PiN results and
# Parameters_Input_Document.docx. Used by run_PiNcalculation_outside_streamlit.py and run_hybrid_step2.py.
from src.save_parameter import generate_parameters, generate_word_document
from src.save_parameter_FR import generate_parameters_FR, generate_word_document_FR


def case_parameters(cfg):
    """Return (parameters, Word document as BytesIO) for a case of run_config.py.

    generate_parameters reads the Streamlit session-state names; some of them are named differently in run_config.py.
    """
    additional_last_var, additional_2_last_var = cfg["additional_last_var"], cfg["additional_2_last_var"]
    param_state = {
        **cfg,
        "selected_disruption_natural_hazard_column": cfg["natural_hazard_var"],
        "natural_hazard_disruption_severity": cfg["natural_hazard_var_sev"],
        "additional_indicator_last_var": additional_last_var,
        "additional_indicator_last_severity": cfg["additional_last_sev"],
        "additional_2_indicator_last_var": additional_2_last_var,
        "additional_2_indicator_last_severity": cfg["additional_2_last_sev"],
        # generate_parameters_FR lists the additional indicators only when these switches are on (set by page 2)
        "additional_indicator_enable": bool(additional_last_var) and additional_last_var != "no_indicator",
        "additional_2_indicator_enable": bool(additional_2_last_var) and additional_2_last_var != "no_indicator",
        "pop_group_value_map": {"status_column": cfg["status_var"], "host": cfg["host_value"], "idp": cfg["idp_value"],
                                "returnee": cfg["returnee_value"], "refugee": cfg["refugee_value"], "other": cfg["other_value"]},
    }
    if cfg["selected_language"] == "French":
        parameters = generate_parameters_FR(param_state)
        return parameters, generate_word_document_FR(parameters)
    parameters = generate_parameters(param_state)
    return parameters, generate_word_document(parameters)
