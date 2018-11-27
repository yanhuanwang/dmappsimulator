var http = require('http');
var https = require('https');

var express = require('express');
const stream = require('stream');
var app = express();
var fs = require("fs");
var path = require('path');
var privateKey  = fs.readFileSync('cert/private.key', 'utf8');
var certificate = fs.readFileSync('cert/certificate.crt', 'utf8');
var credentials = {key: privateKey, cert: certificate};

var bodyParser = require('body-parser')
// app.use(bodyParser.json({limit: "50mb"}));
// app.use(bodyParser.urlencoded({limit: "50mb", extended: true, parameterLimit:50000}));
// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }))

// parse application/json
app.use(bodyParser.json())

// parse application/vnd.api+json as json
app.use(bodyParser.json({ type: 'application/vnd.api+json' }))

// parse some custom thing into a Buffer
app.use(bodyParser.raw({limit:1024*1024*20, type: 'application/octet-stream' }))
// express.bodyParser({limit: '5mb'})
// parse an HTML body into a string
app.use(bodyParser.text({ type: 'text/html' }))
app.get("/",function(req, res){
	res.send("ok");
})
app.post('/publish/1/:filename', function (req, res) {
	console.log(req.files);
	console.log(req.body)
	console.log(req.headers)
	var filename = path.basename(req.params.filename);
  filename = path.resolve(__dirname, filename);
	console.log(req.params.filename);
  fs.writeFile(filename, req.body, function (error) {
  	if (error) { console.error(error); }
	});
	 res.send("ok")
})
app.put('/publish/1/:filename', function (req, res) {
	console.log(req.files);
	console.log(req.body);
	console.log(req.headers);
	var filename = path.basename(req.params.filename);
  // filename = path.resolve(__dirname, filename);
	// console.log(req.params.filename);
  // fs.writeFile(filename, req.body, function (error) {
  // 	if (error) { console.error(error); }
	// });
	 // res.send("ok")
	 res.redirect(301, 'http://127.0.0.1:3908/publish/1/'+filename)
})
var httpServer = http.createServer(app);
var httpsServer = https.createServer(credentials, app);

var httpPort=3906
var httpsPort=3907
httpServer.listen(httpPort);
console.log("Example app http listening at " + httpPort)
httpsServer.listen(httpsPort);
console.log("Example app https listening at "+ httpsPort)

// var server = app.listen(3906, function () {
//
//   var host = server.address().address
//   var port = server.address().port
//
//   console.log("Example app listening at http://%s:%s", host, port)
//
// })
