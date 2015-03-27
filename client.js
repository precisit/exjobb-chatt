var WebSocket = require('ws');
var ws = new WebSocket('ws://localhost:1080/echoSocket')

ws.on('open', function() {
	console.log('Socket open!');
	ws.send('Siri och Kerstin says hi!'); //Json representation skickas om object skall skickas
});

ws.on('message', function(data, flags) {
	console.log('Server says', data);
});

