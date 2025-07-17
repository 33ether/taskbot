import irc
import signal
import os
import threading
import re
import time
from datetime import datetime, timezone
import file_manager

fm = file_manager.FileManager('storage') ##the parent dir inside which all data is stored
tasks_dir = 'tasks'  ##individual tasks are stored inside this dir in respective nick named dirs
tasks_global_dir = 'tasks_all' ##global tasks are stored inside this dir
info_dir = 'registers' ##nick info are stored here inside respective nick named dirs
     

server = "127.0.0.1"
port = 6667
channels = ["#hackers"]
nick = "bot"
ircc = irc.IRC()

levels = ["novice", "basics", "skilled", "master"]
roles = ["student", "collaborator", "teacher"]

ircc.connect(server,port,channels,nick)

def signal_handler(sig,frame):
    print("Caught termination signal, cleaning up and exiting...")
    ircc.disconnect(server,port)
    print("Shut down successfully")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)


def help_msg(channel):
    ircc.send(channel,"https://raw.githubusercontent.com/33ether/taskbot/refs/heads/main/README.md")

def add_task(args,nick):  ##Add individual task
    fm.add_file(args,tasks_dir,nick)

def add_all(args):    ##Add Global task
    fm.add_file(args,tasks_global_dir)

def list_tasks(channel,args,nick):  ##List individual task by nick
    if len(args) > 0:
        nick = args.split(' ')[0]
    files = fm.list_files(tasks_dir,nick)
    i = 1
    for file in files:
        content = fm.read_file(file,tasks_dir,nick)
        if content:
            ircc.send(channel,f"{i}. {content}")
        i+=1

def list_tasks_all(channel): ##List Global tasks
    file_list = fm.list_files(tasks_global_dir)
    i=1
    for file in file_list:
        content = fm.read_file(file,tasks_global_dir) 
        if content:
            ircc.send(channel,f"{i}. {content}")
        i+=1
                

def del_task(num,nick):  ##Delete an individual task by number
    files = fm.list_files(tasks_dir,nick)
    if num-1 < len(files) and num > 0 and len(files) > 0:
        fm.del_file(files[num-1],tasks_dir,nick)

def del_all(num):   ##Delete global tasks
    file_list = fm.list_files(tasks_global_dir)
    if num-1 < len(file_list) and num > 0 and len(file_list) > 0:
        fm.del_file(file_list[num-1],tasks_global_dir)

def show_levels(channel): 
    i=1
    for level in levels:
        ircc.send(channel,f"{i}. {level}")
        i+=1

def show_roles(channel):
    i=1
    for role in roles:
        ircc.send(channel,f"{i}. {role}")
        i+=1

def register(nick,args):    ##register info by an individual on their own about levels, roles and others
    level_num = int(args.split(' ')[0])
    role_num = int(args.split(' ')[1])
    info = ""
    if len(args.split(' ')) > 2:
        info = ' '.join(args.split(' ')[2:]).strip()
        #print(info)
    if level_num > 0 and level_num <= len(levels) and role_num > 0 and role_num <= len(roles):
        fm.add_file(f"[Level: {levels[level_num-1]}] [Role: {roles[role_num-1]}] [{info}]",info_dir,nick)

def info(args,channel,nick):  ##show registered info of a nick or own
    if len(args) > 0:
        nick = args.split(' ')[0]
    nick_files = fm.list_files(info_dir,nick)
    i=1
    for file in nick_files:
        content = fm.read_file(file,info_dir,nick)
        if content:
            ircc.send(channel,f"{i}. [Nick: {nick}] {content}")
        i+=1

def del_info(nick,num):  ## Delete registered info by an individual on their own by info number
    files = fm.list_files(info_dir,nick)
    if num-1 < len(files) and num > 0 and len(files) > 0:
        fm.del_file(files[num-1],info_dir,nick)

def match(nick,args):  ## Match peers based on level and role number supplied as arguments -l <num> and -r <num>
    regex = r'(?:-l\s+(\d+))?(?:\s*-r\s+(\d+))?$'  
    regex_match = re.match(regex,args)
    regex2 = r'\[Level:\s+([a-zA-Z]+)\]\s+\[Role:\s+([a-zA-Z]+)\].*$'

    nick_set = set()
    if regex_match:
        #print(regex_match.group(1),regex_match.group(2))
        if (regex_match.group(1)):
            level = int(regex_match.group(1))
            #print(level)
            if level <= len(levels) and level > 0:
                level-=1
            else:
                level = None
        else:
            level = None
        if (regex_match.group(2)):
            role = int(regex_match.group(2))
            #print(role)
            if role <= len(roles) and role > 0:
                role-=1
            else:
                role = None
        else:
            role = None
        #print(level,role)
        
        if level or role:
            info_folder_list = fm.list_files(info_dir)
            for nick_folder in info_folder_list:
                nick_folder_files = fm.list_files(info_dir,nick_folder)
                for file in nick_folder_files:
                    content = fm.read_file(file,info_dir,nick_folder)
                    if content:
                       regex2_match = re.match(regex2,content)
                       read_level = regex2_match.group(1)
                       read_role = regex2_match.group(2)
                       if level and role:
                           if levels[level] == read_level and roles[role] == read_role:
                               nick_set.add(nick_folder)
                       elif level:
                           if levels[level] == read_level:
                               nick_set.add(nick_folder)
                       elif role:
                           if roles[role] == read_role:
                               nick_set.add(nick_folder)

            #print(nick_set)            
            ircc.send(channel,' '.join(nick_set))

def peers(channel):
    registered_peer_set = set()
    registered_peers = fm.list_files(info_dir)
    for peer in registered_peers:
        registered_peer_set.add(peer)
    task_peer_set = set()
    tasks_peer_list = fm.list_files(tasks_dir)
    for peer in tasks_peer_list:
        task_peer_set.add(peer)

    ircc.send(channel,f'{' '.join(registered_peer_set | task_peer_set)}')
    ircc.send(channel,f"With Tasks [{' '.join(task_peer_set)}]")
    ircc.send(channel,f"Registered [{' '.join(registered_peer_set)}]")


    
## List the tasks at UTC 00:10 in the channels in channels
def poast_task_to_channels():
    target_hour = 0
    target_minute = 10
    poasted = False
    while True:
        now = datetime.now(timezone.utc)
        if now.hour == target_hour and now.minute == target_minute:
            if not poasted:
                for channel in channels:
                    ircc.send(channel,"Global tasks for all this week:")
                    list_tasks_all(channel)
                    poasted = True
        else:
            poasted = False
        time.sleep(1)

poast_task_thread = threading.Thread(target=poast_task_to_channels)
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
            #print(nick)
            channel = text_list[2]
            if channel in channels:
                msg = ' '.join(text_list[3:])
                msg = msg[1:].strip()
                msg = msg.split(' ')
                
                command = msg[0]
                args = ' '.join(msg[1:]).strip()

                if command.lower() == "!help" and len(args) == 0:
                    help_msg(channel)
                elif command.lower() == "!add_all" and len(args) >0:
                    add_all(args)
                elif command.lower() == "!tasks_all":
                    list_tasks_all(channel)
                elif command.lower() == "!del_all" and len(args) >0 and args.isdigit():
                    del_all(int(args))
                elif command.lower() == "!add" and len(args) > 0:
                    add_task(args,nick)
                elif command.lower() == "!tasks":
                    list_tasks(channel,args,nick) 
                elif command.lower() == "!del" and len(args) > 0 and args.isdigit():
                    del_task(int(args),nick)
                elif command.lower() == "!levels" and len(args) == 0:
                    show_levels(channel)
                elif command.lower() == "!roles" and len(args) == 0:
                    show_roles(channel)
                elif command.lower() == "!register" and len(args.split(' ')) >= 2 and args.split(' ')[0].isdigit() and args.split(' ')[1].isdigit():
                    register(nick,args)
                elif command.lower() == "!info":
                    info(args,channel,nick)
                elif command.lower() == "!del_info" and len(args) > 0 and args.isdigit():
                    del_info(nick,int(args))
                elif command.lower() == "!match":
                    match(nick,args)
                elif command.lower() == "!peers":
                    peers(channel)
                else:
                    pass

                
