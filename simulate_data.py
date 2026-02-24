import pandas as pd
import numpy as np

def simulate_indian_demand(start_date="2025-01-01", days=30):
    rng = pd.date_range(start_date, periods=24 * days, freq="H")
    n = len(rng)
    
    # Base demand (MW) — choose a scale. e.g. city level between 500 and 2000 MW
    base = 800  # base constant demand
    daily_amp = 400  # amplitude of daily cycle
    weekly_amp = 100  # difference weekend vs weekday
    
    # Hour-of-day effect: a sinusoidal + more weight in afternoon
    hour = rng.hour
    daily_pattern = np.sin((hour / 24) * 2 * np.pi)  # from 0 to 1 cycle
    
    # Weekday vs weekend modifier
    weekday = rng.weekday  # 0=Monday .. 6=Sunday
    weekend = (weekday >= 5).astype(int)
    week_modifier = 1 - weekend * 0.15  # reduce demand ~15% on weekends
    
    # Seasonal / heat effect: add random “hot day” spikes
    # Let's simulate small temp-driven random variation
    temp_effect = np.random.normal(0, 0.05, size=n)  # ± around 5%
    
    # Combine all
    demand = base + daily_amp * daily_pattern
    demand = demand * week_modifier
    demand = demand * (1 + temp_effect)
    
    # Add random noise
    noise = np.random.normal(0, 20, size=n)  # ±20 MW noise
    demand = demand + noise
    
    # Ensure non-negative
    demand = np.clip(demand, a_min=0, a_max=None)
    
    df = pd.DataFrame({
        "datetime": rng,
        "demand": demand
    })
    return df

# Usage
df = simulate_indian_demand("2025-10-01", days=30)
df.to_csv("simulated_indian_demand.csv", index=False)
print(df.head())
