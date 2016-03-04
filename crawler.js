var request = require('request');
var cheerio = require('cheerio');
var URL = require('url-parse');
var fs = require('fs');

var pageToVisit = "https://ugradcalendar.uwaterloo.ca/page/ENG-Computer-Engineering-Electrical-Engineering";
console.log("Visiting page " + pageToVisit);
request(pageToVisit, function(error, response, body) {
   if(error) {
     console.log("Error: " + error);
   }
   // Check status code (200 is HTTP OK)
   console.log("Status code: " + response.statusCode);
   if(response.statusCode === 200) {
     // Parse the document body
     var $ = cheerio.load(body);
     $('td:has(a)').each(function(index) {
     	var courseName = $(this).text().trim();
    	var link = $(this).attr('href');
    	fs.appendFileSync('ECE.txt', courseName + ' ' + link + '\n');
     });
   }
});

var bioEngPage = "https://ugradcalendar.uwaterloo.ca/page/ENG-Biomedical-Engineering";
console.log("Visting page" + bioEngPage);
request(bioEngPage, function(error, response, body) {
	if(error) {
     console.log("Error: " + error);
   	}
   	// Check status code (200 is HTTP OK)
   	console.log("Status code: " + response.statusCode);
   	if(response.statusCode === 200) {
	    // Parse the document body
	    var $ = cheerio.load(body);
	    $('tr').each(function(index) {
	     	var courseName = $(this).text().trim();
	    	var link = $(this).attr('href');
	    	fs.appendFileSync('BioEng.txt', courseName + ' ' + link + '\n');
	    });
   	}
});