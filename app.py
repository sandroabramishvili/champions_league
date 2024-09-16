from flask import Flask, render_template, request, redirect, url_for
from champions_league import ChampionsLeague  # Import your separate logic
import os

app = Flask(__name__)

# Initialize Champions League with teams and matches
teams = [
    "Milan", "Arsenal", "AS Monaco", "Aston Villa", "Atalanta", "Atl. Madrid", "Leverkusen", "Bayern", "Bologna",
    "Dortmund", "Celtic", "Club Brugge", "Barcelona", "RB Salzburg", "Shakhtar", "Feyenoord", "Crvena zvezda", "Girona",
    "Dinamo", "Inter", "Juventus", "Lille", "Liverpool", "Man City", "PSG", "PSV", "Leipzig", "Real Madrid", "Slovan",
    "Sturm", "Benfica", "Sparta Praha", "Sporting", "Brest", "Stuttgart", "Young Boys"
]

matches = {
    1: [
        ("Young Boys", "Aston Villa"),
        ("Juventus", "PSV"),
        ("Milan", "Liverpool"),
        ("Bayern", "Dinamo"),
        ("Real Madrid", "Stuttgart"),
        ("Sporting", "Lille"),
        ("Sparta Praha", "RB Salzburg"),
        ("Bologna", "Shakhtar"),
        ("Celtic", "Slovan"),
        ("Club Brugge", "Dortmund"),
        ("Man City", "Inter"),
        ("PSG", "Girona"),
        ("Feyenoord", "Leverkusen"),
        ("Crvena zvezda", "Benfica"),
        ("AS Monaco", "Barcelona"),
        ("Atalanta", "Arsenal"),
        ("Atl. Madrid", "Leipzig"),
        ("Brest", "Sturm"),
    ],
    2: [
        ("RB Salzburg", "Brest"),
        ("Stuttgart", "Sparta Praha"),
        ("Arsenal", "PSG"),
        ("Leverkusen", "Milan"),
        ("Dortmund", "Celtic"),
        ("Barcelona", "Young Boys"),
        ("Inter", "Crvena zvezda"),
        ("PSV", "Sporting"),
        ("Slovan", "Man City"),
        ("Shakhtar", "Atalanta"),
        ("Girona", "Feyenoord"),
        ("Aston Villa", "Bayern"),
        ("Dinamo", "AS Monaco"),
        ("Liverpool", "Bologna"),
        ("Lille", "Real Madrid"),
        ("Leipzig", "Juventus"),
        ("Sturm", "Club Brugge"),
        ("Benfica", "Atl. Madrid"),
    ],
    3: [
        ("Milan", "Club Brugge"),
        ("AS Monaco", "Crvena zvezda"),
        ("Arsenal", "Shakhtar"),
        ("Aston Villa", "Bologna"),
        ("Girona", "Slovan"),
        ("Juventus", "Stuttgart"),
        ("PSG", "PSV"),
        ("Real Madrid", "Dortmund"),
        ("Sturm", "Sporting"),
        ("Atalanta", "Celtic"),
        ("Brest", "Leverkusen"),
        ("Atl. Madrid", "Lille"),
        ("Young Boys", "Inter"),
        ("Barcelona", "Bayern"),
        ("RB Salzburg", "Dinamo"),
        ("Man City", "Sparta Praha"),
        ("Leipzig", "Liverpool"),
        ("Benfica", "Feyenoord"),
    ],
    4: [
        ("PSV", "Girona"),
        ("Slovan", "Dinamo"),
        ("Bologna", "AS Monaco"),
        ("Dortmund", "Sturm"),
        ("Celtic", "Leipzig"),
        ("Liverpool", "Leverkusen"),
        ("Lille", "Juventus"),
        ("Real Madrid", "Milan"),
        ("Sporting", "Man City"),
        ("Club Brugge", "Aston Villa"),
        ("Shakhtar", "Young Boys"),
        ("Sparta Praha", "Brest"),
        ("Bayern", "Benfica"),
        ("Inter", "Arsenal"),
        ("Feyenoord", "RB Salzburg"),
        ("Crvena zvezda", "Barcelona"),
        ("PSG", "Atl. Madrid"),
        ("Stuttgart", "Atalanta"),
    ],
    5: [
        ("Sparta Praha", "Atl. Madrid"),
        ("Slovan", "Milan"),
        ("Leverkusen", "RB Salzburg"),
        ("Young Boys", "Atalanta"),
        ("Barcelona", "Brest"),
        ("Bayern", "PSG"),
        ("Inter", "Leipzig"),
        ("Man City", "Feyenoord"),
        ("Sporting", "Arsenal"),
        ("Crvena zvezda", "Stuttgart"),
        ("Sturm", "Girona"),
        ("AS Monaco", "Benfica"),
        ("Aston Villa", "Juventus"),
        ("Bologna", "Lille"),
        ("Celtic", "Club Brugge"),
        ("Dinamo", "Dortmund"),
        ("Liverpool", "Real Madrid"),
        ("PSV", "Shakhtar"),
    ],
    6: [
        ("Girona", "Liverpool"),
        ("Dinamo", "Celtic"),
        ("Atalanta", "Real Madrid"),
        ("Leverkusen", "Inter"),
        ("Club Brugge", "Sporting"),
        ("RB Salzburg", "PSG"),
        ("Shakhtar", "Bayern"),
        ("Leipzig", "Aston Villa"),
        ("Brest", "PSV"),
        ("Atl. Madrid", "Slovan"),
        ("Lille", "Sturm"),
        ("Milan", "Crvena zvezda"),
        ("Arsenal", "AS Monaco"),
        ("Dortmund", "Barcelona"),
        ("Feyenoord", "Sparta Praha"),
        ("Juventus", "Man City"),
        ("Benfica", "Bologna"),
        ("Stuttgart", "Young Boys"),
    ],
    7: [
        ("AS Monaco", "Aston Villa"),
        ("Atalanta", "Sturm"),
        ("Atl. Madrid", "Leverkusen"),
        ("Bologna", "Dortmund"),
        ("Club Brugge", "Juventus"),
        ("Crvena zvezda", "PSV"),
        ("Liverpool", "Lille"),
        ("Slovan", "Stuttgart"),
        ("Benfica", "Barcelona"),
        ("Shakhtar", "Brest"),
        ("Leipzig", "Sporting"),
        ("Milan", "Girona"),
        ("Sparta Praha", "Inter"),
        ("Arsenal", "Dinamo"),
        ("Celtic", "Young Boys"),
        ("Feyenoord", "Bayern"),
        ("PSG", "Man City"),
        ("Real Madrid", "RB Salzburg"),
    ],
    8: [
        ("Aston Villa", "Celtic"),
        ("Leverkusen", "Sparta Praha"),
        ("Dortmund", "Shakhtar"),
        ("Young Boys", "Crvena zvezda"),
        ("Barcelona", "Atalanta"),
        ("Bayern", "Slovan"),
        ("Inter", "AS Monaco"),
        ("RB Salzburg", "Atl. Madrid"),
        ("Girona", "Arsenal"),
        ("Dinamo", "Milan"),
        ("Juventus", "Benfica"),
        ("Lille", "Feyenoord"),
        ("Man City", "Club Brugge"),
        ("PSV", "Liverpool"),
        ("Sturm", "Leipzig"),
        ("Sporting", "Bologna"),
        ("Brest", "Real Madrid"),
        ("Stuttgart", "PSG"),
    ],
}

champions_league = ChampionsLeague(teams, matches)

# Track the current matchday
current_matchday = 1


@app.route('/')
def home():
    # Redirect to matchday 1 automatically
    return redirect(url_for('matchday_form', matchday=current_matchday))


@app.route('/matchday/<int:matchday>', methods=['GET'])
def matchday_form(matchday):
    """Render matchday page with the list of matches."""
    if matchday in champions_league.matches:
        return render_template('matchday.html', matchday=matchday, matches=champions_league.matches[matchday])
    return redirect(url_for('display_table'))  # Show table after the last matchday


@app.route('/submit_scores', methods=['POST'])
def submit_scores():
    """Handle the submission of scores."""
    global current_matchday
    matchday = int(request.form['matchday'])
    if matchday in champions_league.matches:
        # Loop through each match and record the score
        for match in champions_league.matches[matchday]:
            home_team, away_team = match
            try:
                # Get the submitted scores from the form
                goals_home = int(request.form[f"{home_team}_score"])
                goals_away = int(request.form[f"{away_team}_score"])
                # Record the match result in the ChampionsLeague class
                champions_league.record_match(home_team, away_team, goals_home, goals_away)
            except (ValueError, KeyError):
                # If there was an error, reload the matchday form
                return redirect(url_for('matchday_form', matchday=matchday))

        # After recording all matches, move to the next matchday
        current_matchday += 1
        if current_matchday > len(champions_league.matches):
            return redirect(url_for('display_table'))  # Show table after the last matchday
        return redirect(url_for('matchday_form', matchday=current_matchday))

    return redirect(url_for('display_table'))  # Show table if matchday is not valid


@app.route('/table', methods=['GET'])
def display_table():
    """Display the league table."""
    table = champions_league.get_table()
    print("Table data:", table)  # Debugging line
    return render_template('table.html', table=table, matchday=current_matchday - 1)

if __name__ == '__main__':
    # Use the PORT environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
