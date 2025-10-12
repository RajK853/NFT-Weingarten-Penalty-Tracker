import random
from datetime import datetime, timedelta
from typing import Any, Dict, List

import pandas as pd

from src.constants import Columns, Data, Paths, Status

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

    shooters: List[str] = ["Pelé", "Diego Maradona", "Lionel Messi", "Cristiano Ronaldo", "Johan Cruyff", "Franz Beckenbauer", "Zinedine Zidane", "Ronaldo Nazário", "George Best", "Alfredo Di Stéfano", "Eusébio", "Gerd Müller", "Michel Platini", "Roberto Baggio", "Ronaldinho", "Thierry Henry", "Kaká", "Luka Modrić", "Mohamed Salah", "Kylian Mbappé"]
    keepers: List[str] = ["Lev Yashin", "Gianluigi Buffon", "Iker Casillas", "Manuel Neuer", "Peter Schmeichel", "Oliver Kahn", "Dino Zoff", "Gordon Banks", "Edwin van der Sar", "Petr Čech"]
    statuses: List[str] = [Status.GOAL, Status.SAVED, Status.OUT]
    remarks: List[int] = [11, 12, 13, 21, 22, 23, 31, 32, 33]

    # Define a pool of status probability distributions
    status_distributions_pool: List[List[float]] = [
        [0.60, 0.20, 0.20], [0.70, 0.15, 0.15], [0.50, 0.30, 0.20], [0.65, 0.20, 0.15],
        [0.75, 0.10, 0.15], [0.55, 0.25, 0.20], [0.80, 0.10, 0.10], [0.60, 0.30, 0.10]
    ]

    # Randomly assign probability distributions to each player
    player_probabilities: Dict[str, Dict[str, List[float]]] = {}
    for shooter in shooters:
        player_probabilities[shooter] = {
            "status": random.choice(status_distributions_pool)
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
        num_days_to_select: int = random.randint(Data.MIN_DAYS_PER_WEEK, Data.MAX_DAYS_PER_WEEK)
        selected_dates.extend(random.sample(days_in_week, min(num_days_to_select, len(days_in_week))))

    selected_dates.sort() # Ensure dates are in chronological order

    for current_date in selected_dates:
        # Determine the number of players for this session (10 to 20)
        num_players_for_session = random.randint(10, 20)
        
        # Randomly select players for the session
        session_shooters = random.sample(shooters, num_players_for_session)

        # Randomly select one goalkeeper for the day
        daily_keeper: str = random.choice(keepers)

        for shooter in session_shooters:
            for _ in range(penalties_per_player_per_day):
                # Use player-specific probabilities for status
                status: str = random.choices(statuses, weights=player_probabilities[shooter]["status"], k=1)[0]
                remark: int = random.choice(remarks)

                data_list.append([current_date.strftime("%m/%d/%Y"), shooter, daily_keeper, status, remark])

    df = pd.DataFrame(data_list, columns=[Columns.DATE, Columns.SHOOTER_NAME, Columns.KEEPER_NAME, Columns.STATUS, Columns.REMARK])
    return df

if __name__ == "__main__":
    # Example usage:
    # Generate data for the year 2025, with each player taking 3 penalties per day
    pseudo_df: pd.DataFrame = generate_pseudo_data(start_date="2023-01-01", end_date="2025-12-31", penalties_per_player_per_day=3)
    
    # Save to CSV
    output_path: str = Paths.DATA_PSEUDO
    pseudo_df.to_csv(output_path, index=False)
    print(f"Generated {len(pseudo_df)} records and saved to {output_path}")
