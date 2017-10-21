const http = require('http');
const url = require('url');
const fs = require('fs');
const mysql = require('mysql');

const hostname = '127.0.0.1';
const port = 3000;

function findSynonym(data,word, pos){
	return 1;
}

var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "root",
  database: "Dictionary"
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
	

	switch(filename){
		case "./translateword.nf":
			var data = q.query;
			sql = 	"SELECT pronoun, possesion, english, POS " + 
					"FROM vocabulary, rules" +
					"WHERE word=?";
			var vals;

			if(data.suff != "NULL"){
				 sql += " AND suffix=?";
				 vals = [data.word,data.suff];
			}else{
				vals = [data.word];
			}

			con.query(sql, vals, function (err, result, fields) {
			    if (err) {
			    	console.log("could not receive table: " + err);
			    	return;
			    }
			 	res.end(JSON.stringify(result));
			 	return;
			});

			res.end("Bad");
			
			break;
		case "./addentry.nf":
			 var body = "";
			  req.on('data', function (chunk) {
			    body += chunk;
			  });
			  req.on('end', function () {
			    console.log('client sent data: ' + body);
			    var data = JSON.parse(JSON.parse(body));
			    var sql = "INSERT INTO vocabulary VALUES ?";
				vals = [[data.word, findSynonym(data,data.word, data.POS), data.POS, data.meaning, data.translation, data.english]];
				con.query(sql, [vals], function (err, result) {
			    	if (err){
			    		console.log("operation failed: " + err);
			    		res.end("Bad");
			    		return;
			    	}
		    		console.log("Number of records inserted: " + result.affectedRows);
		    		res.end("OK");
	  			});
			  })
			break;

		case "./gettable.nf":
			console.log("Client wants data.");
			con.query("SELECT * FROM vocabulary ORDER BY word", function (err, result, fields) {
			    if (err) {
			    	console.log("could not receive table: " + err);
			    	return;
			    }
			 	res.end(JSON.stringify(result));
			});

			break;

		case "./filtertable.nf":
			console.log("Client wants filtered data.");

			var data = q.query;
			sql = "SELECT * FROM vocabulary WHERE word LIKE ? ORDER BY word";
			val = data.filter + "%";
			con.query(sql, val, function (err, result, fields) {
			    if (err) {
			    	console.log("could not receive table: " + err);
			    	return;
			    }
			 	res.end(JSON.stringify(result));
			});

			break;

		case "./filterregextable.nf":
			console.log("Client wants filtered (by regex) data.");

			var data = q.query;
			sql = "SELECT * FROM vocabulary WHERE word REGEXP ? ORDER BY word";
			val = "^" + data.filter + "$";
			con.query(sql, val, function (err, result, fields) {
			    if (err) {
			    	console.log("could not receive table: " + err);
			    	return;
			    }
			 	res.end(JSON.stringify(result));
			});

			break;

		case "./remtuple.nf":
			var data = q.query;
			console.log("Client wants to remove data data.");
			vals = [data.word];
			con.query("DELETE FROM vocabulary WHERE word = ? ", [vals], function (err, result, fields) {
			    if (err) {
			    	console.log("could not remove tuple: " + err);
			    	res.end("Bad");
			    	return;
			    }
			 	res.end("OK");
			});

			break;
		case "./edittuple.nf":
			var body = "";
			  req.on('data', function (chunk) {
			    body += chunk;
			  });
			  req.on('end', function () {
			    console.log('client sent data: ' + JSON.parse(body));
			    var data = JSON.parse(JSON.parse(body));
			    var sql = "UPDATE vocabulary SET meaning = ?, translation = ?, english = ?, POS = ? WHERE word = ? AND synonym = ?";
				vals = [data.meaning, data.translation, data.english, data.POS, data.word, data.synonym];
				con.query(sql, vals, function (err, result) {
			    	if (err){
			    		console.log("operation failed: " + err);
			    		res.end("Bad");
			    		return;
			    	}
		    		console.log("Number of records inserted: " + result.affectedRows);
		    		res.end("OK");
	  			});
			  })
			break;
		default:
			console.log("Client asked for: " + filename);
			fs.readFile(filename, function(err,data){
				if (err) {
		      		res.writeHead(404, {'Content-Type': 'text/html'});
		      		console.log(filename + ": file could not be sent.");
		      		return res.end("404 Not Found");
		    	}
		    	if(filename.substring(filename.indexOf(".",1)) != ".css")
		    		res.writeHead(200, {'Content-Type': 'text/html'});
		    	else
		    		res.writeHead(200, {'Content-Type': 'text/css'});
	    		res.end(data);
	    		return;		
			});
			break;
	}
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
