import pandas as pd
import numpy as np
from bias_detection import detect_bias
import os

def create_dummy_data():
    print("Generating dummy data...")
    # Create a dummy dataframe matching the expected structure
    data = {
        'Age': np.random.randint(18, 90, 100),
        'Gender': np.random.choice(['Male', 'Female', 'Non-Binary'], 100),
        'Origin': np.random.choice(['Native', 'Immigrant-EU', 'Immigrant-NonEU'], 100),
        'Employment': np.random.choice(['Employed', 'Unemployed', 'Student', 'Retired'], 100),
        'Income': np.random.randint(0, 10000, 100),
        'Criminal Record': np.random.choice(['None', 'Minor', 'Major'], 100),
        'Debt History': np.random.choice(['Low', 'High'], 100),
        'SocialUtilityScore': np.random.randint(0, 1000, 100) # Random scores
    }
    df = pd.DataFrame(data)
    df.to_csv("scored_citizens.csv", index=False)
    print("Dummy " + "scored_citizens.csv" + " created.")

def verify():
    # 1. Create Data
    from data_generation import generate_data
    from score_calculation import calculate_scores
    
    print("Generating and SCORING data with new logic...")
    df = generate_data(1000)
    df = calculate_scores(df) # Apply unfair logic
    df.to_csv("scored_citizens.csv", index=False)
    print("New scores generated.")
    
    # 2. Run Bias Detection
    print("Running detect_bias...")
    try:
        results = detect_bias("scored_citizens.csv", "bias_report.csv")
        print("Bias detection ran successfully.")
    except Exception as e:
        print(f"FAILED: bias_detection raised exception: {e}")
        return

    # 3. Check Output
    if not os.path.exists("bias_report.csv"):
        print("FAILED: bias_report.csv was not created.")
        return
        
    print("bias_report.csv found.")
    df_res = pd.read_csv("bias_report.csv")
    print("Output columns:", df_res.columns.tolist())
    
    expected_cols = ['group_value', 'selection_rate', 'average_raw_score', 'sensitive_feature']
    missing = [c for c in expected_cols if c not in df_res.columns]
    
    if missing:
        print(f"FAILED: Missing columns in report: {missing}")
    else:
        print("SUCCESS: Output contains expected columns.")
        print(df_res.head())

if __name__ == "__main__":
    verify()
