# Taskbot to manage tasks for #hackers in darkirc

Change server address and port in taskbot.py if not using defaults

# Usage:

## For managing individual tasks:

!add <some_task>                                            to add some task for yourself
!tasks <optional nick>                                      to list tasks of nick or your tasks if nick not supplied
!del <number>                                               to delete a task by number

## For managing tasks that are for everybody/globally:

!add_all <some_task>                                        to add some task
!tasks_all                                                  to list the tasks 
!del_all <number>                                           to delete some task by number

## Levels and Roles

!levels                                                     list available levels ["novice", "basics", "skilled", "master"]
!roles                                                      list available roles  ["student", "collaborator", "teacher"]
!register   <level_number> <role_number> <optional info>    register info about yourself
!info   <optional nick>                                     to list registered info about nick or yourself if nick not supplied
!del_info   <number>                                        delete registered info of your nick by number

## Matching peers by common info data

!match -l <optional num> -r <optional num>                  Match peers by -l level number and -r role number
!peers                                                      List all peers and registered peers
