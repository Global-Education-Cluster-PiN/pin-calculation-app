# Children aged 3-4 and teachers in the PiN results file, for the cases of run_config.py with
# "ece_3_4_ratio" (3-4 population / 5-17 population) and "students_per_teacher":
#   3-4      = every 5-17 figure x ece_3_4_ratio (same rates as the 5-17 children)
#   teachers = (5-17 + 3-4) / students_per_teacher
# # figures rounded to whole numbers; % figures the same as the 5-17 ones. Only the Excel results
# change: the snapshot, the maps and the other outputs stay 5-17.
#   - PiN TOTAL: "<group> (3-4 y.o.)" and "<group> teachers" rows after each group's 5-17 row, and the
#     totals TOTAL ALL (3-17 y.o. + teachers), TOTAL (5-17 y.o.), TOTAL (3-4 y.o.), TOTAL teachers
#   - one sheet per age band / teachers and per table by admin: "PiN 3-4 -- Overall",
#     "PiN 3-4 -- <group>", "PiN teachers -- Overall", ... (not "PiN -- ", the prefix that the
#     readers of the group sheets look for); Area severity left empty, with a note
import pandas as pd

LABELS = {
    "English": {
        "age_5_17": "5-17 y.o.", "age_3_4": "3-4 y.o.", "teachers": "teachers",
        "total": "TOTAL", "total_all": "TOTAL ALL (3-17 y.o. + teachers)",
        "sheet_3_4": "PiN 3-4", "sheet_teachers": "PiN teachers", "overall": "Overall",
        "overall_title": "Overall PiN and severity",
        "note": "Area severity: see the 5-17 y.o. sheet (same rates)",
    },
    "French": {
        "age_5_17": "5-17 ans", "age_3_4": "3-4 ans", "teachers": "enseignants",
        "total": "TOTAL", "total_all": "TOTAL TOUS (3-17 ans + enseignants)",
        "sheet_3_4": "PiN 3-4 ans", "sheet_teachers": "PiN enseignants", "overall": "total",
        "overall_title": "PiN total par admin",
        "note": "Sévérité de la zone : voir la feuille 5-17 ans (mêmes taux)",
    },
}
POPULATION_COLUMNS = ("TotN", "Population totale")
AREA_SEVERITY_COLUMNS = ("Area severity", "Sévérité de la zone")


def labels_for(overview_df):
    """Labels of the language of the tables: French only when calculatePIN translated them (5-17 ans)."""
    for labels in LABELS.values():
        if f"{labels['total']} ({labels['age_5_17']})" in set(overview_df["Strata"]):
            return labels
    raise ValueError("ece_3_4_ratio: no TOTAL (5-17 y.o.) row in the PiN overview, the 3-4 and teacher "
                     f"figures need the 5-17 band (strata: {list(overview_df['Strata'])})")


def count_columns(df):
    return [c for c in df.columns if str(c).startswith("#") or c in POPULATION_COLUMNS]


def scale(df, factor):
    """df with its # and population columns x factor, rounded (the % columns are the same)."""
    out = df.copy()
    for col in count_columns(out):
        out[col] = (pd.to_numeric(out[col]) * factor).round().astype("Int64")
    return out


def rename_strata(rows, labels, new_suffix):
    """Strata of the 5-17 rows with another suffix: "host (5-17 y.o.)" -> "host (3-4 y.o.)" or "host teachers"."""
    rows = rows.copy()
    rows["Strata"] = rows["Strata"].str.removesuffix(f" ({labels['age_5_17']})") + new_suffix
    return rows


def extend_overviews(overview_df, overview_ocha_df, ratio, students_per_teacher):
    """PiN TOTAL tables with the 3-4 and teacher rows and totals; the total labels (for the formatting)."""
    labels = labels_for(overview_df)
    total_5_17 = f"{labels['total']} ({labels['age_5_17']})"
    teacher_factor = (1 + ratio) / students_per_teacher

    is_total = overview_df["Strata"] == total_5_17
    groups = overview_df[~is_total]
    rows_3_4 = rename_strata(scale(groups, ratio), labels, f" ({labels['age_3_4']})")
    rows_teachers = rename_strata(scale(groups, teacher_factor), labels, f" {labels['teachers']}")

    # Totals: sums of the group rows (the TOTAL (5-17) row is the sum of the 5-17 group rows)
    total_row = overview_df[is_total]
    totals = {}
    for key, rows in (("3_4", rows_3_4), ("teachers", rows_teachers)):
        row = total_row.copy()
        for col in count_columns(row):
            row[col] = rows[col].sum()
        totals[key] = row
    totals["3_4"]["Strata"] = f"{labels['total']} ({labels['age_3_4']})"
    totals["teachers"]["Strata"] = f"{labels['total']} {labels['teachers']}"
    total_all = total_row.copy()
    for col in count_columns(total_all):
        total_all[col] = (pd.to_numeric(total_row[col]).astype("Int64") + totals["3_4"][col].values
                          + totals["teachers"][col].values)
    total_all["Strata"] = labels["total_all"]

    # Each group: 5-17, 3-4, teachers
    group_blocks = [pd.concat([groups.iloc[[i]], rows_3_4.iloc[[i]], rows_teachers.iloc[[i]]])
                    for i in range(len(groups))]
    new_overview = pd.concat([total_all, total_row, totals["3_4"], totals["teachers"], *group_blocks],
                             ignore_index=True)

    # OCHA table: the same rows (its columns), then its other rows (girls, boys, ECE, ...) unchanged
    ocha_cols = list(overview_ocha_df.columns)
    covered = set(new_overview["Strata"])
    new_ocha = pd.concat([new_overview[[c for c in ocha_cols if c in new_overview.columns]],
                          overview_ocha_df[~overview_ocha_df["Strata"].isin(covered)]],
                         ignore_index=True)[ocha_cols]
    missing = set(overview_ocha_df["Strata"]) - set(new_ocha["Strata"])
    if missing:
        raise ValueError(f"ece_3_4_ratio: rows of the OCHA overview lost: {missing}")

    total_labels = {labels["total_all"], f"{labels['total']} ({labels['age_3_4']})",
                    f"{labels['total']} {labels['teachers']}"}
    return new_overview, new_ocha, total_labels


def admin_sheets(tot_severity, group_tables, ratio, students_per_teacher, overview_df):
    """{sheet name: (table by admin, title, note)} of the 3-4 children and the teachers."""
    labels = labels_for(overview_df)
    teacher_factor = (1 + ratio) / students_per_teacher
    sheets = {}
    for band, factor, sheet_prefix in ((labels["age_3_4"], ratio, labels["sheet_3_4"]),
                                       (labels["teachers"], teacher_factor, labels["sheet_teachers"])):
        tables = {labels["overall"]: (tot_severity, f"{labels['overall_title']} ({band})")}
        tables.update({group: (df, f"PiN -- {group} ({band})") for group, df in group_tables.items()})
        for name, (df, title) in tables.items():
            sheet = f"{sheet_prefix} -- {name}"[:31]
            if sheet in sheets:
                raise ValueError(f"ece_3_4_ratio: two sheets named {sheet} (31 characters at most)")
            table = scale(df, factor)
            for col in AREA_SEVERITY_COLUMNS:
                if col in table.columns:
                    table[col] = None
            sheets[sheet] = (table, title, labels["note"])
    return sheets
