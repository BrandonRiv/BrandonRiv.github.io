import requests
from bs4 import BeautifulSoup

# Step 1: Fetch team data (school names and wins)
def fetch_teams_and_wins():
    url = "https://www.sports-reference.com/cbb/seasons/men/2024-school-stats.html"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'basic_school_stats'})

    if not table:
        print("Could not find the table on the page.")
        return []

    # Extract school names and overall wins
    teams_and_wins = []
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 1:
            school_name = cells[0].text.strip()
            overall_wins = cells[1].text.strip()

            if overall_wins.isdigit():  # Ensure that we only capture valid win numbers
                teams_and_wins.append((school_name, int(overall_wins)))

    return teams_and_wins

# Step 2: Allow owners to choose teams
def select_teams(teams_and_wins, owner_name, available_teams):
    print(f"\n{owner_name}, it's your turn to pick a team!")
    print(f"Available teams: {', '.join([team[0] for team in available_teams])}")

    while True:
        choice = input(f"{owner_name}, select a team by typing its name: ").strip()
        # Find the chosen team in the list of available teams
        for i, team in enumerate(available_teams):
            if team[0].lower() == choice.lower():
                selected_team = available_teams.pop(i)  # Remove from available teams
                print(f"{owner_name} selected {selected_team[0]} with {selected_team[1]} wins.")
                return selected_team
        print("Invalid team selection, please try again.")

# Step 3: Generate HTML output
def generate_html_output(owner_teams, owner_totals, winner):
    # Simple HTML template for the output
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fantasy Basketball Results</title>
    </head>
    <body>
        <h1>Fantasy Basketball Results</h1>
        {results_table}
        <h2>Winner: {winner}</h2>
    </body>
    </html>
    '''

    # Generate the results table
    results_table = "<table border='1'>"
    results_table += "<tr><th>Owner</th><th>Teams</th><th>Total Wins</th></tr>"
    for owner, teams in owner_teams.items():
        team_list = ', '.join([team[0] for team in teams])
        total_wins = owner_totals[owner]
        results_table += f"<tr><td>{owner}</td><td>{team_list}</td><td>{total_wins}</td></tr>"
    results_table += "</table>"

    # Fill the template with the results
    html_content = html_template.format(results_table=results_table, winner=winner)

    # Write the HTML content to a file
    with open("index.html", "w") as f:
        f.write(html_content)

    print("Results have been saved to 'fantasy_basketball_results.html'.")

# Step 4: Run the Fantasy Basketball Game
def run_fantasy_basketball_game():
    teams_and_wins = fetch_teams_and_wins()

    if not teams_and_wins:
        print("No teams available for the game.")
        return

    # Shuffle teams for availability (optional)
    available_teams = teams_and_wins[:]

    # Owners
    owners = ["Owner 1", "Owner 2", "Owner 3"]
    owner_teams = {owner: [] for owner in owners}

    # Team selection rounds
    for round_number in range(1):
        print(f"\n--- Round {round_number + 1} ---")
        for owner in owners:
            selected_team = select_teams(teams_and_wins, owner, available_teams)
            owner_teams[owner].append(selected_team)

    # Calculate the total wins for each owner
    owner_totals = {owner: sum([team[1] for team in teams]) for owner, teams in owner_teams.items()}

    # Determine the winner
    winner = max(owner_totals, key=owner_totals.get)

    # Generate the HTML output
    generate_html_output(owner_teams, owner_totals, winner)

# Run the fantasy basketball game
run_fantasy_basketball_game()
