require('dotenv').config('/.env');
// Instantiate a DialogFlow client.
const dialogflow = require('dialogflow').v2beta1;

const dialogflowClient = new dialogflow.SessionsClient();
// Define session path

// var sessionPath = 

const knowbase = new dialogflow.KnowledgeBasesClient();
const knowledgeBasePath = knowbase.knowledgeBasePath(
  process.env.PROJECT_ID,
  "OTQxNTU2MDA3MjMyMDI1Mzk1Mg"
);


const Discord = require('discord.js');
const discordClient = new Discord.Client();


discordClient.on('ready', () => {
  console.log('Ready!');
});

discordClient.on('message', m => {
  if (!shouldBeInvoked(m)) {
    return;
  }

  const message = remove(discordClient.user.username, m.cleanContent);

  if (message === 'help') {
    return m.channel.send(process.env.DISCORD_HELP_MESSAGE);
  }

  var date = new Date();
  const dialogflowRequest = {
    session: dialogflowClient.sessionPath(process.env.PROJECT_ID, Math.round(date.getTime()/10000).toString()),
    queryInput: {
      text: {
        text: message,
        languageCode: 'en-US',
      },
    },
    queryParams: {
      knowledgeBaseNames: [knowledgeBasePath],
    }
  };

  dialogflowClient.detectIntent(dialogflowRequest).then(responses => {
    // console.log(responses);
    m.channel.send(responses[0].queryResult.fulfillmentText);
  }).catch(err => console.log(err));
});

function shouldBeInvoked(message) {
  return (message.content.startsWith(process.env.DISCORD_PREFIX) ||
          message.content.startsWith('@' + discordClient.user.username) ||
          message.channel.type === 'dm') &&
         discordClient.user.id !== message.author.id;
}

function remove(username, text) {
  return text.replace('@' + username + ' ', '').replace(process.env.DISCORD_PREFIX + ' ', '');
}

discordClient.login(process.env.DISCORD_TOKEN);
