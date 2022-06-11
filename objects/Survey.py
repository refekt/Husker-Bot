import hashlib
import logging
import math
import random
import string
from typing import Optional, AnyStr, Union, List, Any

import discord
from discord import (
    ButtonStyle,
    Client,
    Embed,
    Forbidden,
    HTTPException,
    Interaction,
)
from discord.ext.commands import Bot
from discord.ui import View, Button

from helpers.constants import GLOBAL_TIMEOUT
from helpers.misc import formatPrettyTimeDelta
from objects.Exceptions import SurveyException

logger = logging.getLogger(__name__)

__all__ = ["Survey"]


def generate_random_key() -> str:
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(10)
    )


class SurveyOption:
    def __init__(self, label: AnyStr):
        assert isinstance(label, str), SurveyException("Label must be a string!")

        self.custom_id: AnyStr = f"{generate_random_key()}_survey_option"
        self.label: AnyStr = label
        self.value: int = 0


class Survey:
    def __init__(
        self,
        client: Union[Client, Bot],
        interaction: Interaction,
        options: Union[AnyStr, List[Any], List[SurveyOption]],
        question: AnyStr,
        timeout: Optional[int] = GLOBAL_TIMEOUT,
    ) -> None:
        # Space deliminated options
        options = options.strip()
        if " " in options:
            options = options.split()
        else:
            options = [options]

        assert len(options) == len(set(options)), SurveyException(
            f"You cannot use the same option more than once!"
        )

        for index, opt in enumerate(options):
            options[index] = SurveyOption(opt)  # noqa

        max_options = 3

        assert isinstance(question, str), SurveyException("Question must be a string!")
        assert [isinstance(opt, SurveyOption) for opt in options], SurveyException(
            "Options must be a SurveyOption object!"
        )
        assert 2 <= len(options) <= max_options, SurveyException(
            f"You must have between 2 and {max_options} options!"
        )
        assert timeout is not None, SurveyException("You must provide a timeout value!")

        self.client: Union[Client, client] = client
        self.interaction: Interaction = interaction
        self.embed: Optional[Embed] = None
        self.options: List[SurveyOption] = options
        self.question: Optional[AnyStr] = question
        self.timeout: int = math.ceil(timeout)

    class SurviewButtons(View):
        def __init__(self, options: List[SurveyOption], timeout: int = None) -> None:
            super().__init__(timeout=timeout)
            self.options: List[SurveyOption] = options
            self.tally_str: str = "Tally for: "
            self.footer_str: str = "Users: "

        async def process_button(self, interaction: Interaction, button: Button):
            logger.info(
                f"{interaction.user.display_name} selected option '{button.label.upper()}'"
            )

            await interaction.response.send_message(
                "Processing original_message!", ephemeral=True
            )

            embed: discord.Embed = interaction.message.embeds[0]
            if interaction.user.display_name in embed.footer.text:
                await interaction.edit_original_message(
                    content="You cannot vote more than once!"
                )
                return
            embed.set_footer(
                text=f"{embed.footer.text} {interaction.user.display_name} "
            )

            for index, field in enumerate(embed.fields):
                if field.name == f"{self.tally_str}{button.label.upper()}":
                    field.value = str(int(field.value) + 1)
                    embed.set_field_at(
                        index=index,
                        name=field.name,
                        value=field.value,
                        inline=field.inline,
                    )
                    break

            # try:
            #     await interaction.followup.send_message(content="Response recorded!")
            # except (HTTPException, NotFound, Forbidden, TypeError, ValueError) as e:
            #     logger.info(e)
            #     return

            try:
                await interaction.message.edit(embed=embed)
            except (HTTPException, Forbidden, TypeError) as e:
                logger.info(e)
                return

        @discord.ui.button(label="one", custom_id="opt_one", style=ButtonStyle.gray)
        async def option_one(self, interaction: discord.Interaction, button: Button):
            await self.process_button(interaction=interaction, button=button)

        @discord.ui.button(label="two", custom_id="opt_two", style=ButtonStyle.gray)
        async def option_two(self, interaction: discord.Interaction, button: Button):
            await self.process_button(interaction=interaction, button=button)

        @discord.ui.button(label="three", custom_id="opt_four", style=ButtonStyle.gray)
        async def option_three(self, interaction: discord.Interaction, button: Button):
            await self.process_button(interaction=interaction, button=button)

        async def on_timeout(self) -> None:
            self.stop()

    def create_embed(self) -> None:
        embed = Embed(
            title="Survey",
            description=f"Please provide your feedback. This survey timesout in {formatPrettyTimeDelta(self.timeout)} seconds.",
            color=0xD00000,
        )
        embed.set_footer(text="Users: ")
        embed.add_field(
            name="Survey Question",
            value=self.question,
        )
        for index, opt in enumerate(self.options):
            embed.add_field(
                name=f"Tally for: {opt.label.upper()}",
                value=str(opt.value),
                inline=True,
            )

        self.embed = embed

    def update_embed(self, user_id: str, opt: str) -> None:
        hashed_user = hashlib.sha1(str(user_id).encode("UTF-8")).hexdigest()[:10]
        if hashed_user in self.embed.footer.text:
            return

        for option in self.options:
            if option.label == opt:
                option.value += 1
                break

        footer_text = self.embed.footer.text
        self.create_embed()
        self.embed.set_footer(text=f"{footer_text} {hashed_user} ")

    async def send(self) -> None:
        await self.interaction.response.defer()

        self.create_embed()

        view = self.SurviewButtons(self.options)
        for index, child in enumerate(view.children):
            if index > len(self.options):
                del child
                break
            child.label = self.options[index].label

        await self.interaction.followup.send(embed=self.embed, view=view)

    async def close_survey(self) -> None:
        await self.interaction.edit_original_message(view=None)