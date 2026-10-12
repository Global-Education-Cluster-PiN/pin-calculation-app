# PiN Calculation App

A Streamlit-based web application to calculate Education People in Need (PiN) figures.

## Table of Contents

- [Overview](#overview)
- [Application Structure](#application-structure)
  - [Main Application Files](#main-application-files)
  - [Pages Structure](#pages-structure)
  - [Source Functions (`src/`)](#source-functions-src)
    - [Core Calculation Functions](#core-calculation-functions)
    - [Severity Classification and Indicator Counting](#severity-classification-and-indicator-counting)
    - [Output Generation Functions](#output-generation-functions)
    - [Hybrid Workflow Functions](#hybrid-workflow-functions)
  - [Supporting Files](#supporting-files)
    - [Translation Files](#translation-files)
    - [Data Directories](#data-directories)
    - [Debugging Scripts](#debugging-scripts)
- [Workflow Logic](#workflow-logic)
  - [Standard MSNA Countries](#standard-msna-countries)
  - [Hybrid Countries (Two-Step Process)](#hybrid-countries-two-step-process)
    - [Step 1: Initial Calculation](#step-1-initial-calculation)
    - [Step 2: Extrapolation & Final Calculation](#step-2-extrapolation--final-calculation)
  - [Alternative Data Sources (JENA/EMIS)](#alternative-data-sources-jenaemis)
  - [No OCHA Data Scenario](#no-ocha-data-scenario)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Output Files](#output-files)
- [Configuration: Country Lists](#configuration-country-lists)
- [Debugging Outside Streamlit](#debugging-outside-streamlit)


## Overview

The PiN Calculation App automates the calculation of People in Need (PiN) figures for the Education sector in humanitarian crises. It processes Multi-Sectoral Needs Assessment (MSNA) data and school-level assestment data, applies the global methodology, and generates formatted Excel outputs with snapshots and visualizations.

**Key Features:**

- Multiple data source support (MSNA, JENA, EMIS)
- Hybrid calculation workflows for specific countries
- Automated severity identification 
- Geographic visualization with severity maps
- GitHub integration for automatic file archiving
- word snapshot generation for HNO (Humanitarian Needs Overview) submissions
- Multi-language support (English and French)

## Application Structure

### Main Application Files

```
PiN_app_dev/
├── GEC_PiN.py                    # Main Streamlit app entry point
├── shared_utils.py                # Shared utilities (language selector, etc.)
└── requirements.txt               # Python dependencies
```

**`GEC_PiN.py`**: Main entry point that initializes the Streamlit app, sets up page configuration, handles authentication, and provides the landing page with navigation to the three calculation pages.

**`shared_utils.py`**: Contains shared functions used across all pages, primarily the `language_selector()` function that manages multilingual support.

### Pages Structure

The application has three sequential pages that guide users through the PiN calculation process:

```
pages/
├── 1_📁_Upload_--_Education_Data.py
├── 2_📊_Calculation_--_PiN.py
└── 3_📋_Download_--_PiN_figures_and_other_outputs.py
```

#### **Page 1: Upload -- Education Data**
- **Purpose**: Data upload and initial configuration
- **User Actions**:
  - Select country and education cycle parameters
  - Upload MSNA dataset (household and education data) + KoBoToolbox form (survey structure)
  - Upload OCHA population figures
  - For alternative scenarios: upload JENA or EMIS data
- **Key Functions Called**:
  - Validates uploaded files
  - Stores data in `st.session_state` for use in subsequent pages
  - Performs initial data quality checks

#### **Page 2: Calculation -- PiN**
- **Purpose**: Configure indicators and severity thresholds
- **User Actions**:
  - Map dataset columns to PiN indicators (access, disruption, barriers)
  - Define severity thresholds for barriers (what constitutes severity 4 vs 5)
  - Configure population group mappings (host, IDP, returnee, refugee)
  - Select HNO unit of the analysis 
  - Enable/disable additional custom indicators
- **Key Functions Called**:
  - Column mapping validation
  - Severity threshold configuration
  - Preview of selected indicators
- **Output**: Configuration stored in `st.session_state` for Page 3

#### **Page 3: Download -- PiN Figures and Other Outputs**
- **Purpose**: Execute calculations and generate outputs
- **Main Process Flow**:
  1. Clean and prepare dataset → `clean_make_dataset()`
  2. Add severity scores to indicators → `add_severity()`
  3. Calculate PiN figures → `calculatePIN()` (or variant)
  4. Generate outputs → `create_output()`, `create_snapshot_PiN()`
  5. Create downloadable ZIP file
  6. Upload results to GitHub repository (to be updated)
- **Key Functions Called**: See [Source Functions](#source-functions-src) section
- **Output**: ZIP file containing Excel results, Word snapshots, parameter documents, and severity maps

### Source Functions (`src/`)

The `src/` folder contains all calculation logic and output generation functions:

```
src/
├── clean_dataset.py                              # Data cleaning and preparation
├── add_PiN_severity.py                          # Severity scoring for indicators
├── calculation_for_PiN_Dimension.py             # Main PiN calculation (standard)
├── calculation_for_PiN_Dimension_with_JENA.py   # PiN calculation with JENA data
├── calculation_for_PiN_Dimension_with_EMIS.py   # PiN calculation with EMIS data
├── calculation_for_PiN_Dimension_NO_OCHA.py     # PiN calculation without OCHA data
├── calculation_for_PiN_Dimension_NO_OCHA_2025.py # Updated version for 2025
├── update_re_calculation_for_PiN.py             # Recalculation for hybrid step 2
├── vizualize_PiN.py                             # Excel output formatting
├── snapshot_PiN.py                              # Word snapshot generation (EN)
├── snapshot_PiN_FR.py                           # Word snapshot generation (FR)
├── save_parameter.py                            # Parameter documentation (EN)
├── save_parameter_FR.py                         # Parameter documentation (FR)
├── create_map_severity.py                       # Geographic visualization
├── make_output1_platform.py                     # Hybrid step 1 output merger
├── create_output1_excel.py                      # Hybrid step 1 Excel formatting
├── extrapolation.py                             # Delta method extrapolation
└── cases_country_helpers.py                     # Country variables to be used in the run_PiNcalculation_outside_streamlit.py
```

#### **Core Calculation Functions**

**`clean_make_dataset()`** (`clean_dataset.py`)
- Cleans and standardizes the uploaded MSNA data
- Creates age groups (ECE, primary, upper primary, secondary)
- Normalizes population status groups
- Handles missing values and data type conversions
- Returns cleaned education and household datasets with processing messages

**`add_severity()`** (`add_PiN_severity.py`)
- Maps indicator responses to JIAF severity scores (1-5)
- Applies severity thresholds for barriers
- Handles special cases for disruption indicators
- Creates severity columns for: access, teacher disruption, IDP disruption, armed group disruption, natural hazards, barriers
- Returns dataset with added severity columns

#### **Severity Classification and Indicator Counting**

Each child receives one severity level (`calculate_severity()` in `add_PiN_severity.py`):
- **Out-of-school children**: severity 5 if their barrier is in the severity 5 list, severity 4 if it is in the severity 4 list, otherwise severity 3.
- **In-school children**: the highest level triggered by their answers: school occupied by armed groups → 5; school used as IDP shelter → 4; teacher absence → 3; natural hazard and additional indicators → the severity set for them on Page 2 (3 or 4). With none of these, severity 1-2.
- Afghanistan: with `full_GEC_compliant` (default), out-of-school girls older than 12 are severity 5.

In the PiN by indicator file, **every child at severity 3, 4 or 5 is counted under exactly one indicator, never twice**, so the indicators of each severity level add up to the PiN of that level. When a child in school has several disruptions at the same level, the first one in this order is used:
- **Severity 3**: teacher absence > natural hazard > additional indicator 1 > additional indicator 2
- **Severity 4**: school used as IDP shelter > natural hazard > additional indicator 1 > additional indicator 2
- **Severity 5**: school occupied by armed groups

Out-of-school children are counted only under access (severity 3) or their barrier (severity 4 and 5), never under the in-school indicators.

**`calculatePIN()`** (`calculation_for_PiN_Dimension.py`)
- **Main PiN calculation function** for standard MSNA countries
- Aggregates severity scores by dimension (Access, Learning Environment, Protected Environment)
- Calculates maximum severity across dimensions
- Disaggregates by administrative area, population group, age group, and gender
- Merges with OCHA population figures to calculate absolute PiN numbers
- Returns multiple outputs: severity tables, dimension tables, indicator breakdowns, totals

**Variant Calculation Functions:**
- `calculatePIN_with_JENA()`: Integrates JENA (Joint Education Needs Assessment) data
- `calculatePIN_with_EMIS()`: Integrates EMIS (Education Management Information System) data
- `calculatePIN_NO_OCHA()` / `calculatePIN_NO_OCHA_2025()`: Calculates PiN percentages without OCHA population data
- `UPDATE_calculatePIN()`: Used in hybrid step 2 to recalculate after extrapolation

#### **Output Generation Functions**

**`create_output()`** (`vizualize_PiN.py`)
- Creates the main Excel output file with multiple sheets:
  - PiN TOTAL: Overall PiN by severity
  - By administrative area
  - By population group
  - By age group and gender
  - Dimension breakdowns
- Applies formatting, color coding, and conditional formatting
- Includes parameter documentation sheet

**`create_indicator_output()`** (`vizualize_PiN.py`)
- Generates detailed Excel file showing PiN breakdown by each indicator
- Useful for understanding which indicators drive severity scores

**`create_snapshot_PiN()` / `create_snapshot_PiN_FR()`** (`snapshot_PiN.py` / `snapshot_PiN_FR.py`)
- Creates Word document snapshots with:
  - Key PiN figures summary
  - Severity breakdown charts
  - Gender disaggregation
  - Population group comparison
- Formatted for HNO submission
- Available in English and French

**`generate_word_document()` / `generate_word_document_FR()`** (`save_parameter.py` / `save_parameter_FR.py`)
- Documents all parameters and configuration choices used in the calculation
- Records: country, education cycle, indicator mappings, severity thresholds, data sources
- Critical for reproducibility and transparency

**`make_map_severity()`** (`create_map_severity.py`)
- Generates geographic visualizations showing PiN severity by administrative area
- Creates PNG images for inclusion in reports
- Color-coded by severity level (1-5)

#### **Hybrid Workflow Functions**

**`merge_2025_contextDB()`** (`make_output1_platform.py`)
- **Hybrid Step 1**: Merges calculated PiN from MSNA-covered areas with secondary data
- Integrates: ACLED conflict data, Information Insight (II) indicators, empty columns for manual filling
- Creates temporary output file for users to complete

**`create_output1_user()`** (`create_output1_excel.py`)
- Formats the hybrid step 1 output with color-coding and clear instructions
- Highlights cells that need manual completion

**`extrapolate_df_2025_updated()`** (`extrapolation.py`)
- **Hybrid Step 2**: Uses delta method to extrapolate PiN to non-covered areas
- Compares 2024 vs 2025 patterns in covered areas
- Applies trends to uncovered areas
- Returns extrapolated PiN figures for entire country

### Supporting Files

#### **Translation Files**
```
en.json       # English translations for all UI text
fr.json       # French translations for all UI text
```

These JSON files contain all user-facing text, allowing complete interface translation between English and French.

#### **Data Directories**
```
input/              # User-uploaded data files
input_map/          # shapefiles for mapping
context_DB/         # Secondary data (ACLED, II) for hybrid countries
pin2024_cat/        # 2024 PiN data for extrapolation
platform_PiN_output/  # Archived outputs (uploaded to GitHub)
pics/               # Logo and UI images
icon/               # App icon
output_validation/  # Quality check outputs when the run_PiNcalculation_outside_streamlit is run
```

#### **Debugging Scripts**

**Outside-Streamlit Execution Files:**
```
run_PiNcalculation_outside_streamlit.py        # Debug standard MSNA workflow
run_PiNcalculation_outside_streamlit_EMIS.py   # Debug EMIS workflow (old, settings in the script)
run_PiNcalculation_outside_streamlit_JENA.py   # Debug JENA workflow (old, settings in the script)
run_PiNcalculation_outside_streamlit_EMIS_config.py   # EMIS workflow, case from run_config.py (e.g. LMR_2022_EMIS)
run_PiNcalculation_outside_streamlit_JENA_config.py   # JENA workflow, case from run_config.py (e.g. NER_2024_JENA)
```

These scripts allow developers to:
- Run calculations without launching Streamlit
- Test individual functions in isolation
- Debug with IDE tools and breakpoints
- Rapidly iterate on calculation logic
- Use hardcoded file paths instead of uploads

**Usage Example:**
```python
# In run_PiNcalculation_outside_streamlit.py
country = "Somalia -- SOM"
dataset_path = "input/Somalia_MSNA_2025.xlsx"
# ... set all parameters directly
# Run calculations
results = calculatePIN(country, edu_data, household_data, ...)
```

## Workflow Logic

### Standard MSNA Countries

**Countries**: Most humanitarian contexts with the MSNA coverage == HPC scope

**Flow**:
1. **Upload** (Page 1): MSNA dataset + OCHA figures
2. **Configure** (Page 2): Map indicators, set thresholds
3. **Calculate** (Page 3):
   - Clean data → `clean_make_dataset()`
   - Add severity → `add_severity()`
   - Calculate PiN → `calculatePIN()`
   - Generate outputs → `create_output()`, `create_snapshot_PiN()`
4. **Download**: Single ZIP file with all results

**Outputs** (names: see [Output Files](#output-files)):
- `<ISO>_PiN2026_results_<date-time>.xlsx`
- `<ISO>_PiN2026_by-indicator_<date-time>.xlsx`
- `<ISO>_PiN2026_snapshot_<date-time>.docx`
- `<ISO>_PiN2026_parameters_<date-time>.docx`
- Severity maps: `<ISO>_PiN2026_map-..._<date-time>.png`

### Hybrid Countries (Two-Step Process)

**Which countries**: chosen for each analysis, with the "Hybrid country" tick box on Page 1 (unticked by default; tick it
in both steps). In local runs: `"hybrid_country": True` in the case in `run_config.py` (`"step_2_hpc"` chooses the step).

**Why Hybrid?**: MSNA only covers targeted areas; need to extrapolate to entire country

#### **Step 1: Initial Calculation**

1. **Upload** (Page 1): MSNA for covered areas + OCHA figures
2. **Configure** (Page 2): Standard indicator mapping
3. **Calculate** (Page 3):
   - Calculate PiN for covered areas → `calculatePIN()`
   - Merge with secondary data → `merge_2025_contextDB()`
   - Format for user completion → `create_output1_user()`
4. **Download**: `<ISO>_PiN2026_step1_documents_<date-time>.zip`, with the two files needed for step 2:
   - `<ISO>_PiN2026_step1_to-fill_<date-time>.xlsx`: the user ticks, for each area without 2025 MSNA data, whether
     needs are stable, decreased or worsened, and gives a reference area for decreased/worsened
   - `<ISO>_PiN2026_step1_covered-areas_<date-time>.xlsx`: the PiN of the areas covered by the MSNA, by population
     group, plus the parameters used in step 1 (carried into the step 2 results)

#### **Step 2: Extrapolation & Final Calculation**

1. **Upload** (Page 1): 
   - Completed `step1_to-fill` file and the `step1_covered-areas` file from Step 1
   - (the 2024 PiN is read from `pin2024_cat/<ISO>_PIN2024.xlsx`)
2. **Skip** Page 2 (configuration already done)
3. **Calculate** (Page 3):
   - Extrapolate using delta method → `extrapolate_df_2025_updated()`
   - Recalculate country-wide PiN → `UPDATE_calculatePIN()`
   - Generate final outputs
4. **Download**: Final PiN results for entire country (`<ISO>_PiN2026_step2_documents_<date-time>.zip`); areas that
   could not be extrapolated as asked are listed on Page 3 and in the "Extrapolation notes" sheet of the results

**Key Difference**: Step 2 uses `st.session_state.step_2_hpc = True` flag to trigger extrapolation workflow

### Alternative Data Sources (JENA/EMIS)

**Countries**: Niger, Nigeria, Mozambique (when `data_combination != 'mmmm'`)

**JENA (Joint Education Needs Assessment)**:
- School-level assessment data
- Integrates with MSNA using `calculatePIN_with_JENA()`
- Combines household-level (MSNA) and school-level (JENA) indicators

**EMIS (Education Management Information System)**:
- Government education system data
- Enrollment figures, school infrastructure data
- Integrates with MSNA using `calculatePIN_with_EMIS()`
- Helps validate and complement MSNA findings

**Data Combination Codes**:
- `'mjjm'`: MSNA + JENA (uses JENA data)
- `'emmm'`, `'eemm'`, `'eeem'`: MSNA + EMIS (uses EMIS data)
- `'mmmm'`: MSNA only (standard workflow)

### No OCHA Data Scenario

**When**: User indicates OCHA population figures are not available

**Limitation**: Cannot calculate absolute PiN numbers, only percentages

**Flow**:
1. Calculate severity percentages → `calculatePIN_NO_OCHA_2025()`
2. Generate indicator breakdown → `create_indicator_output_no_ocha()`
3. Generate percentage output → `create_pin_raw_output()`

**Outputs**:
- `<ISO>_PiN2026_percentage_<date-time>.xlsx` (severity %, not absolute numbers)
- `<ISO>_PiN2026_by-indicator_<date-time>.xlsx`
- `<ISO>_PiN2026_parameters_<date-time>.docx`

## Installation and Setup
### Prerequisites

- Python 3.8 or higher
- Git (for cloning repository)

### Installation Steps

1. **Clone the repository**:
```bash
git clone https://github.com/Global-Education-Cluster-PiN/pin-calculation-app.git
cd pin-calculation-app
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
streamlit run GEC_PiN.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

### Basic Workflow

1. **Launch Application**: Run `streamlit run GEC_PiN.py`
2. **Select Language**: Choose English or French
3. **Navigate to Page 1**: Upload your data files
4. **Navigate to Page 2**: Configure indicators and thresholds
5. **Navigate to Page 3**: Execute calculation and download results

### Data Requirements

**Required Files**:
- MSNA dataset (Excel): Household and education loop data
- KoBoToolbox form (Excel): Survey structure with question types
- OCHA population figures (Excel): Population by admin area and group

**Optional Files** (scenario-dependent):
- JENA data (for JENA integration)
- EMIS data (for EMIS integration)
- 2024 PiN data (for hybrid step 2)
- Completed temporary file (for hybrid step 2)


### GitHub Archive

All outputs are automatically uploaded to the GitHub repository at:
```
platform_PiN_output/{country}/
```

This creates a historical archive of all calculations for audit and comparison purposes.



## Output Files

All result files are named `<ISO>_PiN<year>_<content>_<YYYYMMDD-HHMM>.<ext>` (`src/output_names.py`), the same in
the platform downloads (inside and outside the ZIP) and in local runs, e.g. `SOM_PiN2026_results_20261011-1745.xlsx`.
The date and time keep a new download or run from replacing an earlier one. The year is `PIN_YEAR` in
`src/output_names.py`.

| Content | File |
|---|---|
| `documents` | ZIP with all the files of a download (`step1_documents`, `step2_documents` for hybrid countries) |
| `results` | PiN results (Excel), with the "Parameters Used" sheet |
| `by-indicator` | PiN by indicator (Excel) |
| `snapshot` | PiN snapshot (Word) |
| `parameters` | Parameters used (Word) |
| `map-area-severity`, `map-severity-3/4/5`, `map-total-PiN` | Severity maps (PNG) |
| `percentage` | PiN percentages, without OCHA figures |
| `step1_to-fill`, `step1_covered-areas` | Hybrid step 1: the two files to upload for step 2 |
| `step2_results`, `step2_snapshot`, `step2_map-...` | Hybrid step 2 |

In local runs the intermediate check files (`00_...`, `01_...`, `step2_extrapolation_details.xlsx`) go to a folder per
run, `checks_<YYYYMMDD-HHMM>`, next to the result files; in `run_config.py` a step 2 input path with `*` stands for the
newest matching file.

## Configuration: Country Lists

### Overview

The application categorizes countries into different workflow types. When adding or removing countries from these categories, you must update the country lists in **multiple locations** to ensure consistent behavior across the application.

Hybrid countries are not a list: the user ticks "Hybrid country" on Page 1 for each analysis (local runs: `"hybrid_country"` in `run_config.py`).

### Country Categories

**1. Alternative Countries** (JENA/EMIS data integration)
- Niger, Nigeria, Mozambique

**2. Overall Countries** (Special aggregation logic)
- Haiti, Sudan, DRC, South Sudan

### Files Requiring Updates

When modifying country lists, you must update **ALL** of the following locations:

#### **1. Page 1: Upload -- Education Data**
**File:** `pages/1_📁_Upload_--_Education_Data.py`

**Line ~341:** Alternative countries list
```python
alternative_countries = ['Niger -- NER', 'Nigeria -- NRA', 'Mozambique -- MOZ']
```

#### **2. Page 3: Download -- PiN Figures and Other Outputs**
**File:** `pages/3_📋_Download_--_PiN_figures_and_other_outputs.py`

**Line ~337:** Alternative countries list
```python
alternative_countries = ['Niger -- NER', 'Nigeria -- NRA','Mozambique -- MOZ' ]
```

#### **3. Main PiN Calculation Function**
**File:** `src/calculation_for_PiN_Dimension.py`

**Line ~447-448:** Overall countries list
```python
OVERALL_COUNTRIES = {'Haiti -- HTI', 'Sudan -- SDN', 'Democratic Republic of the Congo -- DRC', 'South Sudan -- SSD'}
```

**Line ~572 (inside `reduce_index` function):** Overall countries check
```python
OVERALL_COUNTRIES = {'Haiti -- HTI', 'Sudan -- SDN', 'Democratic Republic of the Congo -- DRC', 'South Sudan -- SSD'}
```

**Line ~788 (inside `calculate_prop` function):** Overall countries logic
```python
OVERALL_COUNTRIES = {'Haiti -- HTI', 'Sudan -- SDN', 'Democratic Republic of the Congo -- DRC','South Sudan -- SSD'}
```

### Update Checklist

When adding or removing a country from a category, follow this checklist:

- [ ] Update `alternative_countries` in `1_📁_Upload_--_Education_Data.py` (Line ~341)
- [ ] Update `alternative_countries` in `3_📋_Download_--_PiN_figures_and_other_outputs.py` (Line ~337)
- [ ] Update `OVERALL_COUNTRIES` in `calculation_for_PiN_Dimension.py` (Lines ~447, ~572, ~788)
- [ ] Test the workflow for the affected country
- [ ] Update corresponding country list in debugging scripts if applicable

### Example: A New Hybrid Country

No code change: tick "Hybrid country" on Page 1 (local runs: `"hybrid_country": True` in `run_config.py`). The country needs:
1. Secondary data in the `context_DB/` folder (`<ISO>_context_db.xlsx`)
2. Its 2024 PiN in the `pin2024_cat/` folder (`<ISO>_PIN2024.xlsx`) for the extrapolation

### Important Notes

⚠️ **Country Code Format**: Always use the format `"Country Name -- CODE"` (e.g., `'Mali -- MLI'`)

⚠️ **Case Sensitivity**: Country codes are case-sensitive

⚠️ **Data Dependencies**: 
- Hybrid countries require data in `context_DB/` and `pin2024_cat/`
- Alternative countries require JENA or EMIS template files in `input/`

⚠️ **Testing**: After updating country lists, test the full workflow for affected countries before deploying



## Debugging Outside Streamlit

### Why Debug Outside Streamlit?

- **Faster iteration**: No need to reload entire Streamlit app
- **Better debugging tools**: Use IDE breakpoints and inspectors
- **Easier testing**: Test individual functions in isolation
- **Reproducible scenarios**: Hardcode parameters for consistent testing

### Using Debug Scripts

1. **Choose the appropriate script** based on your scenario:
   - Standard: `run_PiNcalculation_outside_streamlit.py`
   - Hybrid: `run_PiNcalculation_outside_streamlit.py` with `"hybrid_country": True` (step 1) and `run_hybrid_step2.py` (step 2)
   - JENA: `run_PiNcalculation_outside_streamlit_JENA_config.py` (case from `run_config.py`, e.g. `NER_2024_JENA`)
   - EMIS: `run_PiNcalculation_outside_streamlit_EMIS_config.py` (case from `run_config.py`, e.g. `LMR_2022_EMIS`)

2. **Modify file paths** in the script:
```python
# Example from run_PiNcalculation_outside_streamlit.py
country = "Somalia -- SOM"
dataset_path = "input/Somalia_MSNA_2025.xlsx"
kobo_path = "input/Somalia_kobo_form.xlsx"
ocha_path = "input/Somalia_OCHA_figures.xlsx"
```

3. **Set parameters** directly:
```python
access_var = "edu_access"
teacher_disruption_var = "edu_disruption_teacher"
# ... etc
```

4. **Run the script**:
```bash
python run_PiNcalculation_outside_streamlit.py
```

5. **Inspect outputs**: Results are saved to `output/` directory


**Version**: 2.0 (2025 HNO Cycle)  
**Last Updated**: January 2026  
**Maintained by**: Global Education Cluster (developed by Martina Vit)