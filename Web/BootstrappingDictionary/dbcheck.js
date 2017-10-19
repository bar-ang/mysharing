const mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "root",
  database: "Dictionary"
});

con.connect(function(err) {
  if (err) console.log("Cannot Connect (in 2nd connection): " + err);
  console.log("Connected!");
  var sql = "INSERT INTO vocabulary (word, synonym,POS,english) VALUES ('Kartikos', 0, 'N', 'Job')";
  con.query(sql, function (err2, result) {
    if (err2) onsole.log("Cannot Create Table: " + err2);
    console.log("Query done.");
  });
});