import platform
from utils.consts import TZ
import datetime
import pytz
import re
import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

from utils.consts import HEADERS


class GameBets:
    game_number = None
    over_under = None
    spread = None
    win = None

    def __init__(self, game_number, over_under, spread, win):
        self.game_number = game_number
        self.over_under = over_under
        self.spread = spread
        self.win = win


class GameBetLine:
    provider = None
    spread = None
    formatted_spread = None
    over_under = None

    def __init__(self, provider=None, spread=None, formatted_spread=None, over_under=None):
        self.provider = provider
        self.spread = spread
        self.formatted_spread = formatted_spread
        self.over_under = over_under


class GameBetInfo:
    home_team = None
    home_score = None
    away_team = None
    away_score = None
    userbets = []
    lines = []

    def __init__(self, year, week, team, season="regular"):  # , home_team=None, home_score=None, away_team=None, away_score=None, lines=None):
        self.home_team = None
        self.home_score = None
        self.away_team = None
        self.away_score = None
        self.userbets = []
        self.lines = []

        self.establish(year, week, team, season)

    def establish(self, year, week, team, season="regular"):
        url = f"https://api.collegefootballdata.com/lines?year={year}&week={week}&seasonType={season}&team={team}"
        re = requests.get(url=url, headers=HEADERS)
        data = re.json()

        try:
            self.home_team = data[0]['homeTeam']
            self.home_score = data[0]['homeScore']
            self.away_team = data[0]['awayTeam']
            self.away_score = data[0]['awayScore']
            linedata = data[0]["lines"]

            for line in linedata:
                self.lines.append(
                    GameBetLine(
                        provider=line['provider'],
                        spread=line['spread'],
                        formatted_spread=line['formattedSpread'],
                        over_under=line['overUnder']
                    )
                )
        except:
            pass


class SeasonStats:
    wins = None
    losses = None

    def __init__(self, wins=0, losses=0):
        self.wins = wins
        self.losses = losses


class HuskerOpponent:
    name = None
    ranking = None
    icon = None
    date_time = None
    conference = None

    def __init__(self, name, ranking, icon, date_time, conference):
        self.name = name
        self.ranking = ranking
        self.icon = icon
        self.date_time = date_time
        self.conference = conference


class HuskerDotComSchedule:
    bets = GameBetInfo
    location = None
    opponent = None
    outcome = None
    ranking = None
    week = None
    game_date_time = None
    game_date_time_dt = None

    def __init__(self, bets, location, opponent, outcome, ranking, week, game_date_time, game_date_time_dt=None):
        self.bets = bets
        self.location = location
        self.opponent = opponent
        self.outcome = outcome
        self.ranking = ranking
        self.week = week
        self.game_date_time = game_date_time
        self.game_date_time_dt = game_date_time_dt


def HuskerSchedule(sport: str, year=datetime.datetime.now().year):
    r = requests.get(url=f"https://huskers.com/sports/{sport}/schedule/{year}", headers=HEADERS)

    if not r.status_code == 200:
        raise ConnectionError("Unable to retrieve schedule from Huskers.com.")

    def collect_opponent(g):
        try:
            name = g.contents[1].contents[3].contents[3].contents[3].text.strip().replace("\n", " ")
            icon = "https://huskers.com" + g.contents[1].contents[1].contents[1].attrs["data-src"]
            _date = g.contents[1].contents[3].contents[1].contents[1].contents[1].text.strip()
            _time = g.contents[1].contents[3].contents[1].contents[1].contents[3].text.strip()

            if "(" in _time:
                _time = "TBA"

            if ":" not in _time:
                _time = _time.replace(" ", ":00 ")
            date_time = f"{_date[0:6]} {year} {_time}"
            if "Noon" in date_time:  # I blame Iowa
                date_time = date_time.replace("Noon", "12:00 P.M.")
            conference = g.contents[1].contents[3].contents[1].contents[3]
            if len(conference.contents) > 1:
                conference = conference.contents[1].text.strip()
            else:
                conference = "Non-Con"

            return HuskerOpponent(
                name=name,
                ranking=None,
                icon=icon,
                date_time=date_time,
                conference=conference,
            )
        except IndexError:
            return "Unknown Opponent"

    soup = BeautifulSoup(r.content, "html.parser")

    games_raw = soup.find_all(attrs={"class": "sidearm-schedule-games-container"})
    games_raw = [game for game in games_raw[0].contents if type(game) == Tag]  # Remove all NavigableStrings from the list

    for index, game in enumerate(games_raw):
        if len(game.attrs) == 0:
            games_raw[index] = game.contents[1].contents[3].contents[1]

    games = []
    season_stats = SeasonStats()
    exempt_games = ("Spring Game", "Fan Day")
    special_games = ("Homecoming", "Bowl")
    week = 0

    for game in games_raw:
        week += 1

        if any(g in game.text for g in exempt_games):
            week -= 1
            continue

        if any(g in game.text for g in special_games):
            g = game.contents[1].contents[3].contents[1].contents[1]
        else:
            g = game.contents[1]

        loc = g.contents[3].contents[1].text.strip()
        opp = collect_opponent(g)

        if "Canceled" in g.contents[5].contents[1].text:
            out = "Canceled"
        else:
            try:
                out = f"{g.contents[5].contents[1].contents[3].text.strip()} {g.contents[5].contents[1].contents[5].text}"

                if g.contents[5].contents[1].contents[1].text.strip():
                    out = g.contents[5].contents[1].contents[1].text.strip() + " " + out
            except IndexError:
                out = ""

        if "TBA" in opp.date_time:
            gdt_string = f"{opp.date_time[0:6]} {year} 10:58 PM"
            game_date_time = datetime.datetime.strptime(gdt_string, "%b %d %Y %I:%M %p").astimezone(tz=TZ)
        else:
            game_date_time = datetime.datetime.strptime(opp.date_time.replace("A.M.", "AM").replace("P.M.", "PM"), "%b %d %Y %I:%M %p").astimezone(tz=TZ)
            game_date_time += datetime.timedelta(hours=1)

        if "Linux" in platform.platform():
            offset = 6
            game_date_time += datetime.timedelta(hours=offset)

        games.append(
            HuskerDotComSchedule(
                bets=None,
                location=loc,
                opponent=opp,
                outcome=out,
                ranking=None,
                week=week,
                game_date_time=game_date_time
            )
        )

    for game in games:
        if "W" in game.outcome:
            season_stats.wins += 1
        elif "L" in game.outcome:
            season_stats.losses += 1
        else:
            pass

    return games, season_stats


def Venue():
    r = requests.get("https://api.collegefootballdata.com/venues")
    return r.json()
