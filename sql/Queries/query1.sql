/*==============================================================
GLP-1 PHARMACOVIGILANCE ANALYSIS
SQL ANALYTICAL QUERIES
==============================================================*/


/*==============================================================
BASIC QUERIES
==============================================================*/


-- Q1. How many adverse event cases are reported for each GLP-1 drug?

SELECT
    glp1_drug,
    unique_cases,
    outcome_case_rate,
    avg_reactions_per_case
FROM drug_summary
ORDER BY unique_cases DESC;



-- Q2. What are the adverse reactions occurring in more than 10% of cases?

SELECT
    glp1_drug,
    pt,
    case_percentage
FROM reaction_summary
WHERE case_percentage > 10
ORDER BY
    glp1_drug,
    case_percentage DESC;



-- Q3. What are the reported clinical outcomes for each GLP-1 drug?

SELECT
    glp1_drug,
    outc_cod,
    unique_cases,
    case_percentage
FROM outcome_summary
ORDER BY
    glp1_drug,
    case_percentage DESC;



-- Q4. How many reports were received each year?

SELECT *
FROM reporting_trend
ORDER BY
    report_year,
    glp1_drug;



-- Q5. What percentage of all reported cases belongs to each drug?

SELECT
    glp1_drug,
    unique_cases,
    ROUND(
        unique_cases * 100 /
        SUM(unique_cases) OVER(),
        2
    ) AS percent_of_all_reports
FROM drug_summary
ORDER BY percent_of_all_reports DESC;



-- Q6. Which reactions occur in at least 5% of reported cases?

SELECT
    glp1_drug,
    pt,
    unique_cases,
    ROUND(case_percentage,2) AS percentage
FROM reaction_summary
WHERE case_percentage >= 5
ORDER BY
    glp1_drug,
    percentage DESC;



-- Q7. Which drug has the highest outcome reporting rate?

SELECT
    glp1_drug,
    outcome_case_rate
FROM drug_summary
ORDER BY outcome_case_rate DESC;



-- Q8. Which drug shows the greatest diversity of reaction types?

SELECT
    glp1_drug,
    unique_reaction_types,
    avg_reactions_per_case
FROM drug_summary
ORDER BY unique_reaction_types DESC;



-- Q9. How many unique reaction types are associated with each drug?

SELECT
    glp1_drug,
    COUNT(DISTINCT pt) AS reaction_types
FROM reaction_summary
GROUP BY glp1_drug
ORDER BY reaction_types DESC;



/*==============================================================
INTERMEDIATE QUERIES
==============================================================*/


-- Q10. Rank all reactions within each drug by number of affected cases.

SELECT
    glp1_drug,
    pt,
    unique_cases,
    DENSE_RANK() OVER(
        PARTITION BY glp1_drug
        ORDER BY unique_cases DESC
    ) AS reaction_rank
FROM reaction_summary;



-- Q11. What are the Top 5 most frequently reported reactions for each drug?

SELECT *
FROM
(
SELECT
    glp1_drug,
    pt,
    unique_cases,
    DENSE_RANK() OVER(
        PARTITION BY glp1_drug
        ORDER BY unique_cases DESC
    ) AS rnk
FROM reaction_summary
) x
WHERE rnk <= 5;



-- Q12. Which reactions are reported for all three GLP-1 drugs?

SELECT
    pt,
    COUNT(DISTINCT glp1_drug) AS drugs
FROM reaction_summary
GROUP BY pt
HAVING COUNT(DISTINCT glp1_drug)=3
ORDER BY pt;



-- Q13. Which reactions are unique to only one GLP-1 drug?

SELECT
    glp1_drug,
    pt
FROM reaction_summary r
WHERE NOT EXISTS
(
SELECT *
FROM reaction_summary r2
WHERE r2.pt=r.pt
AND r2.glp1_drug<>r.glp1_drug
);



-- Q14. What is the most common clinical outcome for each drug?

SELECT *
FROM
(
SELECT
    glp1_drug,
    outc_cod,
    unique_cases,
    ROW_NUMBER() OVER(
        PARTITION BY glp1_drug
        ORDER BY unique_cases DESC
    ) rn
FROM outcome_summary
) x
WHERE rn=1;



-- Q15. Which drug contributes the highest percentage of all reaction records?

SELECT
    glp1_drug,
    total_reaction_records,
    ROUND(
        total_reaction_records * 100.0 /
        SUM(total_reaction_records) OVER(),
        2
    ) AS contribution_percent
FROM drug_summary;



-- Q16. Which reactions appear exclusively in one drug?

SELECT
    pt,
    MIN(glp1_drug) AS drug
FROM reaction_summary
GROUP BY pt
HAVING COUNT(DISTINCT glp1_drug)=1;



-- Q17. What is the hospitalization rate (HO outcome) for each drug?

SELECT
    glp1_drug,
    case_percentage
FROM outcome_summary
WHERE outc_cod='HO'
ORDER BY case_percentage DESC;



-- Q18. Compare each drug's outcome rate with the overall average outcome rate.

SELECT
    glp1_drug,
    outcome_case_rate,
    AVG(outcome_case_rate) OVER() AS average_rate
FROM drug_summary;



-- Q19. Compare average reactions per case with the highest observed value.

SELECT
    glp1_drug,
    avg_reactions_per_case,
    MAX(avg_reactions_per_case) OVER() AS highest_value,
    ROUND(
        MAX(avg_reactions_per_case) OVER() -
        avg_reactions_per_case,
        2
    ) AS difference
FROM drug_summary;



/*==============================================================
ADVANCED QUERIES
==============================================================*/


-- Q20. How much does each drug differ from the overall average number of reactions?

SELECT
    glp1_drug,
    avg_reactions_per_case,
    ROUND(
        avg_reactions_per_case-
        AVG(avg_reactions_per_case) OVER(),
        2
    ) AS difference_from_average
FROM drug_summary;



-- Q21. What is the cumulative number of reported cases after sorting by popularity?

SELECT
    glp1_drug,
    unique_cases,
    SUM(unique_cases)
    OVER(
        ORDER BY unique_cases DESC
    ) cumulative_cases
FROM drug_summary;



-- Q22. Calculate a custom safety risk score combining outcome rate and reaction burden.

SELECT
    glp1_drug,
    ROUND(
    (
        outcome_case_rate*0.7
        +
        avg_reactions_per_case*5
    ),2) AS safety_risk_score
FROM drug_summary
ORDER BY safety_risk_score DESC;



-- Q23. Compare the highest reaction percentage with the average reaction percentage.

SELECT
    glp1_drug,
    MAX(case_percentage) AS highest_reaction_percentage,
    AVG(case_percentage) AS average_reaction_percentage
FROM reaction_summary
GROUP BY glp1_drug;



-- Q24. Which reactions occur more frequently than the average reaction rate for that drug?

WITH avg_rate AS
(
    SELECT
        glp1_drug,
        AVG(case_percentage) AS avg_percentage
    FROM reaction_summary
    GROUP BY glp1_drug
)

SELECT
    r.glp1_drug,
    r.pt,
    r.case_percentage
FROM reaction_summary r
JOIN avg_rate a
ON r.glp1_drug = a.glp1_drug
WHERE r.case_percentage > a.avg_percentage
ORDER BY
    r.glp1_drug,
    r.case_percentage DESC;



-- Q25. Find the Top 5 reactions using Common Table Expressions (CTEs) and Window Functions.

WITH RankedReactions AS
(
    SELECT
        glp1_drug,
        pt,
        unique_cases,
        case_percentage,
        DENSE_RANK() OVER
        (
            PARTITION BY glp1_drug
            ORDER BY case_percentage DESC
        ) AS reaction_rank
    FROM reaction_summary
)

SELECT *
FROM RankedReactions
WHERE reaction_rank <= 5;