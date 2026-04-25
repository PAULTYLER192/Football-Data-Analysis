from pathlib import Path

import pandas as pd


def main() -> None:
	"""Load the raw results data and answer the Module 2 goals questions."""
	# Build a project-root-relative path so the script works from any working directory.
	data_path = Path(__file__).resolve().parent.parent / "data" / "raw" / "results.csv"

	# Stop immediately with a helpful message if the required data file is missing.
	if not data_path.exists():
		raise FileNotFoundError(f"Missing required data file: {data_path}")

	# Load the results dataset and convert the date column for time-based reporting.
	df = pd.read_csv(data_path)
	df["date"] = pd.to_datetime(df["date"], errors="coerce")

	# Create a total_goals column so each match can be evaluated by combined scoring.
	df["total_goals"] = df["home_score"] + df["away_score"]

	# Q5: Calculate the average number of goals scored per match.
	average_goals = df["total_goals"].mean()
	print(f"Q5 - Average number of goals per match: {average_goals:.2f}")

	# Q6: Locate the highest scoring match by finding the row with the maximum total_goals value.
	highest_scoring_match = df.loc[df["total_goals"].idxmax()]
	print("Q6 - Highest scoring match:")
	print(
		f"Date: {highest_scoring_match['date'].date()} | "
		f"Teams: {highest_scoring_match['home_team']} vs {highest_scoring_match['away_team']} | "
		f"Score: {int(highest_scoring_match['home_score'])}-{int(highest_scoring_match['away_score'])}"
	)

	# Q7: Compare home and away scoring totals to see which side scored more overall.
	home_goals_total = df["home_score"].sum()
	away_goals_total = df["away_score"].sum()
	print(
		"Q7 - Goals scored at home vs away: "
		f"home={int(home_goals_total)}, away={int(away_goals_total)}"
	)
	if home_goals_total > away_goals_total:
		print("Q7 - More goals were scored at home.")
	elif away_goals_total > home_goals_total:
		print("Q7 - More goals were scored away.")
	else:
		print("Q7 - Home and away goals were scored equally.")

	# Q8: Find the most common total goals value using the statistical mode.
	most_common_total_goals = int(df["total_goals"].mode().iloc[0])
	print(f"Q8 - Most common total goals value: {most_common_total_goals}")


if __name__ == "__main__":
	main()
