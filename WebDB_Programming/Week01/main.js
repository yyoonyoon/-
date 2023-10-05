var http = require("http");
var app = http.createServer( function(req,res){
    //여기에 클라이언트의 요청을 받아서 URL을 분류하고 그에 따른 controller에 해당하는 로직을 작성.
    //req,res에 따른 리턴을 할 callback function 함수를 여기에 적음.
    res.writeHead(200);
    res.end("Hello. My first response, Node.js!");
});
app.listen(3000); //3000 == port num