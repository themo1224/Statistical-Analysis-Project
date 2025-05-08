import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import arabic_reshaper
from bidi.algorithm import get_display
import os

# Set up font for Persian text
plt.rcParams['font.family'] = 'DejaVu Sans'  # This font supports Persian
mpl.rcParams['axes.unicode_minus'] = False

# Function to handle Persian text
def process_persian_text(text):
    reshaped_text = arabic_reshaper.reshape(str(text))
    return get_display(reshaped_text)

# Read the data
df = pd.read_csv('data/Job.csv')

# Map Persian gender labels to more readable format
gender_mapping = {
    'تفاوتی ندارد': 'No Preference - تفاوتی ندارد',
    'فقط آقا': 'Men Only - فقط آقا',
    'فقط خانم': 'Women Only - فقط خانم',
    'ترجیحاً خانم': 'Preferred Women - ترجیحاً خانم',
    'ترجیحاً آقا': 'Preferred Men - ترجیحاً آقا'
}

def analyze_hiring_patterns():
    print("\n=== Who Gets Hired? - Gender Preference & Company Size Analysis ===")
    
    # 1. Basic Frequency Table for Gender Preferences
    print("\nGender Preference Distribution:")
    gender_dist = df['gender'].value_counts()
    print(gender_dist)
    
    # 2. Create Company Size Categories
    df['company_size_numeric'] = pd.to_numeric(df['company_size'], errors='coerce')
    
    size_labels = ['Small - کوچک', 'Medium - متوسط', 'Large - بزرگ', 'Enterprise - سازمان']
    df['company_size_category'] = pd.cut(df['company_size_numeric'], 
                                       bins=[0, 50, 200, 1000, float('inf')],
                                       labels=size_labels)
    
    # 3. Cross Tabulation of Gender vs Company Size
    print("\nGender Preference by Company Size:")
    cross_tab = pd.crosstab(df['gender'].map(lambda x: gender_mapping.get(x, x)), 
                           df['company_size_category'])
    print(cross_tab)
    
    # 4. Calculate Percentages
    print("\nPercentage Distribution:")
    percentage_dist = cross_tab.div(cross_tab.sum(axis=0), axis=1) * 100
    print(percentage_dist.round(2))
    return cross_tab

def create_visualizations():
    try:
        # Create a figure with two subplots
        plt.figure(figsize=(20, 8))
        
        # 1. Gender Distribution Bar Plot
        plt.subplot(1, 2, 1)
        gender_counts = df['gender'].map(lambda x: gender_mapping.get(x, x)).value_counts()
        ax1 = gender_counts.plot(kind='bar')
        plt.title('Gender Preferences Distribution\nتوزیع ترجیحات جنسیتی', fontsize=14, pad=20)
        plt.xlabel('Gender Preference - جنسیت', fontsize=12)
        plt.ylabel('Count - تعداد', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        
        # Adjust label sizes for readability
        ax1.tick_params(axis='x', labelsize=10)
        
        # 2. Gender Distribution by Company Size
        plt.subplot(1, 2, 2)
        cross_tab = pd.crosstab(df['gender'].map(lambda x: gender_mapping.get(x, x)), 
                               df['company_size_category'])
        ax2 = cross_tab.plot(kind='bar', stacked=True)
        plt.title('Gender Preferences by Company Size\nترجیحات جنسیتی بر اساس اندازه شرکت', 
                  fontsize=14, pad=20)
        plt.xlabel('Gender Preference - جنسیت', fontsize=12)
        plt.ylabel('Count - تعداد', fontsize=12)
        plt.legend(title='Company Size - اندازه شرکت', bbox_to_anchor=(1.05, 1))
        plt.xticks(rotation=45, ha='right')
        
        # Adjust label sizes for readability
        ax2.tick_params(axis='x', labelsize=10)
        
        # Ensure the layout is tight but with room for Persian text
        plt.tight_layout()
        
        # Save the plot with high resolution
        output_path = 'hiring_analysis.png'
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()
        
        # Verify the file was created
        if os.path.exists(output_path):
            print(f"\nVisualization saved successfully to {output_path}")
            print(f"File size: {os.path.getsize(output_path)} bytes")
        else:
            print("\nError: Visualization file was not created")
            
    except Exception as e:
        print(f"\nError creating visualizations: {str(e)}")

if __name__ == "__main__":
    print("Starting Analysis...")
    analyze_hiring_patterns()
    create_visualizations()
    print("\nAnalysis complete!")