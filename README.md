# GLP-1 Pharmacovigilance Analysis

A data analytics project focused on analyzing adverse reactions, patient outcomes, demographics, indications, and reporting patterns associated with selected GLP-1 drugs using FDA Adverse Event Reporting System (FAERS) data.

## Project Overview

This project analyzes reported adverse events associated with three GLP-1 drug groups:

- Semaglutide
- Tirzepatide
- Liraglutide

The project follows an end-to-end analytics workflow:

**FDA Raw Data → Data Cleaning → Data Analysis → SQL Analysis → Power BI Dashboard**

## Objectives

- Analyze reported adverse reactions associated with GLP-1 drugs
- Compare adverse reaction patterns across drugs
- Analyze patient demographics and outcomes
- Identify commonly reported reaction types
- Calculate case-level reaction and outcome metrics
- Explore indications associated with GLP-1 drugs
- Compare drug-level safety metrics
- Build an interactive Power BI dashboard

## Tools & Technologies

- **Python** – Data cleaning, transformation, and analysis
- **Pandas** – Data manipulation and aggregation
- **MySQL** – Database creation and analytical queries
- **Power BI** – Interactive visualization and dashboard development
- **CSV** – Processed and analytical data storage

## Project Structure

```text
GLP-1-PharmaCovigilance-Analysis/
│
├── code/
│   ├── 01_explore_fda_data.py
│   ├── 02_Create_clean_tables.py
│   ├── 03_Create_analysis_table.py
│   └── 04_Create_drug_summary.py
│
├── dataset/
│   ├── analysis/
│   └── processed/
│
├── Dashboard/
│   └── GLP-1 Drug Safety Dashboard.pbix
│
├── sql/
│   ├── create_database.sql
│   ├── create_tables.sql
│   └── queries.sql
│
├── .gitignore
└── README.md
```

## Data Source

The project uses data from the **FDA Adverse Event Reporting System (FAERS)**.

The original FDA ASCII dataset is not included in this repository because of its size. The raw dataset is used locally during the data-processing stage.

## Python Workflow

### 1. Exploratory Data Analysis

`01_explore_fda_data.py`

- Loads the FDA ASCII tables
- Examines the structure of the source data
- Identifies GLP-1-related drug records
- Standardizes GLP-1 drug names
- Performs initial exploratory analysis

### 2. Create Clean Tables

`02_Create_clean_tables.py`

Creates cleaned datasets for:

- Drugs
- Patients
- Reactions
- Outcomes
- Indications
- Therapy
- Report sources
- Case summaries

### 3. Create Analysis Tables

`03_Create_analysis_table.py`

Creates analytical datasets for:

- Drug analysis
- Reaction analysis
- Reaction summaries
- Patient demographics
- Outcome analysis
- Outcome summaries
- Indication analysis
- Reporting trends

### 4. Drug Summary

`04_Create_drug_summary.py`

Creates drug-level summary metrics including:

- Unique cases
- Unique reaction types
- Reaction records
- Outcome records
- Outcome case rate
- Average reactions per case
- Overall project-level metrics

## SQL Analysis

The SQL section contains:

- Database creation
- Table creation
- Analytical queries

SQL was used to further explore and summarize the processed GLP-1 pharmacovigilance data.

## Power BI Dashboard

The final Power BI dashboard contains three pages.

### 1. Explorative Analysis

Provides an overview of:

- Total unique cases
- GLP-1 drug distribution
- Patient demographics
- Drug indications
- Overall reporting patterns

### 2. Adverse Reaction Analysis

Focuses on:

- Top adverse reactions
- Adverse reaction distribution by drug
- Serious outcomes
- Reaction case percentages
- Adverse reaction profiles

### 3. Drug Safety Profile

Provides comparative drug-level analysis using:

- Reaction burden
- Outcome rate
- Drug-level case counts
- Indication distribution
- Drug safety metrics

## Important Note

This project analyzes **reported adverse events** from FAERS. Reported cases do not by themselves establish causality, incidence, or clinical risk. The analysis should therefore be interpreted as pharmacovigilance reporting analysis rather than a clinical safety assessment.