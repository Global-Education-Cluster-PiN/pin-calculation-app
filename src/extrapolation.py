import os
import glob
import pandas as pd
import copy

admin_var = 'Admin Pcode'
ref_user_admin = 'Reference area Admin Pcode (for extrapolation)'
ref_suggested_admin = 'Suggested reference area for extrapolation'
ref_suggested_other = 'Alternative reference areas'
severity_2025_cols = [
        '% severity levels 1-2', '# severity levels 1-2',
        '% severity level 3', '# severity level 3',
        '% severity level 4', '# severity level 4',
        '% severity level 5', '# severity level 5'
    ]
stable_cols = [
        "Education needs stable (tick 'X' if no change from last year)",
        "Les besoins en matière d'éducation sont stables (cochez « X » si aucun changement par rapport à l'année dernière)"
    ]
pct_2025_cols = ['% severity levels 1-2', '% severity level 3', '% severity level 4', '% severity level 5']
delta_cols = [
        "Education needs decreased (tick 'X' if improved from last year)",
        "Les besoins en matière d'éducation ont diminué (cochez « X » si la situation s'est améliorée par rapport à l'année dernière)",
        "Education needs worsened (tick 'X' if worsened from last year)",
        "Les besoins en matière d'éducation se sont aggravés (cochez « X » si la situation s'est aggravée par rapport à l'année dernière)"
    ]



## --------------------------------------------------------------------------------------------------------------
def has_2025_data(df):
    """Per row: True if the area has 2025 MSNA results, i.e. its % by severity add up to more than 0 (100 when
    covered). Areas without MSNA data come as empty cells or, in step 1 files made before this check, as 0."""
    cols = [col for col in pct_2025_cols if col in df.columns]
    if not cols:
        return pd.Series(True, index=df.index)
    return df[cols].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1) > 0
## --------------------------------------------------------------------------------------------------------------
def match_pin2024_sheets(pin2025_by_status, pin2024_cat):
    """Name the 2024 sheets as the population groups of the step 1 file, ignoring case and spaces ('IDP' = 'idp').
    2024 sheets without a step 1 group keep their name."""
    def key(name):
        return str(name).strip().lower().replace(" ", "")
    by_key = {key(name): name for name in pin2024_cat}
    matched = {}
    for category in pin2025_by_status:
        name_2024 = by_key.get(key(category))
        if name_2024 is not None:
            matched[category] = pin2024_cat[name_2024]
    used = {by_key[key(category)] for category in matched}
    matched.update({name: df for name, df in pin2024_cat.items() if name not in used and name not in matched})
    return matched
## --------------------------------------------------------------------------------------------------------------
NOTE_TEXT = {
    "English": {
        "no_reference": "no reference area with 2025 data: 2024 values kept (needs considered stable)",
        "no_reference_data": "the reference area {ref} has no usable 2024 and 2025 data: 2024 values kept (needs considered stable)",
        "no_2024": "no 2024 PiN for this area: not extrapolated, the area is left out",
    },
    "French": {
        "no_reference": "aucune zone de référence avec des données 2025 : valeurs 2024 conservées (besoins considérés stables)",
        "no_reference_data": "la zone de référence {ref} n'a pas de données 2024 et 2025 utilisables : valeurs 2024 conservées (besoins considérés stables)",
        "no_2024": "pas de PiN 2024 pour cette zone : non extrapolée, la zone n'est pas incluse",
    },
}
## --------------------------------------------------------------------------------------------------------------
def find_valid_ref(row, valid_list):
    for candidate in [
        row[ref_user_admin],
        row[ref_suggested_admin]
    ]:
        if candidate in valid_list:
            return candidate
    # Check alternative list
    alternatives = str(row[ref_suggested_other]).split(';')
    for alt in alternatives:
        if alt in valid_list:
            return alt
    return ''  # None found
## --------------------------------------------------------------------------------------------------------------



## the pin 2024 will be looked for in the DATA_DIR_PIN2024 according to the country code
## the pin2025 file by population group has to be upload and it is stored: 
## the inputfile filled by the user is the output of the make_output1_platform.py filled by the user on those 4 specific columns

############################################################################################################

def extrapolate_df_2025_updated(base_2025, pin2025_by_status, pin2024_cat, notes=None, selected_language='English'):
    # notes: optional list; one row is added (population group, area, reference area, note) for each area that could
    # not be extrapolated as asked, to be shown to the user and in the PiN results

    print(base_2025.columns)
    note_text = NOTE_TEXT.get(selected_language, NOTE_TEXT["English"])
    def add_note(category, admin, ref, key):
        if notes is not None:
            notes.append({"Population group": category, "Admin Pcode": admin, "Reference area": ref or "",
                          "Note": note_text[key].format(ref=ref)})

    pin2024_cat = match_pin2024_sheets(pin2025_by_status, pin2024_cat)

    # 1. ---- create lists: list_remove, list_2025, list_delta, list_same,
    #        - list_remove = list of admins where the values of the columns containing 'severity' is: 'Missing MSNA data for 2024 AND 2025'
    #        - list_2025 = list of admins where the values of the columns in place 4->11 are not all empty
    #        - list_same = list of admins where the colum called: either  'Education needs stable (tick 'X' if no change from last year)'
    #            or 'Les besoins en matière d'éducation sont stables (cochez « X » si aucun changement par rapport à l'année dernière)' contain 'X' or 'x'
    #        - list_delta = list of admins where the colum called: either  'Education needs decreased (tick 'X' if improved from last year)'
    #            or 'Les besoins en matière d'éducation ont diminué (cochez « X » si la situation s'est améliorée par rapport à l'année dernière)'or 
    #            Education needs worsened (tick 'X' if worsened from last year) or 'Les besoins en matière d'éducation se sont aggravés (cochez « X » si la situation s'est aggravée par rapport à l'année dernière)' contain 'X' or 'x'

        # Initialize empty lists
    # Output lists
    list_remove = []
    list_same = []
    list_delta = []

    pin_2025_delta = {}
    pin_2025_same = {}
    pin_2025_covered = {} ## the ones already covered by 2025 MSNA
    pin_2025_updated = {}

    list_2025_category = {}

    for category, df_2025 in pin2025_by_status.items():
        if df_2025.empty:
            continue
        first_col = df_2025.columns[0]
        df_2025 = df_2025.rename(columns={first_col: "Admin Pcode"})
        # covered (and valid reference areas): only the areas with 2025 MSNA results in this population group
        df_2025 = df_2025[has_2025_data(df_2025)]
        list_2025_cat = df_2025["Admin Pcode"].dropna().unique().tolist()
        list_2025_category[category] = {"list_2025": list_2025_cat}


        keep_cols = [
            "Admin Pcode",
            "% severity levels 1-2",
            "% severity level 3",
            "% severity level 4",
            "% severity level 5"
        ]

        # Filter columns safely
        existing_keep_cols = [col for col in keep_cols if col in df_2025.columns]
        df_2025_filtered = df_2025[existing_keep_cols].copy()

        # Save back
        pin_2025_covered[category] = df_2025_filtered

    print('===========================')    
    print(list_2025_category)    
    print('===========================')    

    # Columns
    severity_cols = [col for col in base_2025.columns if 'severity' in col]
    with_2025_data = has_2025_data(base_2025)
    # checks of the filled step 1 file (as page 1 on the platform): otherwise areas are dropped without a message
    if not severity_cols:
        raise ValueError("The filled step 1 file has no 'severity' columns: every area would be taken as without MSNA data")
    if not any(col in base_2025.columns for col in stable_cols + delta_cols):
        raise ValueError("The filled step 1 file has none of the columns to tick (stable, decreased, worsened): "
                         "were the headers changed?")
    list_no_tick = []

    for idx, row in base_2025.iterrows():
        admin_pcode = row[admin_var]

        # (1) Remove if ALL severity cols contain missing string
        if all(str(row[col]).strip().lower() == 'missing msna data for 2024 and 2025' for col in severity_cols):
            list_remove.append(admin_pcode)
            continue  # Skip further checks

    
        # (3) Check 'same' if the area has no 2025 MSNA results (empty, or 0 in older step 1 files)
        if not with_2025_data[idx]:
            for col in stable_cols:
                if col in row and str(row[col]).strip().lower() == 'x':
                    list_same.append(admin_pcode)
                    break

            # (4) If not stable, check for delta
            else:
                for col in delta_cols:
                    if col in row and str(row[col]).strip().lower() == 'x':
                        list_delta.append(admin_pcode)
                        break
                else:
                    if pd.notna(admin_pcode):   # not the empty rows at the end of the sheet
                        list_no_tick.append(admin_pcode)

    if list_no_tick:
        raise ValueError(f"{len(list_no_tick)} area(s) without 2025 MSNA data and no tick (stable, decreased or worsened) "
                         f"in the filled step 1 file: {', '.join(map(str, list_no_tick))}")

    base_2025 = base_2025[~base_2025['Admin Pcode'].isin(list_remove)].copy()

    pin_2024_missing_2025 = {}
    for category, df_2024 in pin2024_cat.items():
        first_col_2024 = df_2024.columns[0]
        df_2024 = df_2024.rename(columns={first_col_2024: "Admin Pcode 2024"})
        df_2024_filtered = df_2024[df_2024["Admin Pcode 2024"].isin(list_delta)].copy()
        df_2024_filtered.columns = df_2024_filtered.columns.str.replace(" ", "_")
        admin_col = "Admin_Pcode_2024"  # After replacing spaces
        df_2024_filtered = df_2024_filtered.rename(columns={
            col: f"{col}_2024_extrapolation_base"
            for col in df_2024_filtered.columns if col != admin_col
        })
        pin_2024_missing_2025[category] = df_2024_filtered

    pin_2025_same = {}
    for category, df_2024 in pin2024_cat.items():
        first_col_2024 = df_2024.columns[0]
        df_2024 = df_2024.rename(columns={first_col_2024: "Admin Pcode"})
        df_2024_filtered = df_2024[df_2024["Admin Pcode"].isin(list_same)].copy()
        # (Optionally select only the 4 % columns if you want stricter schema)
        pin_2025_same[category] = df_2024_filtered


    print('------------------')
    print(list_remove)    
    print('------------------')
    print(list_same)    
     # ===================== EARLY EXIT: nothing to extrapolate =====================
    if not list_delta:
        def _std(series):
            s = series.copy()
            mask = s.notna()
            s.loc[mask] = s.loc[mask].astype(str).str.strip().str.upper()
            return s

        def _clean_unique(df):
            if df.empty or "Admin Pcode" not in df.columns:
                return df
            df = df.copy()
            df["Admin Pcode"] = _std(df["Admin Pcode"])
            df = df[df["Admin Pcode"].notna() & (df["Admin Pcode"].astype(str).str.len() > 0)]
            return df.drop_duplicates(subset=["Admin Pcode"], keep="first")

        pin_2025_updated = {}
        all_cats = set(pin2025_by_status.keys()) | set(pin_2025_covered.keys()) | set(pin_2025_same.keys())

        for category in all_cats:
            covered = pin_2025_covered.get(category, pd.DataFrame()).copy()
            same    = pin_2025_same.get(category, pd.DataFrame()).copy()

            covered = _clean_unique(covered)
            same    = _clean_unique(same)

            # Anti-join: if an admin is in "same", prefer the 2024 row; remove it from covered
            if not covered.empty and not same.empty:
                covered = covered[~covered["Admin Pcode"].isin(same["Admin Pcode"])]

            # Concat SAME first (to give it priority), then COVERED
            combined = pd.concat([same, covered], axis=0, ignore_index=True)
            combined = _clean_unique(combined)

            pin_2025_updated[category] = combined

        # No extrapolation matrices when early-exiting
        return {}, pin_2025_updated
    # =================== END EARLY EXIT ===================

    ## 2. ---- making the map between missing amdin and reference admin
    df_delta_category = {}

    for category, details in list_2025_category.items():
        valid_refs = details["list_2025"]

        # Filter base_2025 to admins flagged for delta (shared across categories)
        df_delta = base_2025[base_2025[admin_var].isin(list_delta)][[
            admin_var,
            ref_user_admin,
            ref_suggested_admin,
            ref_suggested_other
        ]].copy()

        # Assign admin_ref using the category-specific list_2025
        df_delta['admin_ref'] = df_delta.apply(lambda row: find_valid_ref(row, valid_refs), axis=1)

        # areas without a valid reference in this population group keep their 2024 values (step 5); they are no longer
        # added to the shared list_same, which applied to every population group and duplicated the area

        # Drop reference suggestion columns (cleanup)
        df_delta.drop(columns=[ref_user_admin, ref_suggested_admin, ref_suggested_other], inplace=True)

        # Store in dictionary by category
        df_delta_category[category] = df_delta
 
    

    merged_df_delta_all = {}  # Dictionary to store results per category

    ## 3. ---- delta preparation and merging
    for category, df_2025 in pin2025_by_status.items():
        if df_2025.empty:
            continue

        # Clean and prepare 2025 data
        first_col_2025 = df_2025.columns[0]
        percent_cols = [
            col for col in df_2025.columns
            if "%" in col and col != "% Tot PiN (severity levels 3-5)"
        ]
        keep_cols = [first_col_2025] + percent_cols
        df_2025 = df_2025.loc[:, keep_cols]
        df_2025 = df_2025.rename(columns={first_col_2025: "Admin Pcode REF"})

        # Clean and prepare 2024 data
        if category not in pin2024_cat:
            raise ValueError(f"No sheet for the population group '{category}' in the 2024 PiN file "
                             f"(sheets: {', '.join(map(str, pin2024_cat))}). Rename the sheet of the step 1 file or of the 2024 file.")
        df_2024 = pin2024_cat[category]
        first_col_2024 = df_2024.columns[0]
        df_2024 = df_2024.rename(columns={first_col_2024: "Admin Pcode REF"})

        df_2024 = df_2024.rename(columns={
            col: col.replace(" ", "_") + "_24"
            for col in df_2024.columns if col != "Admin Pcode REF"
        })
        df_2025 = df_2025.rename(columns={
            col: col.replace(" ", "_") + "_25"
            for col in df_2025.columns if col != "Admin Pcode REF"
        })

        # Merge 2025 and 2024 reference data
        matrix_df = df_2025.merge(df_2024, on="Admin Pcode REF", how="left")

        # Merge with df_delta for this category
        df_delta = df_delta_category.get(category)
        if df_delta is not None and not df_delta.empty:
            merged_df_delta = df_delta.merge(
                matrix_df,
                left_on='admin_ref',
                right_on='Admin Pcode REF',
                how='left'
            )

        # Add delta % columns
        for level in ['1-2', '3', '4', '5']:
            if level == '1-2':
                col_24 = "%_severity_levels_1-2_24"
                col_25 = "%_severity_levels_1-2_25"
                delta_col = "delta_%_severity_levels_1-2"
            else:
                col_24 = f"%_severity_level_{level}_24"
                col_25 = f"%_severity_level_{level}_25"
                delta_col = f"delta_%_severity_level_{level}"

            if col_24 in merged_df_delta.columns and col_25 in merged_df_delta.columns:
                def compute_delta(row, col_24=col_24, col_25=col_25):
                    val_24 = row[col_24]
                    val_25 = row[col_25]

                    if pd.isna(val_24) or pd.isna(val_25):
                        return None
                    if val_24 == 0 and val_25 == 0:
                        return 1
                    if val_24 == 0:
                        return 0
                    return (val_24 - val_25) / val_24


                merged_df_delta[delta_col] = merged_df_delta.apply(compute_delta, axis=1)
        print(merged_df_delta.columns)
        merged_df_delta_all[category] = merged_df_delta
           
    ## 4. ---- merging the delta and the pin2024 of refernce  
    for category, df in merged_df_delta_all.items():
        df_sev24 = pin_2024_missing_2025.get(category)
        with_2024 = set(df_sev24["Admin_Pcode_2024"]) if df_sev24 is not None and not df_sev24.empty else set()
        for admin in df["Admin Pcode"]:
            if admin not in with_2024:
                add_note(category, admin, None, "no_2024")
        if df_sev24 is not None and not df_sev24.empty:
            df_merged = df.merge(
                df_sev24,
                left_on='Admin Pcode',
                right_on='Admin_Pcode_2024',
                how='right'
            )
            # Drop duplicated Admin_Pcode_2024 if desired
            df_merged = df_merged.drop(columns=['Admin_Pcode_2024'])
            merged_df_delta_all[category] = df_merged


    ## 5. ---- calculate new severity after extrapolation    
    for category, df in merged_df_delta_all.items():
        new_cols = []

        for level in ['1-2', '3', '4', '5']:
            base_col = f"%_severity_level_{level}_2024_extrapolation_base" if level != '1-2' else "%_severity_levels_1-2_2024_extrapolation_base"
            delta_col = f"delta_%_severity_level_{level}" if level != '1-2' else "delta_%_severity_levels_1-2"
            new_col = f"new_%_severity_level_{level}_extrapolated" if level != '1-2' else "new_%_severity_levels_1-2_extrapolated"

            if base_col in df.columns and delta_col in df.columns:
                df[new_col] = df[base_col] * (1 - df[delta_col])
                new_cols.append(new_col)

        # Normalize so that the sum of new extrapolated columns = 100
        if new_cols:
            sum_col = df[new_cols].sum(axis=1, min_count=len(new_cols))   # empty if a level could not be extrapolated
            # no usable reference (none valid, or without 2024/2025 data): keep the area's 2024 values (needs stable)
            no_ref = ~(sum_col > 0)
            for col in new_cols:
                norm_col = col.replace("new_", "new_normalized_")
                base_col = col[len("new_"):].replace("_extrapolated", "_2024_extrapolation_base")
                df[norm_col] = df[col] / sum_col.where(~no_ref) * 100
                df.loc[no_ref, norm_col] = df.loc[no_ref, base_col]
            for _, row in df[no_ref].iterrows():
                ref = row.get("admin_ref")
                add_note(category, row["Admin Pcode"], ref, "no_reference_data" if isinstance(ref, str) and ref else "no_reference")

        if not new_cols:
            # no area of this group could be extrapolated (e.g. none has 2024 PiN): nothing to add for the group
            pin_2025_delta[category] = pd.DataFrame()
            merged_df_delta_all[category] = df
            continue

        # Select only first column + last 4 normalized severity columns
        first_col = df.columns[0]
        final_cols = [
            first_col,
            "new_normalized_%_severity_levels_1-2_extrapolated",
            "new_normalized_%_severity_level_3_extrapolated",
            "new_normalized_%_severity_level_4_extrapolated",
            "new_normalized_%_severity_level_5_extrapolated"
        ]
        df_only_2025 = df[final_cols].copy()

        # Rename columns to the final display names
        rename_map = {
            "new_normalized_%_severity_levels_1-2_extrapolated": "% severity levels 1-2",
            "new_normalized_%_severity_level_3_extrapolated": "% severity level 3",
            "new_normalized_%_severity_level_4_extrapolated": "% severity level 4",
            "new_normalized_%_severity_level_5_extrapolated": "% severity level 5"
        }
        df_only_2025 = df_only_2025.rename(columns=rename_map)

        # Save outputs
        pin_2025_delta[category] = df_only_2025
        # Save back
        merged_df_delta_all[category] = df

    ## 6. ---- get values from 2024 pin of the admin in the category 'same'   
    for category, df_2024 in pin2024_cat.items():
        first_col_2024 = df_2024.columns[0]
        df_2024 = df_2024.rename(columns={first_col_2024: "Admin Pcode"})
        df_2024_filtered = df_2024[df_2024["Admin Pcode"].isin(list_same)].copy()
        admin_col = "Admin Pcode"  # After replacing spaces
        pin_2025_same[category] = df_2024_filtered

    print('------------------')
    #print(pin_2025_covered['host'])    
    print('------------------')


    ## 7. ---- Combine all DataFrames into one
    for category, df_1 in pin_2025_covered.items():
        df_delta = pin_2025_delta.get(category, pd.DataFrame())
        df_same = pin_2025_same.get(category, pd.DataFrame())

        df_combined = pd.concat([df_delta, df_same, df_1], axis=0, ignore_index=True)
        pin_2025_updated [category] = df_combined






    return merged_df_delta_all ,pin_2025_updated


