import requests
from bs4 import BeautifulSoup

# Step 1: Fetch team data (school names from Cell 0 and wins from Cell 2)
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

    # Extract school names from Cell 0 and overall wins from Cell 2
    teams_and_wins = []
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 2:  # Ensure there are enough columns
            school_name = cells[0].text.strip()  # Team name from Cell 0
            overall_wins = cells[2].text.strip()  # Overall wins from Cell 2

            # Strip 'NCAA' and any leading/trailing spaces if present
            if school_name.endswith('NCAA'):
                school_name = school_name[:-4].strip()  # Remove 'NCAA' and any trailing space

            if overall_wins.isdigit():  # Ensure we only capture valid win numbers
                teams_and_wins.append((school_name, int(overall_wins)))

    return teams_and_wins

# Step 3: Generate HTML output with the rankings displayed at the top
def generate_html_output(owner_teams, owner_totals):
    # Sort the owners based on total points
    sorted_owners = sorted(owner_totals.items(), key=lambda x: x[1], reverse=True)
    
    # Create a ranking order: 1st, 2nd, and 3rd place
    owner_names = {"Owner 1": "JD", "Owner 2": "John", "Owner 3": "Brandon"}
    rankings = f"<h2>1st Place: {owner_names[sorted_owners[0][0]]} ({sorted_owners[0][1]} points)</h2>"
    rankings += f"<h2>2nd Place: {owner_names[sorted_owners[1][0]]} ({sorted_owners[1][1]} points)</h2>"
    rankings += f"<h2>3rd Place: {owner_names[sorted_owners[2][0]]} ({sorted_owners[2][1]} points)</h2>"

    # Simple HTML template for the output with flexbox layout and rankings at the top
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fantasy Basketball Results</title>
        <style>
            .container {{
                display: flex;
                justify-content: space-around;
            }}
            table {{
                width: 30%;
                border-collapse: collapse;
                margin: 10px;
            }}
            table, th, td {{
                border: 1px solid black;
            }}
            th, td {{
                padding: 10px;
                text-align: left;
            }}
            .owner-col {{
                width: 10%;
            }}
            .team-col {{
                width: 20%;
            }}
            .points-col {{
                width: 5%;
            }}
            h2 {{
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h1>Rankings</h1>
        {rankings}
        <div class="container">
            {owner_tables}
        </div>
    </body>
    </html>
    '''

    # Generate a table for each owner
    owner_tables = ""

    for owner, teams in owner_teams.items():
        total_points = sum([team[1] for team in teams])
        owner_table = f"<table><caption><h2>{owner_names[owner]}</h2></caption>"
        owner_table += "<tr><th>Teams</th><th>Points</th></tr>"

        # Create rows for the teams
        for i in range(10):
            if i < len(teams):
                team_name = teams[i][0]
                points = teams[i][1]

                # Truncate team name to 20 characters
                team_name = team_name if len(team_name) <= 20 else team_name[:17] + '...'

                # Truncate points to the first 3 digits
                points = str(points)[:3]
            else:
                team_name = ""
                points = ""

            # Add the row for each team
            owner_table += f"<tr><td class='team-col'>{team_name}</td><td class='points-col'>{points}</td></tr>"

        # Add the total row in the 11th position
        total_points = str(total_points)[:3]  # Truncate total points to 3 digits
        owner_table += f"<tr><td>Total</td><td>{total_points}</td></tr>"
        owner_table += "</table>"

        # Append the owner's table to the owner_tables string
        owner_tables += owner_table

    # Fill the template with the generated tables and rankings
    html_content = html_template.format(owner_tables=owner_tables, rankings=rankings)

    # Write the HTML content to a file named 'index.html'
    with open("index.html", "w") as f:
        f.write(html_content)

    print("Results have been saved to 'index.html'.")

# Step 4: Run the Fantasy Basketball Game with hardcoded teams
def run_fantasy_basketball_game():
    teams_and_wins = fetch_teams_and_wins()

    if not teams_and_wins:
        print("No teams available for the game.")
        return

    # Shuffle teams for availability (optional)
    available_teams = teams_and_wins[:]

    # Owners and their hardcoded team selections
    owner_teams = {
        "Owner 1": [available_teams[0], available_teams[1], available_teams[2], available_teams[3], available_teams[4], available_teams[5], available_teams[6], available_teams[7], available_teams[8], available_teams[9]],
        "Owner 2": [available_teams[10], available_teams[11], available_teams[12], available_teams[13], available_teams[14], available_teams[15], available_teams[16], available_teams[17], available_teams[18], available_teams[19]],
        "Owner 3": [available_teams[20], available_teams[21], available_teams[22], available_teams[23], available_teams[24], available_teams[25], available_teams[26], available_teams[27], available_teams[28], available_teams[29]]
    }

    # Calculate the total wins for each owner
    owner_totals = {owner: sum([team[1] for team in teams]) for owner, teams in owner_teams.items()}

    # Generate the HTML output
    generate_html_output(owner_teams, owner_totals)

# Run the fantasy basketball game
run_fantasy_basketball_game()
