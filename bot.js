require('dotenv').config(); // Load environment variables from .env file
const tmi = require('tmi.js');

const client = new tmi.Client(
    {
        options: { debug: true },
        connection: { reconnect: true },
        identity: {
            username: process.env.BOT_USERNAME, // Replace with your Twitch bot username
            password: process.env.TWITCH_OAUTH_TOKEN 
        },
        channels: [process.env.TWITCH_CHANNEL] // Replace with your Twitch channel name
    });

client.connect();

client.on('message', (channel, tags, message, self) => {

  if (message.toLowerCase() === '!hello') {
    client.say(channel, `Hey ${tags.username}, what's up?`);
  }
});