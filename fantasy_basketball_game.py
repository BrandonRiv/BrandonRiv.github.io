import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Fetch team data (school names and wins)
def fetch_teams_and_wins():
    url = "https://www.sports-reference.com/cbb/seasons/men/2026-school-stats.html"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'basic_school_stats'})

    if not table:
        print("Could not find the table on the page.")
        return {}

    teams_and_wins = {}
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 2:
            school_name = cells[0].text.strip()
            overall_wins = cells[2].text.strip()

            if school_name.endswith('NCAA'):
                school_name = school_name[:-4].strip()

            if overall_wins.isdigit():
                teams_and_wins[school_name] = int(overall_wins)

    return teams_and_wins


def generate_html_output(owner_teams, owner_totals):
    sorted_owners = sorted(owner_totals.items(), key=lambda x: x[1], reverse=True)

    place_labels = {0: "1st", 1: "2nd", 2: "3rd"}

    # NEW OWNER NAME MAPPING (19 owners, Option C)
    owner_names = {
        "Owner 1": "Dollar General",
        "Owner 2": "E-3",
        "Owner 3": "MT Beers",
        "Owner 4": "Mark Bears",
        "Owner 5": "Rick-Dan",
        "Owner 6": "Leonard",
        "Owner 7": "John H",
        "Owner 8": "JJ Stevens",
        "Owner 9": "Mark-Brandon",
        "Owner 10": "Collin-Ty",
        "Owner 11": "Jody",
        "Owner 12": "Mruz",
        "Owner 13": "Leb1",
        "Owner 14": "Leb2",
        "Owner 15": "Ody",
        "Owner 16": "Nemo",
        "Owner 17": "Worthy",
        "Owner 18": "Booty Posse",
        "Owner 19": "JD",
    }

    team_values = []
    low_cost_teams = []

    for owner, teams in owner_teams.items():
        for team_name, wins, cost in teams:
            value = wins - cost
            team_values.append((owner, team_name, wins, cost, value))
            if cost <= 1:
                low_cost_teams.append((owner, team_name, wins, cost))

    team_values = sorted(team_values, key=lambda x: x[4], reverse=True)[:5]
    low_cost_teams = sorted(low_cost_teams, key=lambda x: x[2], reverse=True)[:5]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # (HTML TEMPLATE UNCHANGED — KEEPING EXACTLY AS ORIGINAL)
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

    value_rows = ""
    for owner, team_name, wins, cost, value in team_values:
        owner_name = owner_names[owner]
        value_rows += f"<tr><td>{owner_name}</td><td>{team_name}</td><td>{wins}</td><td>{cost:.2f}</td><td>{value:.2f}</td></tr>"

    low_cost_rows = ""
    for owner, team_name, wins, cost in low_cost_teams:
        owner_name = owner_names[owner]
        low_cost_rows += f"<tr><td>{owner_name}</td><td>{team_name}</td><td>{wins}</td><td>{cost:.2f}</td></tr>"

    ranking_rows = ""
    for i, (owner, total_points) in enumerate(sorted_owners):
        owner_name = owner_names[owner]
        ranking_rows += f"<tr><td>{owner_name}</td><td>{total_points}</td></tr>"

    owner_tables = ""
    owner_counter = 0

    for i, (owner, _) in enumerate(sorted_owners):
        teams = owner_teams[owner]
        total_points = sum([team[1] for team in teams])

        place = f" ({place_labels[i]})" if i in place_labels else ""

        owner_table = f"<table><caption><h2>{owner_names[owner]}{place}</h2></caption>"
        owner_table += "<tr><th>Teams</th><th>Points</th><th>Cost</th></tr>"

        for team_name, points, cost in teams:
            owner_table += f"<tr><td class='team-col'>{team_name}</td><td class='points-col'>{points}</td><td class='cost-col'>{cost}</td></tr>"

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

    html_content = html_template.format(
        value_rows=value_rows,
        low_cost_rows=low_cost_rows,
        ranking_rows=ranking_rows,
        owner_tables=owner_tables,
        timestamp=timestamp
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Results have been saved to 'index.html'.")


def run_fantasy_basketball_game():
    teams_and_wins = fetch_teams_and_wins()

    # ============================
    # 🔥 NEW HARD-CODED TEAMS (ALL 19 OWNERS)
    # ============================

    owner_teams = {

        # Owner 1 — Dollar General
        "Owner 1": [
            ("Arizona", teams_and_wins.get("Arizona", 0), 20),
            ("Jacksonville State", teams_and_wins.get("Jacksonville State", 0), 0.75),
            ("Kennesaw State", teams_and_wins.get("Kennesaw State", 0), 1.5),
            ("UC Santa Barbara", teams_and_wins.get("UC Santa Barbara", 0), 3.5),
            ("California Baptist", teams_and_wins.get("California Baptist", 0), 7.5),
            ("Marshall", teams_and_wins.get("Marshall", 0), 3.5),
            ("Buffalo", teams_and_wins.get("Buffalo", 0), 0.25),
            ("SIU Edwardsville", teams_and_wins.get("SIU Edwardsville", 0), 5.5),
            ("Tennessee Martin", teams_and_wins.get("Tennessee-Martin", 0), 5.5),
            ("Fairfield", teams_and_wins.get("Fairfield", 0), 0.25),
        ],

        # Owner 2 — E-3
        "Owner 2": [
            ("Alabama", teams_and_wins.get("Alabama", 0), 9),
            ("Georgia", teams_and_wins.get("Georgia", 0), 8.5),
            ("Cincinnati", teams_and_wins.get("Cincinnati", 0), 4),
            ("Colorado", teams_and_wins.get("Colorado", 0), 1),
            ("Kansas", teams_and_wins.get("Kansas", 0), 9),
            ("Butler", teams_and_wins.get("Butler", 0), 4.5),
            ("NC State", teams_and_wins.get("NC State", 0), 8),
            ("Colorado State", teams_and_wins.get("Colorado State", 0), 5),
            ("Temple", teams_and_wins.get("Temple", 0), 0.5),
            ("Bowling Green", teams_and_wins.get("Bowling Green", 0), 0.5),
        ],

        # Owner 3 — MT Beers
        "Owner 3": [
            ("Arkansas", teams_and_wins.get("Arkansas", 0), 7),
            ("Texas Tech", teams_and_wins.get("Texas Tech", 0), 9),
            ("Louisville", teams_and_wins.get("Louisville", 0), 13),
            ("Grand Canyon", teams_and_wins.get("Grand Canyon", 0), 3),
            ("UAB", teams_and_wins.get("UAB", 0), 6),
            ("Belmont", teams_and_wins.get("Belmont", 0), 6),
            ("Indiana State", teams_and_wins.get("Indiana State", 0), 0.25),
            ("Middle Tennessee", teams_and_wins.get("Middle Tennessee", 0), 2),
            ("Furman", teams_and_wins.get("Furman", 0), 2),
            ("Jacksonville", teams_and_wins.get("Jacksonville", 0), 0.25),
        ],

        # Owner 4 — Mark Bears
        "Owner 4": [
            ("Vanderbilt", teams_and_wins.get("Vanderbilt", 0), 8),
            ("Michigan", teams_and_wins.get("Michigan", 0), 14),
            ("Northwestern", teams_and_wins.get("Northwestern", 0), 3),
            ("Rutgers", teams_and_wins.get("Rutgers", 0), 0.25),
            ("Providence", teams_and_wins.get("Providence", 0), 2),
            ("Virginia Tech", teams_and_wins.get("Virginia Tech", 0), 2),
            ("Davidson", teams_and_wins.get("Davidson", 0), 2),
            ("George Mason", teams_and_wins.get("George Mason", 0), 8),
            ("Wichita State", teams_and_wins.get("Wichita State", 0), 6),
            ("Seattle", teams_and_wins.get("Seattle", 0), 2),
        ],

        # Owner 5 — Rick-Dan
        "Owner 5": [
            ("Quinnipiac", teams_and_wins.get("Quinnipiac", 0), 8.5),
            ("Milwaukee", teams_and_wins.get("Milwaukee", 0), 0.25),
            ("McNeese State", teams_and_wins.get("McNeese State", 0), 10),
            ("UNC Asheville", teams_and_wins.get("UNC Asheville", 0), 0.5),
            ("James Madison", teams_and_wins.get("James Madison", 0), 2),
            ("Drake", teams_and_wins.get("Drake", 0), 0.25),
            ("UNLV", teams_and_wins.get("Nevada-Las Vegas", 0), 0.5),
            ("St. John's (NY)", teams_and_wins.get("St. John's (NY)", 0), 12.5),
            ("Nebraska", teams_and_wins.get("Nebraska", 0), 7),
            ("San Diego State", teams_and_wins.get("San Diego State", 0), 8.5),
        ],

        # Owner 6 — Leonard
        "Owner 6": [
            ("Florida", teams_and_wins.get("Florida", 0), 12),
            ("Oregon", teams_and_wins.get("Oregon", 0), 2),
            ("Purdue", teams_and_wins.get("Purdue", 0), 20),
            ("Kansas State", teams_and_wins.get("Kansas State", 0), 3.5),
            ("Marquette", teams_and_wins.get("Marquette", 0), 3.5),
            ("Notre Dame", teams_and_wins.get("Notre Dame", 0), 2),
            ("Nevada", teams_and_wins.get("Nevada", 0), 0.25),
            ("Duquesne", teams_and_wins.get("Duquesne", 0), 1),
            ("St. Joseph's", teams_and_wins.get("Saint Joseph's", 0), 0.25),
            ("Tulane", teams_and_wins.get("Tulane", 0), 3.5),
        ],

        # Owner 7 — John H
        "Owner 7": [
            ("Auburn", teams_and_wins.get("Auburn", 0), 3),
            ("Murray State", teams_and_wins.get("Murray State", 0), 4),
            ("Utah Valley", teams_and_wins.get("Utah Valley", 0), 5),
            ("UNC Wilmington", teams_and_wins.get("UNC Wilmington", 0), 8),
            ("Kent State", teams_and_wins.get("Kent State", 0), 5.5),
            ("High Point", teams_and_wins.get("High Point", 0), 14),
            ("Southeast Missouri State", teams_and_wins.get("Southeast Missouri State", 0), 0.25),
            ("Central Connecticut State", teams_and_wins.get("Central Connecticut State", 0), 4.5),
            ("LIU Brooklyn", teams_and_wins.get("Long Island University", 0), 4.5),
            ("Tarleton State", teams_and_wins.get("Tarleton State", 0), 1.25),
        ],

        # Owner 8 — JJ Stevens
        "Owner 8": [
            ("Kentucky", teams_and_wins.get("Kentucky", 0), 9),
            ("West Virginia", teams_and_wins.get("West Virginia", 0), 0.25),
            ("Georgetown", teams_and_wins.get("Georgetown", 0), 4.5),
            ("Miami (FL)", teams_and_wins.get("Miami (FL)", 0), 5.5),
            ("George Washington", teams_and_wins.get("George Washington", 0), 8),
            ("South Florida", teams_and_wins.get("South Florida", 0), 4),
            ("USC", teams_and_wins.get("Southern California", 0), 2),
            ("Columbia", teams_and_wins.get("Columbia", 0), 1.5),
            ("Hawaii", teams_and_wins.get("Hawaii", 0), 5.5),
            ("Portland State", teams_and_wins.get("Portland State", 0), 0.25),
        ],

        # Owner 9 — Mark-Brandon
        "Owner 9": [
            ("Illinois", teams_and_wins.get("Illinois", 0), 10.5),
            ("Iowa", teams_and_wins.get("Iowa", 0), 4),
            ("California", teams_and_wins.get("California", 0), 2),
            ("Syracuse", teams_and_wins.get("Syracuse", 0), 4.5),
            ("VCU", teams_and_wins.get("VCU", 0), 1),
            ("Florida Atlantic", teams_and_wins.get("Florida Atlantic", 0), 7),
            ("East Tennessee State", teams_and_wins.get("East Tennessee State", 0), 1),
            ("UT Arlington", teams_and_wins.get("UT Arlington", 0), 2),
            ("Northern Colorado", teams_and_wins.get("Northern Colorado", 0), 4),
            ("Wright State", teams_and_wins.get("Wright State", 0), 3),
        ],

        # Owner 10 — Collin-Ty
        "Owner 10": [
            ("LSU", teams_and_wins.get("Louisiana State", 0), 3.5),
            ("Wisconsin", teams_and_wins.get("Wisconsin", 0), 3.5),
            ("BYU", teams_and_wins.get("Brigham Young", 0), 10.5),
            ("Villanova", teams_and_wins.get("Villanova", 0), 5.5),
            ("Clemson", teams_and_wins.get("Clemson", 0), 7.5),
            ("Virginia", teams_and_wins.get("Virginia", 0), 6.5),
            ("St. Bonaventure", teams_and_wins.get("St. Bonaventure", 0), 3.5),
            ("Loyola Marymount", teams_and_wins.get("Loyola Marymount", 0), 5),
            ("Western Kentucky", teams_and_wins.get("Western Kentucky", 0), 2),
            ("Northern Kentucky", teams_and_wins.get("Northern Kentucky", 0), 1.5),
        ],

        # Owner 11 — Jody
        "Owner 11": [
            ("Iowa State", teams_and_wins.get("Iowa State", 0), 14),
            ("Duke", teams_and_wins.get("Duke", 0), 15),
            ("Saint Louis", teams_and_wins.get("Saint Louis", 0), 8),
            ("Illinois State", teams_and_wins.get("Illinois State", 0), 1),
            ("UC Davis", teams_and_wins.get("UC Davis", 0), 1),
            ("Mercer", teams_and_wins.get("Mercer", 0), 0.25),
            ("Texas State", teams_and_wins.get("Texas State", 0), 0.25),
            ("Miami (OH)", teams_and_wins.get("Miami (OH)", 0), 7),
            ("Oakland", teams_and_wins.get("Oakland", 0), 0.25),
            ("Youngstown State", teams_and_wins.get("Youngstown State", 0), 3),
        ],

        # Owner 12 — Mruz
        "Owner 12": [
            ("Michigan State", teams_and_wins.get("Michigan State", 0), 14),
            ("Oklahoma State", teams_and_wins.get("Oklahoma State", 0), 6),
            ("SMU", teams_and_wins.get("Southern Methodist", 0), 6),
            ("Richmond", teams_and_wins.get("Richmond", 0), 1.5),
            ("UC Irvine", teams_and_wins.get("UC Irvine", 0), 3),
            ("Wofford", teams_and_wins.get("Wofford", 0), 0.25),
            ("South Alabama", teams_and_wins.get("South Alabama", 0), 5),
            ("Stephen F. Austin", teams_and_wins.get("Stephen F. Austin", 0), 8),
            ("Siena", teams_and_wins.get("Siena", 0), 4),
            ("College of Charleston", teams_and_wins.get("College of Charleston", 0), 0.25),
        ],

        # Owner 13 — Leb1
        "Owner 13": [
            ("Mississippi", teams_and_wins.get("Mississippi", 0), 2),
            ("Texas A&M", teams_and_wins.get("Texas A&M", 0), 1.5),
            ("Indiana", teams_and_wins.get("Indiana", 0), 7.5),
            ("Maryland", teams_and_wins.get("Maryland", 0), 0.25),
            ("Penn State", teams_and_wins.get("Penn State", 0), 4),
            ("UCLA", teams_and_wins.get("UCLA", 0), 6),
            ("Arizona State", teams_and_wins.get("Arizona State", 0), 3),
            ("UCF", teams_and_wins.get("UCF", 0), 1.5),
            ("Gonzaga", teams_and_wins.get("Gonzaga", 0), 26),
            ("Northern Iowa", teams_and_wins.get("Northern Iowa", 0), 9),
        ],

        # Owner 14 — Leb2
        "Owner 14": [
            ("Oklahoma", teams_and_wins.get("Oklahoma", 0), 0.25),
            ("Washington", teams_and_wins.get("Washington", 0), 0.25),
            ("Florida State", teams_and_wins.get("Florida State", 0), 1.5),
            ("North Carolina", teams_and_wins.get("North Carolina", 0), 11),
            ("Rhode Island", teams_and_wins.get("Rhode Island", 0), 1.5),
            ("North Texas", teams_and_wins.get("North Texas", 0), 7),
            ("Oregon State", teams_and_wins.get("Oregon State", 0), 0.25),
            ("Saint Mary's (CA)", teams_and_wins.get("Saint Mary's (CA)", 0), 10),
            ("Bradley", teams_and_wins.get("Bradley", 0), 3),
            ("Liberty", teams_and_wins.get("Liberty", 0), 9),
        ],

        # Owner 15 — Ody
        "Owner 15": [
            ("Missouri", teams_and_wins.get("Missouri", 0), 7),
            ("Wake Forest", teams_and_wins.get("Wake Forest", 0), 4.5),
            ("Boise State", teams_and_wins.get("Boise State", 0), 4.5),
            ("New Mexico", teams_and_wins.get("New Mexico", 0), 4.5),
            ("Wyoming", teams_and_wins.get("Wyoming", 0), 1),
            ("Yale", teams_and_wins.get("Yale", 0), 3),
            ("Akron", teams_and_wins.get("Akron", 0), 9.5),
            ("Winthrop", teams_and_wins.get("Winthrop", 0), 5),
            ("North Dakota State", teams_and_wins.get("North Dakota State", 0), 0),
            ("Iona", teams_and_wins.get("Iona", 0), 6),
        ],

        # Owner 16 — Nemo
        "Owner 16": [
            ("Tennessee", teams_and_wins.get("Tennessee", 0), 12.5),
            ("Baylor", teams_and_wins.get("Baylor", 0), 5.5),
            ("Seton Hall", teams_and_wins.get("Seton Hall", 0), 4.5),
            ("Washington State", teams_and_wins.get("Washington State", 0), 0.25),
            ("New Mexico State", teams_and_wins.get("New Mexico State", 0), 6),
            ("UC San Diego", teams_and_wins.get("UC San Diego", 0), 8),
            ("Sacramento State", teams_and_wins.get("Sacramento State", 0), 0.25),
            ("Lamar", teams_and_wins.get("Lamar", 0), 0.25),
            ("St. Thomas (MN)", teams_and_wins.get("St. Thomas", 0), 9),
            ("Radford", teams_and_wins.get("Radford", 0), 0.25),
        ],

        # Owner 17 — Worthy
        "Owner 17": [
            ("Houston", teams_and_wins.get("Houston", 0), 19),
            ("Creighton", teams_and_wins.get("Creighton", 0), 5),
            ("Memphis", teams_and_wins.get("Memphis", 0), 4),
            ("Sam Houston", teams_and_wins.get("Sam Houston", 0), 0.25),
            ("Montana State", teams_and_wins.get("Montana State", 0), 6),
            ("Nebraska Omaha", teams_and_wins.get("Omaha", 0), 0.25),
            ("Austin Peay", teams_and_wins.get("Austin Peay", 0), 1),
            ("Colgate", teams_and_wins.get("Colgate", 0), 3.5),
            ("Vermont", teams_and_wins.get("Vermont", 0), 8),
            ("Norfolk State", teams_and_wins.get("Norfolk State", 0), 6.5),
        ],

        # Owner 18 — Booty Posse
        "Owner 18": [
            ("Texas", teams_and_wins.get("Texas", 0), 3.5),
            ("Ohio State", teams_and_wins.get("Ohio State", 0), 8),
            ("Connecticut", teams_and_wins.get("Connecticut", 0), 13.5),
            ("Georgia Tech", teams_and_wins.get("Georgia Tech", 0), 0.5),
            ("San Francisco", teams_and_wins.get("San Francisco", 0), 1.5),
            ("Towson", teams_and_wins.get("Towson", 0), 4.5),
            ("Troy", teams_and_wins.get("Troy", 0), 4.5),
            ("Montana", teams_and_wins.get("Montana", 0), 2),
            ("South Dakota State", teams_and_wins.get("South Dakota State", 0), 4),
            ("Queens", teams_and_wins.get("Queens (NC)", 0), 0.25),
        ],

        # Owner 19 — JD
        "Owner 19": [
            ("Utah State", teams_and_wins.get("Utah State", 0), 11.5),
            ("Dayton", teams_and_wins.get("Dayton", 0), 4.5),
            ("Tulsa", teams_and_wins.get("Tulsa", 0), 5.5),
            ("Santa Clara", teams_and_wins.get("Santa Clara", 0), 6),
            ("Chattanooga", teams_and_wins.get("Chattanooga", 0), 2),
            ("William & Mary", teams_and_wins.get("William & Mary", 0), 3.5),
            ("Marist", teams_and_wins.get("Marist", 0), 1),
            ("Florida Gulf Coast", teams_and_wins.get("Florida Gulf Coast", 0), 3),
            ("Navy", teams_and_wins.get("Navy", 0), 5),
            ("Southern", teams_and_wins.get("Southern", 0), 7),
        ],
    }

    owner_totals = {
        owner: sum([team[1] for team in teams])
        for owner, teams in owner_teams.items()
    }

    generate_html_output(owner_teams, owner_totals)


if __name__ == "__main__":
    run_fantasy_basketball_game()
