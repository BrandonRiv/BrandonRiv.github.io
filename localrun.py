import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Fetch team data (school names and wins)
def fetch_teams_and_wins():
    url = "https://www.sports-reference.com/cbb/seasons/men/2025-school-stats.html"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return {}

    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'basic_school_stats'})

    if not table:
        print("Could not find the table on the page.")
        return {}

    # Extract school names and overall wins
    teams_and_wins = {}
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 2:  # Ensure there are enough columns
            school_name = cells[0].text.strip()  # Team name from Cell 0
            overall_wins = cells[2].text.strip()  # Overall wins from Cell 2

            # Strip 'NCAA' and any leading/trailing spaces if present
            if school_name.endswith('NCAA'):
                school_name = school_name[:-4].strip()  # Remove 'NCAA' and any trailing space

            if overall_wins.isdigit():  # Ensure we only capture valid win numbers
                teams_and_wins[school_name] = int(overall_wins)

    return teams_and_wins

def generate_html_output(owner_teams, owner_totals):
    # Sort the owners based on total points in descending order
    sorted_owners = sorted(owner_totals.items(), key=lambda x: x[1], reverse=True)

    # Assign 1st, 2nd, and 3rd place labels
    place_labels = {0: "1st", 1: "2nd", 2: "3rd"}

    # Define owner names
    owner_names = {
        "Owner 1": "E-3", 
        "Owner 2": "Worthy", 
        "Owner 3": "Mt Beers",
        "Owner 4": "Mark Bears",
        "Owner 5": "Rick-Dan",
        "Owner 6": "Booty Posse",
        "Owner 7": "Mruz",
        "Owner 8": "John H",
        "Owner 9": "Leonard",
        "Owner 10": "Team Jody",
        "Owner 11": "Parrott-Depa",
        "Owner 12": "JJ Stevens",
        "Owner 13": "Mark Brandon",
        "Owner 14": "Collin-Ty",
        "Owner 15": "Ody",
        "Owner 16": "Leb1",
        "Owner 17": "Leb2",
        "Owner 18": "Jake W",
        "Owner 19": "JD",
        "Owner 20": "Bryan",
        "Owner 21": "Nemo"
    }

    # Calculate individual team values
    team_values = []
    low_cost_teams = []
    for owner, teams in owner_teams.items():
        for team_name, wins, cost in teams:
            value = wins - cost
            team_values.append((owner, team_name, wins, cost, value))
            if cost <= 1:  # Collect teams with cost ≤ 1
                low_cost_teams.append((owner, team_name, wins, cost))

    # Sort the teams by value in descending order
    team_values = sorted(team_values, key=lambda x: x[4], reverse=True)[:5]

    # Sort low-cost teams by wins in descending order and limit to top 5
    low_cost_teams = sorted(low_cost_teams, key=lambda x: x[2], reverse=True)[:5]

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # HTML template
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
                width: 50%;
                border-collapse: collapse;
                margin: 20px auto;
                word-wrap: break-word;
            }}
            table, th, td {{
                border: 1px solid black;
            }}
            th, td {{
                padding: 10px;
                text-align: center;
                word-break: break-word;
            }}
            .ranking-table {{
                margin: 20px auto;
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
        <div class="ranking-table">
            <h2>Top 5 Teams by Value (Wins - Cost)</h2>
            <table>
                <tr>
                    <th>Owner</th>
                    <th>Team</th>
                    <th>Wins</th>
                    <th>Cost</th>
                    <th>Value</th>
                </tr>
                {value_rows}
            </table>
        </div>
        <div class="ranking-table">
            <h2>Most Wins with Cost ≤ 1</h2>
            <table>
                <tr>
                    <th>Owner</th>
                    <th>Team</th>
                    <th>Wins</th>
                    <th>Cost</th>
                </tr>
                {low_cost_rows}
            </table>
        </div>
        <h1>Rankings</h1>
        <div class="container">
            {owner_tables}
        </div>
    </body>
    </html>
    '''

    # Generate value rows for the top 5 teams
    value_rows = ""
    for owner, team_name, wins, cost, value in team_values:
        owner_name = owner_names[owner]
        value_rows += f"<tr><td>{owner_name}</td><td>{team_name}</td><td>{wins}</td><td>{cost:.2f}</td><td>{value:.2f}</td></tr>"

    # Generate rows for low-cost teams
    low_cost_rows = ""
    for owner, team_name, wins, cost in low_cost_teams:
        owner_name = owner_names[owner]
        low_cost_rows += f"<tr><td>{owner_name}</td><td>{team_name}</td><td>{wins}</td><td>{cost:.2f}</td></tr>"

    # Generate ranking rows
    ranking_rows = ""
    for i, (owner, total_points) in enumerate(sorted_owners):
        owner_name = owner_names[owner]
        ranking_rows += f"<tr><td>{owner_name}</td><td>{total_points}</td></tr>"

    # Generate owner tables
    owner_tables = ""
    owner_counter = 0

    for i, (owner, _) in enumerate(sorted_owners):
        teams = owner_teams[owner]
        total_points = sum([team[1] for team in teams])

        # Assign place label for top 3
        place = f" ({place_labels[i]})" if i in place_labels else ""

        # Create the owner's table
        owner_table = f"<table><caption><h2>{owner_names[owner]}{place}</h2></caption>"
        owner_table += "<tr><th>Teams</th><th>Points</th><th>Cost</th></tr>"

        # Add team rows
        for team_name, points, cost in teams:
            owner_table += f"<tr><td class='team-col'>{team_name}</td><td class='points-col'>{points}</td><td class='cost-col'>{cost}</td></tr>"

        # Add total row
        total_points = str(total_points)[:3]
        owner_table += f"<tr><td>Total</td><td>{total_points}</td><td>-</td></tr>"
        owner_table += "</table>"

        if owner_counter % 3 == 0:
            owner_tables += f"<div class='row'>{owner_table}"
        else:
            owner_tables += f"{owner_table}"

        if owner_counter % 3 == 2:
            owner_tables += "</div>"

        owner_counter += 1

    if owner_counter % 3 != 0:
        owner_tables += "</div>"

    # Fill the template
    html_content = html_template.format(
        value_rows=value_rows,
        low_cost_rows=low_cost_rows,
        ranking_rows=ranking_rows,
        owner_tables=owner_tables,
        timestamp=timestamp
    )

    # Write HTML content to file
    with open("index2.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Results have been saved to 'index2.html'.")



# Run the fantasy basketball game
def run_fantasy_basketball_game():
    # Fetch team data (points) dynamically
    teams_and_wins = fetch_teams_and_wins()

    # Hardcoded teams for each owner with points fetched dynamically and costs hardcoded
    e3_teams = [
        ("Penn State", teams_and_wins.get("Penn State", 0), 6),
        ("Florida", teams_and_wins.get("Florida", 0), 7),
        ("Georgia", teams_and_wins.get("Georgia", 0), 2),
        ("Missouri", teams_and_wins.get("Missouri", 0), 3.5),
        ("Texas", teams_and_wins.get("Texas", 0), 7),
        ("Notre Dame", teams_and_wins.get("Notre Dame", 0), 3),
        ("Pittsburgh", teams_and_wins.get("Pittsburgh", 0), 10),
        ("New Mexico", teams_and_wins.get("New Mexico", 0), 8.5),
        ("East Carolina", teams_and_wins.get("East Carolina", 0), 1),
        ("Southern Utah", teams_and_wins.get("Southern Utah", 0), 2),
    ]

    worthy_teams = [
        ("Houston", teams_and_wins.get("Houston", 0), 12),
        ("Southern Methodist", teams_and_wins.get("Southern Methodist", 0), 5),
        ("Creighton", teams_and_wins.get("Creighton", 0), 10),
        ("Tulane", teams_and_wins.get("Tulane", 0), 0.25),
        ("Columbia", teams_and_wins.get("Columbia", 0), 7),
        ("Utah Valley", teams_and_wins.get("Utah Valley", 0), 5),
        ("Middle Tennessee", teams_and_wins.get("Middle Tennessee", 0), 1.5),
        ("James Madison", teams_and_wins.get("James Madison", 0), 5.5),
        ("Ball State", teams_and_wins.get("Ball State", 0), 0.25),
        ("Omaha", teams_and_wins.get("Omaha", 0), 3.5),
    ]

    mt_beers_teams = [
        ("Wisconsin", teams_and_wins.get("Wisconsin", 0), 8),
        ("Mississippi State", teams_and_wins.get("Mississippi State", 0), 7),
        ("Texas A&M", teams_and_wins.get("Texas A&M", 0), 5),
        ("Stanford", teams_and_wins.get("Stanford", 0), 6),
        ("Boise State", teams_and_wins.get("Boise State", 0), 7),
        ("North Texas", teams_and_wins.get("North Texas", 0), 6),
        ("Belmont", teams_and_wins.get("Belmont", 0), 0.5),
        ("East Tennessee State", teams_and_wins.get("East Tennessee State", 0), 0.5),
        ("Presbyterian", teams_and_wins.get("Presbyterian", 0), 2),
        ("Wright State", teams_and_wins.get("Wright State", 0), 8),
    ]

    mark_bears_teams = [
        ("Colorado", teams_and_wins.get("Colorado", 0), 2),
        ("Michigan", teams_and_wins.get("Michigan", 0), 5),
        ("Alabama", teams_and_wins.get("Alabama", 0), 14),
        ("Vanderbilt", teams_and_wins.get("Vanderbilt", 0), 2),
        ("Louisville", teams_and_wins.get("Louisville", 0), 8),
        ("George Washington", teams_and_wins.get("George Washington", 0), 5),
        ("Wichita State", teams_and_wins.get("Wichita State", 0), 8),
        ("Northern Iowa", teams_and_wins.get("Northern Iowa", 0), 3),
        ("Abilene Christian", teams_and_wins.get("Abilene Christian", 0), 0.25),
        ("Seattle", teams_and_wins.get("Seattle", 0), 2),
    ]

    rick_dan_teams = [
        ("Indiana", teams_and_wins.get("Indiana", 0), 5.5),
        ("Duke", teams_and_wins.get("Duke", 0), 16.5),
        ("Miami (FL)", teams_and_wins.get("Miami (FL)", 0), 1),
        ("Virginia", teams_and_wins.get("Virginia", 0), 0.5),
        ("Connecticut", teams_and_wins.get("Connecticut", 0), 13.5),
        ("Saint Louis", teams_and_wins.get("Saint Louis", 0), 1),
        ("UT Arlington", teams_and_wins.get("UT Arlington", 0), 0.5),
        ("Western Kentucky", teams_and_wins.get("Western Kentucky", 0), 5.5),
        ("Montana", teams_and_wins.get("Montana", 0), 1),
        ("Quinnipiac", teams_and_wins.get("Quinnipiac", 0), 5),
    ]

    # Hardcoded teams for Booty Posse
    booty_posse_teams = [
        ("Arizona", teams_and_wins.get("Arizona", 0), 6),
        ("Kansas State", teams_and_wins.get("Kansas State", 0), 0.5),
        ("Michigan State", teams_and_wins.get("Michigan State", 0), 5.5),
        ("Kentucky", teams_and_wins.get("Kentucky", 0), 10),
        ("Syracuse", teams_and_wins.get("Syracuse", 0), 0.5),
        ("Villanova", teams_and_wins.get("Villanova", 0), 1.5),
        ("Colorado State", teams_and_wins.get("Colorado State", 0), 3.5),
        ("Grand Canyon", teams_and_wins.get("Grand Canyon", 0), 11.5),
        ("UTEP", teams_and_wins.get("UTEP", 0), 1),
        ("Ohio", teams_and_wins.get("Ohio", 0), 10),
    ]

    # Hardcoded teams for Mruz
    mruz_teams = [
        ("Arizona State", teams_and_wins.get("Arizona State", 0), 0.5),
        ("Iowa State", teams_and_wins.get("Iowa State", 0), 11),
        ("Rutgers", teams_and_wins.get("Rutgers", 0), 4),
        ("Oklahoma", teams_and_wins.get("Oklahoma", 0), 1.5),
        ("UAB", teams_and_wins.get("UAB", 0), 4.5),
        ("College of Charleston", teams_and_wins.get("College of Charleston", 0), 6),
        ("Northern Kentucky", teams_and_wins.get("Northern Kentucky", 0), 1),
        ("Vermont", teams_and_wins.get("Vermont", 0), 11),
        ("Weber State", teams_and_wins.get("Weber State", 0), 0.5),
        ("Akron", teams_and_wins.get("Akron", 0), 10),
    ]

    # Hardcoded teams for John H
    john_h_teams = [
        ("Liberty", teams_and_wins.get("Liberty", 0), 10),
        ("Marshall", teams_and_wins.get("Marshall", 0), 0.25),
        ("UNC Wilmington", teams_and_wins.get("UNC Wilmington", 0), 5),
        ("High Point", teams_and_wins.get("High Point", 0), 14),
        ("Marist", teams_and_wins.get("Marist", 0), 5.5),
        ("South Dakota", teams_and_wins.get("South Dakota", 0), 0.25),
        ("McNeese State", teams_and_wins.get("McNeese State", 0), 6),
        ("Texas-Rio Grande Valley", teams_and_wins.get("Texas-Rio Grande Valley", 0), 3.5),
        ("Little Rock", teams_and_wins.get("Little Rock", 0), 2.5),
        ("Wagner", teams_and_wins.get("Wagner", 0), 0.25),
    ]

    # Hardcoded teams for Leonard
    leonard_teams = [
        ("Kansas", teams_and_wins.get("Kansas", 0), 17),
        ("Oregon", teams_and_wins.get("Oregon", 0), 15),
        ("Arkansas", teams_and_wins.get("Arkansas", 0), 5),
        ("Boston College", teams_and_wins.get("Boston College", 0), 1.5),
        ("Butler", teams_and_wins.get("Butler", 0), 3.5),
        ("Massachusetts", teams_and_wins.get("Massachusetts", 0), 0.25),
        ("Florida Atlantic", teams_and_wins.get("Florida Atlantic", 0), 4),
        ("Santa Clara", teams_and_wins.get("Santa Clara", 0), 1),
        ("Wofford", teams_and_wins.get("Wofford", 0), 1.5),
        ("Cal State Fullerton", teams_and_wins.get("Cal State Fullerton", 0), 0.25),
    ]

    # Hardcoded teams for Team Jody
    team_jody_teams = [
        ("Brigham Young", teams_and_wins.get("Brigham Young", 0), 4),
        ("Rhode Island", teams_and_wins.get("Rhode Island", 0), 7),
        ("Memphis", teams_and_wins.get("Memphis", 0), 13),
        ("Gonzaga", teams_and_wins.get("Gonzaga", 0), 18),
        ("Chattanooga", teams_and_wins.get("Chattanooga", 0), 1),
        ("UC Riverside", teams_and_wins.get("UC Riverside", 0), 1),
        ("Texas State", teams_and_wins.get("Texas State", 0), 2),
        ("Northeastern", teams_and_wins.get("Northeastern", 0), 2),
        ("Maine", teams_and_wins.get("Maine", 0), 1),
        ("North Alabama", teams_and_wins.get("North Alabama", 0), 1),
    ]

    # Hardcoded teams for Parrott-Depa
    parrott_depa_teams = [
        ("Baylor", teams_and_wins.get("Baylor", 0), 5.5),
        ("Wake Forest", teams_and_wins.get("Wake Forest", 0), 4),
        ("Marquette", teams_and_wins.get("Marquette", 0), 17.5),
        ("Seton Hall", teams_and_wins.get("Seton Hall", 0), 0.25),
        ("Nevada-Las Vegas", teams_and_wins.get("Nevada-Las Vegas", 0), 4),
        ("Saint Joseph's", teams_and_wins.get("Saint Joseph's", 0), 5.5),
        ("South Florida", teams_and_wins.get("South Florida", 0), 1),
        ("Illinois State", teams_and_wins.get("Illinois State", 0), 2.5),
        ("Saint Mary's (CA)", teams_and_wins.get("Saint Mary's (CA)", 0), 9.5),
        ("Hawaii", teams_and_wins.get("Hawaii", 0), 0.25),
    ]

    # Hardcoded teams for JJ Stevens
    jj_stevens_teams = [
        ("Cincinnati", teams_and_wins.get("Cincinnati", 0), 9),
        ("Purdue", teams_and_wins.get("Purdue", 0), 9.5),
        ("St. John's (NY)", teams_and_wins.get("St. John's (NY)", 0), 9.5),
        ("George Mason", teams_and_wins.get("George Mason", 0), 4),
        ("Cornell", teams_and_wins.get("Cornell", 0), 0.5),
        ("Hofstra", teams_and_wins.get("Hofstra", 0), 4.5),
        ("UNC Asheville", teams_and_wins.get("UNC Asheville", 0), 1),
        ("Toledo", teams_and_wins.get("Toledo", 0), 4.5),
        ("Lipscomb", teams_and_wins.get("Lipscomb", 0), 5.5),
        ("Stephen F. Austin", teams_and_wins.get("Stephen F. Austin", 0), 0.25),
    ]

    # Hardcoded teams for Mark Brandon
    mark_brandon_teams = [
        ("West Virginia", teams_and_wins.get("West Virginia", 0), 3),
        ("Maryland", teams_and_wins.get("Maryland", 0), 5.5),
        ("NC State", teams_and_wins.get("NC State", 0), 5.5),
        ("Xavier", teams_and_wins.get("Xavier", 0), 9.5),
        ("Utah State", teams_and_wins.get("Utah State", 0), 11.5),
        ("Cal State Northridge", teams_and_wins.get("Cal State Northridge", 0), 1.5),
        ("Elon", teams_and_wins.get("Elon", 0), 1),
        ("Longwood", teams_and_wins.get("Longwood", 0), 5.5),
        ("Kent State", teams_and_wins.get("Kent State", 0), 6),
        ("North Florida", teams_and_wins.get("North Florida", 0), 1),
    ]

    # Hardcoded teams for Collin-Ty
    collin_ty_teams = [
        ("Texas Tech", teams_and_wins.get("Texas Tech", 0), 6),
        ("Illinois", teams_and_wins.get("Illinois", 0), 7.5),
        ("Clemson", teams_and_wins.get("Clemson", 0), 9),
        ("San Diego State", teams_and_wins.get("San Diego State", 0), 6.5),
        ("Loyola (IL)", teams_and_wins.get("Loyola (IL)", 0), 6.5),
        ("Princeton", teams_and_wins.get("Princeton", 0), 4.5),
        ("Bryant", teams_and_wins.get("Bryant", 0), 1.5),
        ("Miami (OH)", teams_and_wins.get("Miami (OH)", 0), 1.5),
        ("Saint Peter's", teams_and_wins.get("Saint Peter's", 0), 4),
        ("SIU Edwardsville", teams_and_wins.get("SIU Edwardsville", 0), 0.25),
    ]

    # Hardcoded teams for Ody
    ody_teams = [
        ("Nebraska", teams_and_wins.get("Nebraska", 0), 2),
        ("Louisiana State", teams_and_wins.get("Louisiana State", 0), 3.5),
        ("Florida State", teams_and_wins.get("Florida State", 0), 5.5),
        ("Virginia Commonwealth", teams_and_wins.get("Virginia Commonwealth", 0), 9),
        ("Rice", teams_and_wins.get("Rice", 0), 1.5),
        ("Illinois-Chicago", teams_and_wins.get("Illinois-Chicago", 0), 0.5),
        ("Furman", teams_and_wins.get("Furman", 0), 10),
        ("UC San Diego", teams_and_wins.get("UC San Diego", 0), 7),
        ("Arkansas State", teams_and_wins.get("Arkansas State", 0), 10),
        ("Drexel", teams_and_wins.get("Drexel", 0), 1),
    ]

    # Hardcoded teams for Leb1
    leb1_teams = [
        ("UCLA", teams_and_wins.get("UCLA", 0), 8),
        ("Northwestern", teams_and_wins.get("Northwestern", 0), 0.25),
        ("Indiana State", teams_and_wins.get("Indiana State", 0), 0.25),
        ("Missouri State", teams_and_wins.get("Missouri State", 0), 3),
        ("Oregon State", teams_and_wins.get("Oregon State", 0), 4),
        ("Mercer", teams_and_wins.get("Mercer", 0), 1),
        ("Louisiana Tech", teams_and_wins.get("Louisiana Tech", 0), 10),
        ("Cal State Bakersfield", teams_and_wins.get("Cal State Bakersfield", 0), 0.25),
        ("Milwaukee", teams_and_wins.get("Milwaukee", 0), 5),
        ("Massachusetts-Lowell", teams_and_wins.get("Massachusetts-Lowell", 0), 14),
    ]

    # Hardcoded teams for Leb2
    leb2_teams = [
        ("Iowa", teams_and_wins.get("Iowa", 0), 4),
        ("Mississippi", teams_and_wins.get("Mississippi", 0), 3),
        ("Drake", teams_and_wins.get("Drake", 0), 14),
        ("Washington State", teams_and_wins.get("Washington State", 0), 5.5),
        ("Samford", teams_and_wins.get("Samford", 0), 7),
        ("Kennesaw State", teams_and_wins.get("Kennesaw State", 0), 1.5),
        ("Appalachian State", teams_and_wins.get("Appalachian State", 0), 0.25),
        ("Winthrop", teams_and_wins.get("Winthrop", 0), 5),
        ("Purdue Fort Wayne", teams_and_wins.get("Purdue Fort Wayne", 0), 9),
        ("Idaho State", teams_and_wins.get("Idaho State", 0), 0.75),
    ]

    # Hardcoded teams for Jake W
    jake_w_teams = [
        ("Utah", teams_and_wins.get("Utah", 0), 5),
        ("Ohio State", teams_and_wins.get("Ohio State", 0), 7),
        ("Tennessee", teams_and_wins.get("Tennessee", 0), 16),
        ("Georgetown", teams_and_wins.get("Georgetown", 0), 0.25),
        ("Wyoming", teams_and_wins.get("Wyoming", 0), 1),
        ("Davidson", teams_and_wins.get("Davidson", 0), 3.5),
        ("St. Bonaventure", teams_and_wins.get("St. Bonaventure", 0), 6),
        ("Temple", teams_and_wins.get("Temple", 0), 3),
        ("Bradley", teams_and_wins.get("Bradley", 0), 8),
        ("Georgia Southern", teams_and_wins.get("Georgia Southern", 0), 0.25),
    ]

    # Hardcoded teams for JD
    jd_teams = [
        ("Nevada", teams_and_wins.get("Nevada", 0), 10.5),
        ("Dayton", teams_and_wins.get("Dayton", 0), 9),
        ("UNC Greensboro", teams_and_wins.get("UNC Greensboro", 0), 4),
        ("Sam Houston", teams_and_wins.get("Sam Houston", 0), 2.5),
        ("Troy", teams_and_wins.get("Troy", 0), 5.5),
        ("Towson", teams_and_wins.get("Towson", 0), 4),
        ("Montana State", teams_and_wins.get("Montana State", 0), 3),
        ("Rider", teams_and_wins.get("Rider", 0), 0.25),
        ("South Dakota State", teams_and_wins.get("South Dakota State", 0), 7.5),
        ("St. Thomas", teams_and_wins.get("St. Thomas", 0), 2),
    ]

    # Hardcoded teams for Bryan
    bryan_teams = [
        ("TCU", teams_and_wins.get("TCU", 0), 0.25),
        ("California", teams_and_wins.get("California", 0), 0.25),
        ("North Carolina", teams_and_wins.get("North Carolina", 0), 15),
        ("DePaul", teams_and_wins.get("DePaul", 0), 3.5),
        ("La Salle", teams_and_wins.get("La Salle", 0), 0.5),
        ("Murray State", teams_and_wins.get("Murray State", 0), 7),
        ("UC Santa Barbara", teams_and_wins.get("UC Santa Barbara", 0), 6.5),
        ("South Alabama", teams_and_wins.get("South Alabama", 0), 0.25),
        ("Northern Colorado", teams_and_wins.get("Northern Colorado", 0), 7),
        ("Texas A&M-Corpus Christi", teams_and_wins.get("Texas A&M-Corpus Christi", 0), 3.5),
    ]

    # Hardcoded teams for Nemo
    nemo_teams = [
        ("Auburn", teams_and_wins.get("Auburn", 0), 17),
        ("Providence", teams_and_wins.get("Providence", 0), 1),
        ("San Francisco", teams_and_wins.get("San Francisco", 0), 5.5),
        ("Yale", teams_and_wins.get("Yale", 0), 2),
        ("California Baptist", teams_and_wins.get("California Baptist", 0), 0.5),
        ("UC Irvine", teams_and_wins.get("UC Irvine", 0), 17),
        ("Radford", teams_and_wins.get("Radford", 0), 1.5),
        ("Robert Morris", teams_and_wins.get("Robert Morris", 0), 0.25),
        ("Central Michigan", teams_and_wins.get("Central Michigan", 0), 0.25),
        ("Norfolk State", teams_and_wins.get("Norfolk State", 0), 5),
    ]

    # Final owner_teams dictionary with all owners
    owner_teams = {
        "Owner 1": e3_teams,
        "Owner 2": worthy_teams,
        "Owner 3": mt_beers_teams,
        "Owner 4": mark_bears_teams,
        "Owner 5": rick_dan_teams,
        "Owner 6": booty_posse_teams,
        "Owner 7": mruz_teams,
        "Owner 8": john_h_teams,
        "Owner 9": leonard_teams,
        "Owner 10": team_jody_teams,
        "Owner 11": parrott_depa_teams,
        "Owner 12": jj_stevens_teams,
        "Owner 13": mark_brandon_teams,
        "Owner 14": collin_ty_teams,
        "Owner 15": ody_teams,
        "Owner 16": leb1_teams,
        "Owner 17": leb2_teams,
        "Owner 18": jake_w_teams,
        "Owner 19": jd_teams,
        "Owner 20": bryan_teams,
        "Owner 21": nemo_teams,
    }


    # Calculate total points for each owner
    owner_totals = {
        owner: sum([team[1] for team in teams])
        for owner, teams in owner_teams.items()
    }

    # Generate the HTML output
    generate_html_output(owner_teams, owner_totals)



# Execute the game
run_fantasy_basketball_game()