const mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "root"
});

con.connect(function(err) {
  if (err) console.log("Cannot Connect: " + err);
  console.log("Connected to Mysql!");
   con.query("CREATE DATABASE IF NOT EXISTS Dictionary", function (err2, result) {
    if (err2) console.log("Cannot Create DB: " + err2);
    console.log("Database created");
  });
});

var icon = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "root",
  database: "Dictionary"
});

icon.connect(function(err) {
  if (err) console.log("Cannot Connect (in 2nd connection): " + err);
  console.log("Connected!");
  var sql = "CREATE TABLE vocabulary (word VARCHAR(255), synonym INT, POS VARCHAR(255), meaning VARCHAR(255), translation VARCHAR(255), english VARCHAR(255))";
  icon.query(sql, function (err2, result) {
    if (err2) onsole.log("Cannot Create Table: " + err2);
    console.log("Table created");
  });
});