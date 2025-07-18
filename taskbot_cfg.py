config = {
        # darkirc server host
        "server" : "127.0.0.1",

        # darkirc server port
        "port" : 6667,

        # nick
        "nick" : "bot",

        # channels to join
        "channels" : ["#hackers"],

        # levels
        "levels" : ["novice", "basics", "skilled", "master"],

        # roles
        "roles" : ["student", "collaborator", "teacher"],
        
        # parent directory 
        "parent_dir" : "storage",

        # directory for tasks
        "tasks_dir" : "tasks",

        # directory for global tasks
        "tasks_global_dir" : "tasks_all",

        # directory for registered info
        "info_dir" : "registers",

        # (Hour,Minute) in UTC at which to post Global tasks periodically. If empty () then no posting
        "posting_time" : (0,10),
        }
