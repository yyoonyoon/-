var http = require('http');
var fs = require('fs');
var urlm = require('url');
var app = http.createServer(function(req,res){
    
    var _url = req.url;
    var queryData = urlm.parse(_url, true).query; //자바스크립트에서 매서드 뒤에 . 붙으면 점 뒤에 있는 속성만 뽑는다는 의미. 검색 더 해보기
    var queryData = urlm.parse(_url, true).path;
    var queryData = urlm.parse(_url, true).pathname;
    console.log(_url);
    console.log(queryData.id);
    var title = queryData.id

    if (req.url == '/'){
        // _url = '/index.html'
        title = 'Welcome';
    }
    if (req.url == '/1'){
        _url = '/1.html'
    }
    if (req.url == '/2'){
        _url = '/2.html'
    }
    if (req.url == '/3'){
        _url = '/3.html'
    }
    if (req.url == '/favicon.ico'){
        return res.writeHead(404);
    }
    
    res.writeHead(200);
    var template = `<!doctype html>
    <html>
    <head>
      <title>WEB1 - ${title}</title>
      <meta charset="utf-8">
    </head>
    <body>
      <h1><a href="/">WEB</a></h1>
      <ol>
        <li><a href="/?id=Html">HTML</a></li>
        <li><a href="/?id=Css">CSS</a></li>
        <li><a href="/?id=JavaScript">JavaScript</a></li>
      </ol>
      <h2>${title}</h2>
      <p>The World Wide Web (abbreviated WWW or the Web) is an information space where documents and other web resources are identified by Uniform Resource Locators (URLs), interlinked by hypertext links, and can be accessed via the Internet.[1] English scientist Tim Berners-Lee invented the World Wide Web in 1989. He wrote the first web browser computer program in 1990 while employed at CERN in Switzerland.[2][3] The Web browser was released outside of CERN in 1991, first to other research institutions starting in January 1991 and to the general public on the Internet in August 1991.
      </p>
    </body>
    </html>
    `;
    // res.end(fs.readFileSync(__dirname + _url));
    res.end(template);
})
app.listen(3000);