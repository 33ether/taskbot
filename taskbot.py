import re
import time
from datetime import datetime, timezone

import file_manager

class TaskBot:
    def __init__(self,irc,parent_dir,tasks_dir,tasks_global_dir,info_dir,levels,roles):
        """ Initialize with parent, tasks, globals tasks, info directories and levels, roles """
        self.irc = irc
        self.parent_dir = parent_dir
        self.tasks_dir = tasks_dir
        self.tasks_global_dir = tasks_global_dir
        self.info_dir = info_dir
        self.levels = levels
        self.roles = roles

        self.fm = file_manager.FileManager(parent_dir)
        self.fm.ensure_dir(tasks_dir)
        self.fm.ensure_dir(tasks_global_dir)
        self.fm.ensure_dir(info_dir)


    def help_msg(self,channel):
        """ help message for usage """
        self.irc.send(channel,"https://raw.githubusercontent.com/33ether/taskbot/refs/heads/main/README.md")

    def add_task(self,args,nick):
        """ Add individual tasks """
        self.fm.add_file(args,self.tasks_dir,nick)

    def add_all(self,args):
        self.fm.add_file(args,self.tasks_global_dir)

    def list_tasks(self,channel,args,nick):
        """ List individual tasks """
        if len(args) > 0:
            nick = args.split(' ')[0]
        files = self.fm.list_files(self.tasks_dir,nick)
        i = 1
        for file in files:
            content = self.fm.read_file(file,self.tasks_dir,nick)
            if content:
                self.irc.send(channel,f"{i}. {content}")
            i+=1

    def list_tasks_all(self,channel):
        """ List Global Tasks """
        file_list = self.fm.list_files(self.tasks_global_dir)
        i=1
        for file in file_list:
            content = self.fm.read_file(file,self.tasks_global_dir) 
            if content:
                self.irc.send(channel,f"{i}. {content}")
            i+=1
                    

    def del_task(self,num,nick):
        """ Delete individual tasks """
        files = self.fm.list_files(self.tasks_dir,nick)
        if num-1 < len(files) and num > 0 and len(files) > 0:
            self.fm.del_file(files[num-1],self.tasks_dir,nick)

    def del_all(self,num):
        """ Delete global tasks """
        file_list = self.fm.list_files(self.tasks_global_dir)
        if num-1 < len(file_list) and num > 0 and len(file_list) > 0:
            self.fm.del_file(file_list[num-1],self.tasks_global_dir)

    def show_levels(self,channel): 
        """ list the levels """
        i=1
        for level in self.levels:
            self.irc.send(channel,f"{i}. {level}")
            i+=1

    def show_roles(self,channel):
        """ List the roles """
        i=1
        for role in self.roles:
            self.irc.send(channel,f"{i}. {role}")
            i+=1

    def register(self,nick,args):
        """ Register a nick with level number,role number and optional info """
        level_num = int(args.split(' ')[0])
        role_num = int(args.split(' ')[1])
        info = ""
        if len(args.split(' ')) > 2:
            info = ' '.join(args.split(' ')[2:]).strip()
        if level_num > 0 and level_num <= len(self.levels) and role_num > 0 and role_num <= len(self.roles):
            self.fm.add_file(f"[Level: {self.levels[level_num-1]}] [Role: {self.roles[role_num-1]}] [{info}]",self.info_dir,nick)

    def info(self,args,channel,nick):
        """ Show registered info of a nick """
        if len(args) > 0:
            nick = args.split(' ')[0]
        nick_files = self.fm.list_files(self.info_dir,nick)
        i=1
        for file in nick_files:
            content = self.fm.read_file(file,self.info_dir,nick)
            if content:
                self.irc.send(channel,f"{i}. [Nick: {nick}] {content}")
            i+=1

    def del_info(self,nick,num):
        """ Delete info if registered """
        files = self.fm.list_files(self.info_dir,nick)
        if num-1 < len(files) and num > 0 and len(files) > 0:
            self.fm.del_file(files[num-1],self.info_dir,nick)

    def match(self,channel,args,nick): 
        """ Match peers based on level and role number supplied as arguments -l <num1> and -r <num2> """
        # Regex to match arguments <num1> and <num2> by groups
        regex = r'(?:-l\s+(\d+))?(?:\s*-r\s+(\d+))?$'
        regex_match = re.match(regex,args)
        level,role = (None,None)
        nick_set = set()
        if regex_match:
            if (regex_match.group(1)):
                level = int(regex_match.group(1)) - 1
                level = level if 0 <= level < len(self.levels) else None
            if (regex_match.group(2)):
                role = int(regex_match.group(2)) - 1
                role = role if 0 <= role < len(self.roles) else None
                    
        # Regex to match the level and role in each nick files inside info_dir
        regex2 = r'\[Level:\s+([a-zA-Z]+)\]\s+\[Role:\s+([a-zA-Z]+)\].*$'

        if level is not None or role is not None:
            info_folder_list = self.fm.list_files(self.info_dir)
            for nick_folder in info_folder_list:
                nick_folder_files = self.fm.list_files(self.info_dir,nick_folder)
                for file in nick_folder_files:
                    content = self.fm.read_file(file,self.info_dir,nick_folder)
                    if content:
                       regex2_match = re.match(regex2,content)
                       read_level = regex2_match.group(1)
                       read_role = regex2_match.group(2)
                       if level is not None and role is not None:
                           if self.levels[level] == read_level and self.roles[role] == read_role:
                               nick_set.add(nick_folder)
                       elif level is not None:
                           if self.levels[level] == read_level:
                               nick_set.add(nick_folder)
                       elif role is not None:
                           if self.roles[role] == read_role:
                               nick_set.add(nick_folder)

        if len(nick_set):
            self.irc.send(channel,' '.join(nick_set))


    def peers(self,channel):
        """ Show the peers """
        registered_peer_set = set()
        registered_peers = self.fm.list_files(self.info_dir)
        for peer in registered_peers:
            registered_peer_set.add(peer)
        task_peer_set = set()
        tasks_peer_list = self.fm.list_files(self.tasks_dir)
        for peer in tasks_peer_list:
            task_peer_set.add(peer)
        
        if len(registered_peer_set) or len(task_peer_set):
            self.irc.send(channel,f'{' '.join(registered_peer_set | task_peer_set)}')
        if len(task_peer_set):
            self.irc.send(channel,f"With Tasks [{' '.join(task_peer_set)}]")
        if len(registered_peer_set):
            self.irc.send(channel,f"Registered [{' '.join(registered_peer_set)}]")


        
    def poast_task_to_channels(self,hour,minute):
        """ Post global tasks in channel in channels at target hour and target minute """
        target_hour = hour
        target_minute = minute
        poasted = { channel: False for channel in self.irc.channels }
        while True:
            now = datetime.now(timezone.utc)
            if now.hour == target_hour and now.minute == target_minute:
                file_list = self.fm.list_files(self.tasks_global_dir)
                if len(file_list):
                    for channel in self.irc.channels:
                        if not poasted[channel]:
                            self.irc.send(channel,"Global tasks for all this week:")
                            self.list_tasks_all(channel)
                            poasted[channel] = True
            else:
                poasted = { channel: False for channel in poasted }
            time.sleep(1)

