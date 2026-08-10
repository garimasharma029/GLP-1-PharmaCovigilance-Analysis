USE glp1_pharmacovigilance;

CREATE TABLE drug_summary (
    glp1_drug VARCHAR(50) PRIMARY KEY,
    unique_cases INT,
    unique_reaction_types INT,
    total_reaction_records INT,
    cases_with_outcomes INT,
    outcome_records INT,
    unique_outcome_types INT,
    outcome_case_rate FLOAT,
    avg_reactions_per_case FLOAT
);

CREATE TABLE reaction_summary (
    glp1_drug VARCHAR(50),
    pt VARCHAR(255),
    unique_cases INT,
    total_cases INT,
    case_percentage FLOAT
);

CREATE TABLE outcome_summary (
    glp1_drug VARCHAR(50),
    outc_cod VARCHAR(10),
    unique_cases INT,
    total_cases INT,
    case_percentage FLOAT
);

CREATE TABLE reporting_trend (
    report_year INT,
    glp1_drug VARCHAR(50),
    unique_cases INT
);

