import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Step 1: Fetch team data (school names from Cell 0 and wins from Cell 2)
def fetch_teams_and_wins():
    url = "https://www.sports-reference.com/cbb/seasons/men/2026-school-stats.html"
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

# Step 3: Generate HTML output with the rankings displayed in the tables
def generate_html_output(owner_teams, owner_totals):
    # Sort the owners based on total points in descending order
    sorted_owners = sorted(owner_totals.items(), key=lambda x: x[1], reverse=True)
    
    # Assign 1st, 2nd, and 3rd place labels
    place_labels = {0: "1st", 1: "2nd", 2: "3rd"}

    # Define owner names
    owner_names = {
        "Owner 1": "JD", 
        "Owner 2": "John", 
        "Owner 3": "Brandon", 
        "Owner 4": "Skylar",
        "Owner 5": "Jerry", 
        "Owner 6": "Worthy", 
        "Owner 7": "Sean"
    }

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Simple HTML template for the output with flexbox layout, and timestamp
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fantasy Basketball Results</title>
        <style>
            .container {{
                display: flex;
                flex-wrap: wrap;
                justify-content: space-around;
            }}
            .row {{
                display: flex;
                width: 100%;
                justify-content: space-around;
                margin-bottom: 20px;
            }}
            table {{
                width: 30%;
                border-collapse: collapse;
                margin: 10px;
                word-wrap: break-word;
            }}
            table, th, td {{
                border: 1px solid black;
            }}
            th, td {{
                padding: 10px;
                text-align: left;
                word-break: break-word;
            }}
            .ranking-table {{
                margin: 20px auto;
                width: 50%;
                text-align: center;
            }}
            h1 {{
                text-align: center;
            }}
            .timestamp {{
                text-align: left;
                font-weight: bold;
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <div class="timestamp">
            <p>Last updated: {timestamp}</p>
        </div>
        <div class="ranking-table">
            <table>
                <tr>
                    <th>Owner</th>
                    <th>Total Points</th>
                </tr>
                {ranking_rows}
            </table>
        </div>
        <h1>Rankings</h1>
        <div class="container">
            {owner_tables}
        </div>
    </body>
    </html>
    '''

    # Generate the top table with owner names and total points
    ranking_rows = ""
    for i, (owner, total_points) in enumerate(sorted_owners):
        owner_name = owner_names[owner]
        ranking_rows += f"<tr><td>{owner_name}</td><td>{total_points}</td></tr>"

    # Generate a table for each owner in sorted order
    owner_tables = ""
    owner_counter = 0

    for i, (owner, _) in enumerate(sorted_owners):
        teams = owner_teams[owner]
        total_points = sum([team[1] for team in teams])

        # Assign place label for top 3
        place = f" ({place_labels[i]})" if i in place_labels else ""

        # Create the owner's table with the place label
        owner_table = f"<table><caption><h2>{owner_names[owner]}{place}</h2></caption>"
        owner_table += "<tr><th>Teams</th><th>Points</th></tr>"

        # Create rows for the teams
        for j in range(10):
            if j < len(teams):
                team_name = teams[j][0]
                points = teams[j][1]

                # No character restriction for team name
                owner_table += f"<tr><td class='team-col'>{team_name}</td><td class='points-col'>{points}</td></tr>"

        # Add the total row in the 11th position
        total_points = str(total_points)[:3]  # Truncate total points to 3 digits
        owner_table += f"<tr><td>Total</td><td>{total_points}</td></tr>"
        owner_table += "</table>"

        # Append the owner's table to the owner_tables string
        if owner_counter % 3 == 0:  # Create a new row after every 3 owners
            owner_tables += f"<div class='row'>{owner_table}"
        else:
            owner_tables += f"{owner_table}"

        if owner_counter % 3 == 2:
            owner_tables += "</div>"  # Close the row after 3 owners

        owner_counter += 1

    if owner_counter % 3 != 0:
        owner_tables += "</div>"  # Close the last row if not already closed

    # Fill the template with the generated ranking rows, owner tables, and timestamp
    html_content = html_template.format(ranking_rows=ranking_rows, owner_tables=owner_tables, timestamp=timestamp)

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
        "Owner 3": [available_teams[20], available_teams[21], available_teams[22], available_teams[23], available_teams[24], available_teams[25], available_teams[26], available_teams[27], available_teams[28], available_teams[29]],
        "Owner 4": [available_teams[30], available_teams[31], available_teams[32], available_teams[33], available_teams[34], available_teams[35], available_teams[36], available_teams[37], available_teams[38], available_teams[39]],
        "Owner 5": [available_teams[40], available_teams[41], available_teams[42], available_teams[43], available_teams[44], available_teams[45], available_teams[46], available_teams[47], available_teams[48], available_teams[49]],
        "Owner 6": [available_teams[50], available_teams[51], available_teams[52], available_teams[53], available_teams[54], available_teams[55], available_teams[56], available_teams[57], available_teams[58], available_teams[59]],
        "Owner 7": [available_teams[60], available_teams[61], available_teams[62], available_teams[63], available_teams[64], available_teams[65], available_teams[66], available_teams[67], available_teams[68], available_teams[69]]
    }

    # Calculate the total wins for each owner
    owner_totals = {owner: sum([team[1] for team in teams]) for owner, teams in owner_teams.items()}

    # Generate the HTML output
    generate_html_output(owner_teams, owner_totals)

# Run the fantasy basketball game
run_fantasy_basketball_game()
