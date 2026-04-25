from pathlib import Path

import pandas as pd


def main() -> None:
	"""Load the raw results data and print the answers to the Module 1 questions."""
	# Build a path relative to the project root so the script works from any shell location.
	data_path = Path(__file__).resolve().parent.parent / "data" / "raw" / "results.csv"

	# Fail fast with a clear message if the source data is missing.
	if not data_path.exists():
		raise FileNotFoundError(f"Missing required data file: {data_path}")

	# Load the match results into a DataFrame for exploration.
	df = pd.read_csv(data_path)

	# Convert the date column so we can safely compute the earliest and latest year.
	df["date"] = pd.to_datetime(df["date"], errors="coerce")

	# Q1: Count the total number of matches using the DataFrame shape.
	total_matches = df.shape[0]
	print(f"Q1 - Total matches in the dataset: {total_matches}")

	# Q2: Find the earliest and latest year represented in the dataset.
	earliest_year = int(df["date"].min().year)
	latest_year = int(df["date"].max().year)
	print(f"Q2 - Earliest year: {earliest_year}; Latest year: {latest_year}")

	# Q3: Count how many unique countries appear in the country column.
	unique_countries = df["country"].nunique()
	print(f"Q3 - Unique countries: {unique_countries}")

	# Q4: Identify the home team that appears most frequently.
	home_team_counts = df["home_team"].value_counts().head()
	most_frequent_home_team = home_team_counts.index[0]
	most_frequent_home_team_matches = home_team_counts.iloc[0]
	print("Q4 - Home team frequency ranking (top 5):")
	print(home_team_counts)
	print(
		f"Q4 - Most frequent home team: {most_frequent_home_team} "
		f"({most_frequent_home_team_matches} matches)"
	)


if __name__ == "__main__":
	main()
