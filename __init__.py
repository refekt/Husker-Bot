import discord  # noqa # Beta version thing
from discord.app_commands import CommandInvokeError

from objects.Client import HuskerClient
from objects.Logger import discordLogger

logger = discordLogger(__name__)

logger.info("Loading helpers")
from helpers.constants import *  # noqa
from helpers.embed import *  # noqa
from helpers.encryption import *  # noqa
from helpers.fryer import *  # noqa
from helpers.game_stats_bets import *  # noqa
from helpers.misc import *  # noqa
from helpers.mysql import *  # noqa
from helpers.slowking import *  # noqa

logger.info("Loading objects")
from objects.Bets_Stats_Schedule import *  # noqa
from objects.Exceptions import *  # noqa
from objects.Paginator import *  # noqa
from objects.Recruits import *  # noqa
from objects.Survey import *  # noqa
from objects.Thread import *  # noqa
from objects.TweepyStreamListener import *  # noqa
from objects.Weather import *  # noqa
from objects.Winsipedia import *  # noqa

__all__ = ["client"]

logger.info("Objects loaded. Starting the bot!")

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

client = HuskerClient(
    command_prefix="$",
    fetch_offline_members=True,
    intents=intents,
    owner_id=MEMBER_GEE,
)

tree = client.tree


@tree.error
async def on_app_command_error(
    interaction: discord.Interaction, error: CommandInvokeError
) -> None:
    err = DiscordError(error, interaction.data.get("options", None))
    logger.exception(error, exc_info=True)
    embed = buildEmbed(
        title="",
        fields=[
            dict(
                name=f"Error Type: {err.error_type}",
                value=f"{err.message}",
            ),
            dict(
                name="Command",
                value=f"{'/' + err.command if not err.parent else '/' + err.parent + ' ' + err.command}",
            ),
            dict(
                name="Command Input",
                value=f"{', '.join(err.options) if err.options else 'None'}",
            ),
            dict(name="Originating Module", value=f"{err.modeule}"),
        ],
    )
    if interaction.response.is_done():
        await interaction.followup.send(content="", embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(content="", embed=embed, ephemeral=True)


if __name__ == "__main__":
    client.run(PROD_TOKEN, log_handler=None)
