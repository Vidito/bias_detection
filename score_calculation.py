import pandas as pd
import numpy as np

def calculate_scores(df):
    """
    Calculates the Social Utility Score based on:
    + Employment (Steady = High score)
    + Income (Higher = High score)
    - Criminal Record (Major = Huge penalty)
    - Debt (High = Penalty)
    """
    scores = []
    
    for _, row in df.iterrows():
        base_score = 500 # Starting score
        
        # Employment Impact
        if row['Employment'] == 'Employed':
            base_score += 150
        elif row['Employment'] == 'Retired':
            base_score += 50
        elif row['Employment'] == 'Student':
            base_score += 20
        elif row['Employment'] == 'Unemployed':
            base_score -= 100
            
        # Income Impact
        income_bonus = min(200, row['Income'] / 250) 
        base_score += income_bonus
        
        # Criminal Record Impact
        if row['Criminal Record'] == 'Major':
            base_score -= 300
        elif row['Criminal Record'] == 'Minor':
            base_score -= 100
            
        # Debt Impact
        if row['Debt History'] == 'High':
            base_score -= 150
        elif row['Debt History'] == 'Low':
            base_score -= 50
            
        # New "Risk" Penalties (The Unfairness)
        
        # Single Parent Penalty (Simulating "Economic Risk" bias)
        if row['SingleParent']:
            base_score -= 50
            
        # Disability Penalty (Simulating "Cost/Modification Risk" bias)
        if row['Disability']:
            base_score -= 50
            
        # Housing Status Penalty (Circular Logic: "At Risk" people are "Risky Tenants")
        if row['HousingStatus'] == 'AtRisk':
            base_score -= 150
        elif row['HousingStatus'] == 'Overcrowded':
            base_score -= 50
            
        # Clamp score between 0 and 1000
        final_score = max(0, min(1000, base_score))
        scores.append(int(final_score))
        
    df['SocialUtilityScore'] = scores
    return df

if __name__ == "__main__":
    df = pd.read_csv("citizens_2030.csv")
    df = calculate_scores(df)
    print(df[['Name', 'SocialUtilityScore']].head())
    df.to_csv("scored_citizens.csv", index=False)
    print("Scored data saved to scored_citizens.csv")
