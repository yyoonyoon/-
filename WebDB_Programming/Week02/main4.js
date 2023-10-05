const express = require("express");
const app = express(); //express함수실행

app.set("views", __dirname + "/views"); //ejs파일들을 이 폴더에 저장하겠음
app.set("view engine", "ejs"); //ejs를 사용하겠음

var db = require('./lib/db');

db.connect();

app.get("/", (req, res) => {
    db.query('SELECT * FROM topic', (error,results)=>{
        var lists = '<ol> type="1">';
        var i = 0;
        while(i<results.length){
            lists = lists + `<li><a href="#">${results[i].id}${results[i].title}</a></li>`; 
            i=i+1;    
        }
        lists = lists + '<ol>'
        var context= {list:results,
                    title:'Welcome'};
        console.log(context)
        res.render('home',context, (err,html)=>{
            res.end(html) })
    });
    db.end();
});

app.get("/:id", (req, res) => {
  var id = req.params.id;
  var context = { title: id};
  res.render("home", context, (err, html) => {
    res.end(html);
  });
});
app.get("/favicon.ico", (req, res) => res.writeHead(404));
app.listen(3000, () => console.log("Example app listening on port 3000"));