
#!/usr/bin/env python3.7
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import sys
import random
import json
import config
import crystal_balls
import inspect


botPrefix = '$'
client = commands.Bot(command_prefix=botPrefix)
# client.remove_command('help')

# initialize a global list for crootbot to put search results in
player_search_list = []
emoji_list = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
huskerbot_footer = "Generated by HuskerBot"
hudl_url = None
hudl_location = None

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
             'wisconsin': 'https://i.imgur.com/lgFZFkV.jpg',
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
    print("Logged in as {0}. Discord.py version is: [{1}] and Discord version is [{2}]".format(client.user, discord.__version__, sys.version))
    # print("The client has the following emojis:\n", client.emojis)


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
    # it down even more 
    if len(message.embeds) > 0:
        # Working with crootbot
        # if message.author == client.user and 'Search Results:' in message.content and player_search_list:
        if message.author == client.user and player_search_list and message.embeds[0].footer.text == 'Search Results ' + huskerbot_footer:
            # Pre-add reactions for users
            i = 0
            while i < min(10, len(player_search_list)):
                await message.add_reaction(emoji_list[i])
                i += 1
        if message.author == client.user and message.embeds[0].footer.text == huskerbot_footer:
            url = 'https://www.hudl.com/api/v3/community-search/feed-users/search'
            headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
            embed_field_name = message.embeds[0].fields[0].name.split()
            croot_name = embed_field_name[0] + ' ' + embed_field_name[1]
            croot_name = croot_name.replace('*', '')
            payload = {'query' :  croot_name}
            page = requests.post(url = url, headers = headers, params = payload)
            data = json.loads(page.text)
            results = data['results']
            matching_players = []
            # print("results:\n{}".format(results))
            for r in results:                   
                if r['name'] == croot_name and (r['primaryTeam']['teamName']=='Boys Varsity Football' or r['primaryTeam']['teamName']=='Husker Football'):
                    matching_players.append(r)
            global hudl_url
            # print("len(matching_players) == {}".format(len(matching_players)))
            if len(matching_players) > 0:  
                global hudl_location
                hudl_url = 'https://www.hudl.com' + matching_players[0]['url']
                for m in matching_players:
                    if m['primaryTeam']['schoolName'] == 'University of Nebraska':
                        hudl_url = 'https://www.hudl.com' + m['url']
                    elif m['primaryTeam']['location'] == hudl_location:
                        hudl_url = 'https://www.hudl.com' + m['url']
                hudl_location = None
                page = requests.get(url=hudl_url, headers=headers)
                embed_old = message.embeds[0]
                embed_new = embed_old.set_footer(text='Click the video camera emoji to get the most-viewed Hudl highlight for this recruit')
                await message.edit(embed=embed_new)
                await message.add_reaction('📹')
            #If we can't find a suitable match, then empty the list. Keeps people from pulling up a highlight for a previous crootbot message
            else:
                hudl_url = None

    # Always need this
    await client.process_commands(message)

@client.event
async def on_reaction_add(reaction, user):
    # print(reaction.emoji)
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
    
    # If a hudl highlight is found for a crootbot response and someone reacts to the video camera, call the function to parse through the recruits hudl page and grab a highlight video
    if len(reaction.message.embeds) > 0:
        if user != client.user and reaction.message.author == client.user and reaction.message.embeds[0].footer.text == 'Click the video camera emoji to get the most-viewed Hudl highlight for this recruit' and hudl_url is not None:            
            if reaction.emoji == '📹':
                channel = reaction.message.channel
                await hudl_highlight(channel)
        
# Catch invalid commands/errors
@client.event
async def on_command_error(ctx, error):
    output_msg = "Whoa there {}! Something went wrong. {}. Please review `$help` for a list of all available commands.".format(ctx.message.author, error)
    await ctx.send(output_msg)

@client.command()
async def crootbot(ctx, year, first_name, last_name):
    """ CrootBot provides the ability to search for and return information on football recruits. Usage is `$crootbot <year> <first_name> <last_name>`. The command is able to find partial first and last names. """
    # pulls a json file from the 247 advanced player search API and parses it to give info on the croot.
    # First, pull the message content, split the individual pieces, and make the api call

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
            # body = '**{}, Class of {}**\n{}, {}lbs -- From {}, {}({})\n247 Composite Rating: {}\n\n'.format(position, year, height, int(weight), city, state, high_school, composite_rating)
            body = '**Player Bio**\nHome Town: {}, {}\nHigh School: {}\nHeight: {}\nWeight: {}\n\n**247Sports Info**\nComposite Rating: {}\nProfile: [Click Me]({})\n\n'.format(city, state, high_school, height, int(weight), composite_rating, player_url)
            rankings = '**Rankings**\nNational: #{}\nState: #{}\nPosition: #{}\n'.format(national_rank, state_rank, position_rank)
        else:
            # body = '**{}, Class of {}**\n{}, {}lbs -- From {}, {}({})\n247 Composite Rating: {:.4f}\n\n'.format(position, year, height, int(weight), city, state, high_school, composite_rating)
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
            
        # crootstring = body + rankings + recruitment_status
        crootstring = recruitment_status + body + rankings
        message_embed = discord.Embed(name="CrootBot", color=0xd00000)
        message_embed.add_field(name=title, value=crootstring, inline=False)
        #Don't want to try to set a thumbnail for a croot who has no image on 247
        if image_url != '/.':
            message_embed.set_thumbnail(url = image_url)
        message_embed.set_footer(text=huskerbot_footer)
        await channel.send(embed=message_embed)
        #Decided to send a global variable to location to help hudl highlights find the correct player
        global hudl_location
        hudl_location = '{}, {}'.format(city, state)
        
        global player_search_list
        player_search_list = []

        
@client.command()
async def cb(ctx):
    await crootbot.invoke(ctx)

    
async def hudl_highlight(channel):
    """This function takes the current global hudl_url variable and posts the most viewed highlight video from that profile"""
    global hudl_url
    url = hudl_url
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    #The original hudl url redirects, so we want to request the page, then get the new url after the redirect
    page = requests.get(url=url, headers=headers)
    url = page.url + '/videos'
    # print("Pulling video for recruit at url {}".format(url))
    page = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    # This fucking shit. To avoid using a webdriver, we have to take the direct request and find the script section that corresponds to the script that pulls the
    # profile details, then find the video in the resulting dictionary. Took so much bs to find this
    data = json.loads(soup.find_all('script')[4].get_text()[soup.find_all('script')[4].get_text().find('{'):-1])
    reels = data['model']['highlights']['reels']
    # Initialize our target url as the first video in the returned list, then search through the list and find the video with the most views. 
    video_url = data['model']['highlights']['reels'][0]['videoUrl']
    video_views = data['model']['highlights']['reels'][0]['views']
    for r in reels:
        if r['views'] > video_views:
            video_views = r['views']
            video_url = r['videoUrl']
    await channel.send('https://www.hudl.com' + video_url)   
    hudl_url = None

    
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
    """ Outputs crappy flag.
    The usage is $crappyflag <state>.
    The states are colorado, illinois, indiana, iowa, iowa_state, maryland:, miami, michigan, michigan_state, minnesota, northern_illinois, northwestern, ohio_state, penn_state, purdue, south_alabama, rutgers, texas, wisconsin """

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
    embed = discord.Embed(title="Po-Tay-Toes")
    embed.set_image(url='https://i.imgur.com/Fzw6Gbh.gif')
    await ctx.send(embed=embed)


@client.command()
async def asparagus(ctx):
    """ I guess some people like asparagus. """
    embed = discord.Embed(title="Asparagang")
    embed.set_image(url='https://i.imgur.com/QskqFO0.gif')
    await ctx.send(embed=embed)


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
async def huskerbotquit(ctx):
    """ Did HuskerBot act up? Use this only in emergencies. """
    print("HuskerBot was terminated by {}.".format(ctx.message.author))
    await client.logout()


@client.command()
async def referee(ctx, call):
    """ HuskerBot will tell you about common referee calls. Usage is `$refereee <call>`.\n
    The calls include: chip, chop, encroachment, facemask, hand2face, hold, illfwd, illshift, inelrec, persfoul, pi, ruffkick, ruffpas, safety, targeting, td, unsport """

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
    if number > 5:  # len(crystal_balls.cb_list):
        await ctx.send("The number of retrieved Crystal Balls must be less than 5.")
        return

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
        varProfile = cbs['Profile']
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

    crystal_balls.check_last_run()

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

    # await ctx.send("Steve Wiltfong's Last 10 Predictions for __**{}**__:\n{}".format(team, output_str))

# Run the Discord bot
client.run(config.DISCORD_TOKEN)
