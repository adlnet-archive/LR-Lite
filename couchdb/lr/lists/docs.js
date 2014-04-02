function(head, req) {
  var row;
  var docs = [];
  while (row = getRow()){
  	docs.push(row.doc);
  }
  return JSON.stringify({response: docs});  
}