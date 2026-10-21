
class invalidinput(Exception):
    pass

class invlaidtype(Exception):
    pass

class duplicate_values(Exception):
    pass

teams_obj = []
teams_names = set()
pair_count = {}


def no_of_teams():
    while True:
        try:
            n = int(input("Enter the no of teams: "))
            if n < 2:
                raise invalidinput("At least 2 teams are required")
            return n
        except ValueError:
            print("Please enter only integer")
        except invalidinput as e:
            print(e)

def add_teams():
    n = no_of_teams()

    while len(teams_obj) < n:
        name = input("Enter team name: ").strip()
        if not name:
            print("Name cannot be empty")
            continue

        if name.lower() in teams_names:
            print("Team already exists")
            continue

        teams_names.add(name.lower())
        teams_obj.append(team(name))

class team:
    def __init__(self, name):
        self.name = name
        self.no_matchs = 0
        self.match_won = 0
        self.match_lost = 0
        self.match_tied = 0
        self.total_points = 0
        self.runs_scored = 0
        self.runs_given = 0
        self.balls_faced = 0
        self.balls_bowled = 0
        self.nrr = 0

def get_number(message, low, high):
    while True:
        try:
            n = int(input(message))
            if n < low or n > high:
                raise invalidinput("Invalid value")
            return n
        except ValueError:
            print("Enter only integer")
        except invalidinput as e:
            print(e)

def get_innings(name):
    while True:
        runs = get_number(f"Enter runs of {name}: ", 0, 1000000)
        wickets = get_number(f"Enter wickets of {name}: ", 0, 10)
        overs = get_number(f"Enter overs of {name}: ", 0, 20)
        balls = get_number(f"Enter remaining balls of {name}: ", 0, 5)
        if overs == 20 and balls != 0:
            print("At 20 overs balls must be zero")
            continue

        if overs * 6 + balls == 0:
            print("Overs and balls cannot both be zero")
            continue

        return runs, wickets, overs, balls

def caluclate_nrr(t):
    if t.balls_faced == 0 or t.balls_bowled == 0:
        return 0

    return (
        t.runs_scored / (t.balls_faced / 6)
        - t.runs_given / (t.balls_bowled / 6)
    )

class match:
    def __init__(self, match_number, first_team, second_team,
                 first_team_Score, second_team_Score,
                 first_team_wickets, team1_overs_played,
                 team2_overs_played, second_team_wicket,
                 first_team_ball_played, second_team_ball_played):

        self.match_number = match_number
        self.first_team = first_team
        self.second_team = second_team
        self.first_team_Score = first_team_Score
        self.second_team_Score = second_team_Score
        self.first_team_wickets = first_team_wickets
        self.second_team_wicket = second_team_wicket
        self.first_team_overs = team1_overs_played
        self.second_team_overs = team2_overs_played
        self.first_team_ball_played = first_team_ball_played
        self.second_team_ball_played = second_team_ball_played

    def match_result(self):
        a = self.first_team
        b = self.second_team
        a.no_matchs += 1
        b.no_matchs += 1
        a.runs_scored += self.first_team_Score
        a.runs_given += self.second_team_Score
        b.runs_scored += self.second_team_Score
        b.runs_given += self.first_team_Score
        balls_a = self.first_team_overs[2] * 6 + self.first_team_overs[3]
        balls_b = self.second_team_overs[2] * 6 + self.second_team_overs[3]

        if self.first_team_overs[1] == 10 and balls_a < 120:
            balls_a = 120
        if self.second_team_overs[1] == 10 and balls_b < 120:
            balls_b = 120

        a.balls_faced += balls_a
        a.balls_bowled += balls_b
        b.balls_faced += balls_b
        b.balls_bowled += balls_a

        if self.first_team_Score > self.second_team_Score:
            a.match_won += 1
            b.match_lost += 1
            a.total_points += 2
        elif self.first_team_Score < self.second_team_Score:
            b.match_won += 1
            a.match_lost += 1
            b.total_points += 2
        else:
            a.match_tied += 1
            b.match_tied += 1
            a.total_points += 1
            b.total_points += 1

        a.nrr = caluclate_nrr(a)
        b.nrr = caluclate_nrr(b)

def display():
    for t in sorted(teams_obj,
                    key=lambda x: (x.total_points, x.nrr),
                    reverse=True):
        print(
            t.name, t.no_matchs, t.match_won,
            t.match_lost, t.match_tied,
            t.total_points, t.runs_scored,
            t.runs_given, round(t.nrr, 3)
        )


def main():
    add_teams()

    total_matches = len(teams_obj) * (len(teams_obj) - 1)
    match_number = 1

    while match_number <= total_matches:
        try:
            name1 = input("Enter first team: ").strip().lower()
            name2 = input("Enter second team: ").strip().lower()

            team_dict = {t.name.lower(): t for t in teams_obj}

            if name1 not in team_dict or name2 not in team_dict:
                raise invalidinput("Team does not exist")

            if name1 == name2:
                raise invalidinput("Team cannot play against itself")

            pair = tuple(sorted((name1, name2)))

            if pair_count.get(pair, 0) == 2:
                raise invalidinput("Teams already played twice")

            a = team_dict[name1]
            b = team_dict[name2]

            print("Enter first team innings")
            runs1, wickets1, overs1, balls1 = get_innings(a.name)

            print("Enter second team innings")
            runs2, wickets2, overs2, balls2 = get_innings(b.name)
            m = match(
                match_number, a, b, runs1, runs2,
                wickets1, (overs1, wickets1, overs1, balls1),
                (overs2, wickets2, overs2, balls2),
                wickets2, balls1, balls2
            )

            m.match_result()
            pair_count[pair] = pair_count.get(pair, 0) + 1

            print("Match recorded")
            display()
            match_number += 1

        except invalidinput as e:
            print("Error:", e)

    display()


main()