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
    var message = line.join(' ');
    ws.send(message, {mask: true});
    console.log("Message sent");
});

// Exiting and closing 
function exit() {
  ws.close();
  console.log('Socket closed!');
  console.log('Goodbye!');
  process.exit(); // Exit
}