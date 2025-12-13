import pandas as pd
import numpy as np
from faker import Faker
import random

# Initialize Faker
fake = Faker('de_DE')
Faker.seed(42)
np.random.seed(42)

def generate_data(num_records=1000):
    """
    Generates mock data for the 2030 Germany Housing Crisis scenario.
    """
    data = []
    
    # German Demographics (Approximate for 2030)
    # Origin: Native, EU-Migrant, Non-EU-Migrant
    origins = ['Native', 'EU-Migrant', 'Non-EU-Migrant']
    origin_probs = [0.75, 0.10, 0.15]
    
    # Gender
    genders = ['Male', 'Female', 'Non-Binary']
    gender_probs = [0.49, 0.49, 0.02]
    
    for _ in range(num_records):
        # Basic Demographics
        # 0. Gender & Origin
        gender = np.random.choice(genders, p=gender_probs)
        age = np.random.randint(18, 90)
        origin = np.random.choice(origins, p=origin_probs)

        # 1. Disability Status (Moved up to influence other factors)
        # Random distribution, roughly 10%
        disability = np.random.choice([True, False], p=[0.1, 0.9])
        
        # Name (based on origin for realism, though Faker 'de_DE' is mostly German)
        if origin == 'Native':
            name = fake.name()
        else:
            name = fake.name() 

        # Employment Status
        # Higher unemployment typically for migrants AND people with disabilities (Bias scenario)
        if disability:
             # Systemic barrier simulation: Higher unemployment/retired rate for disabled
             emp_probs = [0.3, 0.2, 0.05, 0.45] # Employed, Unemployed, Student, Retired
             emp_status = np.random.choice(['Employed', 'Unemployed', 'Student', 'Retired'], p=emp_probs)
        elif origin == 'Native':
            emp_status = np.random.choice(['Employed', 'Unemployed', 'Student', 'Retired'], p=[0.7, 0.05, 0.05, 0.2])
        else:
            emp_status = np.random.choice(['Employed', 'Unemployed', 'Student', 'Retired'], p=[0.5, 0.2, 0.1, 0.2])
            
        # Annual Income (Euro)
        if emp_status == 'Employed':
            base_income = np.random.normal(50000, 15000)
        elif emp_status == 'Retired':
            base_income = np.random.normal(25000, 5000)
        else:
            base_income = np.random.normal(12000, 3000) # Welfare level
            
        # Adjust income based on origin AND Disability (bias injection)
        if origin != 'Native':
            base_income *= 0.8
        
        if disability:
            base_income *= 0.7 # Wage gap / part-time constraint simulation
            
        income = max(0, int(base_income))

        # Criminal Record (0 = None, 1 = Minor, 2 = Major)
        # Higher policing in certain areas -> higher record prob (bias)
        if origin == 'Non-EU-Migrant':
            crim_choice = np.random.choice([0, 1, 2], p=[0.85, 0.10, 0.05])
        else:
            crim_choice = np.random.choice([0, 1, 2], p=[0.95, 0.04, 0.01])
            
        record_map = {0: 'None', 1: 'Minor', 2: 'Major'}
        criminal_record = record_map[crim_choice]

        # Debt History (0 = No debt, 1 = Some debt, 2 = Heavy debt)
        if income < 20000:
             debt_prob = [0.4, 0.4, 0.2]
        else:
             debt_prob = [0.8, 0.15, 0.05]
        
        debt_choice = np.random.choice([0, 1, 2], p=debt_prob)
        debt_map = {0: 'None', 1: 'Low', 2: 'High'}
        debt_history = debt_map[debt_choice]
        
        # New Vulnerable Groups (SingleParent - logic here or earlier)
        # Single Parent Status
        if income < 30000:
            single_parent_prob = 0.3
        else:
            single_parent_prob = 0.1
        single_parent = np.random.choice([True, False], p=[single_parent_prob, 1-single_parent_prob])

        # 3. Current Housing Status (Risk Factor)
        # Highly correlated with Income and Origin
        if income < 20000 or origin == 'Non-EU-Migrant':
            housing_probs = [0.4, 0.4, 0.2] # Stable, Overcrowded, AtRisk
        else:
            housing_probs = [0.9, 0.08, 0.02]
            
        housing_status = np.random.choice(['Stable', 'Overcrowded', 'AtRisk'], p=housing_probs)

        data.append({
            'Name': name,
            'Age': age,
            'Gender': gender,
            'Origin': origin,
            'Employment': emp_status,
            'Income': income,
            'Criminal Record': criminal_record,
            'Debt History': debt_history,
            'SingleParent': single_parent,
            'Disability': disability,
            'HousingStatus': housing_status
        })
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_data(1000)
    print(df.head())
    df.to_csv("citizens_2030.csv", index=False)
    print("Data saved to citizens_2030.csv")
