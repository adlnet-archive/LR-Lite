function(doc) {
	if(doc.node_timestamp && doc.doc_type === "resource_data"){
		var timestamp = Math.floor(Date.parse(doc.node_timestamp)/1000);
 		emit(timestamp, doc._id); 
 	}
}