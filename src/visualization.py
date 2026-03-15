import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

def fetch_data(db_name='data/student_performance.db'):
    """Fetch cleaned data from SQLite database."""
    conn = sqlite3.connect(db_name)
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    return df

def plot_score_distribution(df):
    """Plot the distribution of the average scores."""
    plt.figure(figsize=(10, 6))
    sns.histplot(df['average_score'], bins=20, kde=True, color='skyblue')
    plt.title('Distribution of Average Scores')
    plt.xlabel('Average Score')
    plt.ylabel('Frequency')
    
    # Save the plot
    plt.savefig('data/score_distribution_plot.png')
    print("Saved score distribution plot to data/score_distribution_plot.png")
    plt.show()

def plot_performance_by_gender(df):
    """Boxplot comparing average score between genders."""
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='gender', y='average_score', data=df, palette='Set2')
    plt.title('Performance Breakdown by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Average Score')
    
    plt.savefig('data/performance_by_gender.png')
    print("Saved performance by gender plot to data/performance_by_gender.png")
    plt.show()

def plot_prep_course_impact(df):
    """Bar plot representing test preparation course impact."""
    # Compute the average overall score across test prep types
    avg_prep = df.groupby('test_preparation_course')['average_score'].mean().reset_index()
    
    plt.figure(figsize=(8, 6))
    sns.barplot(x='test_preparation_course', y='average_score', data=avg_prep, palette='pastel')
    plt.title('Impact of Test Preparation Course on Average Score')
    plt.xlabel('Test Preparation Course')
    plt.ylabel('Average Overall Score')
    plt.ylim(0, 100)
    
    # Annotate bars
    for index, row in avg_prep.iterrows():
        plt.text(index, row.average_score + 1, round(row.average_score, 2), color='black', ha="center")
        
    plt.savefig('data/prep_course_impact.png')
    print("Saved test prep course impact plot to data/prep_course_impact.png")
    plt.show()

if __name__ == "__main__":
    try:
        data = fetch_data()
        
        sns.set_theme(style='whitegrid')
        print("Rendering visualizations...")
        
        plot_score_distribution(data)
        plot_performance_by_gender(data)
        plot_prep_course_impact(data)
        
    except sqlite3.OperationalError:
        print("Database not found. Please run 'src/data_processing.py' first.")
