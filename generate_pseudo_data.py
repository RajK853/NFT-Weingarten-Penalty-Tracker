import pandas as pd
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
from utils import Constants # Import Constants from utils

def generate_pseudo_data(start_date: str = "2024-01-01", end_date: str = "2024-12-31", penalties_per_player_per_day: int = 3) -> pd.DataFrame:
    """
    Generates pseudo penalty shootout data with more realistic distributions.

    Args:
        start_date (str): The start date for the data in 'YYYY-MM-DD' format.
        end_date (str): The end date for the data in 'YYYY-MM-DD' format.
        penalties_per_player_per_day (int): Number of penalties each player takes per day.

    Returns:
        pd.DataFrame: A DataFrame containing the generated pseudo data.
    """

    shooters: List[str] = ["Aadesh", "Bikash", "Biraj", "Gaganshing", "Arbin", "Anupam", "Binod", "Gautam", "Bhuwan", "Bhawani", "Gopal", "Raj", "Prashant", "Manglunghang", "Sujan", "Prabhat", "Sishir", "Yukpuhang", "Mojamil", "Govin", "Ritik"]
    keepers: List[str] = ["Nawaraj", "Prabin"]
    statuses: List[str] = [Constants.GOAL_STATUS, Constants.SAVED_STATUS, Constants.OUT_STATUS]
    shoot_positions: List[str] = ["top-left", "top-right", "bottom-left", "bottom-right", "center-left", "center-right", "center-top", "center-bottom"]

    # Define a pool of status probability distributions
    status_distributions_pool: List[List[float]] = [
        [0.60, 0.20, 0.20], [0.70, 0.15, 0.15], [0.50, 0.30, 0.20], [0.65, 0.20, 0.15],
        [0.75, 0.10, 0.15], [0.55, 0.25, 0.20], [0.80, 0.10, 0.10], [0.60, 0.30, 0.10]
    ]

    # Define a pool of position probability distributions
    position_distributions_pool: List[List[float]] = [
        [0.20, 0.20, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10], [0.10, 0.10, 0.20, 0.20, 0.10, 0.10, 0.10, 0.10],
        [0.10, 0.10, 0.10, 0.10, 0.20, 0.20, 0.10, 0.10], [0.20, 0.10, 0.10, 0.10, 0.10, 0.10, 0.15, 0.15],
        [0.10, 0.20, 0.10, 0.10, 0.10, 0.10, 0.15, 0.15], [0.15, 0.15, 0.10, 0.10, 0.10, 0.10, 0.10, 0.20],
        [0.10, 0.10, 0.15, 0.15, 0.10, 0.10, 0.20, 0.10], [0.10, 0.10, 0.10, 0.10, 0.10, 0.20, 0.15, 0.25]
    ]

    # Randomly assign probability distributions to each player
    player_probabilities: Dict[str, Dict[str, List[float]]] = {}
    for shooter in shooters:
        player_probabilities[shooter] = {
            "status": random.choice(status_distributions_pool),
            "position": random.choice(position_distributions_pool)
        }

    data_list: List[List[Any]] = []
    start_dt: datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt: datetime = datetime.strptime(end_date, "%Y-%m-%d")

    all_dates: List[datetime] = [start_dt + timedelta(days=i) for i in range((end_dt - start_dt).days + 1)]

    # Group dates by week
    dates_by_week: Dict[Tuple[int, int], List[datetime]] = {}
    for d in all_dates:
        # Using ISO calendar week number (Monday is 1)
        week_num: int = d.isocalendar()[1]
        year_num: int = d.isocalendar()[0]
        if (year_num, week_num) not in dates_by_week:
            dates_by_week[(year_num, week_num)] = []
        dates_by_week[(year_num, week_num)].append(d)

    selected_dates: List[datetime] = []
    for week_key, days_in_week in dates_by_week.items():
        # Randomly select 3 to 4 days from each week
        num_days_to_select: int = random.randint(Constants.MIN_DAYS_PER_WEEK, Constants.MAX_DAYS_PER_WEEK)
        selected_dates.extend(random.sample(days_in_week, min(num_days_to_select, len(days_in_week))))

    selected_dates.sort() # Ensure dates are in chronological order

    for current_date in selected_dates:
        # Randomly select one goalkeeper for the day
        daily_keeper: str = random.choice(keepers)

        for shooter in shooters:
            for _ in range(penalties_per_player_per_day):
                # Use player-specific probabilities for status and position
                status: str = random.choices(statuses, weights=player_probabilities[shooter]["status"], k=1)[0]
                position: str = random.choices(shoot_positions, weights=player_probabilities[shooter]["position"], k=1)[0]

                data_list.append([current_date.strftime("%m/%d/%Y"), shooter, daily_keeper, status, position])

    df = pd.DataFrame(data_list, columns=[Constants.DATE_COL, Constants.SHOOTER_NAME_COL, Constants.KEEPER_NAME_COL, Constants.STATUS_COL, Constants.SHOOT_POSITION_COL])
    return df

if __name__ == "__main__":
    # Example usage:
    # Generate data for the year 2025, with each player taking 3 penalties per day
    pseudo_df: pd.DataFrame = generate_pseudo_data(start_date="2025-01-01", end_date="2025-12-31", penalties_per_player_per_day=3)
    
    # Save to CSV
    output_path: str = Constants.PSEUDO_DATA_OUTPUT_PATH
    pseudo_df.to_csv(output_path, index=False)
    print(f"Generated {len(pseudo_df)} records and saved to {output_path}")
