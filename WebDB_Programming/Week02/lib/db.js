var mysql = require('mysql');
var connection = mysql.createConnection({
    host : 'localhost',
    user : 'nodejs',
    password : 'nodejs',
    database : 'webdb2023'
});
db.connect();
module.exports = db;