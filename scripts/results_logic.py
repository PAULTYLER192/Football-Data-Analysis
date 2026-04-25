from pathlib import Path

import pandas as pd


def match_result(row: pd.Series) -> str:
	"""Classify a match outcome based on home and away scores."""
	# Compare the two scores and return the match outcome expected by the assignment.
	if row["home_score"] > row["away_score"]:
		return "Home Win"
	if row["home_score"] < row["away_score"]:
		return "Away Win"
	return "Draw"


def main() -> None:
	"""Load the raw data, classify each match, and answer the Module 3 questions."""
	# Build a project-root-relative path so the script works from any shell location.
	data_path = Path(__file__).resolve().parent.parent / "data" / "raw" / "results.csv"

	# Stop immediately with a clear error if the required dataset is missing.
	if not data_path.exists():
		raise FileNotFoundError(f"Missing required data file: {data_path}")

	# Load the results dataset and convert the date column for reporting.
	df = pd.read_csv(data_path)
	df["date"] = pd.to_datetime(df["date"], errors="coerce")

	# Apply the match_result function to create a result label for every match.
	df["result"] = df.apply(match_result, axis=1)

	# Q10: Calculate the percentage of matches won by the home team.
	home_win_count = (df["result"] == "Home Win").sum()
	total_matches = df.shape[0]
	home_win_percentage = (home_win_count / total_matches) * 100
	print(f"Q10 - Percentage of matches that are home wins: {home_win_percentage:.2f}%")

	# Q11: Compare home-win and away-win percentages and explain whether home advantage exists.
	away_win_count = (df["result"] == "Away Win").sum()
	home_win_rate = (home_win_count / total_matches) * 100
	away_win_rate = (away_win_count / total_matches) * 100
	print("Q11 - Home advantage analysis:")
	if home_win_rate > away_win_rate:
		print(
			f"**Home advantage exists.** Home wins ({home_win_rate:.2f}%) are more frequent than "
			f"away wins ({away_win_rate:.2f}%)."
		)
	elif away_win_rate > home_win_rate:
		print(
			f"**Home advantage does not exist.** Away wins ({away_win_rate:.2f}%) exceed "
			f"home wins ({home_win_rate:.2f}%)."
		)
	else:
		print(
			f"**No clear home advantage.** Home wins and away wins are tied at {home_win_rate:.2f}% each."
		)

	# Q12: Build a series of winning teams and identify the team with the most historical wins.
	home_winners = df.loc[df["result"] == "Home Win", "home_team"]
	away_winners = df.loc[df["result"] == "Away Win", "away_team"]
	winning_teams = pd.concat([home_winners, away_winners], ignore_index=True)
	top_winner = winning_teams.value_counts().idxmax()
	top_winner_count = winning_teams.value_counts().max()
	print(f"Q12 - Team/country with the most wins historically: {top_winner} ({top_winner_count} wins)")


if __name__ == "__main__":
	main()
