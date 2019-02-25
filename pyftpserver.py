from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import argparse
import os
import pwd
import string
from pathlib import Path
import random

parser = argparse.ArgumentParser(description="An ftp based file sharing tool")
parser.add_argument("-P", "--port", type=int, help="Specify Port")
parser.add_argument("-a", "--anon", help="Allow Anonymous" action="store_true")
parser.add_argument("-u", "--username", help="Specify Username")
parser.add_argument("-p", "--password", help="Specify Password")
parser.add_argument("-r", "--read", help="Read files", action="store_true")
parser.add_argument("-w", "--write", help="Edit files", action="store_true")
parser.add_argument("-d", "--delete", help="Delete files", action="store_true")
parser.add_argument("-c", "--create", help="Create folder",
                    action="store_true")
parser.add_argument(
    "-g", "--get", help="Get files and folders", action="store_true")
parser.add_argument("-H", "--host", help="Host ip")
parser.add_argument("-f", "--files", help="Files to share")
parser.parse_args()
args = parser.parse_args()


# Use the path provided else share the public folder
myfiles = args.files if args.files else str(Path.home())+"/Public/"

# Host will be set to localhost/127.0.0.1 if not provided
address = args.host if args.host else "127.0.0.1"

if not args.anon:
    username = args.username if args.username else pwd.getpwuid(
        os.getuid())[0]  # Create an ftp user with current username

    password = args.password if args.password else ''.join(
        random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=5))  # Generate a password if not provided

port = args.port if args.port else 1026  # If no port specified use port  21

userpermmision = ("el" if args.read else "") + \
    ("a" if args.write else "") + \
    ("r" if args.get else "") + \
    ("d" if args.delete else "") + \
    ("m" if args.create else "")  # Set user permission
if userpermmision == "":
    userpermmision = "r"

if input("Start server to share "+myfiles+" on "+address+" with port " + str(port)+"(y/n)?").upper() == ("Y"):

    authorizer = DummyAuthorizer()
    if args.anon == True:
        print("Anonymous user created")
        authorizer.add_anonymous(myfiles, perm=userpermmision)
    else:
        print("Username for ftp : "+username+"\nPassword : "+password)
        authorizer.add_user(
            username, password, myfiles, perm=userpermmision, msg_login="Login successful for "+username+".", msg_quit="Goodbye."+username+".")

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "I hope I asked you to open this. /n Tony "

    server = FTPServer((address, port), handler)
    server.max_cons = 256
    server.max_cons_per_ip = 5
    server.serve_forever()
