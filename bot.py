import irc
import signal
import threading
from taskbot_cfg import config
import taskbot

# Directory inside where everything is stored
parent_dir = config["parent_dir"]
# Directory for storing individual tasks
tasks_dir = config["tasks_dir"]
# Directory for storing global tasks
tasks_global_dir = config["tasks_global_dir"]
# Directory for storing registered information
info_dir = config["info_dir"]
# Levels 
levels = config["levels"]
# Roles
roles = config["roles"]

# IRC server, port, channels[],nick 
server = config["server"]
port = config["port"]
channels = config["channels"]
nick = config["nick"]

# Initialize IRC with server,port,channels,nick
ircc = irc.IRC()
ircc.connect(server,port,channels,nick)

# Initialize TaskBot with irc, parent, tasks, tasks global, info directories and levels, roles
tb = taskbot.TaskBot(ircc,parent_dir,tasks_dir,tasks_global_dir,info_dir,levels,roles)

def signal_handler(sig,frame):
    print("Caught termination signal, cleaning up and exiting...")
    ircc.disconnect(server,port)
    print("Shut down successfully")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Make a separate thread for posting to channles at UTC Hour,Minute passed as arguments to poast_task_to_channels method from TaskBot
poast_task_thread = threading.Thread(target=tb.poast_task_to_channels,args=(6,24))
poast_task_thread.start()

while True:
    response = ircc.get_response()
    if response is not None:
        text = response.strip()
        text_list = text.split(' ')
        if len(text_list) > 3:
            nick = text_list[0]
            nick = nick[1:].strip()
            nick = nick[:-14]
            channel = text_list[2]
            if channel in channels:
                msg = ' '.join(text_list[3:])
                msg = msg[1:].strip()
                msg = msg.split(' ')
                
                command = msg[0]
                args = ' '.join(msg[1:]).strip()

                if command.lower() == "!help" and len(args) == 0:
                    tb.help_msg(channel)
                elif command.lower() == "!add_all" and len(args) >0:
                    tb.add_all(args)
                elif command.lower() == "!tasks_all":
                    tb.list_tasks_all(channel)
                elif command.lower() == "!del_all" and len(args) >0 and args.isdigit():
                    tb.del_all(int(args))
                elif command.lower() == "!add" and len(args) > 0:
                    tb.add_task(args,nick)
                elif command.lower() == "!tasks":
                    tb.list_tasks(channel,args,nick) 
                elif command.lower() == "!del" and len(args) > 0 and args.isdigit():
                    tb.del_task(int(args),nick)
                elif command.lower() == "!levels" and len(args) == 0:
                    tb.show_levels(channel)
                elif command.lower() == "!roles" and len(args) == 0:
                    tb.show_roles(channel)
                elif command.lower() == "!register" and len(args.split(' ')) >= 2 and args.split(' ')[0].isdigit() and args.split(' ')[1].isdigit():
                    tb.register(nick,args)
                elif command.lower() == "!info":
                    tb.info(args,channel,nick)
                elif command.lower() == "!del_info" and len(args) > 0 and args.isdigit():
                    tb.del_info(nick,int(args))
                elif command.lower() == "!match":
                    tb.match(channel,args,nick)
                elif command.lower() == "!peers":
                    tb.peers(channel)

                
