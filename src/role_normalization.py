import pandas as pd

# Load jobs
df = pd.read_csv("data/raw/jobs.csv")


def normalize_role(title):
    title = str(title).lower().strip()

    # -------------------------
    # QA / TESTING
    # -------------------------
    if any(x in title for x in [
        "qa", "quality assurance", "test engineer",
        "testing engineer", "software tester",
        "test automation", "automation test",
        "quality analyst", "test lead"
    ]):
        return "QA / Testing"

    # -------------------------
    # MLOPS
    # -------------------------
    if "mlops" in title:
        return "MLOps Engineer"

    # -------------------------
    # AI / MACHINE LEARNING
    # -------------------------
    if any(x in title for x in [
        "machine learning", "ml engineer",
        "ai engineer", "ai/ml",
        "artificial intelligence engineer",
        "computer vision engineer",
        "computer vision",
        "deep learning engineer",
        "nlp engineer",
        "generative ai engineer",
        "prompt engineer",
        "ai automation engineer",
        "ai & automation",
        "ai specialist",
        "ai security",
        "ai trust",
        "ai solution",
        "ai solutions",
        "ai architect"
    ]):
        if "computer vision" in title:
            return "Computer Vision Engineer"
        elif "prompt engineer" in title:
            return "Prompt Engineer"
        elif "ml engineer" in title or "machine learning" in title:
            return "ML Engineer"
        elif "ai architect" in title or "ai solution" in title:
            return "AI Architect"
        else:
            return "AI Engineer"

    # -------------------------
    # DATA SCIENCE
    # -------------------------
    if any(x in title for x in [
        "data scientist",
        "data science",
        "research scientist"
    ]):
        return "Data Scientist"

    # -------------------------
    # DATA ENGINEERING
    # -------------------------
    if any(x in title for x in [
        "data engineer",
        "big data engineer",
        "data engineering",
        "data warehouse engineer",
        "data warehouse",
        "data integration engineer",
        "data integration lead",
        "data integration architect",
        "data modeller",
        "data modeler",
        "data modelling",
        "data modeling",
        "databricks engineer",
        "spark data",
        "data migration",
        "data quality engineer",
        "data systems engineer",
        "data platform engineer"
    ]):
        if "data warehouse" in title:
            return "Data Warehouse Engineer"
        elif "data integration" in title:
            return "Data Integration Engineer"
        elif "databricks" in title:
            return "Databricks Engineer"
        elif "data model" in title or "data modell" in title:
            return "Data Modeler"
        elif "data quality" in title:
            return "Data Quality Engineer"
        elif "data migration" in title:
            return "Data Migration Engineer"
        else:
            return "Data Engineer"

    # -------------------------
    # DATA / BUSINESS ANALYTICS
    # -------------------------
    if any(x in title for x in [
        "business intelligence",
        "bi analyst",
        "power bi",
        "tableau analyst"
    ]):
        return "BI Analyst"

    if "product analyst" in title:
        return "Product Analyst"

    if any(x in title for x in [
        "data quality analyst",
        "data operations analyst",
        "data research analyst",
        "data governance analyst",
        "data governance specialist",
        "data verification analyst",
        "data analytics analyst",
        "data analytics intern",
        "data analytic"
    ]):
        return "Data Analyst"

    if "business systems analyst" in title or "business system analyst" in title:
        return "Business Systems Analyst"

    if "business analyst" in title or "business analysis" in title:
        return "Business Analyst"

    if any(x in title for x in [
        "data analyst",
        "mis analyst",
        "mis executive",
        "mis reporting",
        "reporting analyst"
    ]):
        return "Data Analyst"

    # -------------------------
    # CLOUD / DEVOPS
    # -------------------------
    if any(x in title for x in [
        "devops",
        "site reliability",
        "sre engineer",
        "cloud engineer",
        "cloud architect",
        "azure administrator",
        "cloud supply chain",
        "platform engineer"
    ]):
        return "Cloud / DevOps"

    # -------------------------
    # ARCHITECTURE
    # -------------------------
    if any(x in title for x in [
        "solution architect",
        "solutions architect",
        "software architect",
        "technology architect",
        "technical architect",
        "data solution architect",
        "data architect",
        "big data solution architect"
    ]):
        return "Solutions Architect"

    # -------------------------
    # FRONTEND
    # -------------------------
    if any(x in title for x in [
        "frontend", "front-end", "front end"
    ]):
        return "Frontend Developer"

    # -------------------------
    # BACKEND
    # -------------------------
    if any(x in title for x in [
        "backend", "back-end", "back end"
    ]):
        return "Backend Developer"

    # -------------------------
    # FULL STACK
    # -------------------------
    if any(x in title for x in [
        "full stack", "full-stack", "fullstack"
    ]):
        return "Full Stack Developer"

    # -------------------------
    # SOFTWARE ENGINEERING
    # -------------------------
    if any(x in title for x in [
        "software engineer",
        "software development engineer",
        "software development",
        "software developer"
    ]):
        return "Software Engineer"

    # -------------------------
    # PYTHON
    # -------------------------
    if any(x in title for x in [
        "python developer",
        "python engineer"
    ]):
        return "Python Developer"

    # -------------------------
    # JAVA
    # -------------------------
    if "java developer" in title or "java engineer" in title:
        return "Java Developer"

    # -------------------------
    # .NET
    # -------------------------
    if any(x in title for x in [
        ".net developer",
        "dotnet developer",
        "c# developer"
    ]):
        return ".NET Developer"

    # -------------------------
    # GENERIC ENGINEERING
    # -------------------------
    if any(x in title for x in [
        "principal engineer",
        "staff engineer",
        "lead engineer",
        "engineering lead",
        "technical lead",
        "senior engineer"
    ]):
        return "Software Engineer"

    # -------------------------
    # PRODUCT
    # -------------------------
    if any(x in title for x in [
        "product manager",
        "product owner"
    ]):
        return "Product Manager"

    # -------------------------
    # OTHER
    # -------------------------
    return "Other"


def classify_role_family(role):
    mapping = {
        "Data Scientist": "Data & Analytics",
        "Data Analyst": "Data & Analytics",
        "Business Analyst": "Data & Analytics",
        "Business Systems Analyst": "Data & Analytics",
        "BI Analyst": "Data & Analytics",
        "Product Analyst": "Data & Analytics",
        "Data Quality Analyst": "Data & Analytics",

        "Data Engineer": "Data Engineering",
        "Data Warehouse Engineer": "Data Engineering",
        "Data Integration Engineer": "Data Engineering",
        "Databricks Engineer": "Data Engineering",
        "Data Modeler": "Data Engineering",
        "Data Quality Engineer": "Data Engineering",
        "Data Migration Engineer": "Data Engineering",

        "AI Engineer": "AI & Machine Learning",
        "ML Engineer": "AI & Machine Learning",
        "MLOps Engineer": "AI & Machine Learning",
        "Computer Vision Engineer": "AI & Machine Learning",
        "Prompt Engineer": "AI & Machine Learning",
        "AI Architect": "AI & Machine Learning",

        "Software Engineer": "Software Engineering",
        "Python Developer": "Software Engineering",
        "Java Developer": "Software Engineering",
        ".NET Developer": "Software Engineering",
        "Frontend Developer": "Software Engineering",
        "Backend Developer": "Software Engineering",
        "Full Stack Developer": "Software Engineering",

        "Cloud / DevOps": "Cloud & DevOps",

        "QA / Testing": "QA & Testing",

        "Solutions Architect": "Architecture",

        "Product Manager": "Product & Business",

        "Other": "Other"
    }

    return mapping.get(role, "Other")


# Create normalized role
df["normalized_role"] = df["job_title"].apply(normalize_role)

# Create broader role family
df["role_family"] = df["normalized_role"].apply(classify_role_family)


# Save
output_path = "data/cleaned/jobs_with_roles.csv"

df.to_csv(output_path, index=False)


# Display results
print("\n" + "=" * 60)
print("ROLE FAMILY DISTRIBUTION")
print("=" * 60)

print(
    df["role_family"]
    .value_counts()
    .to_string()
)

print("\n" + "=" * 60)
print("NORMALIZED ROLE DISTRIBUTION")
print("=" * 60)

print(
    df["normalized_role"]
    .value_counts()
    .to_string()
)

print("\n" + "=" * 60)
print(f"Total jobs: {len(df):,}")
print(f"Unique normalized roles: {df['normalized_role'].nunique()}")
print(f"Output saved to: {output_path}")
print("=" * 60)