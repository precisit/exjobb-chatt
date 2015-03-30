
// New variable websocket which loads the module ws
var WebSocket = require('ws');



// Neww variable ws which which creates an object (a new websocket)
var ws = new WebSocket('ws://localhost:1080/echoSocket')



// Opens the websocket
ws.on('open', function() {
	console.log('Socket open!');
	ws.send('Welcome to this excellent chat application!'); //Json representation skickas om object skall skickas
});


// By defining an onopen handler attempting to send data ONLY takes place once a connection is established 
ws.onopen = function (event) {
  ws.send("Here's some text that the server is urgently awaiting!"); 
};


ws.on('message', function(data, flags) {
	console.log('Server says', data);
});







// Send text to all users through the server
function sendText() {
  // Construct a msg object containing the data the server needs to process the message from the chat client.
  var msg = {
    type: "message",
    text: document.getElementById("text").value,
    id:   clientID,
    date: Date.now()
  };

  // Send the msg object as a JSON-formatted string.
  ws.send(JSON.stringify(msg));
  
  // Blank the text input element, ready to receive the next line of text from the user.
  document.getElementById("text").value = "";
}




// Receiving messages from the server
ws.onmessage = function (event) {
  console.log(event.data);
}


// Closes the websocket
ws.close():
{
	console.log('Socket closed!');
});

