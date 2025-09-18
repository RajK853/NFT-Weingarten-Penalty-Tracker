import pandas as pd
import random
from datetime import datetime, timedelta

def generate_pseudo_data(start_date="2024-01-01", end_date="2024-12-31", penalties_per_player_per_day=3):
    """
    Generates pseudo penalty shootout data with more realistic distributions.

    Args:
        start_date (str): The start date for the data in 'YYYY-MM-DD' format.
        end_date (str): The end date for the data in 'YYYY-MM-DD' format.
        penalties_per_player_per_day (int): Number of penalties each player takes per day.

    Returns:
        pd.DataFrame: A DataFrame containing the generated pseudo data.
    """

    shooters = ["Aadesh", "Bikash", "Biraj", "Gaganshing", "Arbin", "Anupam", "Binod", "Gautam", "Bhuwan", "Bhawani", "Gopal", "Raj", "Prashant", "Manglunghang", "Sujan", "Prabhat", "Sishir", "Yukpuhang", "Mojamil", "Govin", "Ritik"]
    keepers = ["Nawaraj", "Prabin"]
    statuses = ["goal", "saved", "out"]
    shoot_positions = ["top-left", "top-right", "bottom-left", "bottom-right", "center-left", "center-right", "center-top", "center-bottom"]

    # Define a pool of status probability distributions
    status_distributions_pool = [
        [0.60, 0.20, 0.20], [0.70, 0.15, 0.15], [0.50, 0.30, 0.20], [0.65, 0.20, 0.15],
        [0.75, 0.10, 0.15], [0.55, 0.25, 0.20], [0.80, 0.10, 0.10], [0.60, 0.30, 0.10]
    ]

    # Define a pool of position probability distributions
    position_distributions_pool = [
        [0.20, 0.20, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10], [0.10, 0.10, 0.20, 0.20, 0.10, 0.10, 0.10, 0.10],
        [0.10, 0.10, 0.10, 0.10, 0.20, 0.20, 0.10, 0.10], [0.20, 0.10, 0.10, 0.10, 0.10, 0.10, 0.15, 0.15],
        [0.10, 0.20, 0.10, 0.10, 0.10, 0.10, 0.15, 0.15], [0.15, 0.15, 0.10, 0.10, 0.10, 0.10, 0.10, 0.20],
        [0.10, 0.10, 0.15, 0.15, 0.10, 0.10, 0.20, 0.10], [0.10, 0.10, 0.10, 0.10, 0.10, 0.20, 0.15, 0.25]
    ]

    # Randomly assign probability distributions to each player
    player_probabilities = {}
    for shooter in shooters:
        player_probabilities[shooter] = {
            "status": random.choice(status_distributions_pool),
            "position": random.choice(position_distributions_pool)
        }

    data = []
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    all_dates = [start + timedelta(days=i) for i in range((end - start).days + 1)]

    # Group dates by week
    dates_by_week = {}
    for d in all_dates:
        # Using ISO calendar week number (Monday is 1)
        week_num = d.isocalendar()[1]
        year_num = d.isocalendar()[0]
        if (year_num, week_num) not in dates_by_week:
            dates_by_week[(year_num, week_num)] = []
        dates_by_week[(year_num, week_num)].append(d)

    selected_dates = []
    for week_key, days_in_week in dates_by_week.items():
        # Randomly select 3 to 4 days from each week
        num_days_to_select = random.randint(3, 4)
        selected_dates.extend(random.sample(days_in_week, min(num_days_to_select, len(days_in_week))))

    selected_dates.sort() # Ensure dates are in chronological order

    for current_date in selected_dates:
        # Randomly select one goalkeeper for the day
        daily_keeper = random.choice(keepers)

        for shooter in shooters:
            for _ in range(penalties_per_player_per_day):
                # Use player-specific probabilities for status and position
                status = random.choices(statuses, weights=player_probabilities[shooter]["status"], k=1)[0]
                position = random.choices(shoot_positions, weights=player_probabilities[shooter]["position"], k=1)[0]

                data.append([current_date.strftime("%m/%d/%Y"), shooter, daily_keeper, status, position])

    df = pd.DataFrame(data, columns=["Date", "Shooter Name", "Keeper Name", "Status", "Shoot Position"])
    return df

if __name__ == "__main__":
    # Example usage:
    # Generate data for the year 2025, with each player taking 3 penalties per day
    pseudo_df = generate_pseudo_data(start_date="2025-01-01", end_date="2025-12-31", penalties_per_player_per_day=3)
    
    # Save to CSV
    output_path = "data/penalty.csv"
    pseudo_df.to_csv(output_path, index=False)
    print(f"Generated {len(pseudo_df)} records and saved to {output_path}")