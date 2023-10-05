const express = require("express");
const app = express(); //express함수실행

app.set("views", __dirname + "/views"); //ejs파일들을 이 폴더에 저장하겠음
app.set("view engine", "ejs"); //ejs를 사용하겠음


app.get("/", (req, res) => {
  var context = { title: "Welcome-1"};
  res.render("home", context, (err, html) => {
    res.end(html);
  });
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