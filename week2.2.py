# i have to make a login system store the password and user name securely and shows the logs of the user
import time
import hashlib as hb
from datetime import datetime
def hashpasword( password):
    return hashlib.sha256( password).hexidigest()
def get_current_time_stamp():
    return datetime.now() .strftime("%a, %d %b %Y %H:%M:%S +0000")
