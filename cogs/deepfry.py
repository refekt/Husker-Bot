from PIL import Image
import requests
import utils.fryer as fryer
from utils.consts import HEADERS, CHAN_NORTH_BOTTTOMS, CHAN_TEST_SPAM, CHAN_POSSUMS, CHAN_SCOTTS_BOTS
import discord
from discord.ext import commands
import io
from PIL import ImageFile
import random

'''
    Quick meme thrown together with the help of StackOverflow and some GitHub repos found online
'''
    
async def load(url):
    # image = Image.open(input('Enter the image name: '))
    # layers = int(input('How many layers do you want? '))
    # emote_amount = int(input('How many emotes per layer do you want? '))
    # noise = float(input('Noise level (recommended from 0.1 to 1): '))
    # contrast = float(input('Contrast level (0-500 or more): '))
    # return image, layers, emote_amount, noise, contrast
    image_response = requests.get(url = url, stream = True, headers = HEADERS)
    # file_size, image_size = getsizes(image_response)
    # if image_size is None:
        # image_size = (256, 256)
        
    image = Image.open(io.BytesIO(image_response.content))
    #image = Image.frombytes('RGBA', image_size, image_response.content, 'raw')
    return image

class RecruitCommands(commands.Cog):
    @commands.command()
    async def deepfry(self, ctx, url):
        if ctx.channel.id not in [CHAN_NORTH_BOTTTOMS, CHAN_POSSUMS, CHAN_TEST_SPAM, CHAN_SCOTTS_BOTS]:
            await ctx.send("This command isn't allowed here!")
            return
        msg = await ctx.send("Loading...")
        try:
            emote_amount = random.randrange(1,6)
            noise = random.uniform(0.1, 1.0)
            contrast = random.randrange(501)
            layers = random.randrange(1, 4)
            image = await load(url)
            fried = await fryer.fry(image, emote_amount, noise, contrast)

            for layer in range(layers - 1):
                emote_amount = random.randrange(1,6)
                noise = random.uniform(0.1, 1.0)
                contrast = random.randrange(501)
                fried = await fryer.fry(fried, emote_amount, noise, contrast)
            
            with io.BytesIO() as image_binary:   
                fried.save(image_binary, 'PNG')
                image_binary.seek(0)
                await msg.delete()
                await ctx.send(file = discord.File(fp=image_binary, filename='image.png'))
        except Exception as e:
            print(e)
            await msg.edit(content = "Something went wrong. Blame my creators.")
        
        
def setup(bot):
    bot.add_cog(RecruitCommands(bot))