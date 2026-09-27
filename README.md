Tech Job Market Intelligence Platform

An interactive data analytics project that explores the Indian tech job market to answer a practical question:

What skills are actually being demanded in today's tech job market?

The project analyzes 23,201 technology job postings and combines Python-based data processing, text-based skill extraction, MySQL, SQL analysis, Streamlit, and Plotly to turn raw job-posting data into an interactive market intelligence dashboard.

Project Objective

The goal is to understand hiring demand across technology roles and identify patterns that are useful for job seekers and recruiters.

The analysis focuses on:

Which roles have the highest hiring demand?

Which technical skills appear most frequently?

Which skills commonly occur together?

How do skill requirements differ across role families?

Which skills appear more often in fresher-friendly jobs?

How do work modes and locations vary across the market?

What salary patterns are visible among jobs where salary is disclosed?

Which skills are associated with higher disclosed salary levels?

Salary findings are treated as associations, not causal effects.

Dataset

Source: Kaggle — India Tech Job Market 2026

The dataset contains 23,201 job postings and 32 original columns covering job titles, companies, locations, experience, salary, work mode, skills, and other job attributes.

Dataset:
https://www.kaggle.com/datasets/shree0910/india-tech-job-market-2026-23k-records

The raw dataset is intentionally not committed to this repository. It can be downloaded from the source above.

Tech Stack

Python

Pandas

NumPy

Text / Skill Processing

Rule-based skill extraction from job-posting text

Database

MySQL

Analysis

SQL

Pandas

Dashboard

Streamlit

Plotly

Development

Git / GitHub

Jupyter (for exploratory analysis where applicable)

Project Workflow

Kaggle Job Dataset
        ↓
Python / Pandas
        ↓
Data Cleaning
        ↓
Role Normalization
        ↓
Text-Based Skill Extraction
        ↓
MySQL
        ↓
SQL Analysis
        ↓
Streamlit + Plotly Dashboard

Data Processing

Data Cleaning

The original dataset was inspected for:

duplicate records

missing values

salary validity

inconsistent job-title formats

experience fields

work-mode values

location information

The dataset contains 23,201 unique job postings and no duplicate rows.

Role Normalization

The original role_category field contains six broad categories. Instead of overwriting that original classification, the project creates additional role fields based on job titles:

normalized_role

role_family

This makes it possible to analyze more specific roles while retaining the original dataset classification.

The normalization process groups titles into families such as:

Data & Analytics

Data Engineering

Software Engineering

AI & Machine Learning

QA & Testing

Architecture

Cloud & DevOps

Product & Business

Other

The project intentionally keeps an Other category rather than forcing ambiguous titles into technical roles.

Skill Extraction

A canonical set of 37 tracked skills was created from the skills and job-description information.

Examples include:

Python

SQL

Data Analysis

Machine Learning

Artificial Intelligence

Azure

AWS

GCP

Power BI

Excel

NLP

Generative AI

Deep Learning

PyTorch

Spark

JavaScript

Git

Java

C++

Selenium

Docker

Kubernetes

LangChain

The resulting job-skill relationships are stored separately from the main job table so that skills can be analyzed relationally.

Note: the source dataset's skill information is not necessarily exhaustive, so extracted skill counts should be interpreted as observed demand within the dataset rather than a complete inventory of every skill mentioned in each posting.

MySQL Data Model

The project uses two primary tables.

jobs

Stores job-level information such as:

job ID

title

company

location

role category

normalized role

role family

experience

salary

work mode

fresher-friendly indicator

other job attributes

job_skills

Stores the many-to-many relationship between jobs and tracked skills:

job_id
skill

This structure makes it possible to perform SQL analyses such as:

skill frequency

role × skill demand

skill combinations

fresher vs non-fresher skill demand

salary × skill associations

Dashboard

The project contains a five-page Streamlit dashboard.

1. Market Overview

Provides a high-level view of the market, including:

total job postings

role-family distribution

work-mode distribution

location distribution

experience distribution

fresher-friendly hiring

2. Role Intelligence

Allows users to explore how skill demand changes by role family.

Examples include:

AI & Machine Learning

Data Engineering

Data & Analytics

Software Engineering

QA & Testing

Architecture

Cloud & DevOps

Product & Business

The page connects role demand with the skills appearing in those postings.

3. Skill Intelligence

Explores the most frequently observed skills and skill combinations.

Examples of commonly observed combinations include:

AI + Machine Learning

Machine Learning + Python

Python + SQL

AI + Python

Data Analysis + Python

Data Analysis + SQL

Data Engineering + Python

Data Analysis + Power BI

These combinations represent co-occurrence, not causation.

4. Fresher Intelligence

Compares skill demand between:

fresher-friendly jobs

non-fresher-friendly jobs

The analysis highlights skills whose observed frequency differs between the two groups.

For example, Data Analysis appears more frequently in fresher-friendly postings than in the non-fresher group within this dataset.

Absolute demand is also considered because a relative difference alone can be misleading.

5. Salary Intelligence

Analyzes salary information only for postings where salary is disclosed.

The page explores:

disclosed salary levels

salary patterns by role

skill-associated salary averages

role-controlled salary comparisons

Only around 11.9% of postings in the dataset disclose salary, so salary findings should not be interpreted as representative of the entire job market.

Salary relationships are observational and should not be interpreted as evidence that a particular skill causes higher compensation.

Selected Market Findings

Based on the analyzed dataset:

Work Mode

On-site: 80.60%

Hybrid: 10.12%

Remote: 9.28%

Experience

Mid-level: 10,112

Junior: 4,915

Senior: 4,810

Fresher: 2,219

Lead / Architect: 1,145

Fresher-Friendly Jobs

Fresher-friendly: 4,182

Not fresher-friendly: 19,019

Frequently Observed Skills

Some of the most frequently observed tracked skills include:

Skill

Job postings

Python

4,347

Data Analysis

4,209

SQL

4,132

Machine Learning

3,752

Artificial Intelligence

3,152

Azure

1,376

Data Engineering

1,131

Power BI

1,114

GCP

1,107

AWS

1,001

These figures represent the tracked skills extracted from this dataset, not the complete universe of skills mentioned in all postings.

Example SQL Analysis

A simplified example of role-specific skill demand:

SELECT
    j.role_family,
    js.skill,
    COUNT(DISTINCT j.job_id) AS job_count
FROM jobs j
JOIN job_skills js
    ON j.job_id = js.job_id
WHERE j.role_family <> 'Other'
GROUP BY j.role_family, js.skill
ORDER BY j.role_family, job_count DESC;

This allows the dashboard to compare which skills appear most frequently across different role families.

Project Structure

job-market-intelligence/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── notebooks/
│
├── src/
│   ├── data_cleaning.py
│   ├── fresher_skill_analysis.py
│   ├── load_to_mysql.py
│   ├── role_normalization.py
│   ├── role_skill_analysis.py
│   ├── skill_analysis.py
│   ├── skill_combinations.py
│   ├── skill_extraction.py
│   └── update_mysql_roles.py
│
├── sql/
│
├── README.md
├── requirements.txt
└── .gitignore

