/*
var myObj = {
	myValue: 5,
	getValue: function() {
		return this.myValue;
	}
}*/

var myClass = function(enPerson) {
	if(typeof enPerson !== 'object') {
		throw new Error('Du använder klassen fel! Ett objekt måste skickas in');
	}

	this.myValue = 5;

	this.myPerson = enPerson;
}

myClass.prototype.getValue = function() {
	return this.myValue;
}

myClass.prototype.getPerson = function() {
	return this.myPerson;
}

module.exports = myClass;

