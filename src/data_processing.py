import pandas as pd
import sqlite3

def clean_data(df):
    """Clean the loaded dataset by handling missing values."""
    print("Initial missing values:")
    print(df.isnull().sum())
    
    # Fill any missing math_score values with the median
    if df['math_score'].isnull().any():
        median_math = df['math_score'].median()
        df['math_score'].fillna(median_math, inplace=True)
    
    print("\nMissing values after cleaning:")
    print(df.isnull().sum())
    return df

def feature_engineering(df):
    """Add new features like the average score."""
    # Ensure scores are numeric
    score_cols = ['math_score', 'reading_score', 'writing_score']
    for col in score_cols:
        df[col] = pd.to_numeric(df[col])
        
    df['average_score'] = df[score_cols].mean(axis=1).round(2)
    return df

def store_in_db(df, db_name='data/student_performance.db'):
    """Store the cleaned dataframe inside an SQLite database."""
    conn = sqlite3.connect(db_name)
    try:
        # Save table. Replace if exists.
        df.to_sql('students', conn, if_exists='replace', index=False)
        print(f"\nData successfully stored inside {db_name} SQLite DB.")
    finally:
        conn.close()

def analyze_performance(db_name='data/student_performance.db'):
    """Query data from SQLite to perform analysis."""
    conn = sqlite3.connect(db_name)
    
    print("\n--- PERFORMANCE ANALYSIS ---")
    
    # 1. Average score by Gender
    print("\nAverage Scores by Gender:")
    query_gender = '''
        SELECT gender, round(avg(math_score), 2) as avg_math, 
                       round(avg(reading_score), 2) as avg_reading, 
                       round(avg(writing_score), 2) as avg_writing,
                       round(avg(average_score), 2) as avg_overall
        FROM students 
        GROUP BY gender
    '''
    df_gender = pd.read_sql(query_gender, conn)
    print(df_gender)
    
    # 2. Average score by Test Preparation Course
    print("\nAverage Scores by Test Preparation Course:")
    query_prep = '''
        SELECT test_preparation_course, 
               round(avg(average_score), 2) as avg_overall
        FROM students 
        GROUP BY test_preparation_course
    '''
    df_prep = pd.read_sql(query_prep, conn)
    print(df_prep)

    conn.close()

if __name__ == "__main__":
    file_path = "data/students_performance.csv"
    
    print(f"Loading data from {file_path}...")
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print("Please run 'src/generate_dataset.py' to generate the mock dataset first.")
        exit(1)
        
    cleaned_data = clean_data(data)
    engineered_data = feature_engineering(cleaned_data)
    store_in_db(engineered_data)
    
    analyze_performance()
