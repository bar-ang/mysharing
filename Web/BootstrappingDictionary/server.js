const http = require('http');
const url = require('url');
const fs = require('fs');
const mysql = require('mysql');

const hostname = '127.0.0.1';
const port = 3000;


var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "root"
});

con.connect(function(err) {
  if (err) throw err;
  console.log("Connected to Mysql!");
});

const server = http.createServer((req, res) => {
	var q = url.parse(req.url, true);
	var filename
	if(req.url.length > 1){
		filename = "." + q.pathname;
	}else{
		filename = "./index.html";
	}
	

	if(filename != "./proc.nf"){
		console.log("Client asked for: " + filename);
		fs.readFile(filename, function(err,data){
			if (err) {
	      		res.writeHead(404, {'Content-Type': 'text/html'});
	      		console.log(file + ": file could not be sent.");
	      		return res.end("404 Not Found");
	    	}
	    	res.writeHead(200, {'Content-Type': 'text/html'});
    		res.write(data);
    		return res.end();		
		});
	}else{
		var data = q.query;
		console.log("Client sent data: " + data);

		var build = {
			"word":data.word,
			"mean":data.mean,
			"trans":data.trans,
			"eng":data.eng
		};

		res.write("OK");
	}
	res.end();
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
