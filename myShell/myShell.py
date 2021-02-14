#! /usr/bin/env python3

import os, sys, re

def execute(args):
    #if empty then return
    if len(args) == 0:
        return

    #exit command
    elif args[0].lower() == "exit":
        sys.exit(0)

    #cd changing directory command
    elif args[0].lower() == "cd":
        try:
            #cd ..
            if len(args) == 1:
                os.chdir("..")
            else: #other directory
                os.chdir(args[1])
        except: #file directory does
            pass
    else:
        rc = os.fork()

        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rx).encode())
            sys.exit(1)
        elif rc == 0:
            #trying each directory in path
            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program, args, os.environ) #trying to execute
                except FileNotFoundError:
                    pass

            #could not execute
            os.write(2, ("Could not execute %s\n" %args[0]).encode())
            sys.exit(1) #terminate with error

        else:
            os.wait()
 
#main shell
while True:
    if 'PS1' in os.environ:
        os.write(1, (os.environ['PS1']).encode())
    else:
        os.write(1, ("$ ").encode())
    args = os.read(0, 1000) #this reads 1000 bytes of input fd
    #No input
    if len(args) == 0:
        break
    args = args.decode().splitlines()
    #splits input into diferent tokens
    for token in args:  
        execute(token.split())
