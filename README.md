# pytextcmd
A tool, detecting user's keyboard typing, recognizes command then return response by simulating user keyboard typing in the same place. Support MacOS Only.

##Dependence:
pynput

##How to use:
Run textcmd.py with python3
First select a command handler.
For example, type
    `tpy`
A handler change message will be typed.
Then type
    `for i from 1 to 10`
The command handler will return a for loop in python like:
    for i in range(1, 10):
