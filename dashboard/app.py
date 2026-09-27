import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Tech Job Market Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# COLOR PALETTE
# ============================================================

COLORS = {
    "coral": "#FF7F6E",
    "lavender": "#A78BFA",
    "mint": "#5EEAD4",
    "amber": "#F6C453",
    "rose": "#F472B6",
    "teal": "#2DD4BF",
    "orange": "#FB923C",
    "green": "#86EFAC",
    "purple": "#C084FC",
    "blue": "#7DD3FC",
}

CHART_TEXT = "#E5E7EB"
MUTED_TEXT = "#9CA3AF"
GRID = "#252B38"
PANEL = "#111722"
PANEL_BORDER = "#28303D"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>

    /* ---------- PAGE ---------- */

    .block-container {{
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        padding-left: 4rem;
        padding-right: 4rem;
        max-width: 1500px;
    }}

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {{
        background: #0B0F17;
        border-right: 1px solid #202631;
    }}

    section[data-testid="stSidebar"] h1 {{
        font-size: 1.35rem;
    }}

    /* ---------- HEADINGS ---------- */

    h1 {{
        letter-spacing: -0.03em;
    }}

    h2, h3 {{
        letter-spacing: -0.02em;
    }}

    /* ---------- METRIC CARDS ---------- */

    div[data-testid="metric-container"] {{
        background: {PANEL};
        border: 1px solid {PANEL_BORDER};
        border-radius: 14px;
        padding: 1rem 1.15rem;
        min-height: 110px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.10);
    }}

    div[data-testid="metric-container"] label {{
        color: {MUTED_TEXT};
    }}

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {{
        font-size: 1.8rem;
        font-weight: 700;
    }}

    /* ---------- SELECT BOX ---------- */

    div[data-baseweb="select"] > div {{
        border-radius: 10px;
    }}

    /* ---------- CAPTIONS ---------- */

    .subtle-text {{
        color: {MUTED_TEXT};
        font-size: 0.92rem;
        line-height: 1.55;
    }}

    /* ---------- TAKEAWAY CARD ---------- */

    .takeaway {{
        background: {PANEL};
        border: 1px solid {PANEL_BORDER};
        border-left: 4px solid {COLORS["mint"]};
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }}

    .takeaway-title {{
        font-weight: 700;
        font-size: 0.98rem;
        margin-bottom: 0.35rem;
    }}

    .takeaway-body {{
        color: #D1D5DB;
        line-height: 1.6;
        font-size: 0.92rem;
    }}

    /* ---------- SIDEBAR FOOTER ---------- */

    .sidebar-note {{
        color: #7F8795;
        font-size: 0.78rem;
        line-height: 1.5;
    }}
    .small-note {{
    color: #9CA3AF;
    font-size: 0.82rem;
    line-height: 1.5;
    padding-top: 8px;
}}

    /* ---------- DIVIDERS ---------- */

    hr {{
        border-color: #202631;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATABASE
# ============================================================

@st.cache_resource
def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Your_Password",
        database="Your_db"
    )


conn = get_connection()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def run_query(query, params=None):

    return pd.read_sql(
        query,
        conn,
        params=params
    )


def section_header(title, description):

    st.header(title)

    st.markdown(
        f'<div class="subtle-text">{description}</div>',
        unsafe_allow_html=True
    )

    st.write("")


def takeaway(text, accent=None):

    if accent is None:
        accent = COLORS["mint"]

    st.markdown(
        f"""
        <div class="takeaway" style="border-left-color:{accent};">
            <div class="takeaway-title">💡 The takeaway</div>
            <div class="takeaway-body">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def style_chart(fig, height=420):

    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color=CHART_TEXT,
            family="Inter, -apple-system, BlinkMacSystemFont, sans-serif"
        ),
        margin=dict(l=10, r=35, t=20, b=20),
        xaxis=dict(
            gridcolor=GRID,
            zeroline=False,
            title_font=dict(color=MUTED_TEXT),
            tickfont=dict(color=MUTED_TEXT)
        ),
        yaxis=dict(
            gridcolor=GRID,
            zeroline=False,
            title_font=dict(color=MUTED_TEXT),
            tickfont=dict(color=MUTED_TEXT)
        )
    )

    return fig


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        font-size:1.35rem;
        font-weight:700;
        margin-bottom:0.25rem;
    ">
        📊 Job Market
    </div>
    <div style="
        color:#9CA3AF;
        font-size:0.82rem;
        line-height:1.45;
    ">
        A closer look at India's tech hiring market
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Explore",
    [
        "🏠 Market Overview",
        "💼 Role Intelligence",
        "🧠 Skill Intelligence",
        "🎓 Fresher Intelligence",
        "💰 Salary Intelligence"
    ],
    label_visibility="visible"
)

st.sidebar.divider()

st.sidebar.markdown(
    """
    <div class="sidebar-note">
        <b>Dataset</b><br>
        India Tech Job Market 2026<br><br>

        23K+ job postings<br>
        37 tracked skills
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MARKET OVERVIEW
# ============================================================

if page == "🏠 Market Overview":

    st.title("📊 Tech Job Market Intelligence")

    st.markdown(
        """
        **What does the current tech job market actually look like?**
        """
    )

    st.markdown(
        """
        A look at job volume, skills, locations, work arrangements,
        experience levels and salary information across Indian tech
        job postings.
        """
    )

    st.divider()

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    total_jobs = run_query(
        "SELECT COUNT(*) AS total FROM jobs"
    ).iloc[0]["total"]

    total_skills = run_query(
        "SELECT COUNT(DISTINCT skill) AS total FROM job_skills"
    ).iloc[0]["total"]

    fresher_jobs = run_query(
        """
        SELECT COUNT(*) AS total
        FROM jobs
        WHERE is_fresher_friendly = TRUE
        """
    ).iloc[0]["total"]

    salary_jobs = run_query(
        """
        SELECT COUNT(*) AS total
        FROM jobs
        WHERE salary_disclosed = TRUE
        """
    ).iloc[0]["total"]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📊 Job postings",
        f"{total_jobs:,}"
    )

    col2.metric(
        "🧠 Skills tracked",
        f"{total_skills}"
    )

    col3.metric(
        "🎓 Fresher-friendly",
        f"{fresher_jobs:,}"
    )

    col4.metric(
        "💰 Salary disclosed",
        f"{salary_jobs:,}"
    )

    st.divider()

    # --------------------------------------------------------
    # ROLE FAMILY
    # --------------------------------------------------------

    section_header(
        "Where the jobs are",
        "Job postings grouped into the main technical role families."
    )

    role_df = run_query(
        """
        SELECT
            role_family,
            COUNT(*) AS job_count
        FROM jobs
        WHERE role_family <> 'Other'
        GROUP BY role_family
        ORDER BY job_count DESC
        """
    )

    fig_role = px.bar(
        role_df.sort_values("job_count"),
        x="job_count",
        y="role_family",
        orientation="h",
        text="job_count"
    )

    fig_role.update_traces(
        marker_color=COLORS["coral"],
        texttemplate="%{text:,}",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Job postings: %{x:,}"
            "<extra></extra>"
        )
    )

    fig_role.update_layout(
        xaxis_title="Job postings",
        yaxis_title="",
        showlegend=False,
        yaxis=dict(categoryorder="total ascending")
    )

    style_chart(fig_role, 450)

    st.plotly_chart(
        fig_role,
        use_container_width=True
    )

    takeaway(
        "Data & Analytics makes up the largest share of the technical "
        "roles in this dataset, followed by Data Engineering and "
        "Software Engineering.",
        COLORS["coral"]
    )

    # --------------------------------------------------------
    # WORK MODE + LOCATIONS
    # --------------------------------------------------------

    col1, col2 = st.columns([1, 1.5])

    with col1:

        st.subheader("🏢 How are people expected to work?")

        work_df = run_query(
            """
            SELECT
                work_mode,
                COUNT(*) AS job_count
            FROM jobs
            GROUP BY work_mode
            ORDER BY job_count DESC
            """
        )

        fig_work = px.pie(
            work_df,
            names="work_mode",
            values="job_count",
            hole=0.58,
            color_discrete_sequence=[
                COLORS["coral"],
                COLORS["mint"],
                COLORS["lavender"]
            ]
        )

        fig_work.update_traces(
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Jobs: %{value:,}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )

        style_chart(fig_work, 400)

        fig_work.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                y=-0.08
            )
        )

        st.plotly_chart(
            fig_work,
            use_container_width=True
        )

    with col2:

        st.subheader("📍 Where are the jobs concentrated?")

        city_df = run_query(
            """
            SELECT
                primary_city,
                COUNT(*) AS job_count
            FROM jobs
            WHERE primary_city IS NOT NULL
            GROUP BY primary_city
            ORDER BY job_count DESC
            LIMIT 10
            """
        )

        fig_city = px.bar(
            city_df.sort_values("job_count"),
            x="job_count",
            y="primary_city",
            orientation="h",
            text="job_count"
        )

        fig_city.update_traces(
            marker_color=COLORS["mint"],
            texttemplate="%{text:,}",
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Job postings: %{x:,}"
                "<extra></extra>"
            )
        )

        fig_city.update_layout(
            xaxis_title="Job postings",
            yaxis_title="",
            showlegend=False,
            yaxis=dict(categoryorder="total ascending")
        )

        style_chart(fig_city, 400)

        st.plotly_chart(
            fig_city,
            use_container_width=True
        )


# ============================================================
# ROLE INTELLIGENCE
# ============================================================

elif page == "💼 Role Intelligence":

    section_header(
        "💼 Role Intelligence",
        "Pick a role family and see the skills and experience levels that show up most often."
    )

    # --------------------------------------------------------
    # ROLE SELECTOR
    # --------------------------------------------------------

    role_family_df = run_query(
        """
        SELECT DISTINCT role_family
        FROM jobs
        WHERE role_family <> 'Other'
        ORDER BY role_family
        """
    )

    selected_role = st.selectbox(
        "Role family",
        role_family_df["role_family"].tolist()
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    role_summary = run_query(
        """
        SELECT
            COUNT(*) AS total_jobs,
            ROUND(AVG(experience_min_yrs), 1) AS avg_min_experience,
            SUM(is_fresher_friendly) AS fresher_jobs
        FROM jobs
        WHERE role_family = %s
        """,
        params=(selected_role,)
    ).iloc[0]

    total_role_jobs = int(role_summary["total_jobs"])
    fresher_role_jobs = int(role_summary["fresher_jobs"])

    fresher_share = (
        fresher_role_jobs / total_role_jobs * 100
        if total_role_jobs
        else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📌 Job postings",
        f"{total_role_jobs:,}"
    )

    col2.metric(
        "⏳ Avg. minimum experience",
        f"{role_summary['avg_min_experience']:.1f} yrs"
    )

    col3.metric(
        "🎓 Fresher-friendly",
        f"{fresher_share:.1f}%"
    )

    st.divider()

    # --------------------------------------------------------
    # TOP SKILLS
    # --------------------------------------------------------

    st.subheader("🧠 Skills that show up most often")

    st.markdown(
        '<div class="subtle-text">Share of postings mentioning each tracked skill.</div>',
        unsafe_allow_html=True
    )

    skill_df = run_query(
        """
        SELECT
            s.skill,
            COUNT(DISTINCT s.job_id) AS job_count,
            ROUND(
                COUNT(DISTINCT s.job_id) * 100.0 /
                (
                    SELECT COUNT(*)
                    FROM jobs
                    WHERE role_family = %s
                ),
                2
            ) AS demand_pct
        FROM jobs j
        JOIN job_skills s
            ON j.job_id = s.job_id
        WHERE j.role_family = %s
        GROUP BY s.skill
        ORDER BY demand_pct DESC
        LIMIT 10
        """,
        params=(selected_role, selected_role)
    )

    sorted_skill_df = skill_df.sort_values("demand_pct")

    fig_skills = px.bar(
        sorted_skill_df,
        x="demand_pct",
        y="skill",
        orientation="h",
        text="demand_pct"
    )

    fig_skills.update_traces(
        marker_color=COLORS["lavender"],
        texttemplate="%{text:.1f}%",
        textposition="outside",
        customdata=sorted_skill_df[["job_count"]],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Mentioned in: %{x:.2f}% of postings<br>"
            "Job postings: %{customdata[0]:,}"
            "<extra></extra>"
        )
    )

    fig_skills.update_layout(
        xaxis_title="Share of postings",
        yaxis_title="",
        showlegend=False
    )

    style_chart(fig_skills, 500)

    st.plotly_chart(
        fig_skills,
        use_container_width=True
    )

    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    st.subheader("📈 Experience levels")

    experience_df = run_query(
        """
        SELECT
            experience_tier,
            COUNT(*) AS job_count
        FROM jobs
        WHERE role_family = %s
        GROUP BY experience_tier
        ORDER BY job_count DESC
        """,
        params=(selected_role,)
    )

    fig_experience = px.bar(
        experience_df,
        x="experience_tier",
        y="job_count",
        text="job_count",
        color="experience_tier",
        color_discrete_sequence=[
            COLORS["mint"],
            COLORS["lavender"],
            COLORS["amber"],
            COLORS["coral"],
            COLORS["rose"]
        ]
    )

    fig_experience.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Job postings: %{y:,}"
            "<extra></extra>"
        )
    )

    fig_experience.update_layout(
        xaxis_title="Experience level",
        yaxis_title="Job postings",
        showlegend=False
    )

    style_chart(fig_experience, 400)

    st.plotly_chart(
        fig_experience,
        use_container_width=True
    )

    # --------------------------------------------------------
    # TAKEAWAY
    # --------------------------------------------------------

    top_skill = skill_df.iloc[0]["skill"]
    top_skill_pct = skill_df.iloc[0]["demand_pct"]

    takeaway(
        f"<b>{top_skill}</b> is the most frequently mentioned tracked "
        f"skill for <b>{selected_role}</b>, appearing in "
        f"<b>{top_skill_pct:.1f}%</b> of postings in this dataset.",
        COLORS["lavender"]
    )


# ============================================================
# SKILL INTELLIGENCE
# ============================================================

elif page == "🧠 Skill Intelligence":


    st.title("🧠 Skills people are actually hiring for")
    st.markdown(
        """
        <div class="subtle">
        A closer look at the skills appearing across Indian tech job postings —
        and how their demand changes from one role family to another.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 1. OVERALL SKILL DEMAND
    # ---------------------------------------------------------

    section_header(
        "What shows up most often?",
        "Percentage of non-'Other' tech postings mentioning each tracked skill."
    )

    skill_demand = run_query("""
        SELECT
            s.skill,
            COUNT(DISTINCT s.job_id) AS job_count,
            ROUND(
                COUNT(DISTINCT s.job_id) * 100.0 /
                (
                    SELECT COUNT(*)
                    FROM jobs
                    WHERE role_family <> 'Other'
                ),
                2
            ) AS demand_pct
        FROM job_skills s
        JOIN jobs j
            ON s.job_id = j.job_id
        WHERE j.role_family <> 'Other'
        GROUP BY s.skill
        ORDER BY job_count DESC
        LIMIT 15;
    """)

    if not skill_demand.empty:

        fig = px.bar(
            skill_demand.sort_values("demand_pct"),
            x="demand_pct",
            y="skill",
            orientation="h",
            text="demand_pct",
            color="demand_pct",
            color_continuous_scale=[
                "#312E81",
                "#7C3AED",
                "#A78BFA",
                "#5EEAD4",
                "#F6C453"
            ],
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Demand: %{x:.2f}%<br>"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            height=560,
            coloraxis_showscale=False,
            xaxis_title="Share of tech postings (%)",
            yaxis_title="",
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

        top_skill = skill_demand.iloc[0]["skill"]
        top_pct = skill_demand.iloc[0]["demand_pct"]

        takeaway(
            f"<b>{top_skill}</b> appears most often in the tracked skill set, "
            f"showing up in <b>{top_pct:.1f}%</b> of the tech postings in this analysis."
        )

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 2. ROLE × SKILL HEATMAP
    # ---------------------------------------------------------

    section_header(
        "The skill mix changes by role",
        "Compare how frequently the same skills appear across different role families."
    )

    heatmap_data = run_query("""
        SELECT
            j.role_family,
            s.skill,
            COUNT(DISTINCT s.job_id) AS job_count,
            ROUND(
                COUNT(DISTINCT s.job_id) * 100.0 /
                (
                    SELECT COUNT(*)
                    FROM jobs j2
                    WHERE j2.role_family = j.role_family
                ),
                2
            ) AS demand_pct
        FROM jobs j
        JOIN job_skills s
            ON j.job_id = s.job_id
        WHERE j.role_family <> 'Other'
        GROUP BY
            j.role_family,
            s.skill
        ORDER BY
            j.role_family,
            demand_pct DESC;
    """)

    if not heatmap_data.empty:

        # Pick the 12 most frequently occurring skills overall
        top_heatmap_skills = (
            heatmap_data
            .groupby("skill")["job_count"]
            .sum()
            .sort_values(ascending=False)
            .head(12)
            .index
            .tolist()
        )

        heatmap_filtered = heatmap_data[
            heatmap_data["skill"].isin(top_heatmap_skills)
        ].copy()

        heatmap_pivot = heatmap_filtered.pivot(
            index="role_family",
            columns="skill",
            values="demand_pct"
        ).fillna(0)

        # Order rows by total role size
        role_order = [
            "Data & Analytics",
            "Data Engineering",
            "Software Engineering",
            "AI & Machine Learning",
            "QA & Testing",
            "Architecture",
            "Cloud & DevOps",
            "Product & Business"
        ]

        role_order = [
            role for role in role_order
            if role in heatmap_pivot.index
        ]

        heatmap_pivot = heatmap_pivot.reindex(role_order)

        fig = px.imshow(
            heatmap_pivot,
            text_auto=".1f",
            aspect="auto",
            color_continuous_scale=[
                "#171528",
                "#312E81",
                "#7C3AED",
                "#A78BFA",
                "#5EEAD4"
            ],
            labels={
                "x": "Skill",
                "y": "Role family",
                "color": "Demand %"
            }
        )

        fig.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Skill: %{x}<br>"
                "Mentioned in: %{z:.2f}% of postings"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            height=560,
            xaxis_title="",
            yaxis_title="",
            coloraxis_colorbar_title="Demand %"
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            <div class="small-note">
            💡 Each cell represents the percentage of postings within that role
            family that mention the skill. A role can mention multiple skills,
            so percentages do not add up to 100%.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 3. SKILL DEEP DIVE
    # ---------------------------------------------------------

    section_header(
        "Pick a skill",
        "See where a particular skill appears most often across the market."
    )

    available_skills = skill_demand["skill"].tolist()

    selected_skill = st.selectbox(
        "Choose a skill to explore",
        available_skills,
        index=0
    )

    skill_detail = run_query(
        f"""
        SELECT
            j.role_family,
            COUNT(DISTINCT j.job_id) AS job_count,
            ROUND(
                COUNT(DISTINCT j.job_id) * 100.0 /
                (
                    SELECT COUNT(*)
                    FROM jobs j2
                    WHERE j2.role_family = j.role_family
                ),
                2
            ) AS demand_pct
        FROM jobs j
        JOIN job_skills s
            ON j.job_id = s.job_id
        WHERE
            j.role_family <> 'Other'
            AND s.skill = '{selected_skill}'
        GROUP BY j.role_family
        ORDER BY demand_pct DESC;
        """
    )

    if not skill_detail.empty:

        col1, col2 = st.columns([1.2, 2])

        with col1:

            total_mentions = int(skill_detail["job_count"].sum())

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">JOBS MENTIONING THIS SKILL</div>
                    <div class="metric-value">{total_mentions:,}</div>
                    <div class="metric-caption">
                        Across the tracked tech role families
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            fig = px.bar(
                skill_detail.sort_values("demand_pct"),
                x="demand_pct",
                y="role_family",
                orientation="h",
                text="demand_pct",
                color="role_family",
                color_discrete_sequence=[
                    COLORS["coral"],
                    COLORS["lavender"],
                    COLORS["mint"],
                    COLORS["amber"],
                    COLORS["rose"],
                    COLORS["orange"],
                    COLORS["teal"],
                    COLORS["purple"],
                ]
            )

            fig.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Demand: %{x:.2f}%<br>"
                    "<extra></extra>"
                )
            )

            fig.update_layout(
                height=420,
                xaxis_title="Share of postings (%)",
                yaxis_title="",
                showlegend=False
            )

            style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)

        top_role = skill_detail.iloc[0]["role_family"]
        top_role_pct = skill_detail.iloc[0]["demand_pct"]

        takeaway(
            f"<b>{selected_skill}</b> appears most frequently within "
            f"<b>{top_role}</b>, where it is mentioned in "
            f"<b>{top_role_pct:.1f}%</b> of postings."
        )


# ============================================================
# FRESHER INTELLIGENCE
# ============================================================

elif page == "🎓 Fresher Intelligence":

    st.title("🎓 What does the market ask from freshers?")
    st.markdown(
        """
        <div class="subtle">
        A closer look at fresher-friendly postings — the roles, skills and
        patterns that show up when experience requirements are lower.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

    # =========================================================
    # 1. MARKET SNAPSHOT
    # =========================================================

    section_header(
        "How big is the fresher market?",
        "Fresher-friendly postings compared with the rest of the dataset."
    )

    fresher_summary = run_query("""
        SELECT
            SUM(CASE WHEN is_fresher_friendly = TRUE THEN 1 ELSE 0 END)
                AS fresher_jobs,
            SUM(CASE WHEN is_fresher_friendly = FALSE THEN 1 ELSE 0 END)
                AS other_jobs,
            COUNT(*) AS total_jobs
        FROM jobs
        WHERE role_family <> 'Other';
    """)

    if not fresher_summary.empty:

        fresher_jobs = int(fresher_summary.iloc[0]["fresher_jobs"])
        other_jobs = int(fresher_summary.iloc[0]["other_jobs"])
        total_jobs = int(fresher_summary.iloc[0]["total_jobs"])

        fresher_pct = fresher_jobs / total_jobs * 100
        other_pct = other_jobs / total_jobs * 100

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">FRESHER-FRIENDLY</div>
                    <div class="metric-value">{fresher_jobs:,}</div>
                    <div class="metric-caption">
                        {fresher_pct:.1f}% of tracked tech postings
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">OTHER POSTINGS</div>
                    <div class="metric-value">{other_jobs:,}</div>
                    <div class="metric-caption">
                        {other_pct:.1f}% of tracked tech postings
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">TOTAL TECH POSTINGS</div>
                    <div class="metric-value">{total_jobs:,}</div>
                    <div class="metric-caption">
                        Excluding unclassified roles
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

    # =========================================================
    # 2. FRESHER-FRIENDLY SHARE BY ROLE FAMILY
    # =========================================================

    section_header(
        "Where do fresher-friendly openings show up?",
        "Share of postings within each role family marked as fresher-friendly."
    )

    role_fresher = run_query("""
        SELECT
            role_family,
            COUNT(*) AS total_jobs,
            SUM(
                CASE
                    WHEN is_fresher_friendly = TRUE THEN 1
                    ELSE 0
                END
            ) AS fresher_jobs,
            ROUND(
                SUM(
                    CASE
                        WHEN is_fresher_friendly = TRUE THEN 1
                        ELSE 0
                    END
                ) * 100.0 / COUNT(*),
                2
            ) AS fresher_share_pct
        FROM jobs
        WHERE role_family <> 'Other'
        GROUP BY role_family
        HAVING COUNT(*) >= 100
        ORDER BY fresher_share_pct DESC;
    """)

    if not role_fresher.empty:

        fig = px.bar(
            role_fresher.sort_values("fresher_share_pct"),
            x="fresher_share_pct",
            y="role_family",
            orientation="h",
            text="fresher_share_pct",
            color="fresher_share_pct",
            color_continuous_scale=[
                "#312E81",
                "#7C3AED",
                "#A78BFA",
                "#5EEAD4",
                "#F6C453"
            ]
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Fresher-friendly: %{x:.2f}%<br>"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            height=470,
            coloraxis_showscale=False,
            xaxis_title="Fresher-friendly share (%)",
            yaxis_title=""
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

        top_role = role_fresher.iloc[0]["role_family"]
        top_share = role_fresher.iloc[0]["fresher_share_pct"]

        takeaway(
            f"<b>{top_role}</b> has the highest fresher-friendly share among "
            f"the role families shown, at <b>{top_share:.1f}%</b>."
        )

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

    # =========================================================
    # 3. WHICH SKILLS DIFFER MOST?
    # =========================================================

    section_header(
        "Which skills stand out in fresher-friendly jobs?",
        "The difference in skill demand between fresher-friendly and other postings."
    )

    skill_comparison = run_query("""
        SELECT
            s.skill,

            COUNT(
                DISTINCT CASE
                    WHEN j.is_fresher_friendly = TRUE
                    THEN j.job_id
                END
            ) AS fresher_jobs,

            COUNT(
                DISTINCT CASE
                    WHEN j.is_fresher_friendly = FALSE
                    THEN j.job_id
                END
            ) AS other_jobs,

            ROUND(
                COUNT(
                    DISTINCT CASE
                        WHEN j.is_fresher_friendly = TRUE
                        THEN j.job_id
                    END
                ) * 100.0
                /
                NULLIF(
                    (
                        SELECT COUNT(*)
                        FROM jobs
                        WHERE
                            role_family <> 'Other'
                            AND is_fresher_friendly = TRUE
                    ),
                    0
                ),
                2
            ) AS fresher_demand_pct,

            ROUND(
                COUNT(
                    DISTINCT CASE
                        WHEN j.is_fresher_friendly = FALSE
                        THEN j.job_id
                    END
                ) * 100.0
                /
                NULLIF(
                    (
                        SELECT COUNT(*)
                        FROM jobs
                        WHERE
                            role_family <> 'Other'
                            AND is_fresher_friendly = FALSE
                    ),
                    0
                ),
                2
            ) AS other_demand_pct

        FROM jobs j
        JOIN job_skills s
            ON j.job_id = s.job_id

        WHERE j.role_family <> 'Other'

        GROUP BY s.skill
        ORDER BY
            ABS(
                (
                    fresher_demand_pct
                    - other_demand_pct
                )
            ) DESC
        LIMIT 15;
    """)

    if not skill_comparison.empty:

        skill_comparison["difference_pp"] = (
            skill_comparison["fresher_demand_pct"]
            - skill_comparison["other_demand_pct"]
        )

        chart_data = skill_comparison.sort_values("difference_pp")

        fig = px.bar(
            chart_data,
            x="difference_pp",
            y="skill",
            orientation="h",
            text="difference_pp",
            color="difference_pp",
            color_continuous_scale=[
                "#F472B6",
                "#312E81",
                "#5EEAD4"
            ],
            color_continuous_midpoint=0
        )

        fig.update_traces(
            texttemplate="%{text:+.1f} pp",
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Fresher-friendly: %{customdata[0]:.2f}%<br>"
                "Other postings: %{customdata[1]:.2f}%<br>"
                "Difference: %{x:+.2f} pp"
                "<extra></extra>"
            ),
            customdata=chart_data[
                [
                    "fresher_demand_pct",
                    "other_demand_pct"
                ]
            ]
        )

        fig.update_layout(
            height=560,
            coloraxis_showscale=False,
            xaxis_title="Difference in demand (percentage points)",
            yaxis_title=""
        )

        # Add a zero reference line
        fig.add_vline(
            x=0,
            line_width=1,
            line_dash="dash"
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

        strongest_positive = skill_comparison.sort_values(
            "difference_pp",
            ascending=False
        ).iloc[0]

        strongest_negative = skill_comparison.sort_values(
            "difference_pp",
            ascending=True
        ).iloc[0]

        takeaway(
            f"<b>{strongest_positive['skill']}</b> shows the largest positive "
            f"difference in this comparison at "
            f"<b>+{strongest_positive['difference_pp']:.1f} percentage points</b>. "
            f"<br><br>"
            f"At the other end, <b>{strongest_negative['skill']}</b> appears "
            f"more often in non-fresher-friendly postings."
        )

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

    # =========================================================
    # 4. EXPERIENCE MIX
    # =========================================================

    section_header(
        "What experience level is being requested?",
        "Experience tiers across the tracked tech job market."
    )

    experience_data = run_query("""
        SELECT
            experience_tier,
            COUNT(*) AS job_count
        FROM jobs
        WHERE role_family <> 'Other'
        GROUP BY experience_tier
        ORDER BY job_count DESC;
    """)

    if not experience_data.empty:

        fig = px.pie(
            experience_data,
            names="experience_tier",
            values="job_count",
            hole=0.58,
            color_discrete_sequence=[
                COLORS["coral"],
                COLORS["lavender"],
                COLORS["mint"],
                COLORS["amber"],
                COLORS["rose"]
            ]
        )

        fig.update_traces(
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Jobs: %{value:,}<br>"
                "Share: %{percent}<br>"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            height=440,
            showlegend=True
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            <div class="small-note">
            💡 "Fresher-friendly" is based on the dataset's existing
            classification. It should be read as a property of these postings,
            not as a guarantee that a candidate with no experience will qualify.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# SALARY INTELLIGENCE
# ============================================================

elif page == "💰 Salary Intelligence":

    st.title("💰 What do the disclosed salaries look like?")
    st.markdown(
        """
        <div class="subtle">
        A closer look at salary information disclosed in the job postings —
        across roles, locations and selected skills.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

    # =========================================================
    # IMPORTANT DATA NOTE
    # =========================================================

    st.markdown(
        """
        <div class="small-note">
        ℹ️ Salary analysis uses only postings where salary information was
        disclosed. In this dataset, that is a subset of the overall job market,
        so these figures should be read as patterns within disclosed postings,
        not as market-wide salary estimates.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

    # =========================================================
    # 1. SALARY SNAPSHOT
    # =========================================================

    section_header(
        "The salary picture at a glance",
        "A few numbers from the postings that actually disclose salary."
    )

    salary_summary = run_query("""
        SELECT
            COUNT(*) AS disclosed_jobs,
            ROUND(AVG(salary_min_lpa), 2) AS avg_min_lpa,
            ROUND(AVG(salary_max_lpa), 2) AS avg_max_lpa,
            ROUND(AVG(salary_midpoint_lpa), 2) AS avg_midpoint_lpa
        FROM jobs
        WHERE
            salary_disclosed = TRUE
            AND role_family <> 'Other';
    """)

    total_tech_jobs = run_query("""
        SELECT COUNT(*) AS total_jobs
        FROM jobs
        WHERE role_family <> 'Other';
    """)

    if not salary_summary.empty and not total_tech_jobs.empty:

        disclosed_jobs = int(salary_summary.iloc[0]["disclosed_jobs"])
        avg_min = float(salary_summary.iloc[0]["avg_min_lpa"])
        avg_max = float(salary_summary.iloc[0]["avg_max_lpa"])
        avg_midpoint = float(salary_summary.iloc[0]["avg_midpoint_lpa"])

        total_jobs = int(total_tech_jobs.iloc[0]["total_jobs"])
        disclosure_rate = disclosed_jobs / total_jobs * 100

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">SALARY-DISCLOSED</div>
                    <div class="metric-value">{disclosed_jobs:,}</div>
                    <div class="metric-caption">
                        {disclosure_rate:.1f}% of tracked tech postings
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">AVG. MINIMUM</div>
                    <div class="metric-value">₹{avg_min:.1f}L</div>
                    <div class="metric-caption">
                        Average disclosed lower bound
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">AVG. MIDPOINT</div>
                    <div class="metric-value">₹{avg_midpoint:.1f}L</div>
                    <div class="metric-caption">
                        Average disclosed midpoint
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">AVG. MAXIMUM</div>
                    <div class="metric-value">₹{avg_max:.1f}L</div>
                    <div class="metric-caption">
                        Average disclosed upper bound
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

    # =========================================================
    # 2. SALARY BY ROLE FAMILY
    # =========================================================

    section_header(
        "How does disclosed salary vary by role family?",
        "Average disclosed salary midpoint for role families with enough salary data."
    )

    salary_by_role = run_query("""
        SELECT
            role_family,
            COUNT(*) AS disclosed_jobs,
            ROUND(AVG(salary_midpoint_lpa), 2) AS avg_salary_lpa,
            ROUND(MIN(salary_min_lpa), 2) AS lowest_min_lpa,
            ROUND(MAX(salary_max_lpa), 2) AS highest_max_lpa
        FROM jobs
        WHERE
            salary_disclosed = TRUE
            AND role_family <> 'Other'
        GROUP BY role_family
        HAVING COUNT(*) >= 20
        ORDER BY avg_salary_lpa DESC;
    """)

    if not salary_by_role.empty:

        fig = px.bar(
            salary_by_role.sort_values("avg_salary_lpa"),
            x="avg_salary_lpa",
            y="role_family",
            orientation="h",
            text="avg_salary_lpa",
            color="role_family",
            color_discrete_sequence=[
                COLORS["coral"],
                COLORS["lavender"],
                COLORS["mint"],
                COLORS["amber"],
                COLORS["rose"],
                COLORS["orange"],
                COLORS["teal"],
                COLORS["purple"],
            ]
        )

        fig.update_traces(
            texttemplate="₹%{text:.1f}L",
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Average disclosed midpoint: ₹%{x:.2f}L<br>"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            height=500,
            xaxis_title="Average disclosed salary midpoint (LPA)",
            yaxis_title="",
            showlegend=False
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

        highest_salary_role = salary_by_role.iloc[0]["role_family"]
        highest_salary_value = salary_by_role.iloc[0]["avg_salary_lpa"]

        takeaway(
            f"Among role families with at least 20 salary-disclosed postings, "
            f"<b>{highest_salary_role}</b> has the highest average disclosed "
            f"salary midpoint at <b>₹{highest_salary_value:.1f} LPA</b>."
        )

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

    # =========================================================
    # 3. SALARY BY CITY
    # =========================================================

    section_header(
        "What does disclosed salary look like by location?",
        "Average disclosed salary midpoint in the cities with enough observations."
    )

    salary_by_city = run_query("""
        SELECT
            primary_city,
            COUNT(*) AS disclosed_jobs,
            ROUND(AVG(salary_midpoint_lpa), 2) AS avg_salary_lpa
        FROM jobs
        WHERE
            salary_disclosed = TRUE
            AND role_family <> 'Other'
            AND primary_city IS NOT NULL
            AND primary_city <> 'Remote'
        GROUP BY primary_city
        HAVING COUNT(*) >= 20
        ORDER BY avg_salary_lpa DESC
        LIMIT 12;
    """)

    if not salary_by_city.empty:

        fig = px.bar(
            salary_by_city.sort_values("avg_salary_lpa"),
            x="avg_salary_lpa",
            y="primary_city",
            orientation="h",
            text="avg_salary_lpa",
            color="avg_salary_lpa",
            color_continuous_scale=[
                "#312E81",
                "#7C3AED",
                "#A78BFA",
                "#5EEAD4",
                "#F6C453"
            ]
        )

        fig.update_traces(
            texttemplate="₹%{text:.1f}L",
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Average disclosed midpoint: ₹%{x:.2f}L<br>"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            height=470,
            coloraxis_showscale=False,
            xaxis_title="Average disclosed salary midpoint (LPA)",
            yaxis_title=""
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            <div class="small-note">
            📍 Location comparisons can also reflect differences in role mix,
            experience requirements and the kinds of jobs that disclose salary.
            They should not be interpreted as a pure location effect.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

    # =========================================================
    # 4. SKILL-ASSOCIATED SALARY
    # =========================================================

    section_header(
        "Do some skills appear alongside higher disclosed salaries?",
        "Compare disclosed salary among postings within a selected role family."
    )

    role_options = [
        role for role in [
            "Data & Analytics",
            "Data Engineering",
            "AI & Machine Learning",
            "Software Engineering",
            "QA & Testing",
            "Architecture",
            "Cloud & DevOps",
            "Product & Business"
        ]
        if not salary_by_role.empty
        and role in salary_by_role["role_family"].tolist()
    ]

    if role_options:

        selected_salary_role = st.selectbox(
            "Choose a role family",
            role_options
        )

        role_skill_salary = run_query(
            f"""
            SELECT
                s.skill,
                COUNT(DISTINCT j.job_id) AS disclosed_jobs,
                ROUND(AVG(j.salary_midpoint_lpa), 2) AS avg_salary_lpa
            FROM jobs j
            JOIN job_skills s
                ON j.job_id = s.job_id
            WHERE
                j.salary_disclosed = TRUE
                AND j.role_family = '{selected_salary_role}'
            GROUP BY s.skill
            HAVING COUNT(DISTINCT j.job_id) >= 5
            ORDER BY avg_salary_lpa DESC;
            """
        )

        baseline_salary = run_query(
            f"""
            SELECT
                ROUND(AVG(salary_midpoint_lpa), 2) AS baseline_salary
            FROM jobs
            WHERE
                salary_disclosed = TRUE
                AND role_family = '{selected_salary_role}';
            """
        )

        if not role_skill_salary.empty and not baseline_salary.empty:

            baseline = float(
                baseline_salary.iloc[0]["baseline_salary"]
            )

            role_skill_salary["difference_lpa"] = (
                role_skill_salary["avg_salary_lpa"] - baseline
            )

            chart_data = (
                role_skill_salary
                .sort_values("difference_lpa")
                .tail(12)
            )

            fig = px.bar(
                chart_data,
                x="difference_lpa",
                y="skill",
                orientation="h",
                text="difference_lpa",
                color="difference_lpa",
                color_continuous_scale=[
                    "#F472B6",
                    "#312E81",
                    "#5EEAD4"
                ],
                color_continuous_midpoint=0
            )

            fig.update_traces(
                texttemplate="%{text:+.1f}L",
                textposition="outside",
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Average disclosed salary: ₹%{customdata[0]:.2f}L<br>"
                    "Role baseline: ₹%{customdata[1]:.2f}L<br>"
                    "Difference: ₹%{x:+.2f}L"
                    "<extra></extra>"
                ),
                customdata=chart_data[
                    ["avg_salary_lpa"]
                ].assign(
                    role_baseline=baseline
                )[
                    ["avg_salary_lpa", "role_baseline"]
                ].values
            )

            fig.add_vline(
                x=0,
                line_width=1,
                line_dash="dash"
            )

            fig.update_layout(
                height=500,
                coloraxis_showscale=False,
                xaxis_title="Difference from role-family average (LPA)",
                yaxis_title=""
            )

            style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)

            top_skill = chart_data.iloc[-1]["skill"]
            top_difference = chart_data.iloc[-1]["difference_lpa"]

            takeaway(
                f"Within <b>{selected_salary_role}</b>, postings mentioning "
                f"<b>{top_skill}</b> have the largest positive salary difference "
                f"in this comparison: <b>+₹{top_difference:.1f} LPA</b> versus "
                f"the role-family average."
            )

            st.markdown(
                """
                <div class="small-note">
                ⚠️ This is an association within salary-disclosed postings,
                not evidence that the skill itself causes higher pay. Differences
                can also reflect experience, seniority, company, role scope and
                other factors.
                </div>
                """,
                unsafe_allow_html=True
            )