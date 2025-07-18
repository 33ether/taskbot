# Taskbot for #hackers in darkirc

[Link https://github.com/33ether/taskbot] https://github.com/33ether/taskbot
Taskbot is a bot designed to manage tasks and facilitate collaboration among users in the #hackers channel on darkirc. This README provides instructions for configuring and using the bot.

## Configuration

Modify taskbot_cfg.py to your liking.

## Running

Make sure that darkirc daemon is running at the correct `server` address and `port` specified in taskbot_cfg.py
The run `bot.py`

## Usage

Taskbot supports commands for managing individual tasks, global tasks, user levels, roles, and peer matching. All commands are prefixed with `!`.

### Managing Individual Tasks

- `!add <some_task>`  
  Add a task for yourself.  
  Example: `!add Submit a pr after finishing`

- `!tasks <optional nick>`  
  List tasks for a specified nick. If no nick is provided, lists your own tasks.  
  Example: `!tasks` or `!tasks anon`

- `!del <number>`  
  Delete a task by its number.  
  Example: `!del 1`

### Managing Global Tasks

- `!add_all <some_task>`  
  Add a task for everyone.  
  Example: `!add_all make an anon dapp`

- `!tasks_all`  
  List all global tasks.  
  Example: `!tasks_all`

- `!del_all <number>`  
  Delete a global task by its number.  
  Example: `!del_all 2`

### Levels and Roles

- `!levels`  
  List available levels: `["novice", "basics", "skilled", "master"]`.  
  Example: `!levels`

- `!roles`  
  List available roles: `["student", "collaborator", "teacher"]`.  
  Example: `!roles`

- `!register <level_number> <role_number> <optional info>`  
  Register information about yourself, including level number, role number, and optional additional info.  
  Example: `!register 2 1 Rust ninjs`

- `!info <optional nick>`  
  Display registered information for a specified nick. If no nick is provided, shows your own info.  
  Example: `!info` or `!info anon`

- `!del_info <number>`  
  Delete registered information for your nick by number.  
  Example: `!del_info 1`

### Matching Peers by Common Info

- `!match -l <optional num> -r <optional num>`  
  Match peers based on level number (`-l`) and/or role number (`-r`).  
  Example: `!match -l 2 -r 1` (matches users with level "basics" and role "collaborator")

- `!peers`  
  List all peers and their registered information.  
  Example: `!peers`


### How it Works
It creates files for each task under each separate directory for each nick. The file_manager.py module that i wrote help with this.
