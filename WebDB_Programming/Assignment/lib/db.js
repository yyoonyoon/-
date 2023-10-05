//201935291 염상윤

var mysql = require('mysql');
var db = mysql.createConnection({
    host : 'localhost',
    user : 'nodejs',
    password : 'nodejs',
    database : 'webdb2023'
});
db.connect();
module.exports = db;