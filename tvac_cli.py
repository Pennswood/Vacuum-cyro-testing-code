import struct
import pathlib
import readline
from argparse import ArgumentParser
# import Adafruit_BBIO.GPIO as GPIO

COMMAND_LIST = ["CLOCK_SYNC", "TEMP_LIST", "TLC_PING", "PI_TUNE", "PID_TUNE", "STATUS_REQUEST", "LOG_DUMP", "SHUTDOWN"]

running = True
BBB_RX_LINE = 21
BBB_TX_LINE = 22



# Make the BeagleBone time = the time imputted (time will be an integer, epoch time).
def clock_sync(time):
    pass

# Print the current 9 thermistor reading in a grid of 3 by 3.
def temp_list():
    pass

# The TLC actually doesn't have a PING code. All this is going to do is return 1 if the TLC is throwing data at us
# And return 0 if the TLC is not throwing data at us.
def tlc_ping():
    pass

def pi_tune(p = None,i = None):
    pass

def pid_tune(p = None,i = None,d = None):
    pass

# Prints current time, duty cycle, temperature list, and PID constants. Create a file and save this information.
def status_request():
    pass

def log_dump():
    pass

def give_help():
    """Outputs a list of commands to the user for use in interactive mode."""
    print("\nInteractive Mode Commands")
    print("\thelp\t\t\t\tDisplay this help message.")
    print("\texit OR quit\t\t\tExit the program.")
    print("\tCLOCK_SYNC [TIME]\t\t\tSets the time with the epoch time provided.")
    print("\tTEMP_LIST\t\tDisplays the nine thermistor readings.")
    print("\tTLC_PING\t\tPings the thermal logic controller for 10 seconds or until response received.")
    print("\tPI_TUNE ?[P I]\t\tSets the thermal logic controller constants to input provided, or based on recent feedback if none provided. Sets derivativ constant as 0.")
    print("\tPID_TUNE ?[P I D]\t\tSets the thermal logic controller constants to input provided, or based on recent feedback if none provided.")
    print("\tSTATUS_REQUEST\t\tDisplays the status of the thermistor duty cycles, PID constants, temperatures, and more.")
    print("\tLOG_DUMP\t\tCompresses and transfers data to host computer.")

# Taken from: https://stackoverflow.com/questions/5637124/tab-completion-in-pythons-raw-input
def tab_completer(text, state):
    for cmd in COMMAND_LIST:
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1

def command_loop():
    global running
    while running:
        c = input("?").strip()  # Get a command from the user and remove any extra whitespace
        parts = c.split()  # split the command up into the command and any arguments
        if parts[0] == "help":  # check to see what command we were given
            give_help()
        elif parts[0] == "CLOCK_SYNC":
            clock_sync(parts[1])
        elif parts[0] == "TEMP_LIST":
            temp_list()
        elif parts[0] == "TLC_PING":
            tlc_ping()
        elif parts[0] == "PI_TUNE":
            if len(parts) == 1:
                pi_tune()
            elif len(parts) == 3:
                pi_tune(parts[1],parts[2])
            elif len(parts) == 4:
                print("Please use PID_Tune instead.")
            else:
                print("Invalid number of commands.")
        elif parts[0] == "PID_TUNE":
            if len(parts) == 1:
                pid_tune()
            elif len(parts) == 4:
                pid_tune(parts[1], parts[2],parts[3])
            elif len(parts) == 3:
                print("Please use PID_Tune instead.")
            else:
                print("Invalid number of commands.")
        elif parts[0] == "STATUS_REQUEST":
            status_request()
        elif parts[0] == "LOG_DUMP":
            log_dump()


def main():
    parser = ArgumentParser(
        description="CLI for performing vaccuum test.",
        epilog="Created for the 2020 NASA BIG Idea challenge, Penn State Oasis team. Questions: tylersengia@gmail.com",
        prog="libs_cli.py")

    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.add_argument("--spec-dev", "-s",
                        help="Specify the USB device for the spectrometer. Default is autodetected by seabreeze.",
                        nargs=1, default=None)
    parser.add_argument("--laser-dev", "-l", help="Specify the USB device for the laser.", nargs=1,
                        default=None)
    parser.add_argument("--config", "-c", help="Read test configuration from the specified JSON file.",
                        nargs=1, default=None)
    parser.add_argument("--no-interact", "-n",
                        help="Do not run in interactive mode. Usually used when a pre-written test configuration file is being used.",
                        dest="interactive", action="store_false", default=True)
    a = parser.parse_args()

    if a.interactive:
        readline.parse_and_bind("tab: complete")
        readline.set_completer(tab_completer)
        command_loop()

main()