# OptiLive: Social Utility Score Audit (2030 Scenario)

This project demonstrates algorithmic bias in a fictional 2030 housing crisis scenario. It simulates a "Social Utility Score" algorithm used to allocate public housing and exposes how systemic biases (like penalties for unemployment, debt, or disability) exclude vulnerable populations.

## Project Structure
- `data_generation.py`: Generates synthetic population data with baked-in systemic inequalities (wage gaps, unemployment risks).
- `score_calculation.py`: The "black box" algorithm that scores citizens. It includes unfair penalties for proxies of poverty.
- `bias_detection.py`: Uses the **Fairlearn** library to audit the scoring algorithm and detect disparities in Selection Rates.
- `app.py`: A Streamlit dashboard to interactively generate data, score citizens, and visualize the bias.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the dashboard:
```bash
streamlit run app.py
```

1. **Control Panel**: Set the number of citizens and random seed.
2. **Generate & Score**: Click to create a new batch of 2030 citizens.
3. **Data Explorer**: View the raw demographics and stats.
4. **Bias Audit**: Run the Fairlearn analysis to see how Single Parents, People with Disabilities, and Migrants are systematically disadvantaged.

## Disclaimer
This is a **simulation** for educational and auditing demonstration purposes (specially for my Data Ethics project). The biases implemented are intentional to showcase how algorithms can amplify existing social inequalities.
