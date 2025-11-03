## IADAI102-2405460--PravarGolecha.

# ⚽ FootLens Analytics Pro — Football Injury Impact Dashboard

**SA of Maths-2** | Mathematics for AI-II | CRS: Artificial Intelligence
**Developed by:** Pravar Golecha

## Project Overview

**FootLens Analytics Pro** is an advanced analytical dashboard built using **Streamlit** to analyze the impact of injuries on football player and team performance.

It transforms complex datasets into meaningful insights for coaches, analysts, and medical staff to evaluate injury severity, recovery trends, and post-injury performance patterns across players and teams.

The project satisfies all FA-2 deliverables — data processing, analysis, dashboard design, and Streamlit Cloud deployment — integrating mathematical reasoning, data visualization, and artificial intelligence concepts.


## Key Features

### Core Analytical Modules

1. **🔴 Comprehensive Injury Impact Analysis**
   Summarizes the effect of different injuries on team performance, injury severity distribution, and recovery duration patterns.

2. **👥 Player Performance Insights**
   Displays pre- and post-injury ratings, performance recovery rates, and comparative player trends.

3. **🏆 Team Analytics Dashboard**
   Measures collective performance drop, recovery rates, and identifies which teams experience the highest injury burdens.

4. **📅 Temporal Patterns Explorer**
   Evaluates injury occurrences over time (months/seasons) and recovery durations to highlight time-based performance trends.

5. **🔬 Advanced Statistics & Correlations**
   Provides analytical metrics such as average recovery rate, injury-to-performance correlation, and statistical summaries.


## Interactive Elements

* Player Name
* Team Name
* Injury Type
* Position
* Season / Year

All analyses and KPIs update dynamically based on user selections. If any input is incorrect or incomplete, the app displays a clear **warning** message notifying the user of mismatched data.

## Key Performance Indicators (KPIs)

* Average Player Rating Before and After Injury
* Performance Drop Index
* Performance Recovery Rate (%)
* Average Injury Duration (Days)
* Team Performance Drop

Each KPI dynamically adjusts based on filters applied and updates in real-time for player and team comparisons.


## Additional Features

* Automated **data cleaning** and missing-value handling
* Conditional **alerts** for incorrect user inputs
* Dynamic **data tables** for detailed summaries
* Export filtered results as **Excel files**
* User-friendly and minimalistic **Streamlit UI design**

## Live Demo

**Dashboard URL:** https://iadai102-2405460--pravargolecha-footballinjury.streamlit.app/

## Snippets of the Project:
<img width="1755" height="787" alt="Screenshot 2025-11-03 235537" src="https://github.com/user-attachments/assets/8a12d11d-75af-4930-9f44-6ed76e109e7e" />
<img width="1826" height="696" alt="Screenshot 2025-11-03 235132" src="https://github.com/user-attachments/assets/f7bcab2e-9e2b-42fe-8f62-8f7aa191c9ab" />
<img width="1797" height="655" alt="Screenshot 2025-11-03 235149" src="https://github.com/user-attachments/assets/50d8c29c-f914-403a-a09c-cda88f09fb76" />
<img width="1809" height="661" alt="Screenshot 2025-11-03 235233" src="https://github.com/user-attachments/assets/8beb29b2-fd19-4da6-a7f7-022db6d54e79" />
<img width="1737" height="768" alt="Screenshot 2025-11-03 235248" src="https://github.com/user-attachments/assets/13a4ee2a-b2d6-4775-9a20-18bf53722a20" />
<img width="1762" height="755" alt="Screenshot 2025-11-03 235304" src="https://github.com/user-attachments/assets/fd2a0d9e-5fd6-40e9-91d0-d6154e4397c1" />
<img width="1831" height="782" alt="Screenshot 2025-11-03 235326" src="https://github.com/user-attachments/assets/aa3546af-620c-4019-9d6e-6a450a28046d" />
<img width="1754" height="788" alt="Screenshot 2025-11-03 235404" src="https://github.com/user-attachments/assets/49f5e2d9-8fe5-4c09-9342-6b4b755d5fe4" />
<img width="1744" height="785" alt="Screenshot 2025-11-03 235430" src="https://github.com/user-attachments/assets/0ad7b3ef-1261-4e6b-b6dd-41ffff0bc018" />
<img width="1776" height="772" alt="Screenshot 2025-11-03 235451" src="https://github.com/user-attachments/assets/99d3e96d-b24c-403f-8a07-0d2740e4f7e1" />
<img width="1750" height="778" alt="Screenshot 2025-11-03 235506" src="https://github.com/user-attachments/assets/0df70789-5750-4def-8457-4a8cc6037965" />
<img width="1754" height="789" alt="Screenshot 2025-11-03 235523" src="https://github.com/user-attachments/assets/4c1c9b39-6efc-4612-8f74-d57c1ce4c486" />


## Project Structure

```
footlens-analytics-pro/
│
├── SAcode.py                # Main Streamlit application (Football Injury Dashboard)
├── requirements.txt          # Python dependencies (for Python 3.11)
├── README.md                 # Repository documentation
├── .gitignore                # Ignored files and folders
│
└── data/
    └── player_injuries_impact.csv   # Dataset used for the analysis
```


## Installation and Setup

### Prerequisites

* Python 3.11 or higher
* pip package manager
* Git (for version control)

### Local Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/footlens-analytics-pro.git
   cd footlens-analytics-pro
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Add the dataset**
   Place your dataset file (`player_injuries_impact.csv`) in the `data/` folder.

5. **Run the dashboard**

   ```bash
   streamlit run SAcode.py
   ```

6. **Open in browser**
   Visit `http://localhost:8501` to explore the dashboard.

## Data Processing Workflow

1. **Data Loading**
   Loads player injury data from CSV and validates structure automatically.

2. **Data Cleaning**

   * Detects and handles missing values
   * Normalizes column names and data types
   * Ensures valid player and injury information

3. **Feature Engineering**

   * Calculates `Performance_Drop_Index`
   * Computes `Performance_Recovery_Rate`
   * Groups by player, team, and injury type

4. **Aggregation & Analysis**

   * Summarizes team-level and player-level injury statistics
   * Analyzes injury severity distribution and recovery durations

5. **Dynamic User Interaction**

   * Filters by player, team, injury, and position
   * Displays “⚠️ Wrong Option Chosen” if no data matches selections


## Business Questions Addressed

| Question                                                | Dashboard Section           | Outcome                                        |
| ------------------------------------------------------- | --------------------------- | ---------------------------------------------- |
| Which injuries cause the largest drop in performance?   | Injury Impact Analysis      | Identifies injury types affecting teams        |
| How do players recover post-injury?                     | Player Performance Insights | Displays recovery rate and consistency         |
| Which teams are most impacted by injuries?              | Team Analytics              | Highlights teams with maximum performance loss |
| How do injuries vary by time period or season?          | Temporal Patterns           | Shows injury trends across months/seasons      |
| What is the relationship between recovery and severity? | Advanced Statistics         | Correlation between severity and recovery      |


## Technology Stack

| Category        | Tool            | Purpose                               |
| --------------- | --------------- | ------------------------------------- |
| Framework       | Streamlit       | Dashboard design and interactivity    |
| Data Processing | Pandas          | Data cleaning and aggregation         |
| Computation     | NumPy & SciPy   | Mathematical and statistical analysis |
| Visualization   | Plotly          | Interactive visualizations            |
| Deployment      | Streamlit Cloud | Cloud hosting and sharing             |
| Version Control | Git & GitHub    | Repository management                 |


## Troubleshooting

| Issue                                | Solution                                                         |
| ------------------------------------ | ---------------------------------------------------------------- |
| `KeyError: 'Performance_Drop_Index'` | Ensure the dataset includes rating columns before and after      |
| Graphs not displaying                | Check if sufficient data exists for visualizations               |
| “Wrong option chosen” displayed      | Verify all input details (player, team, injury type) are correct |
| `ModuleNotFoundError: scipy`         | Run `pip install scipy==1.11.4`                                  |
| Streamlit Cloud dependency errors    | Ensure correct versions in `requirements.txt`                    |


## Future Enhancements

* Machine learning–based injury risk prediction model
* Correlation network between injury type and recovery time
* Comparative analytics between leagues or seasons
* Integration with real-time injury databases
* Automatic PDF export for player injury reports
* Enhanced statistical regression summaries

## Author

**Pravar Golecha**
IBCP Student | CRS: Artificial Intelligence

## Acknowledgments

* Streamlit, Plotly, and Pandas for the visualization and analysis framework

## References

* [Streamlit Documentation](https://docs.streamlit.io/)
* [Plotly Python Docs](https://plotly.com/python/)
* [Pandas Documentation](https://pandas.pydata.org/)
* [SciPy Documentation](https://docs.scipy.org/)
* [SA-Maths 2 Assessment Brief](./docs/)

**Developed by Pravar Golecha | SA- Mathematics II for AI**
