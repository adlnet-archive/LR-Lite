function(head, req) {
  var row;
  var ids = [];
  while (row = getRow()){
  	ids.push(row.value);
  }
  return JSON.stringify({response: ids});  
}