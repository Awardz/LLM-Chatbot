from twitchio.ext import commands
from dotenv import load_dotenv
import os
import requests

load_dotenv()  # Load environment variables from .env file


TWITCH_OAUTH_TOKEN = os.getenv('TWITCH_OAUTH_TOKEN')
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
TWITCH_CHANNEL = os.getenv('TWITCH_CHANNEL')
BOT_ID = os.getenv('BOT_ID')

headers = {
    'Authorization': f'OAuth {TWITCH_OAUTH_TOKEN.split("oauth:")[1] if TWITCH_OAUTH_TOKEN.startswith("oauth:") else TWITCH_OAUTH_TOKEN}'
}
response = requests.get('https://id.twitch.tv/oauth2/validate', headers=headers)
if response.status_code == 200:
    token_info = response.json()
    print("Token is valid!")
    print(f"Scopes: {token_info.get('scopes', [])}")
    print(f"Client ID: {token_info.get('client_id')}")
    print(f"User ID: {token_info.get('user_id')}")
    print(f"Expires in: {token_info.get('expires_in')} seconds")
else:
    print(f"Token validation failed: {response.status_code} - {response.text}")

print(f"Initial Channel: '{TWITCH_CHANNEL}'")
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TWITCH_OAUTH_TOKEN,
            client_id=TWITCH_CLIENT_ID,
            client_secret=TWITCH_CLIENT_SECRET,
            bot_id=BOT_ID,
            prefix='!', 
            initial_channels=[TWITCH_CHANNEL]
        )
        print(f"Attempting to authenticate with BOT_ID: '{BOT_ID}'")

    async def event_ready(self):
        print('Bot Ready')
        print(f"Joined channels: {self.connected_channels}")
        # Send a test message to confirm the bot can send messages
        channel = self.get_channel(TWITCH_CHANNEL.lower())
        if channel:
            await channel.send("Bot is online!")
        else:
            print(f"Failed to find channel: {TWITCH_CHANNEL}")
        
    async def event_error(self, error):
        print(f"Error occurred: {type(error).__name__}")
        print(f"Error message: {str(error)}")
        if hasattr(error, 'event'):
            print(f"Event: {error.event}")
        if hasattr(error, 'exception'):
            print(f"Exception: {type(error.exception).__name__}: {str(error.exception)}")

    async def event_raw_data(self, data):
        print(f"Raw data: {data}")  # Log all raw IRC messages

    async def event_message(self, message):
        if message.echo:
            return
        print(f"Received: {message.content}")  # Debug
        await self.handle_commands(message)  # REQUIRED
    
    @commands.command()
    async def hello(self, ctx):
        print(f"!hello executed by {ctx.author.name}")  # Debug
        await ctx.send(f'Hello, {ctx.author.name}!')

    
if __name__ == '__main__':
    bot = Bot()
    bot.run()