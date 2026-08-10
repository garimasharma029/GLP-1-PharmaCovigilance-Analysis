import pandas as pd

# ============================================
# Folder containing the FDA ASCII files
# ============================================

base_path = r"E:\glp1\dataset by fda\ASCII"


# ============================================
# 1. DEMO - Patient and report information
# ============================================

demo_file_path = base_path + r"\DEMO26Q1.txt"

demo_data = pd.read_csv(
    demo_file_path,
    sep="$",
    encoding="latin1"
)

print("\n" + "=" * 60)
print("DEMO TABLE")
print("=" * 60)

print("Shape:", demo_data.shape)
print("Columns:")
print(demo_data.columns.tolist())

print("\nFirst 5 rows:")
print(demo_data.head())


# ============================================
# 2. DRUG - Drug information
# ============================================

drug_file_path = base_path + r"\DRUG26Q1.txt"

drug_data = pd.read_csv(
    drug_file_path,
    sep="$",
    encoding="latin1"
)

print("\n" + "=" * 60)
print("DRUG TABLE")
print("=" * 60)

print("Shape:", drug_data.shape)
print("Columns:")
print(drug_data.columns.tolist())

print("\nFirst 5 rows:")
print(drug_data.head())


# ============================================
# 3. REAC - Reported adverse reactions
# ============================================

reac_file_path = base_path + r"\REAC26Q1.txt"

reac_data = pd.read_csv(
    reac_file_path,
    sep="$",
    encoding="latin1"
)

print("\n" + "=" * 60)
print("REAC TABLE")
print("=" * 60)

print("Shape:", reac_data.shape)
print("Columns:")
print(reac_data.columns.tolist())

print("\nFirst 5 rows:")
print(reac_data.head())


# ============================================
# 4. OUTC - Patient outcomes
# ============================================

outc_file_path = base_path + r"\OUTC26Q1.txt"

outc_data = pd.read_csv(
    outc_file_path,
    sep="$",
    encoding="latin1"
)

print("\n" + "=" * 60)
print("OUTC TABLE")
print("=" * 60)

print("Shape:", outc_data.shape)
print("Columns:")
print(outc_data.columns.tolist())

print("\nFirst 5 rows:")
print(outc_data.head())


# ============================================
# 5. INDI - Indication/reason for drug use
# ============================================

indi_file_path = base_path + r"\INDI26Q1.txt"

indi_data = pd.read_csv(
    indi_file_path,
    sep="$",
    encoding="latin1"
)

print("\n" + "=" * 60)
print("INDI TABLE")
print("=" * 60)

print("Shape:", indi_data.shape)
print("Columns:")
print(indi_data.columns.tolist())

print("\nFirst 5 rows:")
print(indi_data.head())


# ============================================
# 6. THER - Therapy/treatment information
# ============================================

ther_file_path = base_path + r"\THER26Q1.txt"

ther_data = pd.read_csv(
    ther_file_path,
    sep="$",
    encoding="latin1"
)

print("\n" + "=" * 60)
print("THER TABLE")
print("=" * 60)

print("Shape:", ther_data.shape)
print("Columns:")
print(ther_data.columns.tolist())

print("\nFirst 5 rows:")
print(ther_data.head())


# ============================================
# 7. RPSR - Report source information
# ============================================

rpsr_file_path = base_path + r"\RPSR26Q1.txt"

rpsr_data = pd.read_csv(
    rpsr_file_path,
    sep="$",
    encoding="latin1"
)

print("\n" + "=" * 60)
print("RPSR TABLE")
print("=" * 60)

print("Shape:", rpsr_data.shape)
print("Columns:")
print(rpsr_data.columns.tolist())

print("\nFirst 5 rows:")
print(rpsr_data.head())

# ============================================
# 8. Check drug names
# ============================================

print("\n" + "=" * 60)
print("UNIQUE DRUG NAMES")
print("=" * 60)

print("Number of unique drug names:")
print(drug_data["drugname"].nunique())

print("\nFirst 100 drug names:")
print(drug_data["drugname"].dropna().unique()[:100])

# ============================================
# Search for GLP-1-related drugs
# ============================================

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

print("\n" + "=" * 60)
print("GLP-1 DRUG RECORDS")
print("=" * 60)

print("Shape:", glp1_drugs.shape)

print("\nDrug name counts:")
print(glp1_drugs["drugname"].value_counts())

print("\nUnique matching drug names:")
print(glp1_drugs["drugname"].unique())

print("\nFirst 10 GLP-1 records:")
print(glp1_drugs.head(10))

print(glp1_drugs["drugname"].value_counts().to_string())

# ============================================
# Standardize GLP-1 drug names
# ============================================

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


glp1_drugs["glp1_drug"] = glp1_drugs["drugname"].apply(
    classify_glp1_drug
)


# ============================================
# Standardized GLP-1 drug counts
# ============================================

print("\n" + "=" * 60)
print("STANDARDIZED GLP-1 DRUG COUNTS")
print("=" * 60)

print(glp1_drugs["glp1_drug"].value_counts())

# ============================================
# Analyze drug role in GLP-1 reports
# ============================================

print("\n" + "=" * 60)
print("GLP-1 DRUG ROLE ANALYSIS")
print("=" * 60)

print("\nOverall role counts:")
print(glp1_drugs["role_cod"].value_counts())

print("\nRole by standardized GLP-1 drug:")
print(
    pd.crosstab(
        glp1_drugs["glp1_drug"],
        glp1_drugs["role_cod"]
    )
)

# ============================================
# Unique case analysis
# ============================================

print("\n" + "=" * 60)
print("UNIQUE CASE ANALYSIS")
print("=" * 60)

print("\nTotal GLP-1 drug records:")
print(len(glp1_drugs))

print("\nUnique primary IDs:")
print(glp1_drugs["primaryid"].nunique())

print("\nUnique case IDs:")
print(glp1_drugs["caseid"].nunique())

print("\nUnique cases by GLP-1 drug:")
print(
    glp1_drugs.groupby("glp1_drug")["caseid"]
    .nunique()
    .sort_values(ascending=False)
)

# ============================================
# Extract reactions for GLP-1 cases
# ============================================

# Get the unique case IDs involving GLP-1 drugs
glp1_case_ids = glp1_drugs["caseid"].unique()

# Filter the REAC table to only those cases
glp1_reactions = reac_data[
    reac_data["caseid"].isin(glp1_case_ids)
].copy()


print("\n" + "=" * 60)
print("GLP-1 ADVERSE REACTIONS")
print("=" * 60)

print("\nShape:")
print(glp1_reactions.shape)

print("\nColumns:")
print(glp1_reactions.columns.tolist())

print("\nFirst 10 reactions:")
print(glp1_reactions.head(10))

# ============================================
# Most common GLP-1 adverse reactions
# ============================================

print("\n" + "=" * 60)
print("MOST COMMON GLP-1 ADVERSE REACTIONS")
print("=" * 60)

print(
    glp1_reactions["pt"]
    .value_counts()
    .head(20)
)

# ============================================
# Connect GLP-1 drugs with their reactions
# ============================================

# Keep only the columns needed from the drug table
drug_case_mapping = glp1_drugs[
    ["caseid", "glp1_drug"]
].drop_duplicates()


# Merge drug information with reaction information
glp1_drug_reactions = glp1_reactions.merge(
    drug_case_mapping,
    on="caseid",
    how="inner"
)


print("\n" + "=" * 60)
print("GLP-1 DRUG + REACTION DATASET")
print("=" * 60)

print("Shape:")
print(glp1_drug_reactions.shape)

print("\nFirst 10 rows:")
print(
    glp1_drug_reactions[
        ["caseid", "glp1_drug", "pt"]
    ].head(10)
)

# ============================================
# Top adverse reactions by GLP-1 drug
# ============================================

for drug in ["SEMAGLUTIDE", "TIRZEPATIDE", "LIRAGLUTIDE"]:

    print("\n" + "=" * 60)
    print(f"TOP 20 REACTIONS: {drug}")
    print("=" * 60)

    top_reactions = (
        glp1_drug_reactions[
            glp1_drug_reactions["glp1_drug"] == drug
        ]["pt"]
        .value_counts()
        .head(20)
    )

    print(top_reactions)

# ============================================
# Unique cases per adverse reaction
# ============================================

for drug in ["SEMAGLUTIDE", "TIRZEPATIDE", "LIRAGLUTIDE"]:

    drug_data = glp1_drug_reactions[
        glp1_drug_reactions["glp1_drug"] == drug
    ]

    top_reactions = (
        drug_data
        .groupby("pt")["caseid"]
        .nunique()
        .sort_values(ascending=False)
        .head(20)
    )

    print("\n" + "=" * 60)
    print(f"TOP 20 REACTIONS BY UNIQUE CASES: {drug}")
    print("=" * 60)

    print(top_reactions)

    # ============================================
# Reaction frequency by percentage of cases
# ============================================

reaction_summary = (
    glp1_drug_reactions
    .groupby(["glp1_drug", "pt"])["caseid"]
    .nunique()
    .reset_index(name="unique_cases")
)


# Count total unique cases per drug
total_cases_by_drug = (
    glp1_drugs
    .groupby("glp1_drug")["caseid"]
    .nunique()
    .reset_index(name="total_cases")
)


# Merge total cases into reaction summary
reaction_summary = reaction_summary.merge(
    total_cases_by_drug,
    on="glp1_drug",
    how="left"
)


# Calculate percentage of cases reporting each reaction
reaction_summary["case_percentage"] = (
    reaction_summary["unique_cases"]
    / reaction_summary["total_cases"]
    * 100
)


# Sort by drug and percentage
reaction_summary = reaction_summary.sort_values(
    ["glp1_drug", "case_percentage"],
    ascending=[True, False]
)


print("\n" + "=" * 60)
print("TOP REACTIONS BY PERCENTAGE OF CASES")
print("=" * 60)


for drug in ["SEMAGLUTIDE", "TIRZEPATIDE", "LIRAGLUTIDE"]:

    print("\n" + "-" * 60)
    print(drug)

    print(
        reaction_summary[
            reaction_summary["glp1_drug"] == drug
        ][
            ["pt", "unique_cases", "total_cases", "case_percentage"]
        ].head(20)
    )

# ============================================
# Explore unique reaction terms
# ============================================

print("\n" + "=" * 60)
print("REACTION TERM ANALYSIS")
print("=" * 60)

print(
    "Total unique reaction terms:",
    glp1_drug_reactions["pt"].nunique()
)

print("\nSample reaction terms:")
print(
    glp1_drug_reactions["pt"]
    .dropna()
    .drop_duplicates()
    .head(100)
    .to_string(index=False)
)