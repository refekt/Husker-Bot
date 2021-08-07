import os
import platform

import pytz
from discord.ext.commands import BucketType, CommandError, UserInputError
from dotenv import load_dotenv

from encryption import load_key, decrypt_return_data

print(f"### Platform == {platform.platform()} ###")

win_vars = "./variables.json"

variables = ""

if "Windows" in platform.platform():
    print("### ~~~ Windows environment set ###")
    variables = os.getcwd() + "\\variables.json"
    load_dotenv(dotenv_path=variables)
elif "Linux" in platform.platform():
    print("### ~~~ Linux environment set ###")
    variables = "/home/botfrost/bot/variables.json"
    load_dotenv(dotenv_path=variables)
else:
    print(f"### ~~~ Unknown Platform: {platform.platform()} ###")

# Decrypt Env file
env_file = variables
key = load_key()

# Save decrypted file
# decrypt(env_file, key)
# encrypt(env_file, key)

env_vars = decrypt_return_data(env_file, key)

# Cooldown rates for commands
CD_GLOBAL_RATE = env_vars["global_rate"]
CD_GLOBAL_PER = env_vars["global_per"]
CD_GLOBAL_TYPE = BucketType.user

# Discord Bot Tokens
TEST_TOKEN = env_vars["TEST_TOKEN"]
PROD_TOKEN = env_vars["DISCORD_TOKEN"]
BACKUP_TOKEN = env_vars["BACKUP_TOKEN"]

# SQL information
SQL_HOST = env_vars["sqlHost"]
SQL_USER = env_vars["sqlUser"]
SQL_PASSWD = env_vars["sqlPass"]
SQL_DB = env_vars["sqlDb"]

# Reddit Bot Info
REDDIT_CLIENT_ID = env_vars["reddit_client_id"]
REDDIT_SECRET = env_vars["reddit_secret"]
REDDIT_PW = env_vars["reddit_pw"]

# SSH Information
# SSH_HOST = env_vars["ssh_host"]
# SSH_USER = env_vars["ssh_user"]
# SSH_PW = env_vars["ssh_pw"]

# Twitter variables
# TWITTER_CONSUMER_KEY = env_vars["twitter_consumer_key"]
# TWITTER_CONSUMER_SECRET = env_vars["twitter_consumer_secret"]
# TWITTER_TOKEN_KEY = env_vars["twitter_token_key"]
# TWITTER_TOKEN_SECRET = env_vars["twitter_token_secret"]
# TWITTER_WEBHOOK_ENV = "dev"

del env_vars, env_file, key

# Headers for `requests`
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}

# Embed titles
EMBED_TITLE_HYPE = "Nebraska Football Hype Squad 📈 ⚠ ⛔"

# Consistent timezone
TZ = pytz.timezone("US/Central")

# Discord Roles
ROLE_ADMIN_PROD = 440639061191950336
ROLE_ADMIN_TEST = 606301197426753536
ROLE_MOD_PROD = 443805741111836693
ROLE_POTATO = 583842320575889423
ROLE_ASPARAGUS = 583842403341828115
ROLE_LILRED = 464903715854483487
ROLE_RUNZA = 485086088017215500
ROLE_MEME = 448690298760200195
ROLE_ISMS = 592425861534449674
ROLE_PACKER = 609409451836964878
ROLE_PIXEL = 633698252809699369
ROLE_AIRPOD = 633702209703378978
ROLE_GUMBY = 459569717430976513
ROLE_MINECRAFT = 661409899481268238
ROLE_HYPE_MAX = 682380058261979176
ROLE_HYPE_SOME = 682380101077434480
ROLE_HYPE_NO = 682380119666720789
ROLE_TIME_OUT = 663881203983843338
ROLE_QDOBA = 797587264112820264
ROLE_ALDIS = 802639913824550952

# Discord Channels
CHAN_HOF_PROD = 487431877792104470
CHAN_HOF_TEST = 606655884340232192
CHAN_SHAME = 860686057850798090
CHAN_DBL_WAR_ROOM = 538419127535271946
CHAN_WAR_ROOM = 525519594417291284
CHAN_BOTLOGS = 458474143403212801
CHAN_SCOTT = 507520543096832001
CHAN_RULES = 651523695214329887
CHAN_NORTH_BOTTTOMS = 620043869504929832
CHAN_RADIO_PROD = 660610967733796902
CHAN_RADIO_TEST = 595705205069185050
CHAN_SCOTTS_BOTS = 593984711706279937
CHAN_POLITICS = 504777800100741120
CHAN_MINECRAFT_ADMIN = 662110504843739148
CHAN_TWITTERVERSE = 636220560010903584
CHAN_TEST_SPAM = 595705205069185047
CHAN_GENERAL = 440868279150444544
CHAN_BETS = 622581511488667699
CHAN_POSSUMS = 442047437561921548
CHAN_IOWA = 749339421077274664

CHAN_BANNED = (CHAN_BOTLOGS, CHAN_RULES, CHAN_POLITICS, CHAN_MINECRAFT_ADMIN, CHAN_TWITTERVERSE, CHAN_HOF_PROD, CHAN_RULES)
CHAN_STATS_BANNED = (CHAN_DBL_WAR_ROOM, CHAN_WAR_ROOM, CHAN_BOTLOGS, CHAN_HOF_PROD, CHAN_SHAME)

# Reactions
REACTION_HYPE_MAX = "📈"
REACTION_HYPE_SOME = "⚠"
REACTION_HYPE_NO = "⛔"

REACITON_HYPE_SQUAD = (REACTION_HYPE_MAX, REACTION_HYPE_SOME, REACTION_HYPE_NO)

# Servers/guilds
GUILD_PROD = 440632686185414677
GUILD_TEST = 595705205069185045

# Member ID
TEST_BOT_MEMBER = 595705663997476887
PROD_BOT_MEMBER = 593949013443608596
TWITTER_BOT_MEMBER = 755193317997674607

# Currency
CURRENCY_NAME = "Husker Coins"

# Bot Info
BOT_DISPLAY_NAME = "Bot Frost"
BOT_GITHUB_URL = "https://github.com/refekt/Husker-Bot"
BOT_ICON_URL = "https://i.imgur.com/Ah3x5NA.png"
BOT_THUMBNAIL_URL = "https://ucomm.unl.edu/images/brand-book/Our-marks/nebraska-n.jpg"
BOT_FOOTER_SECRET = "These messages are anonymous and there is no way to verify messages are accurate."
BOT_FOOTER_BOT = "Created by Bot Frost"

#
CROOT_SEARCH_LIMIT = 5


# Global Errors
def command_error(message: str):
    return CommandError(message=message)


def user_error(message: str):
    return UserInputError(message=message)


