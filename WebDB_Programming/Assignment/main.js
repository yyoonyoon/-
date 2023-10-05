//201935291 염상윤

const express = require("express");
const app = express();
const port = 3000;

app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');

var db = require('./lib/db');
var author = require('./lib/author');

// "localhost:3000"으로 접속 했을 때 결과 화면 리턴
app.get('/', (req, res) => {
  var context = {title: "Welcome", list:""};
  res.render("home", context, (err, html) => {
    res.end(html);
  });
});

// "localhost:3000/author"로 접속했을 때 결과 화면 반환
app.get('/author', (req, res) => {
  author.home(req,res);
  // res.send('<h1>결과 화면</h1><p>이곳에 결과 내용이 표시됩니다.</p>');
});

app.get('/favicon.ico',(req, res)=>res.writeHead(404));

// 서버 시작
app.listen(port, () => {
  console.log(`서버가 실행 중입니다.`);
});