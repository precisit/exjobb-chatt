//Creating port and websocket

// New variable which loads the module ws
var WebSocket = require('ws');
// module used for the prompt
var prompt = require('cli-input');

// Creates a port
var port = 3000;

/* If the user has given another port the variable port is changed to the given number
process.argv is an array which contains the command line argument. 
The first element is 'node' 
The second element is the name of the JavaScript file
The next element (element number 2) will be any additional command line arguments*/
if (process.argv.length > 2) {
  port = process.argv[2];
}

// Creates a websocket
var ws = new WebSocket('ws://127.0.0.1:'+ port +'/websocket')

var ps = prompt({
  input: process.stdin,
  output: process.stderr,
  infinite: true,
  prompt: '',
  name: '',
});

// Opens the websocket
ws.on('open', function open() {
	console.log('Socket open!');
  console.log('Set a username by writing \"setUsername; username\"');
  console.log('Send a message by writing \"sendMessage; message; room\"');
  console.log('Join chat room by writing \"join; room');
  console.log('Leave chat room by writing \"leave; room');
  ps.run();
});

ws.on('error', function(error) {
  console.log(error);
});

// ensures that interval timers arent still running after the
// client has disconnected
ws.on('close', function close() {
  console.log('Disconnected');
  exit();
});

ws.on('message', function message(data, flags) {
  // flags.binary will be set if binary data is received
  // flags.masked will be set if the data was masked
  console.log(data);

  //TODO Change so it shows who sent and what it was e.g. "siri: hej!" or "error: set username first!"
});

ps.on('value', function(line) {
    var input = line.join(' ');
    var partsOfMessage = input.split('; ');
    var message = {};

    message['command'] = partsOfMessage[0];
    message['body'] = partsOfMessage[1];

    console.log(partsOfMessage);

    if (partsOfMessage.length < 3) {
      message['room'] = 'default';
    } else {
      message['room'] = partsOfMessage[2];
    }

    jsonMessage = JSON.stringify(message);

    ws.send(jsonMessage, {mask: true});
    console.log("Message sent");
});

// Exiting and closing 
function exit() {
  ws.close();
  console.log('Socket closed!');
  console.log('Goodbye!');
  process.exit(); // Exit
}