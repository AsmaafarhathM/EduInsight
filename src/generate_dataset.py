import pandas as pd
import numpy as np

def create_mock_data():
    np.random.seed(42)
    n_students = 1000
    
    genders = ['female', 'male']
    educations = ["bachelor's degree", 'some college', "master's degree", "associate's degree", 'high school', 'some high school']
    lunches = ['standard', 'free/reduced']
    test_preps = ['none', 'completed']
    
    data = {
        'gender': np.random.choice(genders, n_students),
        'parental_education': np.random.choice(educations, n_students),
        'lunch_type': np.random.choice(lunches, n_students),
        'test_preparation_course': np.random.choice(test_preps, n_students),
        'math_score': np.random.normal(loc=65, scale=15, size=n_students).clip(0, 100).astype(int),
        'reading_score': np.random.normal(loc=68, scale=14, size=n_students).clip(0, 100).astype(int),
        'writing_score': np.random.normal(loc=67, scale=15, size=n_students).clip(0, 100).astype(int)
    }
    
    df = pd.DataFrame(data)
    
    # Introduce some logical correlations:
    # E.g., completing the test prep slightly increases scores
    df.loc[df['test_preparation_course'] == 'completed', ['math_score', 'reading_score', 'writing_score']] += 5
    
    # Ensure scores don't exceed 100 after addition
    df[['math_score', 'reading_score', 'writing_score']] = df[['math_score', 'reading_score', 'writing_score']].clip(upper=100)
    
    # Create a few basic nulls for cleaning practice
    df.loc[np.random.choice(df.index, size=15), 'math_score'] = np.nan
    
    df.to_csv('data/students_performance.csv', index=False)
    print("Dataset generated and saved to data/students_performance.csv")

if __name__ == "__main__":
    create_mock_data()
