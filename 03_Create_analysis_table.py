import pandas as pd
import os


# ============================================================
# PATHS
# ============================================================

INPUT_PATH = r"E:\glp1\dataset\processed"
OUTPUT_PATH = r"E:\glp1\dataset\analysis"

os.makedirs(OUTPUT_PATH, exist_ok=True)


# ============================================================
# LOAD CLEAN TABLES
# ============================================================

print("Loading clean tables...")

drug = pd.read_csv(
    INPUT_PATH + r"\glp1_drug.csv"
)

patient = pd.read_csv(
    INPUT_PATH + r"\glp1_patient.csv"
)

reactions = pd.read_csv(
    INPUT_PATH + r"\glp1_reactions.csv"
)

outcomes = pd.read_csv(
    INPUT_PATH + r"\glp1_outcomes.csv"
)

indications = pd.read_csv(
    INPUT_PATH + r"\glp1_indications.csv"
)

therapy = pd.read_csv(
    INPUT_PATH + r"\glp1_therapy.csv"
)

report_source = pd.read_csv(
    INPUT_PATH + r"\glp1_report_source.csv"
)


print("✓ Clean tables loaded successfully.")


# ============================================================
# 1. DRUG CASE ANALYSIS
# ============================================================

drug_case_analysis = (
    drug[
        [
            "caseid",
            "glp1_drug",
            "drugname",
            "role_cod",
            "route",
            "dose_amt",
            "dose_unit",
            "dose_form",
            "dose_freq"
        ]
    ]
    .drop_duplicates()
)


# ============================================================
# 2. REACTION ANALYSIS
# ============================================================

reaction_analysis = (
    reactions
    .merge(
        drug[
            [
                "caseid",
                "glp1_drug"
            ]
        ].drop_duplicates(),
        on="caseid",
        how="inner"
    )
)


# Remove duplicate drug-reaction-case combinations

reaction_analysis = (
    reaction_analysis
    .drop_duplicates(
        subset=[
            "caseid",
            "glp1_drug",
            "pt"
        ]
    )
)


# ============================================================
# 3. REACTION SUMMARY
# ============================================================

reaction_summary = (
    reaction_analysis
    .groupby(
        [
            "glp1_drug",
            "pt"
        ]
    )
    .agg(
        unique_cases=(
            "caseid",
            "nunique"
        )
    )
    .reset_index()
)


# Total cases per drug

total_cases_by_drug = (
    drug[
        [
            "caseid",
            "glp1_drug"
        ]
    ]
    .drop_duplicates()
    .groupby("glp1_drug")
    .agg(
        total_cases=(
            "caseid",
            "nunique"
        )
    )
    .reset_index()
)


reaction_summary = reaction_summary.merge(
    total_cases_by_drug,
    on="glp1_drug",
    how="left"
)


reaction_summary["case_percentage"] = (
    reaction_summary["unique_cases"]
    /
    reaction_summary["total_cases"]
    *
    100
)


reaction_summary = reaction_summary.sort_values(
    [
        "glp1_drug",
        "case_percentage"
    ],
    ascending=[
        True,
        False
    ]
)


# ============================================================
# 4. TOP REACTIONS
# ============================================================

top_reactions = (
    reaction_summary
    .sort_values(
        [
            "glp1_drug",
            "unique_cases"
        ],
        ascending=[
            True,
            False
        ]
    )
    .groupby("glp1_drug")
    .head(20)
)


# ============================================================
# 5. PATIENT DEMOGRAPHIC ANALYSIS
# ============================================================

patient_analysis = patient.copy()


# Clean age

patient_analysis["age"] = pd.to_numeric(
    patient_analysis["age"],
    errors="coerce"
)


# Create custom age groups

def create_age_group(age):

    if pd.isna(age):
        return "Unknown"

    elif age < 18:
        return "Under 18"

    elif age <= 30:
        return "18-30"

    elif age <= 45:
        return "31-45"

    elif age <= 60:
        return "46-60"

    elif age <= 75:
        return "61-75"

    else:
        return "76+"


patient_analysis["age_group_custom"] = (
    patient_analysis["age"]
    .apply(create_age_group)
)


# ============================================================
# 6. CASE-LEVEL DRUG + PATIENT DATASET
# ============================================================

case_drug = (
    drug[
        [
            "caseid",
            "glp1_drug"
        ]
    ]
    .drop_duplicates()
)


case_patient_analysis = case_drug.merge(
    patient_analysis,
    on="caseid",
    how="left"
)


# ============================================================
# 7. DRUG DEMOGRAPHIC SUMMARY
# ============================================================

drug_demographic_summary = (
    case_patient_analysis
    .groupby(
        [
            "glp1_drug",
            "age_group_custom",
            "sex"
        ]
    )
    .agg(
        unique_cases=(
            "caseid",
            "nunique"
        )
    )
    .reset_index()
)


# ============================================================
# 8. OUTCOME ANALYSIS
# ============================================================

outcome_analysis = (
    outcomes
    .merge(
        drug[
            [
                "caseid",
                "glp1_drug"
            ]
        ].drop_duplicates(),
        on="caseid",
        how="inner"
    )
    .drop_duplicates(
        subset=[
            "caseid",
            "glp1_drug",
            "outc_cod"
        ]
    )
)


# ============================================================
# 9. OUTCOME SUMMARY
# ============================================================

outcome_summary = (
    outcome_analysis
    .groupby(
        [
            "glp1_drug",
            "outc_cod"
        ]
    )
    .agg(
        unique_cases=(
            "caseid",
            "nunique"
        )
    )
    .reset_index()
)


outcome_summary = outcome_summary.merge(
    total_cases_by_drug,
    on="glp1_drug",
    how="left"
)


outcome_summary["case_percentage"] = (
    outcome_summary["unique_cases"]
    /
    outcome_summary["total_cases"]
    *
    100
)


# ============================================================
# 10. INDICATION ANALYSIS
# ============================================================

indication_analysis = (
    indications
    .merge(
        drug[
            [
                "caseid",
                "glp1_drug"
            ]
        ].drop_duplicates(),
        on="caseid",
        how="inner"
    )
    .drop_duplicates(
        subset=[
            "caseid",
            "glp1_drug",
            "indi_pt"
        ]
    )
)


# ============================================================
# 11. INDICATION SUMMARY
# ============================================================

indication_summary = (
    indication_analysis
    .groupby(
        [
            "glp1_drug",
            "indi_pt"
        ]
    )
    .agg(
        unique_cases=(
            "caseid",
            "nunique"
        )
    )
    .reset_index()
)


# ============================================================
# 12. REPORTING TREND
# ============================================================

patient_analysis["fda_dt"] = pd.to_numeric(
    patient_analysis["fda_dt"],
    errors="coerce"
)


patient_analysis["report_year"] = (
    patient_analysis["fda_dt"]
    .astype("Int64")
    .astype(str)
    .str[:4]
)


patient_analysis["report_year"] = pd.to_numeric(
    patient_analysis["report_year"],
    errors="coerce"
)


reporting_trend = (
    case_drug
    .merge(
        patient_analysis[
            [
                "caseid",
                "report_year"
            ]
        ],
        on="caseid",
        how="left"
    )
    .groupby(
        [
            "report_year",
            "glp1_drug"
        ]
    )
    .agg(
        unique_cases=(
            "caseid",
            "nunique"
        )
    )
    .reset_index()
)


# ============================================================
# SAVE ANALYTICAL TABLES
# ============================================================

print("\nSaving analysis tables...")


drug_case_analysis.to_csv(
    OUTPUT_PATH + r"\drug_case_analysis.csv",
    index=False
)


reaction_analysis.to_csv(
    OUTPUT_PATH + r"\reaction_analysis.csv",
    index=False
)


reaction_summary.to_csv(
    OUTPUT_PATH + r"\reaction_summary.csv",
    index=False
)


top_reactions.to_csv(
    OUTPUT_PATH + r"\top_reactions.csv",
    index=False
)


patient_analysis.to_csv(
    OUTPUT_PATH + r"\patient_analysis.csv",
    index=False
)


drug_demographic_summary.to_csv(
    OUTPUT_PATH + r"\drug_demographic_summary.csv",
    index=False
)


outcome_analysis.to_csv(
    OUTPUT_PATH + r"\outcome_analysis.csv",
    index=False
)


outcome_summary.to_csv(
    OUTPUT_PATH + r"\outcome_summary.csv",
    index=False
)


indication_analysis.to_csv(
    OUTPUT_PATH + r"\indication_analysis.csv",
    index=False
)


indication_summary.to_csv(
    OUTPUT_PATH + r"\indication_summary.csv",
    index=False
)


reporting_trend.to_csv(
    OUTPUT_PATH + r"\reporting_trend.csv",
    index=False
)


print("\n" + "=" * 60)
print("ANALYSIS TABLES CREATED SUCCESSFULLY")
print("=" * 60)


print("\nReaction summary:")
print(reaction_summary.head(10))


print("\nOutcome summary:")
print(outcome_summary.head(10))


print("\nReporting trend:")
print(reporting_trend.head(10))


print("\nFiles saved to:")
print(OUTPUT_PATH)