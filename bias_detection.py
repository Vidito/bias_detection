import pandas as pd
import numpy as np
from fairlearn.metrics import MetricFrame, selection_rate, count
from sklearn.metrics import accuracy_score, precision_score
# accuracy/precision require ground truth, for purely generated scores we might focus on selection_rate and mean predictions

def detect_bias(input_file="scored_citizens.csv", output_file="bias_report.csv"):
    df = pd.read_csv(input_file)
    
    # Define sensitive features
    sensitive_features = ['Gender', 'Origin', 'Employment', 'SingleParent', 'Disability', 'HousingStatus']
    
    # We need to define a "favorable outcome" to calculate some metrics like selection_rate
    # Let's assume a score >= 500 is "Qualified" for housing
    df['Qualified'] = (df['SocialUtilityScore'] >= 600).astype(int)
    
    # We can also track the raw score as our 'y_pred' (though it's continuous)
    # Fairlearn MetricFrame can handle continuous predictions for some metrics or custom functions
    
    results = []
    
    for feature in sensitive_features:
        # Calculate metrics for each sensitive feature
        # 1. Selection Rate (proportion of group getting score >= 600)
        # 2. Average Score
        # 3. Count
        
        mf = MetricFrame(
            metrics={
                'selection_rate': selection_rate,
                'average_score': lambda y_true, y_pred: np.mean(y_pred),
                'count': count
            },
            y_true=df['Qualified'], # Placeholder ground truth (not used for selection_rate or simple means but required by API)
            y_pred=df['Qualified'], # For selection rate
            sensitive_features=df[feature]
        )
        
        # We also want average raw score, so let's do a second simple groupby or use MetricFrame with the raw score
        # Note: MetricFrame is flexible.
        
        # Let's make a cleaner MetricFrame using the raw score for average
        mf_score = MetricFrame(
            metrics={'average_raw_score': lambda y_true, y_pred: np.mean(y_pred)},
            y_true=df['Qualified'], # not used
            y_pred=df['SocialUtilityScore'],
            sensitive_features=df[feature]
        )
        
        # Combine
        group_results = mf.by_group.copy()
        group_results['average_raw_score'] = mf_score.by_group['average_raw_score']
        group_results['sensitive_feature'] = feature
        group_results.reset_index(inplace=True)
        group_results.rename(columns={feature: 'group_value'}, inplace=True)
        
        # Add overall metrics for comparison (to calculate disparity later if needed in UI)
        group_results['overall_selection_rate'] = mf.overall['selection_rate']
        group_results['overall_average_raw_score'] = mf_score.overall['average_raw_score']
        
        results.append(group_results)

    final_df = pd.concat(results, ignore_index=True)
    
    # Calculate simple disparities (Difference from overall) or max difference?
    # Let's leave visualization to the UI, just save the metric frame data.
    
    final_df.to_csv(output_file, index=False)
    print(f"Bias report saved to {output_file}")
    return final_df

if __name__ == "__main__":
    detect_bias()
