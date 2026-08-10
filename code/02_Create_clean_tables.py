import pandas as pd
import os

# ============================================
# PROJECT PATH
# ============================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ============================================
# Base folder containing FDA ASCII files
# ============================================

base_path = r"E:\glp1\dataset by fda\ASCII"

output_path = os.path.join(PROJECT_ROOT, "dataset", "processed")

os.makedirs(output_path, exist_ok=True)

# Function to load FDA tables

def load_fda_table(filename):
    return pd.read_csv(
        base_path + "\\" + filename,
        sep="$",
        encoding="latin1",
        low_memory=False
    )

# Load all FDA tables

demo_data = load_fda_table("DEMO26Q1.txt")
drug_data = load_fda_table("DRUG26Q1.txt")
reac_data = load_fda_table("REAC26Q1.txt")
outc_data = load_fda_table("OUTC26Q1.txt")
indi_data = load_fda_table("INDI26Q1.txt")
ther_data = load_fda_table("THER26Q1.txt")
rpsr_data = load_fda_table("RPSR26Q1.txt")

print("✓ All FDA tables loaded successfully.")

# Filter GLP-1 drugs

glp1_keywords = (
    "SEMAGLUTIDE|OZEMPIC|WEGOVY|RYBELSUS|"
    "TIRZEPATIDE|MOUNJARO|ZEPBOUND|"
    "LIRAGLUTIDE|SAXENDA|VICTOZA"
)

glp1_drugs = drug_data[
    drug_data["drugname"]
    .str.upper()
    .str.contains(glp1_keywords, na=False)
].copy()

# ============================================================
# STANDARDIZE GLP-1 DRUG NAMES
# ============================================================

def classify_glp1_drug(drug_name):

    drug_name = str(drug_name).upper()

    if any(keyword in drug_name for keyword in [
        "SEMAGLUTIDE",
        "OZEMPIC",
        "WEGOVY",
        "RYBELSUS"
    ]):
        return "SEMAGLUTIDE"

    elif any(keyword in drug_name for keyword in [
        "TIRZEPATIDE",
        "MOUNJARO",
        "ZEPBOUND"
    ]):
        return "TIRZEPATIDE"

    elif any(keyword in drug_name for keyword in [
        "LIRAGLUTIDE",
        "VICTOZA",
        "SAXENDA"
    ]):
        return "LIRAGLUTIDE"

    else:
        return "OTHER"


glp1_drugs["glp1_drug"] = (
    glp1_drugs["drugname"]
    .apply(classify_glp1_drug)
)


print("\nGLP-1 drug classification:")
print(
    glp1_drugs["glp1_drug"].value_counts()
)

# ============================================================
# GET UNIQUE GLP-1 CASE IDS
# ============================================================

glp1_case_ids = (
    glp1_drugs["caseid"]
    .dropna()
    .unique()
)

print("\nTotal unique GLP-1 cases:")
print(len(glp1_case_ids))

# ============================================================
# FILTER ALL TABLES TO GLP-1 CASES
# ============================================================

glp1_demo = demo_data[
    demo_data["caseid"].isin(glp1_case_ids)
].copy()

glp1_reac = reac_data[
    reac_data["caseid"].isin(glp1_case_ids)
].copy()

glp1_outc = outc_data[
    outc_data["caseid"].isin(glp1_case_ids)
].copy()

glp1_indi = indi_data[
    indi_data["caseid"].isin(glp1_case_ids)
].copy()

glp1_ther = ther_data[
    ther_data["caseid"].isin(glp1_case_ids)
].copy()

glp1_rpsr = rpsr_data[
    rpsr_data["caseid"].isin(glp1_case_ids)
].copy()

# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("FILTERED GLP-1 TABLES")
print("=" * 60)

print("GLP-1 DRUG:", glp1_drugs.shape)
print("GLP-1 DEMO:", glp1_demo.shape)
print("GLP-1 REAC:", glp1_reac.shape)
print("GLP-1 OUTC:", glp1_outc.shape)
print("GLP-1 INDI:", glp1_indi.shape)
print("GLP-1 THER:", glp1_ther.shape)
print("GLP-1 RPSR:", glp1_rpsr.shape)

# ============================================================
# CREATE CLEAN DRUG TABLE
# ============================================================

clean_drug = glp1_drugs[
    [
        "primaryid",
        "caseid",
        "drug_seq",
        "glp1_drug",
        "drugname",
        "role_cod",
        "route",
        "dose_vbm",
        "dose_amt",
        "dose_unit",
        "dose_form",
        "dose_freq",
        "dechal",
        "rechal"
    ]
].copy()

print("\nClean drug table:")
print(clean_drug.shape)
print(clean_drug.head())

# ============================================================
# CREATE CLEAN PATIENT TABLE
# ============================================================

clean_patient = glp1_demo[
    [
        "primaryid",
        "caseid",
        "age",
        "age_cod",
        "age_grp",
        "sex",
        "reporter_country",
        "occr_country",
        "rept_cod",
        "occp_cod",
        "event_dt",
        "mfr_dt",
        "init_fda_dt",
        "fda_dt",
        "rept_dt"
    ]
].copy()

# One patient/report profile per case
clean_patient = clean_patient.drop_duplicates(
    subset=["caseid"]
)

print("\nClean patient table:")
print(clean_patient.shape)
print(clean_patient.head())

# ============================================================
# CREATE CLEAN REACTIONS TABLE
# ============================================================

clean_reactions = glp1_reac[
    [
        "primaryid",
        "caseid",
        "pt",
        "drug_rec_act"
    ]
].copy()

clean_reactions = clean_reactions.drop_duplicates()

print("\nClean reactions table:")
print(clean_reactions.shape)
print(clean_reactions.head())

# ============================================================
# CREATE CLEAN OUTCOMES TABLE
# ============================================================

clean_outcomes = glp1_outc[
    [
        "primaryid",
        "caseid",
        "outc_cod"
    ]
].copy()

clean_outcomes = clean_outcomes.drop_duplicates()

print("\nClean outcomes table:")
print(clean_outcomes.shape)
print(clean_outcomes.head())

# ============================================================
# CREATE CLEAN INDICATIONS TABLE
# ============================================================

clean_indications = glp1_indi[
    [
        "primaryid",
        "caseid",
        "indi_drug_seq",
        "indi_pt"
    ]
].copy()

clean_indications = clean_indications.drop_duplicates()

print("\nClean indications table:")
print(clean_indications.shape)
print(clean_indications.head())

# ============================================================
# CREATE CLEAN THERAPY TABLE
# ============================================================

clean_therapy = glp1_ther[
    [
        "primaryid",
        "caseid",
        "dsg_drug_seq",
        "start_dt",
        "end_dt",
        "dur",
        "dur_cod"
    ]
].copy()

clean_therapy = clean_therapy.drop_duplicates()

print("\nClean therapy table:")
print(clean_therapy.shape)
print(clean_therapy.head())

# ============================================================
# CREATE CLEAN REPORT SOURCE TABLE
# ============================================================

clean_report_source = glp1_rpsr[
    [
        "primaryid",
        "caseid",
        "rpsr_cod"
    ]
].copy()

clean_report_source = clean_report_source.drop_duplicates()

print("\nClean report source table:")
print(clean_report_source.shape)
print(clean_report_source.head())

# ============================================================
# CREATE CASE SUMMARY TABLE
# ============================================================

case_summary = (
    clean_drug
    .groupby("caseid")
    .agg(
        primaryid=("primaryid", "first"),
        glp1_drugs=(
            "glp1_drug",
            lambda x: ", ".join(sorted(x.unique()))
        ),
        number_of_glp1_drugs=(
            "glp1_drug",
            "nunique"
        ),
        number_of_drug_records=(
            "drug_seq",
            "count"
        )
    )
    .reset_index()
)


# Add reaction count
reaction_count = (
    clean_reactions
    .groupby("caseid")
    .agg(
        number_of_reactions=("pt", "nunique")
    )
    .reset_index()
)

case_summary = case_summary.merge(
    reaction_count,
    on="caseid",
    how="left"
)


# Add outcome count
outcome_count = (
    clean_outcomes
    .groupby("caseid")
    .agg(
        number_of_outcomes=("outc_cod", "nunique")
    )
    .reset_index()
)

case_summary = case_summary.merge(
    outcome_count,
    on="caseid",
    how="left"
)


print("\nCase summary:")
print(case_summary.shape)
print(case_summary.head())

# ============================================================
# CREATE REPORTING YEAR
# ============================================================

clean_patient["fda_year"] = (
    pd.to_numeric(
        clean_patient["fda_dt"],
        errors="coerce"
    )
    .astype("Int64")
    .astype(str)
    .str[:4]
)

clean_patient["fda_year"] = pd.to_numeric(
    clean_patient["fda_year"],
    errors="coerce"
)

# ============================================================
# CLEAN AGE GROUPS
# ============================================================

def clean_age_group(age_group):

    if pd.isna(age_group):
        return "Unknown"

    age_group = str(age_group).upper()

    if "INFANT" in age_group:
        return "Infant"

    elif "CHILD" in age_group:
        return "Child"

    elif "ADOLESCENT" in age_group:
        return "Adolescent"

    elif "ADULT" in age_group:
        return "Adult"

    elif "ELDERLY" in age_group:
        return "Elderly"

    else:
        return "Unknown"


clean_patient["age_group_clean"] = (
    clean_patient["age_grp"]
    .apply(clean_age_group)
)

# ============================================================
# SAVE CLEAN TABLES
# ============================================================

os.makedirs(output_path, exist_ok=True)


clean_drug.to_csv(
    output_path + r"\glp1_drug.csv",
    index=False
)

clean_patient.to_csv(
    output_path + r"\glp1_patient.csv",
    index=False
)

clean_reactions.to_csv(
    output_path + r"\glp1_reactions.csv",
    index=False
)

clean_outcomes.to_csv(
    output_path + r"\glp1_outcomes.csv",
    index=False
)

clean_indications.to_csv(
    output_path + r"\glp1_indications.csv",
    index=False
)

clean_therapy.to_csv(
    output_path + r"\glp1_therapy.csv",
    index=False
)

clean_report_source.to_csv(
    output_path + r"\glp1_report_source.csv",
    index=False
)

case_summary.to_csv(
    output_path + r"\glp1_case_summary.csv",
    index=False
)


print("\n" + "=" * 60)
print("ALL CLEAN TABLES SAVED SUCCESSFULLY")
print("=" * 60)