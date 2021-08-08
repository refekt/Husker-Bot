from discord.ext import commands
from datetime import datetime
from utilities.constants import TZ, CFBD_KEY
from cfbd import BettingApi, ApiClient, Configuration
from cfbd.rest import ApiException
from objects.Schedule import HuskerSchedule
import calendar
from discord_slash import cog_ext, SlashContext
from utilities.constants import DT_TBA_HR, DT_TBA_MIN, DT_OBJ_FORMAT_TBA, DT_OBJ_FORMAT
from utilities.server_detection import which_guild


class FootballStatsCommands(commands.Cog):
    @cog_ext.cog_slash(
        name="countdown",
        description="Countdown to the most current or specific Husker game",
        guild_ids=[which_guild()]
    )
    async def _countdown(self, ctx: SlashContext, team: str = None, sport: str = "football"):
        await ctx.defer()

        def convert_seconds(n):
            secs = n % (24 * 3600)
            hour = secs // 3600
            secs %= 3600
            mins = secs // 60

            return hour, mins

        def get_consensus_line(check_game):
            configuration = Configuration()
            configuration.api_key["Authorization"] = CFBD_KEY
            configuration.api_key_prefix["Authorization"] = "Bearer"

            cfb_api = BettingApi(ApiClient(configuration))

            nebraska_team = "Nebraska"
            year = datetime.now().year

            if check_game.location == "Lincoln, NE":
                home_team = "Nebraska"
                away_team = check_game.opponent
            else:
                home_team = check_game.opponent
                away_team = "Nebraska"

            try:
                api_response = cfb_api.get_lines(team=nebraska_team, year=year, away=away_team, home=home_team)
            except ApiException:
                return None

            try:
                consensus_line = api_response[0].lines[0]["formattedSpread"]
            except IndexError:
                consensus_line = None

            return consensus_line

        async def send_countdown(days: int, hours: int, minutes: int, opponent, _datetime: datetime, consensus, location):
            if _datetime.hour == DT_TBA_HR and _datetime.minute == DT_TBA_MIN:
                await ctx.send(content=f"📢 📅:There are [ {days} days ] until the [ {opponent} {f'({consensus})' if consensus else '(Line TBD)'} ] game at [ {_datetime.strftime(DT_OBJ_FORMAT_TBA)} ] played at [ {location} ].")
            else:
                await ctx.send(content=f"📢 📅:There are [ {days} days, {hours} hours, {minutes} minutes ] until the [ {opponent} {f'({consensus})' if consensus else '(Line TBD)'} ] game at [ {_datetime.strftime(DT_OBJ_FORMAT)} ] played at [ {location} ].")

        now_cst = datetime.now().astimezone(tz=TZ)

        games, stats = HuskerSchedule(sport=sport, year=now_cst.year)

        if not games:
            return await ctx.send(content="No games found!")

        for game in games:
            if game.game_date_time > now_cst:  # If the game's date time is in the future
                dt_game_time_diff = game.game_date_time - now_cst
                diff_hours_minutes = convert_seconds(dt_game_time_diff.seconds)  # datetime object does not have hours or minutes

                if dt_game_time_diff.days < 0:
                    if calendar.isleap(now_cst.year):
                        year_days = 366
                    else:
                        year_days = 365

                    return await send_countdown(
                        days=dt_game_time_diff.days + year_days,
                        hours=diff_hours_minutes[0],
                        minutes=diff_hours_minutes[1],
                        opponent=game.opponent,
                        _datetime=game.game_date_time,
                        consensus=get_consensus_line(game),
                        location=game.location
                    )

                return await send_countdown(
                    days=dt_game_time_diff.days,
                    hours=diff_hours_minutes[0],
                    minutes=diff_hours_minutes[1],
                    opponent=game.opponent,
                    _datetime=game.game_date_time,
                    consensus=get_consensus_line(game),
                    location=game.location
                )

        # else:
        #     for game in games:
        #         if team.lower() == game.opponent.name.lower():
        #             diff = game.game_date_time - now_cst
        #             diff_cd = convert_seconds(diff.seconds)
        #             if diff.days < 0:
        #                 if calendar.isleap(now_cst.year):
        #                     year_days = 366
        #                 else:
        #                     year_days = 365
        #                 await send_countdown(diff.days + year_days, diff_cd[0], diff_cd[1], game.opponent, game.game_date_time, get_consensus_line(game), game.location)
        #             await send_countdown(diff.days, diff_cd[0], diff_cd[1], game.opponent, game.game_date_time, get_consensus_line(game), game.location)
        #             break


def setup(bot):
    bot.add_cog(FootballStatsCommands(bot))
