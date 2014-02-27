def includeme(config):
	config.add_route("api", "/lr")
	config.add_route('document', "/lr/:doc_id")
	pass