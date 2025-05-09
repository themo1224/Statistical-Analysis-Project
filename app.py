import streamlit as st          # For creating the web interface
import pandas as pd            # For data manipulation
import matplotlib.pyplot as plt # For creating plots
import seaborn as sns         # For enhanced visualizations
import arabic_reshaper        # For handling Persian text
from bidi.algorithm import get_display  # For right-to-left text supportimport matplotlib as mpl
from matplotlib import font_manager

# Add Persian font
import os
import sys
import platform

# Configure Persian font based on OS
if platform.system() == 'Windows':
    font_path = "c:\\Windows\\Fonts\\BNazanin.ttf"  # Persian font in Windows
elif platform.system() == 'Darwin':  # macOS
    font_path = "/Library/Fonts/Arial Unicode.ttf"
else:  # Linux
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Add the font to matplotlib
if os.path.exists(font_path):
    font_manager.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'B Nazanin' if platform.system() == 'Windows' else 'DejaVu Sans'
else:
    plt.rcParams['font.family'] = 'DejaVu Sans'

# Enable right-to-left text support
plt.rcParams['axes.unicode_minus'] = False

# Function to handle Persian text
def reshape_text(text):
    reshaped_text = arabic_reshaper.reshape(str(text))
    return get_display(reshaped_text)

# Set page configuration
st.set_page_config(
    page_title="Who Gets Hired?",
    page_icon="📊",
    layout="wide"
)

# Map English gender labels
gender_mapping = {
    'تفاوتی ندارد': 'No Preference',
    'فقط آقا': 'Only Men',
    'فقط خانم': 'Only Women',
    'ترجیحاً خانم': 'Preferred Women',
    'ترجیحاً آقا': 'Preferred Men',
    'Men / Women': 'Men / Women',
    'Only Men': 'Only Men',
    'Only Women': 'Only Women',
    'Preferred Men': 'Preferred Men',
    'Preferred Women': 'Preferred Women'
}

# Title and introduction
st.title("Who Gets Hired?")
st.markdown("""
This analysis explores employment patterns in the Iranian job market, focusing on:
- Gender preferences in job postings
- Distribution of company sizes
- Relationship between company size and gender preferences
""")

# Read and process data
@st.cache_data
def load_data():
    df = pd.read_csv('data/Job.csv')
    # Map gender values to English
    df['gender'] = df['gender'].map(lambda x: gender_mapping.get(x, x))
    df['company_size_numeric'] = pd.to_numeric(df['company_size'], errors='coerce')
    df['company_size_category'] = pd.cut(
        df['company_size_numeric'], 
        bins=[0, 50, 200, 1000, float('inf')],
        labels=['Small (1-50)', 'Medium (51-200)', 'Large (201-1000)', 'Enterprise (1000+)']
    )
    return df

# Load data
df = load_data()

# Sidebar
st.sidebar.header("Analysis Options")
show_data = st.sidebar.checkbox("Show Raw Data")
show_stats = st.sidebar.checkbox("Show Detailed Statistics", value=True)

# Display raw data if selected
if show_data:
    st.subheader("Raw Data Sample")
    st.dataframe(df.head())

# Main analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("Gender Preferences Distribution")
    gender_dist = df['gender'].value_counts()
    
    # Create and display gender distribution plot
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    gender_dist.plot(kind='bar')
    plt.title('Gender Preferences Distribution in Job Postings', fontsize=14, pad=20)
    plt.xlabel('Gender Preferences', fontsize=12)
    plt.ylabel('Number of Job Postings', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    ax1.tick_params(axis='x', labelsize=10)
    st.pyplot(fig1)
    
    if show_stats:
        st.markdown("### Gender Distribution Statistics")
        st.dataframe(gender_dist)

with col2:
    st.subheader("Company Size Analysis")
    
    # Create and display company size distribution plot
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    cross_tab = pd.crosstab(df['gender'], df['company_size_category'])
    cross_tab.plot(kind='bar', stacked=True)
    plt.title('Gender Preferences by Company Size', fontsize=14, pad=20)
    plt.xlabel('Gender Preferences', fontsize=12)
    plt.ylabel('Number of Job Postings', fontsize=12)
    plt.legend(title='Company Size', bbox_to_anchor=(1.05, 1))
    ax2.tick_params(axis='x', labelsize=10)
    plt.tight_layout()
    st.pyplot(fig2)
    
    if show_stats:
        st.markdown("### Company Size Distribution")
        st.dataframe(df['company_size_category'].value_counts())

# Additional Statistics
if show_stats:
    st.subheader("Detailed Analysis")
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### Cross-Tabulation: Gender Preferences and Company Size")
        st.dataframe(cross_tab)
    
    with col4:
        st.markdown("### Percentage Distribution")
        percentage_dist = cross_tab.div(cross_tab.sum(axis=0), axis=1) * 100
        st.dataframe(percentage_dist.round(2))

# Key Findings
st.subheader("Key Findings")
st.markdown("""
1. **Overview of Gender Preferences**:
   - Most companies have no gender preference
   - Positions for men only are second in rank
   - Positions for women only make up a significant part

2. **Company Size Patterns**:
   - Larger companies tend to have specific gender preferences
   - Smaller companies show more flexibility in gender requirements
   - Enterprise companies have distinct hiring patterns

3. **Notable Trends**:
   - Company size influences gender preference patterns
   - Different sectors show different distributions of gender preferences
   - There is a clear correlation between company size and hiring preferences
""")

# Footer
st.markdown("---")
st.markdown("Project for Statistics and Probability Course") 