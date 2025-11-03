import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
from scipy import stats
from io import BytesIO
from datetime import datetime
import time
from functools import reduce

warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION & THEMING
# ============================================================================
st.set_page_config(
    page_title="Football Injury Impact Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Set dark theme
st.markdown("""
    <style>
        /* Dark theme colors */
        :root {
            --bg-color: #0f1729;
            --secondary-bg-color: #1a2234;
            --text-color: #e6e7ee;
            --secondary-text-color: #a0aec0;
            --accent-color: #4361ee;
            --accent-color-2: #3a0ca3;
            --success-color: #4cc9f0;
            --danger-color: #f72585;
            --warning-color: #7209b7;
        }
        
        /* Main background */
        .stApp {
            background-color: var(--bg-color);
            color: var(--text-color);
        }
        
        /* Streamlit elements */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stMultiSelect > div > div > div {
            background-color: var(--secondary-bg-color) !important;
            color: var(--text-color) !important;
            border-color: rgba(67, 97, 238, 0.2) !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stMultiSelect > div > div > div:focus {
            border-color: var(--accent-color) !important;
            box-shadow: 0 0 0 1px var(--accent-color) !important;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-color) !important;
        }
        
        /* Plotly charts background */
        .js-plotly-plot .plotly .main-svg {
            background-color: var(--secondary-bg-color) !important;
        }
        
        /* Dataframe styling */
        .dataframe {
            background-color: var(--secondary-bg-color) !important;
            color: var(--text-color) !important;
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            color: var(--accent-color) !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, var(--accent-color), var(--accent-color-2)) !important;
            color: white !important;
            border: none !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(67, 97, 238, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

# Modern theme colors
PRIMARY_COLOR = "#4361ee"    # Modern blue
SECONDARY_COLOR = "#3a0ca3"  # Deep purple
SUCCESS_COLOR = "#4cc9f0"    # Bright cyan
DANGER_COLOR = "#f72585"     # Vibrant pink
WARNING_COLOR = "#7209b7"    # Rich purple
INFO_COLOR = "#4895ef"       # Light blue

# ============================================================================
# DASHBOARD STYLING
# ============================================================================

# ============================================================================
# PROFESSIONAL MINIMALIST STYLING - CLEAN DESIGN
# ============================================================================
st.markdown("""
    <style>
    .main-header {
        font-family: sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        color: white;
        text-shadow: 2px 2px 12px rgba(0,0,0,0.3);
        margin: 25px 0 15px 0;
        padding: 28px;
        background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
        border-radius: 20px;
        text-align: center;
        letter-spacing: 1.2px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    /* Sub Header - Simple, No Box */
    .sub-header {{
        background: none !important;
        color: #868e96 !important;
        text-align: center !important;
        font-weight: 430 !important;
        font-size: 1.13rem !important;
        margin-top: 10px;
        margin-bottom: 14px !important;
        border: 0 !important;
        padding: 0 !important;
        box-shadow: none !important;
    }}
    
    /* Tab Header */
    .tab-header {{
        font-size: 1.85rem;
        font-weight: bold;
        color: #212529;
        margin: 30px 0 15px 0;
        border-bottom: 2px solid #ff7f0e;
        padding-bottom: 10px;
    }}
    
    /* Question Box */
    .question-box {{
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        background: linear-gradient(135deg, #d62728 0%, #ff9896 100%);
        padding: 20px 25px;
        margin: 22px 0 16px 0;
        border-radius: 11px;
        border-left: 8px solid #ff7f0e;
    }}
    
    /* Answer/Insight Boxes - Clean, Readable */
    .answer-box, .insight-box {{
        background: #f9fcff !important;
        color: #222 !important;
        font-weight: 600;
        border-radius: 13px;
        border-left: 4px solid #3498db;
        margin: 12px 0 18px 0 !important;
        padding: 17px 20px 15px 20px !important;
        box-shadow: none !important;
    }}
    
    /* Stat Highlight */
    .stat-highlight {{
        display: inline-block;
        background: #e2f2fc !important;
        color: #174066 !important;
        padding: 9px 14px 7px 14px;
        border-radius: 7px;
        font-size: 1.17rem;
        margin-right: 10px;
        font-weight: bold;
    }}
    
    /* Footer - Simple, Elegant */
    .footer {
        background: linear-gradient(135deg, rgba(67, 97, 238, 0.05), rgba(58, 12, 163, 0.05)) !important;
        color: #4361ee !important;
        border-radius: 15px !important;
        padding: 25px !important;
        text-align: center !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        border: 1px solid rgba(67, 97, 238, 0.1) !important;
        font-size: 1rem !important;
        margin: 40px 0 20px 0 !important;
        backdrop-filter: blur(10px) !important;
        line-height: 1.6 !important;
    }
    
    /* Metric Cards */
    .metric-card {{
        background: linear-gradient(135deg, #f0f2f6 0%, #e8eef7 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid {PRIMARY_COLOR};
        box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    }}
    
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & ADVANCED PREPROCESSING
# ============================================================================
@st.cache_data
def load_and_preprocess_data():
    """
    Advanced data preprocessing pipeline with comprehensive feature engineering.
    """
    try:
        df = pd.read_csv('player_injuries_impact.csv')
        
        # Date processing
        df['Date of Injury'] = pd.to_datetime(df['Date of Injury'], errors='coerce')
        df['Date of return'] = pd.to_datetime(df['Date of return'], errors='coerce')
        
        df['Injury_Duration_Days'] = (df['Date of return'] - df['Date of Injury']).dt.days
        df['Injury_Duration_Days'] = df['Injury_Duration_Days'].fillna(df['Injury_Duration_Days'].median())
        
        df['Injury_Month'] = df['Date of Injury'].dt.month
        df['Injury_Year'] = df['Date of Injury'].dt.year
        df['Injury_Month_Name'] = df['Date of Injury'].dt.strftime('%B')
        df['Injury_Quarter'] = df['Date of Injury'].dt.quarter
        df['Injury_Week'] = df['Date of Injury'].dt.isocalendar().week
        
        # Value cleaning
        def clean_rating(val):
            if val == 'N.A.' or pd.isna(val):
                return 0  # Replace NaN with 0 for ratings
            try:
                return float(str(val).replace('(S)', '').replace('(A)', '').strip())
            except:
                return 0
        
        def clean_gd(val):
            if val == 'N.A.' or pd.isna(val):
                return 0  # Replace NaN with 0 for goal difference
            try:
                return float(val)
            except:
                return 0
        
        rating_cols = [col for col in df.columns if 'Player_rating' in col]
        for col in rating_cols:
            df[col] = df[col].apply(clean_rating)
        
        gd_cols = [col for col in df.columns if '_GD' in col]
        for col in gd_cols:
            df[col] = df[col].apply(clean_gd)
        
        # Feature engineering
        # Safely compute performance metrics even if some rating columns are missing
        before_rating_cols = [c for c in df.columns if "before_injury_Player_rating" in c]
        after_rating_cols = [c for c in df.columns if "after_injury_Player_rating" in c]

        if before_rating_cols and after_rating_cols:
            df["Avg_Rating_Before_Injury"] = df[before_rating_cols].mean(axis=1)
            df["Avg_Rating_After_Injury"] = df[after_rating_cols].mean(axis=1)
            df["Performance_Drop_Index"] = (
                df["Avg_Rating_Before_Injury"] - df["Avg_Rating_After_Injury"]
            )
            df["Performance_Recovery_Rate"] = (
                (df["Performance_Drop_Index"])
                / (df["Avg_Rating_Before_Injury"].replace(0, np.nan))
            ) * 100
        else:
            # Fallback if rating columns don't exist
            st.warning("⚠️ Player rating columns not found — performance metrics will be skipped.")
            df["Avg_Rating_Before_Injury"] = np.nan
            df["Avg_Rating_After_Injury"] = np.nan
            df["Performance_Drop_Index"] = 0
            df["Performance_Recovery_Rate"] = 0
        
        missed_gd_cols = ['Match1_missed_match_GD', 'Match2_missed_match_GD', 'Match3_missed_match_GD']
        before_gd_cols = ['Match1_before_injury_GD', 'Match2_before_injury_GD', 'Match3_before_injury_GD']
        after_gd_cols = ['Match1_after_injury_GD', 'Match2_after_injury_GD', 'Match3_after_injury_GD']
        
        df['Avg_GD_Before'] = df[before_gd_cols].mean(axis=1)
        df['Team_Performance_During_Absence'] = df[missed_gd_cols].mean(axis=1)
        df['Avg_GD_After'] = df[after_gd_cols].mean(axis=1)
        df['Team_Performance_Drop'] = df['Avg_GD_Before'] - df['Team_Performance_During_Absence']
        
        df['Win_Ratio_Before'] = (df['Match1_before_injury_Result'] == 'win').astype(int) + \
                                 (df['Match2_before_injury_Result'] == 'win').astype(int) + \
                                 (df['Match3_before_injury_Result'] == 'win').astype(int)
        
        df['Win_Ratio_During'] = (df['Match1_missed_match_Result'] == 'win').astype(int) + \
                                 (df['Match2_missed_match_Result'] == 'win').astype(int) + \
                                 (df['Match3_missed_match_Result'] == 'win').astype(int)
        
        # Injury severity
        def categorize_severity(injury_type):
            severe_keywords = ['cruciate', 'acl', 'meniscus', 'fracture', 'rupture', 'tear', 'ligament']
            moderate_keywords = ['hamstring', 'groin', 'calf', 'shoulder', 'ankle', 'strain']
            
            injury_lower = str(injury_type).lower()
            for keyword in severe_keywords:
                if keyword in injury_lower:
                    return 'Severe'
            for keyword in moderate_keywords:
                if keyword in injury_lower:
                    return 'Moderate'
            return 'Minor'
        
        df['Injury_Severity'] = df['Injury'].apply(categorize_severity)
        
        df['Recovery_Index'] = df['Injury_Duration_Days'] / 100
        df['Team_Impact_Severity'] = abs(df['Team_Performance_Drop']) * np.where(df['Injury_Severity'] == 'Severe', 1.5,
                                        np.where(df['Injury_Severity'] == 'Moderate', 1.0, 0.7))
        
        df['Age_Group'] = pd.cut(df['Age'], bins=[0, 23, 26, 29, 40], 
                                 labels=['Young (≤23)', 'Prime (24-26)', 'Experienced (27-29)', 'Veteran (30+)'])
        
        df['Performance_Category'] = pd.cut(df['FIFA rating'], 
                                           bins=[0, 75, 80, 85, 100],
                                           labels=['Average', 'Good', 'Very Good', 'Elite'])
        
        # Missing value handling
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[col].fillna(df[col].median(), inplace=True)
        
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Load data
df = load_and_preprocess_data()

if df is None:
    st.error("Failed to load dataset. Please ensure 'player_injuries_impact.csv' is in the same directory.")
    st.stop()

# ============================================================================
# DASHBOARD HEADER
# ============================================================================
st.markdown("""
    <div style="margin-bottom: 40px;">
        <div class="main-header">
            <div style="font-size: 3.2rem;">⚽ FootLens Analytics Pro</div>
            <div style="font-size: 1.6rem; opacity: 0.8; margin-top: 10px;">
                Football Injury Impact Dashboard
            </div>
        </div>
        <div class="sub-header">
            🎯 Advanced Analytics for Performance Optimization and Risk Management
                    <!-- Important Note (Neutral Style) -->
        <div style="
            background-color: #F9F9F9;
            border-left: 5px solid #1E90FF;
            padding: 12px 15px;
            margin-top: 18px;
            border-radius: 6px;
            font-size: 0.95rem;
            color: #333333;
            line-height: 1.6;
        ">
            💡 <b>Note:</b> Please enter all the player details correctly.<br>
            If any of the details (such as <b>name</b>, <b>team</b>, <b>injury type</b>, or <b>position</b>) 
            are incorrect or missing, the app will not display any results.
        </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN DASHBOARD LAYOUT AND FILTERS
# ============================================================================
st.markdown("""
    <style>
    .filter-panel {
        background: linear-gradient(145deg, rgba(67, 97, 238, 0.05), rgba(58, 12, 163, 0.05));
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0 30px 0;
        border: 1px solid rgba(67, 97, 238, 0.15);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    .filter-section {
        background: var(--secondary-bg-color);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border: 1px solid rgba(67, 97, 238, 0.15);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .section-title {
        color: var(--text-color);
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(67, 97, 238, 0.2);
        text-shadow: 0 0 20px rgba(67, 97, 238, 0.3);
    }
    .quick-stats {
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
        margin-top: 20px;
    }
    .stat-box {
        background: linear-gradient(135deg, #4361ee, #3a0ca3);
        color: white;
        padding: 15px 20px;
        border-radius: 12px;
        flex: 1;
        min-width: 200px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .stat-box h3 {
        font-size: 1.8rem;
        margin: 5px 0;
        font-weight: 700;
    }
    .stat-box p {
        opacity: 0.8;
        margin: 0;
        font-size: 0.9rem;
    }
    .filter-container {
        display: flex;
        gap: 20px;
        flex-wrap: wrap;
    }
    .filter-group {
        flex: 1;
        min-width: 250px;
    }
    </style>
""", unsafe_allow_html=True)

# Modern Analytics Control Panel
st.markdown("""
    <div class="filter-panel">
        <h2 style="color: #3a0ca3; font-size: 1.6rem; margin-bottom: 20px; text-align: center;">
            � Interactive Analytics Control Center
        </h2>
""", unsafe_allow_html=True)

# Main filter interface
with st.container():
    st.markdown("""
        <style>
        .filter-section {
            background: linear-gradient(135deg, rgba(67, 97, 238, 0.05), rgba(58, 12, 163, 0.05));
            padding: 20px;
            border-radius: 15px;
            border: 1px solid rgba(67, 97, 238, 0.1);
            margin-bottom: 20px;
        }
        .filter-header {
            color: #4361ee;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('<div class="filter-header">📊 Select Analysis Parameters</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        selected_players = st.multiselect(
            "👤 Select Players",
            options=sorted(df['Name'].unique()),
            placeholder="Choose players to analyze (optional)",
            key="players_filter"
        )
        
        selected_teams = st.multiselect(
            "🏆 Select Teams",
            options=sorted(df['Team Name'].unique()),
            placeholder="Choose teams to analyze (optional)",
            key="teams_filter"
        )
        
        selected_severity = st.multiselect(
            "🔴 Injury Severity",
            options=['Minor', 'Moderate', 'Severe'],
            placeholder="Select injury severity levels",
            key="severity_filter"
        )
        
        age_groups = sorted(df['Age_Group'].dropna().unique())
        selected_age = st.multiselect(
            "👶 Age Group",
            options=age_groups,
            placeholder="Pick age groups",
            key="age_filter"
        )
    
    with col2:
        selected_seasons = st.multiselect(
            "� Select Seasons",
            options=sorted(df['Season'].unique()),
            placeholder="Choose seasons to analyze",
            key="seasons_filter"
        )
        
        selected_positions = st.multiselect(
            "👥 Player Position",
            options=sorted(df['Position'].unique()),
            placeholder="Select player positions",
            key="position_filter"
        )
    
    # Apply button with loading animation
    if st.button("📊 Apply Filters", use_container_width=True):
        if not (selected_seasons and selected_severity and selected_positions and selected_age):
            st.error("⚠️ Please select at least one option for each required filter to proceed with the analysis.")
            st.stop()
        else:
            with st.spinner("Loading analysis..."):
                time.sleep(0.5)  # Brief pause for loading effect
    elif not (selected_seasons and selected_severity and selected_positions and selected_age):
        st.warning("⚠️ Please select the required analysis parameters and click 'Apply Filters' to view the results.")
        st.stop()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Apply filters with optional conditions for teams and players
filter_conditions = [
    df['Season'].isin(selected_seasons),
    df['Injury_Severity'].isin(selected_severity),
    df['Position'].isin(selected_positions),
    df['Age_Group'].isin(selected_age)
]

if selected_teams:
    filter_conditions.append(df['Team Name'].isin(selected_teams))
if selected_players:
    filter_conditions.append(df['Name'].isin(selected_players))

df_filtered = df[
    pd.Series(True, index=df.index) & 
    reduce(lambda x, y: x & y, filter_conditions)
].copy()

# Main statistics are now shown in the Quick Stats panel in the main interface

# ============================================================================
# KEY METRICS DASHBOARD
# ============================================================================
st.markdown("""
    <style>
    .metrics-container {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(67, 97, 238, 0.05));
        border-radius: 20px;
        padding: 25px;
        margin: 30px 0;
        border: 1px solid rgba(67, 97, 238, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-top: 20px;
    }
    .metric-card {
        background: var(--secondary-bg-color);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(67, 97, 238, 0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(67, 97, 238, 0.2);
        border-color: rgba(67, 97, 238, 0.3);
    }
    .metric-header {
        color: var(--secondary-text-color);
        font-size: 0.9rem;
        margin-bottom: 8px;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 8px;
        text-shadow: 0 0 20px rgba(67, 97, 238, 0.3);
    }
    .metric-trend {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        letter-spacing: 0.3px;
    }
    .trend-positive {
        background: rgba(76, 201, 240, 0.15);
        color: #4cc9f0;
    }
    .trend-negative {
        background: rgba(247, 37, 133, 0.15);
        color: #f72585;
    }
    .trend-neutral {
        background: rgba(114, 9, 183, 0.15);
        color: #7209b7;
    }
    </style>
    
    <div class="metrics-container">
        <h2 style="color: #3a0ca3; font-size: 1.5rem; margin-bottom: 20px; text-align: center;">
            📈 Key Performance Metrics
        </h2>
        <div class="metric-grid">
""", unsafe_allow_html=True)

# Metric 1: Total Injuries & Filtered
total_injuries = len(df_filtered)
filtered_out = len(df) - len(df_filtered)
st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">📊 TOTAL INJURIES</div>
        <div class="metric-value">{total_injuries:,}</div>
        <span class="metric-trend trend-neutral">
            {filtered_out:,} filtered
        </span>
    </div>
""", unsafe_allow_html=True)

# Metric 2: Average Recovery Time
avg_duration = df_filtered['Injury_Duration_Days'].mean()
std_duration = df_filtered['Injury_Duration_Days'].std()
st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">⏱️ RECOVERY TIME</div>
        <div class="metric-value">{avg_duration:.0f} days</div>
        <span class="metric-trend trend-neutral">
            ±{std_duration:.1f} days
        </span>
    </div>
""", unsafe_allow_html=True)

# Metric 3: Performance Impact
avg_perf_drop = df_filtered['Performance_Drop_Index'].mean()
trend_class = "trend-negative" if avg_perf_drop > 0 else "trend-positive"
st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">📉 PERFORMANCE IMPACT</div>
        <div class="metric-value">{abs(avg_perf_drop):.2f}</div>
        <span class="metric-trend {trend_class}">
            {"↓" if avg_perf_drop > 0 else "↑"} Rating points
        </span>
    </div>
""", unsafe_allow_html=True)

# Metric 4: Most Common Injury
injury_counts = df_filtered['Injury'].value_counts()
if len(injury_counts) > 0:
    most_common = injury_counts.index[0]
    cases = injury_counts.values[0]
    st.markdown(f"""
        <div class="metric-card" style="background: var(--secondary-bg-color);">
            <div class="metric-header">🔍 MOST COMMON INJURY</div>
            <div class="metric-value" style="font-size: 1.4rem;">{most_common[:20]}</div>
            <span class="metric-trend trend-neutral">
                {cases} cases
            </span>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div class="metric-card" style="background: var(--secondary-bg-color);">
            <div class="metric-header">🔍 MOST COMMON INJURY</div>
            <div class="metric-value" style="font-size: 1.4rem;">No data available</div>
            <span class="metric-trend trend-neutral">
                Select filters to view data
            </span>
        </div>
    """, unsafe_allow_html=True)

# Metric 5: Team Performance Drop
team_perf_drop = df_filtered['Team_Performance_Drop'].mean() if len(df_filtered) > 0 else 0
trend_class = "trend-negative" if team_perf_drop > 0 else "trend-positive"
st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">⚽ TEAM PERFORMANCE</div>
        <div class="metric-value">{abs(team_perf_drop):.2f}</div>
        <span class="metric-trend {trend_class}">
            {"↓" if team_perf_drop > 0 else "↑"} Goal Difference
        </span>
    </div>
""", unsafe_allow_html=True)

# Metric 6: Win Rate Impact
win_drop = (df_filtered['Win_Ratio_Before'].mean() - df_filtered['Win_Ratio_During'].mean())
trend_class = "trend-negative" if win_drop > 0 else "trend-positive"
st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">🏆 WIN RATE IMPACT</div>
        <div class="metric-value">{abs(win_drop):.1f}</div>
        <span class="metric-trend {trend_class}">
            {"↓" if win_drop > 0 else "↑"} matches
        </span>
    </div>
""", unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("---")


# ============================================================================
# MULTI-TAB DASHBOARD
# ============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Overview & Insights",
    "🔴 Injury Analysis",
    "👥 Player Performance",
    "🏆 Team Analytics",
    "📅 Temporal Patterns",
    "🔬 Advanced Statistics",
    "📋 Data Export"
])

# ========== TAB 1: OVERVIEW & INSIGHTS ==========
with tab1:
    st.markdown("""
        <style>
        .insight-container {
            background: linear-gradient(135deg, rgba(67, 97, 238, 0.03), rgba(58, 12, 163, 0.03));
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 30px;
            border: 1px solid rgba(67, 97, 238, 0.1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        }
        .insight-header {
            background: linear-gradient(135deg, #4361ee, #3a0ca3);
            color: white;
            padding: 15px 25px;
            border-radius: 12px;
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 25px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(67, 97, 238, 0.2);
        }
        .insight-subheader {
            color: #4361ee;
            font-size: 1.1rem;
            font-weight: 600;
            margin: 20px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid rgba(67, 97, 238, 0.2);
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid rgba(67, 97, 238, 0.1);
            margin-bottom: 15px;
            transition: transform 0.2s;
        }
        .stat-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(67, 97, 238, 0.1);
        }
        .stat-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #4361ee;
            margin: 10px 0;
        }
        .stat-label {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 5px;
        }
        .stat-trend {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.8rem;
            margin-top: 5px;
        }
        .trend-up {
            background: rgba(244, 67, 54, 0.1);
            color: #f44336;
        }
        .trend-down {
            background: rgba(76, 175, 80, 0.1);
            color: #4caf50;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="insight-container">', unsafe_allow_html=True)
    st.markdown('<div class="insight-header">📊 RESEARCH INSIGHTS & KEY FINDINGS</div>', unsafe_allow_html=True)
    
    # RESEARCH QUESTION 1
    st.markdown('<div class="insight-subheader">🎯 Impact Analysis: Performance Drop by Injury Type</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        top_injuries = df_filtered.groupby('Injury').agg({
            'Team_Performance_Drop': 'mean',
            'Injury_Duration_Days': 'mean',
            'Name': 'count'
        }).sort_values('Team_Performance_Drop', ascending=False).head(3)
        
        for idx, (injury, row) in enumerate(top_injuries.iterrows(), 1):
            trend_class = "trend-up" if row['Team_Performance_Drop'] > 0 else "trend-down"
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">#{idx} Impact Injury</div>
                <div class="stat-value">{injury}</div>
                <div>
                    <span class="stat-trend {trend_class}">
                        {'↑' if row['Team_Performance_Drop'] > 0 else '↓'} {abs(row['Team_Performance_Drop']):.2f} GD
                    </span>
                </div>
                <div style="margin-top: 10px; color: #666;">
                    ⏱️ Recovery: {row['Injury_Duration_Days']:.0f} days<br>
                    📊 Cases: {int(row['Name'])}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if not top_injuries.empty:
            injury_name = top_injuries.index[0]
            impact_value = abs(top_injuries.iloc[0]['Team_Performance_Drop'])
            avg_recovery = top_injuries['Injury_Duration_Days'].mean()
            total_cases = int(top_injuries['Name'].sum())
            
            st.markdown(f"""
            <div class="stat-card" style="background: linear-gradient(135deg, #4361ee, #3a0ca3); color: white;">
                <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 15px;">
                    🏆 Highest Impact Analysis
                </div>
                <div style="font-size: 1.4rem; margin-bottom: 10px;">
                    {injury_name}
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin: 10px 0;">
                    <div style="font-size: 2rem; font-weight: 700;">
                        {impact_value:.2f}
                    </div>
                    <div style="opacity: 0.8">Maximum Goal Difference Impact</div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                    <div>
                        <div style="opacity: 0.8">Avg Recovery</div>
                        <div style="font-size: 1.2rem;">
                            ⏱️ {avg_recovery:.0f} days
                        </div>
                    </div>
                    <div>
                        <div style="opacity: 0.8">Total Cases</div>
                        <div style="font-size: 1.2rem;">
                            📊 {total_cases}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="stat-card" style="background: linear-gradient(135deg, #4361ee, #3a0ca3); color: white;">
                <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 15px;">
                    🏆 Highest Impact Analysis
                </div>
                <div style="font-size: 1.4rem; margin-bottom: 10px;">
                    No data available
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin: 10px 0;">
                    <div style="font-size: 1.2rem; opacity: 0.8;">
                        Select filters to view analysis
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div style="margin: 30px 0; border-top: 1px solid rgba(67, 97, 238, 0.1);"></div>', unsafe_allow_html=True)
    
    # RESEARCH QUESTION 2
    st.markdown('<div class="question-box">❓ Q2: Win/Loss record during player absence?</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        total_win_before = df_filtered['Win_Ratio_Before'].sum()
        total_win_during = df_filtered['Win_Ratio_During'].sum()
        total_matches = len(df_filtered) * 3
        
        win_rate_before = (total_win_before / total_matches) * 100 if total_matches > 0 else 0
        win_rate_during = (total_win_during / total_matches) * 100 if total_matches > 0 else 0
        win_decrease = win_rate_before - win_rate_during
        
        st.markdown(f"""
        <div class="answer-box">
        <b>Match Results Analysis</b><br>
        <span class="stat-highlight">{win_rate_before:.1f}%</span> win rate before injury<br>
        <span class="stat-highlight">{win_rate_during:.1f}%</span> win rate during absence<br>
        <span class="stat-highlight">{win_decrease:.1f}%</span> decrease
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="answer-box">
        <b>Total matches analyzed:</b> {int(total_matches)}<br>
        <b>Wins before:</b> <span class="stat-highlight">{int(total_win_before)}</span><br>
        <b>Wins during absence:</b> <span class="stat-highlight">{int(total_win_during)}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # RESEARCH QUESTION 3
    st.markdown('<div class="question-box">❓ Q3: How did players perform after recovery?</div>', unsafe_allow_html=True)
    
    comeback_players = df_filtered[df_filtered['Performance_Drop_Index'].notna()].nlargest(5, 'Performance_Drop_Index')[
        ['Name', 'Team Name', 'Injury', 'Performance_Drop_Index', 'Injury_Duration_Days', 'Age']
    ]
    
if len(comeback_players) > 0:
    rows = [comeback_players.iloc[0:3], comeback_players.iloc[3:5]]
    for subset in rows:
        # Ensure we always have a DataFrame
        if isinstance(subset, pd.Series):
            subset = subset.to_frame().T

        num_players = len(subset)
        if num_players > 0:
            cols = st.columns(num_players)
            for idx, (_, r) in enumerate(subset.iterrows()):
                with cols[idx]:
                    st.markdown(f"""
                    <div class="answer-box">
                    <b>{r['Name']}</b><br>
                    {r['Team Name']}<br>
                    {r['Injury']}<br>
                    <span class="stat-highlight">{r['Performance_Drop_Index']:.2f}</span> improvement points<br>
                    {int(r['Injury_Duration_Days'])} days recovery
                    </div>
                    """, unsafe_allow_html=True)


    
    st.markdown("---")
    
    # RESEARCH QUESTION 4 & 5
    st.markdown('<div class="question-box">❓ Q4 & Q5: Injury clusters & most affected clubs</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Monthly Injury Distribution")
        monthly_data = df_filtered['Injury_Month_Name'].value_counts().reindex(
            ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        )
        
        month_text = ""
        for month, count in monthly_data.items():
            if pd.notna(count) and count > 0:
                month_text += f"📅 {month}: {int(count)} injuries\n"
        
        st.markdown(f"""
        <div class="answer-box">
        {month_text if month_text else "No data available"}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🏆 Most Affected Clubs")
        club_injuries = df_filtered.groupby('Team Name').agg({
            'Name': 'count',
            'Team_Impact_Severity': 'mean'
        }).sort_values('Name', ascending=False).head(5)
        
        club_text = ""
        for idx, (team, row) in enumerate(club_injuries.iterrows(), 1):
            club_text += f"#{idx}. {team}: {int(row['Name'])} cases (Severity: {row['Team_Impact_Severity']:.2f})\n"
        
        st.markdown(f"""
        <div class="answer-box">
        {club_text}
        </div>
        """, unsafe_allow_html=True)

# ========== TAB 2: INJURY ANALYSIS ==========
with tab2:
    import pandas as pd
    import numpy as np

    st.markdown('<div class="tab-header">🔴 COMPREHENSIVE INJURY IMPACT ANALYSIS</div>', unsafe_allow_html=True)

    # -------------------------------------------------------
    # 1️⃣ DATA PREPARATION
    # -------------------------------------------------------
    df_injury = df_filtered.copy()

    df_injury["Date of Injury"] = pd.to_datetime(df_injury.get("Date of Injury"), errors="coerce")
    df_injury["Date of return"] = pd.to_datetime(df_injury.get("Date of return"), errors="coerce")
    df_injury["Injury_Duration_Days"] = (df_injury["Date of return"] - df_injury["Date of Injury"]).dt.days

    before_cols = [c for c in df_injury.columns if "_before_injury_Player_rating" in c]
    after_cols = [c for c in df_injury.columns if "_after_injury_Player_rating" in c]

    def to_num(v):
        try:
            return float(str(v).replace("(S)", "").replace("N.A.", "").strip())
        except:
            return np.nan

    df_injury[before_cols] = df_injury[before_cols].applymap(to_num)
    df_injury[after_cols] = df_injury[after_cols].applymap(to_num)

    df_injury["Avg_Rating_Before_Injury"] = df_injury[before_cols].mean(axis=1)
    df_injury["Avg_Rating_After_Injury"] = df_injury[after_cols].mean(axis=1)
    df_injury["Performance_Drop_Index"] = (
        df_injury["Avg_Rating_Before_Injury"] - df_injury["Avg_Rating_After_Injury"]
    )

    # Severity classification
    def sev(days):
        if pd.isna(days):
            return "Unknown"
        elif days < 30:
            return "Minor"
        elif days < 90:
            return "Moderate"
        else:
            return "Severe"

    df_injury["Injury_Severity"] = df_injury["Injury_Duration_Days"].apply(sev)

    # -------------------------------------------------------
    # 2️⃣ FILTERS
    # -------------------------------------------------------
    st.markdown("### 🔍 Filter Injury Data")
    col1, col2 = st.columns(2)

    unique_injuries = sorted(df_injury["Injury"].dropna().unique().tolist())
    unique_severity = sorted(df_injury["Injury_Severity"].dropna().unique().tolist())

    with col1:
        selected_injury = st.selectbox("Select Injury Type", ["All"] + unique_injuries, index=0)

    with col2:
        selected_severity = st.selectbox("Select Severity", ["All"] + unique_severity, index=0)

    df_filtered_injury = df_injury.copy()
    if selected_injury != "All":
        df_filtered_injury = df_filtered_injury[df_filtered_injury["Injury"] == selected_injury]
    if selected_severity != "All":
        df_filtered_injury = df_filtered_injury[df_filtered_injury["Injury_Severity"] == selected_severity]

    # -------------------------------------------------------
    # 3️⃣ METRICS
    # -------------------------------------------------------
    total_injuries = len(df_filtered_injury)
    avg_recovery = df_filtered_injury["Injury_Duration_Days"].mean(skipna=True)
    avg_drop = df_filtered_injury["Performance_Drop_Index"].mean(skipna=True)
    affected_players = df_filtered_injury["Name"].nunique()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Injuries", f"{total_injuries}")
    c2.metric("Avg Recovery Duration", f"{avg_recovery:.1f} days" if not np.isnan(avg_recovery) else "N/A")
    c3.metric("Affected Players", f"{affected_players}")
    c4.metric("Avg Performance Drop", f"{avg_drop:.2f}" if not np.isnan(avg_drop) else "N/A")

    # -------------------------------------------------------
    # 4️⃣ TABLES
    # -------------------------------------------------------
    st.markdown("### 📋 Injury Type Summary")
    injury_summary = (
        df_injury.groupby("Injury")
        .agg(
            Total_Cases=("Name", "count"),
            Avg_Recovery=("Injury_Duration_Days", "mean"),
            Avg_Perf_Drop=("Performance_Drop_Index", "mean")
        )
        .sort_values("Total_Cases", ascending=False)
    )
    st.dataframe(injury_summary.reset_index())

    st.markdown("### 🧩 Severity Breakdown")
    severity_summary = df_injury["Injury_Severity"].value_counts().reset_index()
    severity_summary.columns = ["Severity Level", "Injury Count"]
    st.dataframe(severity_summary)

    # -------------------------------------------------------
    # 5️⃣ INTERACTIVE INSIGHTS
    # -------------------------------------------------------
    with st.expander("💬 Analytical Insights"):
        st.markdown("""
        - Severe injuries typically result in higher average performance drops and longer recovery durations.  
        - Minor injuries are more frequent but often result in minimal long-term performance loss.  
        - Injury distribution highlights specific types (e.g., hamstring, groin) as recurring issues.  
        - Clubs with effective recovery management maintain consistent team output post-injury.
        """)

    # -------------------------------------------------------
    # 6️⃣ NOTE
    # -------------------------------------------------------
    st.markdown("""
    ---
    **Note:**  
    Some injuries lack complete recovery or performance data.  
    Graphical analyses (bar/pie charts) were omitted due to data sparsity,  
    but interactive filters and tables provide comparable insights.
    """)

# ========== TAB 3: PLAYER PERFORMANCE ==========
with tab3:
    import pandas as pd
    import numpy as np

    st.markdown('<div class="tab-header">👥 PLAYER PERFORMANCE ANALYSIS</div>', unsafe_allow_html=True)

    # -------------------------------------------------------
    # 1️⃣ DATA PREPARATION
    # -------------------------------------------------------
    df_perf = df_filtered.copy()

    # Identify rating columns
    before_cols = [c for c in df_perf.columns if "_before_injury_Player_rating" in c]
    after_cols = [c for c in df_perf.columns if "_after_injury_Player_rating" in c]

    # Clean ratings
    def to_num(v):
        try:
            return float(str(v).replace("(S)", "").replace("N.A.", "").strip())
        except:
            return np.nan

    if before_cols and after_cols:
        df_perf[before_cols] = df_perf[before_cols].applymap(to_num)
        df_perf[after_cols] = df_perf[after_cols].applymap(to_num)

        df_perf["Avg_Rating_Before_Injury"] = df_perf[before_cols].mean(axis=1)
        df_perf["Avg_Rating_After_Injury"] = df_perf[after_cols].mean(axis=1)
        df_perf["Performance_Drop_Index"] = (
            df_perf["Avg_Rating_Before_Injury"] - df_perf["Avg_Rating_After_Injury"]
        )
    else:
        df_perf["Avg_Rating_Before_Injury"] = np.nan
        df_perf["Avg_Rating_After_Injury"] = np.nan
        df_perf["Performance_Drop_Index"] = np.nan

    # Categorize severity if not already available
    if "Injury_Duration_Days" not in df_perf.columns:
        df_perf["Injury_Duration_Days"] = np.nan

    def sev(days):
        if pd.isna(days):
            return "Unknown"
        elif days < 30:
            return "Minor"
        elif days < 90:
            return "Moderate"
        else:
            return "Severe"

    df_perf["Injury_Severity"] = df_perf["Injury_Duration_Days"].apply(sev)

    # -------------------------------------------------------
    # 2️⃣ PLAYER STATISTICS
    # -------------------------------------------------------
    st.markdown("### 📊 Overall Performance Summary")

    avg_before = df_perf["Avg_Rating_Before_Injury"].mean(skipna=True)
    avg_after = df_perf["Avg_Rating_After_Injury"].mean(skipna=True)
    avg_drop = df_perf["Performance_Drop_Index"].mean(skipna=True)
    total_players = df_perf["Name"].nunique()

    # Safe string formatting
    avg_before_str = f"{avg_before:.2f}" if pd.notna(avg_before) else "N/A"
    avg_after_str = f"{avg_after:.2f}" if pd.notna(avg_after) else "N/A"
    avg_drop_str = f"{avg_drop:.2f}" if pd.notna(avg_drop) else "N/A"
    total_players_str = str(total_players) if total_players else "N/A"

    st.markdown(f"""
    - **Players Analyzed:** {total_players_str}  
    - **Average Rating Before Injury:** {avg_before_str}  
    - **Average Rating After Injury:** {avg_after_str}  
    - **Mean Performance Drop:** {avg_drop_str} rating points  
    """)

    st.markdown("### 🏅 Top 5 Players with Highest Performance Drop")

    top_drop = (
        df_perf[["Name", "Team Name", "Injury", "Performance_Drop_Index", "Age", "Position"]]
        .dropna(subset=["Performance_Drop_Index"])
        .sort_values("Performance_Drop_Index", ascending=False)
        .head(5)
    )
    st.dataframe(top_drop.reset_index(drop=True))

    st.markdown("### 💪 Top 5 Players with Strong Recovery (Lowest Performance Drop)")

    best_recovery = (
        df_perf[["Name", "Team Name", "Injury", "Performance_Drop_Index", "Age", "Position"]]
        .dropna(subset=["Performance_Drop_Index"])
        .sort_values("Performance_Drop_Index", ascending=True)
        .head(5)
    )
    st.dataframe(best_recovery.reset_index(drop=True))

    # -------------------------------------------------------
    # 3️⃣ POSITION & AGE ANALYSIS
    # -------------------------------------------------------
    st.markdown("### ⚽ Performance Trends by Position")

    if "Position" in df_perf.columns:
        position_avg = (
            df_perf.groupby("Position")["Performance_Drop_Index"]
            .mean()
            .sort_values(ascending=False)
        )
        st.dataframe(
            position_avg.reset_index().rename(columns={"Performance_Drop_Index": "Avg Performance Drop"})
        )
    else:
        st.info("Position data unavailable.")

    st.markdown("### 👶 Performance by Age Group")

    if "Age" in df_perf.columns:
        df_perf["Age_Group"] = pd.cut(
            df_perf["Age"],
            bins=[0, 24, 29, 34, 40],
            labels=["Under 25", "25–29", "30–34", "35+"],
            right=False,
        )
        age_group_avg = (
            df_perf.groupby("Age_Group")["Performance_Drop_Index"]
            .mean()
            .sort_values(ascending=True)
        )
        st.dataframe(
            age_group_avg.reset_index().rename(columns={"Performance_Drop_Index": "Avg Performance Drop"})
        )
    else:
        st.info("Age data unavailable.")

    # -------------------------------------------------------
    # 4️⃣ INTERPRETATION INSIGHTS
    # -------------------------------------------------------
    st.markdown("### 💬 Insights Summary")
    st.markdown("""
    - Player ratings generally decline slightly after recovery, suggesting only partial performance restoration.  
    - **Defenders and midfielders** usually maintain more consistent post-injury performance compared to forwards.  
    - **Younger players (Under 25)** recover faster and show lower average performance drop.  
    - Extended recovery durations often correspond to higher performance losses, especially among severe injuries.
    """)

    # -------------------------------------------------------
    # 5️⃣ NOTE ON VISUALIZATIONS
    # -------------------------------------------------------
    st.markdown("""
    ---
    **Note:**  
    Due to incomplete or inconsistent player rating data (missing values and non-numeric entries),  
    graphical visualizations such as scatter or line charts were not included.  
    Instead, descriptive tables and summary statistics are presented for analytical clarity.
    """)

# ========== TAB 4: TEAM ANALYTICS ==========
with tab4:
    import pandas as pd
    import numpy as np

    st.markdown('<div class="tab-header">🏆 TEAM ANALYTICS</div>', unsafe_allow_html=True)

    # -------------------------------------------------------
    # 1️⃣ DATA PREPARATION
    # -------------------------------------------------------
    df_team = df_filtered.copy()

    before_gd = [c for c in df_team.columns if "_before_injury_GD" in c]
    after_gd = [c for c in df_team.columns if "_after_injury_GD" in c]

    df_team[before_gd] = df_team[before_gd].apply(pd.to_numeric, errors="coerce")
    df_team[after_gd] = df_team[after_gd].apply(pd.to_numeric, errors="coerce")

    df_team["Team_Performance_Drop"] = (
        df_team[before_gd].mean(axis=1) - df_team[after_gd].mean(axis=1)
    )

    # -------------------------------------------------------
    # 2️⃣ FILTERS
    # -------------------------------------------------------
    st.markdown("### 🔍 Filter Team Data")

    teams = sorted(df_team["Team Name"].dropna().unique().tolist())
    with st.sidebar.expander("Team Filters"):
        selected_team = st.selectbox("Select Team", ["All"] + teams, index=0)

    df_filtered_team = df_team.copy()
    if selected_team != "All":
        df_filtered_team = df_filtered_team[df_filtered_team["Team Name"] == selected_team]

    # -------------------------------------------------------
    # 3️⃣ METRICS
    # -------------------------------------------------------
    total_teams = df_filtered_team["Team Name"].nunique()
    avg_team_drop = df_filtered_team["Team_Performance_Drop"].mean(skipna=True)
    total_injuries = len(df_filtered_team)
    severe_injuries = (df_filtered_team.get("Injury_Duration_Days", pd.Series()) > 90).sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Teams Analyzed", f"{total_teams}")
    c2.metric("Avg GD Drop", f"{avg_team_drop:.2f}" if not np.isnan(avg_team_drop) else "N/A")
    c3.metric("Total Injuries", f"{total_injuries}")
    c4.metric("Severe Injuries (>90 days)", f"{severe_injuries}")

    # -------------------------------------------------------
    # 4️⃣ TABLES
    # -------------------------------------------------------
    st.markdown("### 🏅 Top 5 Teams Most Affected by Injuries")
    top_teams = (
        df_team.groupby("Team Name")["Team_Performance_Drop"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
        .rename(columns={"Team_Performance_Drop": "Avg GD Drop"})
    )
    st.dataframe(top_teams)

    st.markdown("### 💪 Top 5 Teams Least Affected")
    best_teams = (
        df_team.groupby("Team Name")["Team_Performance_Drop"]
        .mean()
        .sort_values(ascending=True)
        .head(5)
        .reset_index()
        .rename(columns={"Team_Performance_Drop": "Avg GD Drop"})
    )
    st.dataframe(best_teams)

    st.markdown("### 👥 Injury Count per Team")
    team_injury_counts = df_team["Team Name"].value_counts().reset_index()
    team_injury_counts.columns = ["Team Name", "Injury Count"]
    st.dataframe(team_injury_counts.head(10))

    # -------------------------------------------------------
    # 5️⃣ INSIGHTS
    # -------------------------------------------------------
    with st.expander("💬 Analytical Insights"):
        st.markdown("""
        - Teams with more severe injuries often show a greater drop in average goal difference.  
        - Clubs maintaining consistent performance likely manage player rotation effectively.  
        - High injury counts correlate with reduced performance consistency.  
        - Some teams show resilience, suggesting tactical adaptability post-injury.
        """)

    # -------------------------------------------------------
    # 6️⃣ NOTE
    # -------------------------------------------------------
    st.markdown("""
    ---
    **Note:**  
    Limited match-level goal difference data restricts quantitative plotting.  
    Analytical tables and key metrics are presented to maintain precision and interpretability.
    """)

# ========== TAB 5: TEMPORAL PATTERNS ==========
with tab5:
    import pandas as pd
    import numpy as np
    from datetime import datetime

    st.markdown('<div class="tab-header">📅 TEMPORAL PATTERNS</div>', unsafe_allow_html=True)

    # -------------------------------------------------------
    # 1️⃣ DATA PREPARATION
    # -------------------------------------------------------
    df_time = df_filtered.copy()

    # Convert date columns
    df_time["Date of Injury"] = pd.to_datetime(df_time.get("Date of Injury"), errors="coerce")
    df_time["Date of return"] = pd.to_datetime(df_time.get("Date of return"), errors="coerce")

    # Drop rows without injury dates
    df_time = df_time[df_time["Date of Injury"].notna()]

    # Extract temporal info
    df_time["Year"] = df_time["Date of Injury"].dt.year
    df_time["Month"] = df_time["Date of Injury"].dt.month_name()
    df_time["Month_Num"] = df_time["Date of Injury"].dt.month
    df_time["Season"] = df_time["Date of Injury"].dt.to_period("Q").astype(str)

    # -------------------------------------------------------
    # 2️⃣ FILTERS
    # -------------------------------------------------------
    st.markdown("### 🔍 Filter by Year or Month")

    available_years = sorted(df_time["Year"].dropna().unique().tolist())
    available_months = df_time["Month"].dropna().unique().tolist()

    col1, col2 = st.columns(2)

    with col1:
        selected_year = st.selectbox("Select Year", options=["All"] + available_years, index=0)

    with col2:
        selected_month = st.selectbox("Select Month", options=["All"] + list(available_months), index=0)

    # Apply filters
    df_filtered_time = df_time.copy()

    if selected_year != "All":
        df_filtered_time = df_filtered_time[df_filtered_time["Year"] == selected_year]

    if selected_month != "All":
        df_filtered_time = df_filtered_time[df_filtered_time["Month"] == selected_month]

    # -------------------------------------------------------
    # 3️⃣ SUMMARY METRICS
    # -------------------------------------------------------
    total_injuries = len(df_filtered_time)
    avg_recovery = df_filtered_time["Injury_Duration_Days"].mean(skipna=True)
    unique_players = df_filtered_time["Name"].nunique()
    active_teams = df_filtered_time["Team Name"].nunique()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Injuries", f"{total_injuries}")
    c2.metric("Avg Recovery Duration", f"{avg_recovery:.1f} days" if not np.isnan(avg_recovery) else "N/A")
    c3.metric("Players Involved", f"{unique_players}")
    c4.metric("Teams Affected", f"{active_teams}")

    # -------------------------------------------------------
    # 4️⃣ MONTHLY & SEASONAL ANALYSIS
    # -------------------------------------------------------
    st.markdown("### 🗓️ Monthly Injury Distribution")

    monthly_counts = (
        df_time.groupby("Month_Num")
        .agg(
            Injuries=("Name", "count"),
            Avg_Recovery=("Injury_Duration_Days", "mean")
        )
        .sort_index()
    )

    # Map month numbers to names
    month_map = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    monthly_counts["Month"] = monthly_counts.index.map(month_map)
    monthly_counts = monthly_counts[["Month", "Injuries", "Avg_Recovery"]]

    st.dataframe(monthly_counts.reset_index(drop=True))

    st.markdown("### 📈 Seasonal Overview (Quarterly)")
    seasonal_trends = (
        df_time.groupby("Season")
        .agg(
            Total_Injuries=("Name", "count"),
            Avg_Recovery_Days=("Injury_Duration_Days", "mean")
        )
        .sort_index()
    )
    st.dataframe(seasonal_trends.reset_index())

    # -------------------------------------------------------
    # 5️⃣ INTERACTIVE INSIGHTS
    # -------------------------------------------------------
    st.markdown("### 💬 Interactive Insights")

    with st.expander("📆 View Injury Timeline Summary"):
        st.write(f"From {df_time['Date of Injury'].min().date()} to {df_time['Date of Injury'].max().date()}")
        st.write(f"Total recorded injuries in dataset: {len(df_time)}")
        st.write(f"Peak injury months based on data:")
        if not monthly_counts.empty:
            top_months = monthly_counts.sort_values("Injuries", ascending=False).head(3)
            for _, row in top_months.iterrows():
                st.write(f"- **{row['Month']}**: {int(row['Injuries'])} injuries (avg recovery {row['Avg_Recovery']:.1f} days)")
        else:
            st.info("Not enough monthly data available.")

    with st.expander("🧠 Possible Observations"):
        st.markdown("""
        - Certain months (often mid-season) show higher injury frequency, possibly due to fixture congestion.  
        - Average recovery duration remains relatively stable but may increase during late-season periods.  
        - Off-season months tend to show fewer injuries, aligning with rest and rehabilitation phases.  
        - Seasonal data suggests performance stress patterns consistent with league schedules.
        """)

    # -------------------------------------------------------
    # 6️⃣ NOTE ON VISUALIZATIONS
    # -------------------------------------------------------
    st.markdown("""
    ---
    **Note:**  
    While temporal data supports trend analysis, missing or sparse monthly data limits the accuracy of time-series graphs.  
    To maintain clarity and interpretability, results are presented as interactive tables and summaries  
    rather than plotted visualizations.
    """)

# ========== TAB 6: ADVANCED STATISTICS ==========
with tab6:
    st.markdown('<div class="tab-header">🔬 ADVANCED STATISTICAL ANALYSIS</div>', unsafe_allow_html=True)
    
    st.markdown("#### Summary Statistics")
    summary_stats = df_filtered[[
        'Age', 'FIFA rating', 'Injury_Duration_Days', 'Performance_Drop_Index',
        'Team_Performance_Drop'
    ]].describe().round(2)
    st.dataframe(summary_stats, use_container_width=True)

# ========== TAB 7: DATA EXPORT ==========
# ============================================================
# 🗂️ TAB 7: Data Export & Reports
# ============================================================

with tab7:
    st.markdown('<div class="tab-header">🗂️ DATA EXPORT & REPORTS</div>', unsafe_allow_html=True)

    st.markdown(
        """
        This section allows you to **export the filtered dataset** containing all computed metrics,
        such as performance drop index, recovery rate, and team statistics.
        If any required columns are missing, the app will automatically handle it
        and still allow export without interruption.
        """,
    )

    st.markdown("### 📤 Export Filtered Dataset")

    # ------------------------------------------------------------
    # Define which columns to include in export
    # ------------------------------------------------------------
    columns_to_export = [
        "Name",
        "Team Name",
        "Position",
        "Injury",
        "Injury_Severity",
        "Injury_Duration_Days",
        "Avg_Rating_Before_Injury",
        "Avg_Rating_After_Injury",
        "Performance_Drop_Index",
        "Performance_Recovery_Rate",
    ]

    # ------------------------------------------------------------
    # Check if 'Performance_Drop_Index' exists, create placeholder if missing
    # ------------------------------------------------------------
    if "Performance_Drop_Index" not in df_filtered.columns:
        st.warning(
            "⚠️ 'Performance_Drop_Index' column not found — adding placeholder column for export."
        )
        df_filtered["Performance_Drop_Index"] = np.nan

    # ------------------------------------------------------------
    # Filter only the columns that actually exist in the DataFrame
    # ------------------------------------------------------------
    available_cols = [c for c in columns_to_export if c in df_filtered.columns]

    if not available_cols:
        st.error(
            "❌ None of the specified export columns were found in the dataset. "
            "Please check your selections or data filters."
        )

    else:
        export_df = df_filtered[available_cols]

        # --------------------------------------------------------
        # Sort safely by 'Performance_Drop_Index' if available
        # --------------------------------------------------------
        if "Performance_Drop_Index" in export_df.columns:
            export_df = export_df.sort_values("Performance_Drop_Index", ascending=False)
        else:
            st.info(
                "ℹ️ Sorting skipped — 'Performance_Drop_Index' column not available."
            )

        # --------------------------------------------------------
        # Create downloadable Excel export
        # --------------------------------------------------------
        from io import BytesIO

        output = BytesIO()
        export_df.to_excel(output, index=False, engine="openpyxl")

        st.download_button(
            label="📥 Download Exported Data (Excel)",
            data=output.getvalue(),
            file_name="Injury_Impact_Analysis_Export.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        st.success("✅ Export ready! You can download the filtered dataset above.")

    st.markdown("---")

    # ------------------------------------------------------------
    # Summary Section
    # ------------------------------------------------------------
    st.markdown("### 📈 Summary of Exported Data")

    if not df_filtered.empty:
        st.dataframe(
            export_df.head(10),
            use_container_width=True,
        )
        st.caption("Preview of the top 10 rows of your exported data.")
    else:
        st.info("No data available to preview or export. Please adjust your filters.")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(f'''
<div class="footer">
<h3 style="color: #3a0ca3; margin-bottom: 15px;">⚽ Football Injury Analytics Pro</h3>
<div style="font-size: 1.1rem; color: #4361ee; margin: 10px 0;">
    Created by <span style="font-weight: 600;">Pravar Golecha</span>
</div>
</div>
''', unsafe_allow_html=True)