var mysql = require('mysql');
var connection = mysql.createConnection({
    host : 'localhost',
    user : 'nodejs',
    password : 'nodejs',
    database : 'webdb2023'
});

connection.connect();

connection.query('SELECT * from topic', (error, results, fields) => {
    if (error) {
        console.log(error);
    }
    console.log(fields);
    console.log(results);
    console.log(results[0].title); //title값을 읽고싶을 때 [Output]: Mysql
    console.log(results[0].descrpt); //내용을 읽고싶을 때 [Output]: MySQL is Database Name.
});
connection.end();