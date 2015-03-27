var colors = require('colors');

//Demo #0 - Colors (npm)
console.log('Hej green world'.green);

//Demo #1 - Function
var matte = require('./mattematik');
console.log(matte(5));

//Demo #2 - Class
var myClass = require('./classDemo');
var myObj = new myClass({name: 'kalle', age: 5});
console.log(myObj.getPerson());
