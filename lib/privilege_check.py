import os, subprocess,sys

def privileged_or_exit():
    privileged = True
    if os.getuid() != 0:
        msg = "[sudo] password for %u:"
        try:
            privileged = subprocess.check_call("sudo -v -p '%s'" % msg, shell=True) == 0
        except subprocess.CalledProcessError as e:
            privileged = False
    
    if not privileged:
        print("you need to be privileged", file=sys.stderr)
        exit(1)
    
