# Student Performance Data Analysis

## 1. Project Overview
The "Student Performance Data Analysis" project aims to uncover the various factors that influence the academic success of students. It analyzes a fictional but representative dataset to determine how demographics, lunch types, and test preparation impact student performance on math, reading, and writing exams.

## 2. Technologies Used
- **Python**: Core programming language.
- **Pandas**: Used for data loading, handling missing values, and feature engineering.
- **SQLite**: A lightweight relational database inside standard library to store cleaned data.
- **Matplotlib & Seaborn**: Data visualization libraries to plot scores and draw visual insights.
- **NumPy**: Used to generate dummy dataset.

## 3. Dataset Description
The dataset contains several records of students specifying:
- **gender**: Categorical feature (female/male).
- **parental_education**: Educational background of the student's parents (e.g., high school, bachelor's degree).
- **lunch_type**: The daily lunch a student receives (standard vs. free/reduced) - acts as an economic indicator.
- **test_preparation_course**: Indication if the student completed a preparatory course before testing.
- **math_score**, **reading_score**, **writing_score**: Student scores out of 100 on their respective tests.

*Note: For the sake of this project, if the real dataset isn't immediately available, a mock dataset is generated programmatically on runtime constraint to simulate real conditions.*

## 4. Project Structure
```
student_performance_analysis/
│
├── data/
│   ├── students_performance.csv     # Raw dataset generated initially
│   ├── student_performance.db       # SQLite Database holding clean data
│   └── *.png                        # Output visual plots generated from scripts
│
├── src/
│   ├── generate_dataset.py          # Script to generate a simulated dataset 
│   ├── data_processing.py           # Checks missing values, adds features, and exports to DB
│   └── visualization.py             # Pulls from DB to generate analytics graphs
│
├── requirements.txt                 # Contains libraries required for running the scripts
└── README.md                        # Project documentation (You are here!)
```

## 5. How to Run the Project
1. **Clone the repository** (or download the directory).
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Generate the dummy dataset**:
   ```bash
   python src/generate_dataset.py
   ```
4. **Run the Data Processor**:
   ```bash
   python src/data_processing.py
   ```
   *This cleans data, logs initial analytical summaries to terminal, and stores the processed dataframe into a local SQLite database (`data.student_performance.db`).*
5. **Generate Visualizations**:
   ```bash
   python src/visualization.py
   ```
   *This reads the SQLite database to plot the different graphs and saves them into the `data/` directory.*

## 6. Insights
After querying and plotting the dataset, potential insights normally include:
- **Test Preparation Matters**: Students who completed the test preparation course generally score higher overall on average than those who didn't.
- **Gender Variances**: Performance variations might exist across different exam subjects among genders (e.g., females often outperforming on reading/writing).
- **Financial Situations (Lunch)**: Historically (with this data logic), standard lunch (which assumes no financial aid logic) typically correlates with higher scores than free/reduced lunches, showcasing socioeconomic elements influencing student performance.
