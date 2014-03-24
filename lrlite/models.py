

def create_new_user(db, username, password):
    user_info = {
        "_id": "org.couchdb.user:" + username,
        "name": username,
        "type": "user",
        "roles": [],
        "password": password
    }
    result = db.save_doc(user_info)
    return result
