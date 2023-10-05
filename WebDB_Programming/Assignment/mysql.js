var mysql = require('mysql');
var connection = mysql.createConnection({
    host : 'localhost',
    user : 'root',
    password : 'nodejs',
    database : 'webdb2023'
});

connection.connect();

connection.query('SELECT * from author', (error, results, fields) => {
    if (error) {
        console.log(error);
    }
    console.log(results);
});
connection.end();