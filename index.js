const csvParser = require("csv-parser");
var port = 4444;
var serverUrl = "127.0.0.1";

var http = require("http");
var path = require("path");
var fs = require("fs");


function readCSV(file) {
    let csvData = [];
    fs.createReadStream(file)
        .pipe(csvParser())
        .on('data', function (row) {
            csvData.push(row);
        }).on('end', function () {
        console.log('CSV file successfully processed')
    });
    return csvData;
}


console.log("Starting web server at " + serverUrl + ":" + port);

http.createServer( function(req, res) {
    var filename = "index.html";
    fs.readFile(filename, 'utf-8', function (err, content) {
        if (err) {
            console.log("File not found or read error: " + filename);
            res.writeHead(404);
            res.end();
            return;
        }
        console.log("Serving file: " + filename);
        res.writeHead(200, {'Content-Type': 'text/html'});
        res.end(content, 'utf-8');
    });
}).listen(4444, '127.0.0.1')




//geodata.forEach(row => {
//  console.log(`City: ${row['city']}, State: ${row['state']}, Country: ${row['country']}`);
//});