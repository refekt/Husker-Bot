#!/usr/bin/env python3.7
import discord
from discord.ext import commands
from discord.utils import get
import requests
from bs4 import BeautifulSoup
import sys
import random
import json
import datetime
import pandas
import config
import function_helper
import cb_settings
import crystal_balls

botPrefix = '$'
client = commands.Bot(command_prefix=botPrefix)

# initialize a global list for crootbot to put search results in
player_search_list = []
emoji_list = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
welcome_emoji_list = ['🔴', '🍞', '🥔', '🥒', '😂']
huskerbot_footer = "Generated by HuskerBot"
welcome_footer = 'HusekrBot welcomes you!'
profile_url = None
highlight_url = None
wrong_channel_text = 'The command you sent is not authorized for use in this channel.'
authorized_to_quit = [440639061191950336, 443805741111836693]

with open('team_ids.json', 'r') as fp:
    team_ids = json.load(fp)

# Reference - https://www.cougcenter.com/2013/6/28/4445944/common-ncaa-football-penalties-referee-signals
ref_dict = {'bs': ['Bull shit', 'Referee still gets paid for that horrible call','https://i.imgur.com/0nQGIZs.gif'],
            'chip': ['Blocking below the waist', 'OFF: 15 yards\nDEF: 15 yards and an automatic first down', 'https://i.imgur.com/46aDB8t.gif'],
            'chop': ['Blocking below the waist', 'OFF: 15 yards\nDEF: 15 yards and an automatic first down', 'https://i.imgur.com/cuiRu7T.gif'],
            'encroachment': ['Encroachment', 'DEF: 5 yards', 'https://i.imgur.com/4ekGPs4.gif'],
            'facemask': ['Face mask', 'OFF: Personal foul, 15 yards\nDEF: Personal foul, 15 yards from the end spot of the play, automatic first down', 'https://i.imgur.com/xzsJ8MB.gif'],
            'falsestart': ['False start', 'OFF: 5 yards', 'https://i.imgur.com/i9ZyMpn.gif'],
            'hand2face': ['Hands to the face', 'OFF: Personal foul, 15 yards\nDEF: Personal foul, 15 yards, automatic first down', 'https://i.imgur.com/DNw5Qsq.gif'],
            'hold': ['Holding', 'OFF: 10 yards from the line of scrimmage and replay the down.\nDEF: 10 yards', 'https://i.imgur.com/iPUNHJi.gif'],
            'illfwd': ['Illegal forward pass', 'OFF: 5 yards from the spot of the foul and a loss of down', 'https://i.imgur.com/4CuuTDH.gif'],
            'illshift': ['Illegal shift', 'OFF: 5 yards', 'https://i.imgur.com/RDhSuUw.gif'],
            'inelrec': ['Inelligible receiver downfield', 'OFF: 5 yards', 'https://i.imgur.com/hIfsc5D.gif'],
            'persfoul': ['Personal foul', 'OFF: 15 yards\nDEF: 15 yards from the end spot of the play, automatic first down', 'https://i.imgur.com/dyWMN7p.gif'],
            'pi': ['Pass interference', 'OFF: 15 yards\nDEF: Lesser of either 15 yards or the spot of the foul, and an automatic first down (ball placed at the 2 yard line if penalty occurs in the endzone)', 'https://i.imgur.com/w1Tglj4.gif'],
            'ruffkick': ['Roughing/Running into the kicker', 'DEF: (running) 5 yards, (roughing, personal foul) 15 yards and automatic first down ', 'https://i.imgur.com/UuTBUJv.gif'],
            'ruffpass': ['Roughing the passer', 'DEF: 15 yards and an automatic first down (from the end of the play if pass is completed)', 'https://i.imgur.com/XqPE1Pf.gif'],
            'safety': ['Safety', 'DEF: 2 points and possession, opponent free kicks from their own 20 yard line', 'https://i.imgur.com/Y8pKXaH.gif'],
            'targeting': ['Targeting', 'OFF/DEF: 15 yard penalty, ejection ', 'https://i.imgur.com/qOsjBCB.gif'],
            'td': ['Touchdown', 'OFF: 6 points', 'https://i.imgur.com/UJ0AC5k.mp4'],
            'unsport': ['Unsportsmanlike', 'OFF: 15 yards\nDEF: 15 yards', 'https://i.imgur.com/6Cy9UE4.gif'],
            }

long_positions = {'PRO' : 'Pro-Style Quarterback',
                  'DUAL': 'Dual-Threat Quarterback',
                  'APB' : 'All-Purpose Back',
                  'RB' : 'Running Back',
                  'FB' : 'Fullback',
                  'WR' : 'Wide Receiver',
                  'TE' : 'Tight End',
                  'OT' : 'Offensive Tackle',
                  'OG' : 'Offensive Guard',
                  'OC' : 'Center',
                  'SDE' : 'Strong-Side Defensive End',
                  'WDE' : 'Weak-Side Defensive End',
                  'DT' : 'Defensive Tackle',
                  'ILB' : 'Inside Linebacker',
                  'OLB' : 'Outside Linebacker',
                  'CB' : 'Cornerback',
                  'S' : 'Safety',
                  'ATH' : 'Athlete',
                  'K' : 'Kicker',
                  'P' : 'Punter',
                  'LS' : 'Long Snapper',
                  'RET' : 'Returner'
                  }

flag_dict = {'iowa': 'https://i.imgur.com/xoeCOwp.png',
             'northwestern': 'https://i.imgur.com/WG4kFP6.jpg',
             'ohio_state': 'https://i.imgur.com/coxjUAZ.jpg',
             'minnesota': 'https://i.imgur.com/54mF0sK.jpg',
             'michigan': 'https://i.imgur.com/XWEDsFf.jpg',
             'miami': 'https://i.imgur.com/MInQMLb.jpg',
             'iowa_state': 'https://i.imgur.com/w9vg0QX.jpg',
             'indiana': 'https://i.imgur.com/uc0Q8Z0.jpg',
             'colorado': 'https://i.imgur.com/If6MPtT.jpg',
             'wisconsin': 'https://giant.gfycat.com/PolishedFeminineBeardedcollie.gif',
             'texas': 'https://i.imgur.com/rB2Rduq.jpg',
             'purdue': 'https://i.imgur.com/8SYhZKc.jpg',
             'illinois': 'https://i.imgur.com/MxMaS3e.jpg',
             'maryland': 'https://i.imgur.com/G6RX8Oz.jpg',
             'michigan_state': 'https://i.imgur.com/90a9g3v.jpg',
             'penn_state': 'https://i.imgur.com/JkQuMXf.jpg',
             'rutgers': 'https://i.imgur.com/lyng39h.jpg',
             'south_alabama': 'https://i.imgur.com/BOH5reA.jpg',
             'northern_illinois': 'https://i.imgur.com/HpmAoIh.jpg'
             }

eight_ball = ['Try again',
              'Definitely yes',
              'It is certain',
              'It is decidedly so',
              'Without a doubt',
              'Yes – definitely',
              'You may rely on it',
              'As I see it, yes',
              'Most Likely',
              'These are the affirmative answers.',
              'Don’t count on it',
              'My reply is no',
              'My sources say no',
              'Outlook not so good, and very doubtful',
              'Reply hazy',
              'Try again',
              'Ask again later',
              'Better not tell you now',
              'Cannot predict now',
              'Concentrate and ask again',
              'Fuck Iowa',
              'Scott Frost approves',
              'Coach V\'s cigar would like this'
               ]


@client.event
async def on_ready():
    game = discord.Game('Husker Football 24/7')
    await client.change_presence(status=discord.Status.online, activity=game)
    print("***\nLogged in as [{0}].\nDiscord.py version is: [{1}].\nDiscord version is [{2}].\n***".format(client.user, discord.__version__, sys.version))


@client.event
async def on_message(message):
    """ Commands processed as messages are entered """
    if not message.author.bot:
        # Good bot, bad bot
        if "good bot" in message.content.lower():
            await message.channel.send("OwO thanks")
        elif "bad bot" in message.content.lower():
            embed = discord.Embed(title="I'm a bad, bad bot")
            embed.set_image(url='https://i.imgur.com/qDuOctd.gif')
            await message.channel.send(embed=embed)
        # Husker Bot hates Isms
        if "isms" in message.content.lower():
            dice_roll = random.randint(1,101)
            if dice_roll >= 90:
                await message.channel.send("Isms? That no talent having, no connection having hack? All he did was lie and "
                                           "make **shit** up for fake internet points. I'm glad he's gone.")
        # Add Up Votes and Down Votes
        if (".addvotes") in message.content.lower():
            # Upvote = u"\u2B06" or "\N{UPWARDS BLACK ARROW}"
            # Downvote = u"\u2B07" or "\N{DOWNWARDS BLACK ARROW}"
            emojiUpvote = "\N{UPWARDS BLACK ARROW}"
            emojiDownvote = "\N{DOWNWARDS BLACK ARROW}"
            await message.add_reaction(emojiUpvote)
            await message.add_reaction(emojiDownvote)
    elif message.author.bot:
        if "$crootbot" in message.content or "$cb" in message.content or "$recentballs" in message.content or "$cb_search" in message.content:
            if crystal_balls.updating_cb_list:
                await message.send("HuskerBot is in the process of updating the crystal ball database. Try again in 30 seconds.")

    # HUDL highlight puller on react. This section is to take the crootbot message, find if a hudl profile exists, and pull the video. 
    # Next would be to monitor reactions and post the video if someone reacted to the video camera emoji.
    # TODO If there are multiple football players with the same name we may get the wrong guy. Especially for croots from previous classes. We will want to add more logic to narrow 
    # TODO it down even more
    if len(message.embeds) > 0:
        # Welcome message dection
        if message.author == client.user and message.embeds[0].footer.text == welcome_footer:
            i = 0
            while i < len(welcome_emoji_list):
                await message.add_reaction(welcome_emoji_list[i])
                i += 1
        # CrootBot Search Results detection
        if message.author == client.user and player_search_list and message.embeds[0].footer.text == 'Search Results ' + huskerbot_footer:
            # Pre-add reactions for users
            i = 0
            while i < min(10, len(player_search_list)):
                await message.add_reaction(emoji_list[i])
                i += 1
        # CrootBot dection
        if message.author == client.user and message.embeds[0].footer.text == huskerbot_footer:
            print("***\nChecking for highlight video")
            global profile_url
            url = profile_url + 'videos'           
            headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
            page = requests.get(url = url, headers = headers)
            soup = BeautifulSoup(page.text, 'html.parser')
            videos = soup.find_all(class_ = 'title_lnk')
            if len(videos) > 0:
                print("Highlight video found")
                global highlight_url
                highlight_url = videos[0].get('href')
                for v in videos:
                    if 'senior' in v.get('title').lower():                       
                        highlight_url = v.get('href')
                        break
                    elif 'junior' in v.get('title').lower():
                        highlight_url = v.get('href')
                        break
                    elif 'sophomore' in v.get('title').lower():
                        highlight_url = v.get('href')
                print("{}\n***".format(highlight_url))
                embed_old = message.embeds[0]
                embed_new = embed_old.set_footer(text='Click the video camera emoji to get a highlight video for this recruit')
                await message.edit(embed=embed_new)
                await message.add_reaction('📹')
            else:
                print("No highlight video found\n***")
            profile_url = None
    # Always need this
    await client.process_commands(message)


@client.event
async def on_member_join(member):
    embed = discord.Embed(title="HuskerBot's Welcome Message", color=0xff0000)
    embed.add_field(name="Welcome __`{}`__ to the Huskers Discord!".format(member.name), value="The Admin team and Frost Approved members hope you have a good time while here. I am your full-serviced Discord bot, HuskerBot! You can find a list of my commands by sending `$help`.\n\n"
                   "We also have some fun roles that may interest you and you're welcome to join! The first, we have the 🔴 `@Lil' Huskers Squad`--those who are fans of Lil Red. Next up we have the 🍞 `@/r/unza` team. They are our resident Runza experts. Right behind the sandwich lovers are the 😂 `@Meme Team`! Their meme creation is second to none. Finally, we have our two food gangs: 🥔 `@POTATO GANG` and 🥒 `@Asparagang`. Which is better?\n\n"
                   "React to this message with the emojis below to automatically join the roles!", inline=False)
    embed.set_footer(text=welcome_footer)

    # welcome_channel = client.get_channel(487431877792104470)
    # await welcome_channel.send(embed=embed)
    await member.send(embed=embed)


@client.event
async def on_reaction_add(reaction, user):
    # Debugging
    # print("***\nReaction: {}\mUser: {}\m***".format(reaction, user))

    if user != client.user and reaction.message.author == client.user and player_search_list and reaction.message.embeds[0].footer.text == 'Search Results ' + huskerbot_footer:
        channel = reaction.message.channel
        emoji_dict = {'1⃣' : 0,
                      '2⃣' : 1,
                      '3⃣' : 2,
                      '4⃣' : 3,
                      '5⃣' : 4,
                      '6⃣' : 5,
                      '7⃣' : 6, 
                      '8⃣' : 7, 
                      '9⃣' : 8, 
                      '🔟' : 9
                      }
        if reaction.emoji in emoji_dict:
            await parse_search(search=player_search_list[emoji_dict[reaction.emoji]], channel=channel)
    
    # If a 247 highlight is found for a crootbot response and someone reacts to the video camera, call the function to parse through the recruits hudl page and grab a highlight video
    if len(reaction.message.embeds) > 0:
        global highlight_url
        if user != client.user and reaction.message.author == client.user and reaction.message.embeds[0].footer.text == 'Click the video camera emoji to get a highlight video for this recruit' and highlight_url is not None:
            print("***\nHighlight videos\n***")
            if reaction.emoji == '📹':                
                channel = reaction.message.channel
                headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
                url = highlight_url
                page = requests.get(url = url, headers = headers)
                soup = BeautifulSoup(page.text, 'html.parser')
                try:
                    video_url = soup.find(class_='video-wrapper').find('iframe').get('src')
                except:
                    video_url = soup.find(class_='video-container').find('iframe').get('src')
                if 'https:' not in video_url:
                    video_url = 'https:' + video_url               
                await channel.send(video_url)
                highlight_url = None
        if user != client.user and reaction.message.author == client.user and reaction.message.embeds[0].footer.text == huskerbot_footer:
            print("***\nNew member joins\n***")
            if reaction.emoji == '🍞':
                role = get(user.server.roles, name='/r/unza')
                await user.add_roles(role)
            elif reaction.emoji == '😂':
                role = get(user.server.roles, name='Meme Team')
                await user.add_roles(role)
            elif reaction.emoji == '🥒':
                role = get(user.server.roles, name='/r/Asparagang')
                await user.add_roles(role)
            elif reaction.emoji == '🥔':
                role = get(user.server.roles, name='POTATO GANG')
                await user.add_roles(role)
            elif reaction.emoji == '🔴':
                role = get(user.server.roles, name='Lil\' Huskers Squad')
                await user.add_roles(role)


# Catch invalid commands/errors
@client.event
async def on_command_error(ctx, error):
    output_msg = "Whoa there {}! Something went wrong. {}. Please review `$help` for a list of all available commands.".format(ctx.message.author, error)
    await ctx.send(output_msg)


async def check_last_run(ctx=None):
    """ Check when the last time the JSON was pulled. """
    now = datetime.datetime.now()
    temp_check = cb_settings.last_run
    check = pandas.to_datetime(temp_check) + datetime.timedelta(minutes=crystal_balls.CB_REFRESH_INTERVAL)

    print("***\nNow: {}\nTemp Check: {}\nCheck: {}\nNow > Check: {}\n***".format(now, temp_check, check, now > check))

    if now > check:
        print("Last time the JSON was pulled exceeded threshold")

        if ctx: await ctx.send("The crystal ball database is stale. Updating now; standby...")

        crystal_balls.move_cb_to_list_and_json(json_dump=True)

        f = open('cb_settings.py', 'w')
        f.write('last_run = \'{}\''.format(datetime.datetime.now()))
        f.close()

        if ctx: await ctx.send("The crystal ball database is fresh and ready to go! {} entries were collected.".format(len(crystal_balls.cb_list)))
    else:
        # print("Last time JSON was pulled does not exceed threshold")
        await ctx.send("The crystal ball database is already fresh.")
        # print(cb_list)
        if len(crystal_balls.cb_list) <= 1:
            crystal_balls.load_cb_to_list()


@client.command()
async def crootbot(ctx, year, first_name, last_name):
    """ CrootBot provides the ability to search for and return information on football recruits. Usage is `$crootbot <year> <first_name> <last_name>`. The command is able to find partial first and last names. """
    # pulls a json file from the 247 advanced player search API and parses it to give info on the croot.
    # First, pull the message content, split the individual pieces, and make the api call

    # This keeps bot spam down to a minimal.
    await function_helper.check_command_channel(ctx.command, ctx.channel)
    if not function_helper.correct_channel:
        await ctx.send(wrong_channel_text)
        return

    search_first_name = first_name
    search_last_name = last_name

    url = 'https://247sports.com/Season/{}-Football/Recruits.json?&Items=15&Page=1&Player.FirstName={}&Player.LastName={}'.format(year, first_name, last_name)
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    search = requests.get(url=url, headers=headers)
    search = json.loads(search.text)

    if not search:
        await ctx.send("I could not find any player named {} {} in the {} class".format(first_name, last_name, year))
    elif len(search) > 1:
        global player_search_list
        # players_string = 'Mulitple results found for **[{}, {} {}]**. React with the corresponding emoji for CrootBot results.\n__**Search Results:**__\n'.format(year, first_name, last_name)
        players_string = ''
        players_list = []
        player_search_list = search
        for i in range(min(10, len(search))):
            player = search[i]['Player']
            first_name = player['FirstName']
            last_name = player['LastName']
            position = player['PrimaryPlayerPosition']['Abbreviation']
            if position in long_positions:
                position = long_positions[position]
            players_string += '{}: {} {} - {}\n'.format(emoji_list[i], first_name, last_name, position)
            players_list.append(['FirstName', 'LastName'])

        # Embed stuff
        result_text = 'Mulitple results found for __**[{}, {} {}]**__. React with the corresponding emoji for CrootBot results.\n\n'.format(year, search_first_name, search_last_name)
        embed_text = result_text + players_string
        embed = discord.Embed(title="Search Results",description=embed_text, color=0xff0000)
        embed.set_author(name="HuskerBot CrootBot")
        embed.set_footer(text='Search Results ' + huskerbot_footer)
        # await ctx.send(players_string)
        await ctx.send(embed=embed)
    else:
        channel = ctx.channel
        await parse_search(search[0], channel) #The json that is returned is a list of dictionaries, I pull the first item in the list (may consider adding complexity)


async def parse_search(search, channel):
        year = search['Year']
        player = search['Player']
        first_name = player['FirstName']
        last_name = player['LastName']
        position = player['PrimaryPlayerPosition']['Abbreviation']
        if position in long_positions:
            position = long_positions[position]
        hometown = player['Hometown']
        state = hometown['State']
        city = hometown['City']
        height = player['Height'].replace('-', "'") + '"'
        weight = player['Weight']
        high_school = player['PlayerHighSchool']['Name']
        image_url = player['DefaultAssetUrl']
        composite_rating = player['CompositeRating']
        if composite_rating is None:
            composite_rating = 'N/A'
        else:
            composite_rating = player['CompositeRating']/100
        composite_star_rating = player['CompositeStarRating']
        national_rank = player['NationalRank']
        if national_rank is None:
            national_rank = 'N/A'
        position_rank = player['PositionRank']
        if position_rank is None:
            position_rank = 'N/A'
        state_rank = player['StateRank']
        if state_rank is None:
            state_rank = 'N/A'
        player_url = player['Url']
        global profile_url
        profile_url = player_url
        stars = ''
        for i in range(int(composite_star_rating)):
            stars += '\N{WHITE MEDIUM STAR}'
            
        #Check if they are committed. It's a little different with signed players.
        commit_status = search['HighestRecruitInterestEventType']
        if commit_status == 'HardCommit' or commit_status == 'SoftCommit':
            commit_status = 'Committed'
        else:
            commit_status = 'Uncommitted'
        if type(search['SignedInstitution']) is int:
            commit_status = 'Signed'  
        title = '{} **{} {}, {} {}**'.format(stars, first_name, last_name, year, position)
        
        #Now that composite rating can be str or float, we need to handle both cases. Also, don't want the pound sign in front of N/A values.
        if type(composite_rating) is str:
            body = '**Player Bio**\nHome Town: {}, {}\nHigh School: {}\nHeight: {}\nWeight: {}\n\n**247Sports Info**\nComposite Rating: {}\nProfile: [Click Me]({})\n\n'.format(city, state, high_school, height, int(weight), composite_rating, player_url)
            rankings = '**Rankings**\nNational: #{}\nState: #{}\nPosition: #{}\n'.format(national_rank, state_rank, position_rank)
        else:
            body = '**Player Bio**\nHome Town: {}, {}\nHigh School: {}\nHeight: {}\nWeight: {}\n\n**247Sports Info**\nComposite Rating: {:.4f}\nProfile: [Click Me]({})\n\n'.format(city, state, high_school, height, int(weight), composite_rating, player_url)
            rankings = '**Rankings**\nNational: #{}\nState: #{}\nPosition: #{}\n'.format(national_rank, state_rank, position_rank)
        
        #Create a recruitment status string. If they are committed, use our scraped json team_ids dictionary to get the team name from the id in the committed team image url.
        #I've found that if a team does not have an image on 247, they use a generic image with 0 as the id. Also if the image id is not in the dictionary, we want to say Unknown.
        recruitment_status = 'Currently {}'.format(commit_status)
        if commit_status == 'Committed' or commit_status == 'Signed':
            school_id = str(search['CommitedInstitutionTeamImage'].split('/')[-1].split('.')[0])
            if school_id == '0' or school_id not in team_ids:
                school = 'Unknown'
            else:
                school = team_ids[school_id]
            if school == 'Nebraska':
                school += ' 💯:corn::punch:'
            recruitment_status += ' to {}'.format(school)
        recruitment_status = '**' + recruitment_status + '**\n\n'
            
        crootstring = recruitment_status + body + rankings
        message_embed = discord.Embed(name="CrootBot", color=0xd00000)
        message_embed.add_field(name=title, value=crootstring, inline=False)
        #Don't want to try to set a thumbnail for a croot who has no image on 247
        if image_url != '/.':
            message_embed.set_thumbnail(url = image_url)
        message_embed.set_footer(text=huskerbot_footer)
        await channel.send(embed=message_embed)

        global player_search_list
        player_search_list = []

        
@client.command()
async def cb(ctx):
    await crootbot.invoke(ctx)

    
@client.command()
async def billyfacts(ctx):
    """ Real facts about Bill Callahan. """
    facts = []
    with open("facts.txt") as f:
        for line in f:
            facts.append(line)
    f.close()

    random.shuffle(facts)
    await ctx.message.channel.send(random.choice(facts))


@client.command()
async def randomflag(ctx):
    """ A random ass, badly made Nebraska flag. """

    # This keeps bot spam down to a minimal.
    await function_helper.check_command_channel(ctx.command, ctx.channel)
    if not function_helper.correct_channel:
        await ctx.send(wrong_channel_text)
        return

    flags = []
    with open("flags.txt") as f:
        for line in f:
            flags.append(line)
    f.close()

    random.shuffle(flags)
    embed = discord.Embed(title="Random Ass Nebraska Flag")
    embed.set_image(url=random.choice(flags))
    await ctx.send(embed=embed)


@client.command()
async def crappyflag(ctx, state):
    """ Outputs crappy flag. The usage is $crappyflag <state>.

    The states are colorado, illinois, indiana, iowa, iowa_state, maryland:, miami, michigan, michigan_state, minnesota, northern_illinois, northwestern, ohio_state, penn_state, purdue, south_alabama, rutgers, texas, wisconsin """

    # This keeps bot spam down to a minimal.
    await function_helper.check_command_channel(ctx.command, ctx.channel)
    if not function_helper.correct_channel:
        await ctx.send(wrong_channel_text)
        return

    state = state.lower()

    embed = discord.Embed(title="Crappy Flags")
    embed.set_image(url=flag_dict[state.lower()])
    await ctx.send(embed=embed)


@client.command()
async def iowasux(ctx):
    """ Iowa has the worst corn. """
    emoji = client.get_emoji(441038975323471874)
    embed = discord.Embed(title="{} IOWA SUX {}".format(emoji, emoji))
    embed.set_image(url='https://i.imgur.com/j7JDuGe.gif')
    await ctx.send(embed=embed)


@client.command()
async def stonk(ctx):
    """ Isms hates stocks. """
    await ctx.send("Stonk!")


@client.command()
async def potatoes(ctx):
    """ Potatoes are love; potatoes are life. """
    authorized = False

    for r in ctx.author.roles:
        if r.id == 583842320575889423:
            authorized = True

    if authorized:
        embed = discord.Embed(title="Po-Tay-Toes")
        embed.set_image(url='https://i.imgur.com/Fzw6Gbh.gif')
        await ctx.send(embed=embed)
    else:
        await ctx.send('You are not a member of the glorious Potato Gang!')


@client.command()
async def asparagus(ctx):
    """ I guess some people like asparagus. """
    authorized = False

    for r in ctx.author.roles:
        if r.id == 583842403341828115:
            authorized = True

    if authorized:
        embed = discord.Embed(title="Asparagang")
        embed.set_image(url='https://i.imgur.com/QskqFO0.gif')
        await ctx.send(embed=embed)
    else:
        await ctx.send('You are not a member of the glorious Asparagang!')


@client.command()
async def flex(ctx):
    """ S T R O N K """
    embed = discord.Embed(title="FLEXXX 😩")
    embed.set_image(url='https://i.imgur.com/92b9uFU.gif')
    await ctx.send(embed=embed)


@client.command()
async def shrug(ctx):
    """ Who knows 😉 """
    embed = discord.Embed(title="🤷‍♀️")
    embed.set_image(url='https://i.imgur.com/Yt63gGE.gif')
    await ctx.send(embed=embed)


@client.command()
async def ohno(ctx):
    """ This is not ideal. """
    embed = discord.Embed(title="Big oof")
    embed.set_image(url='https://i.imgur.com/f4P6jBO.png')
    await ctx.send(embed=embed)


@client.command()
async def bigsexy(ctx):
    """ Give it to me Kool Aid man. """
    embed = discord.Embed(title="OOOHHH YEAAHHH 😩")
    embed.set_image(url='https://i.imgur.com/UpKIx5I.png')
    await ctx.send(embed=embed)


@client.command()
async def whoami(ctx):
    """ OH YEAH! """
    embed = discord.Embed(title="OHHH YEAAAHHH!!")
    embed.set_image(url='https://i.imgur.com/jgvr8pd.gif')
    await ctx.send(embed=embed)


@client.command()
async def thehit(ctx):
    """ The hardest clean hit ever. """
    embed = discord.Embed(title="CLEAN HIT!")
    embed.set_image(url='https://i.imgur.com/mKRUPoD.gif')
    await ctx.send(embed=embed)

@client.command()
async def strut(ctx):
    """ Martinez struttin his stuff """
    embed = discord.Embed(title = "dat strut")
    embed.set_image(url = 'https://media.giphy.com/media/iFrlakPVXLIj8bAqCc/giphy.gif')
    await ctx.send(embed = embed)
    
@client.command()    
async def huskerbotquit(ctx):
    """ Did HuskerBot act up? Use this only in emergencies. """
    authorized = False

    for r in ctx.author.roles:
        # # await ctx.send("Name: `{}`\n, ID: `{}`".format(r.name, r.id))
        if r.id in authorized_to_quit:
             authorized = True

    if authorized:
        await ctx.send("You are authorized to turn me off. Good bye cruel world 😭.")
        print("!!! I was turned off by '{}' in '{}'.".format(ctx.author, ctx.channel))
        await client.logout()
    else:
        await ctx.send("Nice try buddy! 👋")


@client.command()
async def cb_refresh(ctx):
    """ Did HuskerBot act up? Use this only in emergencies. """
    authorized = False

    for r in ctx.author.roles:
        # await ctx.send("Name: `{}`\n, ID: `{}`".format(r.name, r.id))
        if r.id in authorized_to_quit:
            authorized = True

    if authorized:
        await check_last_run(ctx)
    else:
        await ctx.send("Nice try buddy! 👋")


@client.command()
async def referee(ctx, call):
    """ HuskerBot will tell you about common referee calls. Usage is `$refereee <call>`.\n
    The calls include: chip, chop, encroachment, facemask, hand2face, hold, illfwd, illshift, inelrec, persfoul, pi, ruffkick, ruffpas, safety, targeting, td, unsport """

    # This keeps bot spam down to a minimal.
    await function_helper.check_command_channel(ctx.command, ctx.channel)
    if not function_helper.correct_channel:
        await ctx.send(wrong_channel_text)
        return

    call = call.lower()

    penalty_name = ref_dict[call][0]
    penalty_comment = ref_dict[call][1]
    penalty_url = ref_dict[call][2]

    embed = discord.Embed(title='HuskerBot Referee', color=0xff0000)
    embed.add_field(name='Referee Call', value=penalty_name, inline=False)
    embed.add_field(name='Description', value=penalty_comment, inline=False)
    embed.set_thumbnail(url=penalty_url)
    embed.set_footer(text=huskerbot_footer)
    await ctx.send(embed=embed)


@client.command()
async def ref(ctx):
    await referee.invoke(ctx)


@client.command()
async def recentballs(ctx, number=0):
    """ Send the last 1-5 crystal ball predictions from Steve Wiltfong. Usage is `$recent_balls [1-5]`. """
    # Error handling, Random number of 5 to prevent spam

    # This keeps bot spam down to a minimal.
    await function_helper.check_command_channel(ctx.command, ctx.channel)
    if not function_helper.correct_channel:
        await ctx.send(wrong_channel_text)
        return

    if number > 5:  # len(crystal_balls.cb_list):
        await ctx.send("The number of retrieved Crystal Balls must be less than 5.")
        return

    await check_last_run(ctx)

    limitSpam = -1

    if number > 0:
        number -= 1

    for cbs in crystal_balls.cb_list:
        if limitSpam >= number:
            return

        varPhoto = cbs['Photo']
        varName = cbs['Name']
        varPrediction = cbs['Prediction']
        varPredictionDate = cbs['PredictionDate']
        varProfile = "[Profile]({})".format(cbs['Profile'])
        varResult = cbs['Result']
        varTeams = dict(cbs['Teams'])
        varTeamString = ""

        for x, y in varTeams.items():
            varTeamString += '{} : {}\n'.format(x, y)

        embed = discord.Embed(title="Steve Wiltfong Crystal Ball Predictions", color=0xff0000)
        embed.set_thumbnail(url=varPhoto)
        embed.add_field(name="Player Name", value=varName, inline=False)
        embed.add_field(name="Prediction", value=varPrediction, inline=True)
        embed.add_field(name="Prediction Date/Time", value=varPredictionDate, inline=True)
        embed.add_field(name="Result", value=varResult, inline=False)
        embed.add_field(name="Predicted Teams", value=varTeamString, inline=True)
        embed.add_field(name="247Sports Profile", value=varProfile, inline=False)
        embed.set_footer(text=huskerbot_footer)
        await ctx.send(embed=embed)

        limitSpam += 1


@client.command()
async def eightball(ctx, *, question):
    """ Ask a Magic 8-Ball a question. """
    dice_roll = random.randint(0, len(eight_ball))

    embed = discord.Embed(title=':8ball: HuskerBot 8-Ball :8ball:')
    embed.add_field(name=question, value=eight_ball[dice_roll])

    await ctx.send(embed=embed)


@client.command()
async def cb_search(ctx, *, team):
    """ Search through all of Steve Wiltfong's crystal ball predictions by team. """

    # This keeps bot spam down to a minimal.
    await function_helper.check_command_channel(ctx.command, ctx.channel)
    if not function_helper.correct_channel:
        await ctx.send(wrong_channel_text)
        return

    # await check_last_run(ctx)

    search_list = crystal_balls.cb_list
    saved_results = []

    for key in search_list:
        first_name = key['Name']
        prediction = key['Prediction']
        predictiondate = key['PredictionDate']
        # profile = key['Profile']
        result = key['Result']

        search_team = dict(key['Teams'])

        for x, y in search_team.items():
            if team.lower() in x.lower():
                saved_results.append("· **{}** to [**{}**] is/was: **{}**".format(first_name, prediction, result))

    output_str = ""
    i = 1

    # Discord errors out if character limit exceeds 2,000
    for player in saved_results:
        if i > 10:
            break
        i += 1

        output_str += "{}\n".format(player)

    embed = discord.Embed(title=" ", color=0xff0000)
    embed.set_author(name="HuskerBot")
    embed.add_field(name="Crystal Ball Search Results for {}".format(team), value=output_str, inline=False)
    await ctx.send(embed=embed)


@client.command()
async def on_join_test(ctx):
    authorized = False

    for r in ctx.author.roles:
        # # await ctx.send("Name: `{}`\n, ID: `{}`".format(r.name, r.id))
        if r.id in authorized_to_quit:
            authorized = True

    if authorized:
        embed = discord.Embed(title="HuskerBot's Welcome Message", color=0xff0000)
        embed.add_field(name="Welcome __`{}`__ to the Huskers Discord!".format(ctx.author), value="The Admin team and Frost Approved members hope you have a good time while here. I am your full-serviced Discord bot, HuskerBot! You can find a list of my commands by sending `$help`.\n\n"
                       "We also have some fun roles that may interest you and you're welcome to join! The first, we have the 🔴 `@Lil' Huskers Squad`--those who are fans of Lil Red. Next up we have the 🥪 `@/r/unza` team. They are our resident Runza experts. Right behind the sandwich lovers are the 😂 `@Meme Team`! Their meme creation is second to none. Finally, we have our two food gangs: 🥔 `@POTATO GANG` and 🥒 `@Asparagang`. Which is better?\n\n"
                       "React to this message with the emojis below to automatically join the roles!", inline=False)
        embed.set_footer(text=huskerbot_footer)
        await ctx.message.author.send(embed=embed)
    else:
        await ctx.send("Not authorized to use this command.")


# Run the Discord bot
client.run(config.DISCORD_TOKEN)
