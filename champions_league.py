class Team:
    def __init__(self, name):
        self.name = name
        self.played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
        self.last_five = []  # Track the results of the last 5 games as a list

    def update_results(self, goals_for, goals_against):
        """Update the team's stats based on the match result."""
        self.played += 1
        self.goals_for += goals_for
        self.goals_against += goals_against
        if goals_for > goals_against:
            self.wins += 1
            self.points += 3
            self.last_five.append('W')
        elif goals_for == goals_against:
            self.draws += 1
            self.points += 1
            self.last_five.append('D')
        else:
            self.losses += 1
            self.last_five.append('L')
        # Keep last five results only
        if len(self.last_five) > 5:
            self.last_five.pop(0)

    def display_team_info(self):
        """Return the team's current statistics."""
        last_five_str = ''.join(self.last_five[-5:])
        goal_difference = self.goals_for - self.goals_against
        return {
            "name": self.name,
            "played": self.played,
            "wins": self.wins,
            "draws": self.draws,
            "losses": self.losses,
            "goals_for": self.goals_for,
            "goals_against": self.goals_against,
            "goal_difference": goal_difference,
            "points": self.points,
            "last_five": last_five_str
        }

class ChampionsLeague:
    def __init__(self, teams, matches):
        self.teams = {team: Team(team) for team in teams}
        self.matches = matches

    def record_match(self, team1, team2, goals1, goals2):
        """Record the result of a match between two teams."""
        if team1 in self.teams and team2 in self.teams:
            self.teams[team1].update_results(goals1, goals2)
            self.teams[team2].update_results(goals2, goals1)
        else:
            raise ValueError(f"One of the teams '{team1}' or '{team2}' does not exist.")

    def get_matchday_matches(self, matchday):
        """Return matches for a given matchday."""
        return self.matches.get(matchday, [])

    def get_team_info(self, team_name):
        """Return information for a given team."""
        team = self.teams.get(team_name)
        if team:
            return team.display_team_info()
        return None

    def get_table(self):
        """Return the current standings."""
        sorted_teams = sorted(self.teams.values(),
                              key=lambda x: (-x.points, -(x.goals_for - x.goals_against), -x.goals_for))
        table_data = []
        for team in sorted_teams:
            team_info = {
                "name": team.name,
                "played": team.played,
                "wins": team.wins,
                "draws": team.draws,
                "losses": team.losses,
                "goals_for": team.goals_for,
                "goals_against": team.goals_against,
                "goal_difference": team.goals_for - team.goals_against,
                "last_five": ''.join(team.last_five[-5:]),
                "points": team.points
            }
            table_data.append(team_info)
        return table_data

