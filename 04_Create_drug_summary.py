import pandas as pd
import os


# ============================================================
# PATHS
# ============================================================

INPUT_PATH = r"E:\glp1\dataset\processed"
OUTPUT_PATH = r"E:\glp1\dataset\analysis"


# ============================================================
# LOAD CLEAN TABLES
# ============================================================

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


# ============================================================
# UNIQUE CASE-DRUG RELATIONSHIP
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


# ============================================================
# DRUG SUMMARY
# ============================================================

drug_summary = (
    case_drug
    .groupby("glp1_drug")
    .agg(
        unique_cases=(
            "caseid",
            "nunique"
        )
    )
    .reset_index()
)


# ============================================================
# UNIQUE REACTION COUNT
# ============================================================

reaction_case_drug = (
    reactions
    .merge(
        case_drug,
        on="caseid",
        how="inner"
    )
    .drop_duplicates(
        subset=[
            "caseid",
            "glp1_drug",
            "pt"
        ]
    )
)


reaction_counts = (
    reaction_case_drug
    .groupby("glp1_drug")
    .agg(
        unique_reaction_types=(
            "pt",
            "nunique"
        ),

        total_reaction_records=(
            "pt",
            "count"
        ),

        cases_with_reactions=(
            "caseid",
            "nunique"
        )
    )
    .reset_index()
)


# ============================================================
# OUTCOME COUNT
# ============================================================

outcome_case_drug = (
    outcomes
    .merge(
        case_drug,
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


outcome_counts = (
    outcome_case_drug
    .groupby("glp1_drug")
    .agg(
        cases_with_outcomes=(
            "caseid",
            "nunique"
        ),

        outcome_records=(
            "outc_cod",
            "count"
        ),

        unique_outcome_types=(
            "outc_cod",
            "nunique"
        )
    )
    .reset_index()
)


# ============================================================
# MERGE SUMMARY TABLE
# ============================================================

drug_summary = (
    drug_summary
    .merge(
        reaction_counts,
        on="glp1_drug",
        how="left"
    )
    .merge(
        outcome_counts,
        on="glp1_drug",
        how="left"
    )
)


# ============================================================
# CALCULATE RATES
# ============================================================

# Reaction case rate is not calculated because
# the FDA REAC table only contains cases
# with at least one reported reaction.

drug_summary["outcome_case_rate"] = (
    drug_summary["cases_with_outcomes"]
    /
    drug_summary["unique_cases"]
    *
    100
)


drug_summary["avg_reactions_per_case"] = (
    drug_summary["total_reaction_records"]
    /
    drug_summary["unique_cases"]
)


# ============================================================
# SORT
# ============================================================

drug_summary = drug_summary.sort_values(
    "unique_cases",
    ascending=False
)


# ============================================================
# REMOVE MISLEADING COLUMN
# ============================================================

drug_summary = drug_summary.drop(
    columns=[
        "cases_with_reactions"
    ]
)


# ============================================================
# SAVE
# ============================================================

drug_summary.to_csv(
    OUTPUT_PATH + r"\drug_summary.csv",
    index=False
)


# ============================================================
# DISPLAY
# ============================================================

print("\n" + "=" * 60)
print("DRUG SUMMARY")
print("=" * 60)

print(drug_summary.to_string(index=False))

print("\n✓ Drug summary saved successfully.")

# ============================================================
# OVERALL SUMMARY
# ============================================================

total_unique_cases = drug["caseid"].nunique()

unique_reaction_types = reactions["pt"].nunique()

total_cases_with_outcomes = outcomes["caseid"].nunique()

total_reaction_records = (
    reactions
    .drop_duplicates(subset=["caseid", "pt"])
    .shape[0]
)

avg_reactions_per_case = (
    total_reaction_records / total_unique_cases
)

overall_summary = pd.DataFrame({
    "total_unique_cases": [total_unique_cases],
    "unique_reaction_types": [unique_reaction_types],
    "total_cases_with_outcomes": [total_cases_with_outcomes],
    "total_reaction_records": [total_reaction_records],
    "avg_reactions_per_case": [avg_reactions_per_case]
})

overall_summary.to_csv(
    OUTPUT_PATH + r"\overall_summary.csv",
    index=False
)

print("\nOVERALL SUMMARY")
print(overall_summary)

print("Raw unique reaction terms:", reactions["pt"].nunique())

print(
    "Unique reaction terms after stripping spaces and ignoring case:",
    reactions["pt"].astype(str).str.strip().str.upper().nunique()
)