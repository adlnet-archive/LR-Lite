from gnupg import GPG
import requests
from multiprocessing import Process
import random
def generate_entropy(): 
    while True:
        with open("/dev/null", "wb") as f:
            f.write(str(random.random()))
def _generate_key(username):
    gpg = GPG()
    key_input = gpg.gen_key_input(key_type="RSA", key_length=1024, name_email=username+"@node.org", name_real=username)

    entropy_thread = Process(target=generate_entropy)
    entropy_thread.start()
    key = gpg.gen_key(key_input)
    entropy_thread.terminate()
    keys = gpg.list_keys(True)
    for k in keys:
        if k.get("fingerprint") == key.fingerprint:
            return k['keyid']

def create_new_user(db, username, password):
    user_info = {
        "_id": "org.couchdb.user:" + username,
        "name": username,
        "type": "user",
        "roles": [],
        "password": password,
        "keyid": _generate_key(username)
    }
    result = db.save_doc(user_info)    
    return result

def get_user(db, username, cookie):
    user = requests.get(db.uri + '/org.couchdb.user:' + username, headers={"set-cookie": cookie}).json()
    return user
