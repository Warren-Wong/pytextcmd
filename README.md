# pytextcmd
A tool, detecting user's keyboard typing, recognizes command then return response by simulating user keyboard typing in the same place. Support MacOS Only.

## Dependence
pynput

## How to use
Run textcmd.py with python3 <br/>
First select a command handler. <br/>
For example, type <br/>
    `` `tpy` `` <br/>
A handler change message will be typed. <br/>
Then type <br/>
    `` `for i from 1 to 10` `` <br/>
The command handler will return a for loop in python like: <br/>
    `for i in range(1, 10):` <br/>
