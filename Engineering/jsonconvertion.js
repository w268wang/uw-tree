var fs = require('fs');


fs.readFile('/Users/calvinzhou/devel/uw-tree/engineering/BioEng.txt', 'utf8', function (err,data) {
  if (err) {
    return console.log(err);
  }
  var jsonObject = {};

  var str = data.toString();
  var strSplit = str.split("\n");
  var terms = 0;
  var course = [];
  var regex = /[0-9][A-Z]/gi;
  var regex2 = /[A-Z]/g;
  for (var i = 0; i < strSplit.length; i++) {
  	var line = strSplit[i].trim();
  	if (line.match(regex)) {
  		var dataObject = {};
  		course = [];
  		terms++;
  		dataObject.push({
  			"term": terms,
  			"courses": course
  		});
  		console.log(dataObject.toString());
  	} else if (line.match(regex2)) {
  		course.push(line);
  	}
  }
  fs.writeFile('BioEng.json', dataObj, function (err) {
	  if (err) return console.log(err);
	});

});


