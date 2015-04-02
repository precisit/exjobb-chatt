
// 1 
//Creating port and websocket

// New variable which loads the module ws
var WebSocket = require('ws');

// Creates a port
var port= 8000;

// Creates a websocket
var ws = new WebSocket('ws://0.0.0.0:'+ port+'/echoWebSocket')

// localhost

/* If the user has given another port the variable port is changed to the given number
process.argv is an array which contains the command line argument. 
The first element is 'node' 
The second element is the name of the JavaScript file
The next element (element number 2) will be any additional command line arguments*/
if (process.argv.length > 2) {
  port = process.argv[2];
}

// 2
// Opens web socket and starts

// Opens the websocket
ws.on('open', function() {
	console.log('Socket open!');
	// Sending message
	// ws.send('Welcome to this excellent chat application!'); //Json representation skickas om object skall skickas
});

// ensures that interval timers arent still running after the
// client has disconnected
ws.on('close', function() {
  console.log('Disconnected');
  clearInterval(id);
  exit();
});

ws.on('message', function(data, flags) {
  // flags.binary will be set if binary data is received
  // flags.masked will be set if the data was masked
  console.log(data);
});

// 3
// Client input 

// To get input from the user the prompt module is used 
/*
 var prompt = require('prompt');

  prompt.start();


  prompt.get(['username'], function (err, result) {
    if (err) { return onErr(err); }
    console.log('Command-line input received:');
    console.log('  Username: ' + result.username);

  });

  prompt.on('Input', function(text) {
  if (text[0] === '/quit') {
    exit();
  }
  else {
    var message = text.join(' ');
    ws.send(message, {mask: true});
  }
});
*/

var promptModule = require('cli-input');

// Initialize prompt
var prompt = promptModule({
  input: process.stdin,
  output: process.stderr,
  infinite: true,
  prompt: '',
  name: ''
});

prompt.on('value', function(line) {
  if (line[0] === '/quit') {
    exit();
  }
  else {
    var message = line.join(' ');
    connection.send(message, {mask: true});
  }
});



function onErr(err) {
  console.log(err);
  return 1;
}

process.on('uncaughtException', function (err) {
    console.log(err);
}); 

// 4
// Sending and receiving messages

// By defining an onopen handler attempting to send data ONLY 
// takes place once a connection is established 
ws.onopen = function open() {
  ws.send("Here's some text that the server is urgently awaiting!"); 
  prompt.run()
};

// Receiving messages from the server
ws.onmessage = function (event) {
  console.log(event.data);
}

// 5
// Exiting and closing 
function exit() {
ws.close(); // Close the websocket connection 
console.log('Socket closed!');
console.log('Goodbye!');
process.exit(); // Exit
}


// BEHÖVS DETTA?
// Send text to all users through the server
// function sendText() {
  // Construct a msg object containing the data the server needs to process the message from the chat client.
//  var msg = {
//    type: "message",
//    text: document.getElementById("text").value,
//    id:   clientID,
//    date: Date.now()
//  };
//  // Send the msg object as a JSON-formatted string.
//  ws.send(JSON.stringify(msg));
  // Blank the text input element, ready to receive the next line of text from the user.
//  document.getElementById("text").value = "";
//}