import discord, os, openai, re
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = '-', intents = intents)


# .env parts

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')



# getting things ready

@bot.event
async def on_ready():
	print("{0.user} is ready to go!".format(bot))



# member join event

async def intro_dm(member):
	print(f"Sending a DM to {member.name} to welcome them to the channel!")
	
	await member.send(f"""🎉	Hi {member.name} !	🎉
	
	ε(´｡•᎑•`)っ 💕		Welcome to the server Krinlee's Roost!		ε(´｡•᎑•`)っ 💕
	
	Do you like to code?	🇵 🇾 🐍	-	🇯 🇸 ♨️	-	🇨  #⃣
	Do you like to game?	🎮	🕹️	👾
	Are you a content creator looking for a place to hang out?	💡	🎥	🎬
	
	We do that here. For now there isn't much, but there's always room to grow!
	
	Please be respectful to everyone, and have fun!		🎉""")




# chatgpt command

@bot.command()
async def chat(ctx):
	openai.api_key = os.getenv('OPENAI_API_KEY')
	await ctx.send("What would you like to chat about?")
	while True:
		print("Chat initiated\n\n")
		prompt = await bot.wait_for('message', check = lambda message: message.author == ctx.author, timeout = 180)
		if prompt != 'done':
			print("Prompt received\n\n")
			completion = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = [{"role": "user", "content": str(prompt.content)}], temperature = 0.1, max_tokens = 100)
			reMsg = completion.choices[0].message
			response = reMsg['content']
			await ctx.send(response)
			print("Reply sent\n\n")
		elif prompt == 'done':
			print("Session ended")
			return



@bot.event
async def on_member_join(member):
	await intro_dm(member)



try:
	bot.run(TOKEN)
except discord.HTTPException as e:
	if e.status == 429:
		print("The Discord servers denied the connection for making too many requests")
		print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
	else:
		raise e
