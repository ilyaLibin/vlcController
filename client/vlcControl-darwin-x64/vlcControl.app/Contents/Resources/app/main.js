var menubar = require('menubar');
var mb = menubar({height: 194, width: 448})
var express = require('express');
var app = express();

require('electron-debug')({showDevTools: true});

mb.on('ready', function ready () {
  console.log('app is ready')
})



app.post('/check', function (req, res) {
  res.send('Hello World!');
});


app.listen(5000, function () {
  console.log('Example app listening on port 5000!');
});