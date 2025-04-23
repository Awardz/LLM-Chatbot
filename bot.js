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

//async functions returns a promise
// The async function getJoke fetches a random joke from the API and returns it as a string.
async function getJoke() 
{
  try 
  {
    const response = await fetch('https://official-joke-api.appspot.com/random_joke');
    const joke = await response.json();
    return `${joke.setup}  ${joke.punchline}`;
  }
  catch (error) 
  {
    console.error('Error fetching joke:', error);
    return 'Sorry, I could not fetch a joke at the moment.';
  }
  
}

async function getWeather() 
{
  const city = 'New York';
  const apiKey = process.env.WEATHER_API_KEY;
  
  try 
  {
    const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${apiKey}`);
    if (!response.ok) 
    {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    console.log('Weather data:', data); // Debug: Log full response
    return `${data.name}: ${data.weather[0].description}, ${data.main.temp}°C`;
  } 
  catch (error) 
  {
    console.error('Error fetching weather:', error.message);
    return `Sorry, I couldn’t fetch the weather: ${error.message}`;
  }
}


client.on('message', async (channel, tags, message, self) => {

  if (message.toLowerCase() === '!hello') {
    client.say(channel, `Hey ${tags.username}, what's up?`);
  }
  else if (message.toLowerCase() === '!joke')
  {
    //then means that the function is called when the message is sent
    //then is used to handle the promise returned by the getJoke function
    //the joke is fetched from the API and sent to the channel
    getJoke().then(joke => {
      client.say(channel, joke);
    });
  }
  else if (message.toLowerCase() === '!weather')
  {
    const weather = await getWeather();
    client.say(channel, weather);
  }


});