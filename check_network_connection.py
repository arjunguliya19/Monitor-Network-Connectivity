import socket
import time
import datetime
import os
import sys


# If enabled, the log file will be created in the current working folder.    
log_filename = "network_monitor.log"
FILE = os.path.join(os.getcwd(), log_filename)

# Send ping request on external IP address (Cloudflare) to check if network connectivity is on.
def send_ping_request(host="1.1.1.1", port=53, timeout=3):

# Input Parameters:
# host: (string) 1.1.1.1 (1dot1dot1dot1.cloudflare-dns.com)
# port: (integer) (53/tcp DNS Service)
# timeout: (float) timeout in seconds

# Returns:
# True (Boolean) if external IP address is reachable.
# False (Boolean) if external IP address is unreachable.

    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
    except OSError as error:
        return False
    else:
        s.close()
        return True

    
def write_permission_check():
    try:
        with open(FILE, "a") as file:
            pass
    except OSError as error:
        print("Log file creation failed")
        sys.exit()
    finally:
        pass

    
def cal_time(start, stop):

# Calculate duration between two times and return as HH:MM:SS

# Input Parameters:
#   start and stop times
#   both datetime objects created from datetime.datetime.now()

# Returns:
#   The duration (string) in the form HH:MM:SS
    
    time_difference = stop - start
    seconds = float(str(time_difference.total_seconds()))
    return str(datetime.timedelta(seconds=seconds)).split(".")[0]


def mon_net_con(ping_freq=1):
    
# Monitor network connection
    
    monitor_start_time = datetime.datetime.now()
    motd = "Network connection monitoring started at: " + str(monitor_start_time).split(".")[0] + " Sending ping request in " + str(ping_freq) + " seconds"
    print(motd)
     
    with open(FILE, "a") as file:
        file.write("\n")
        file.write(motd + "\n")

    while True:
        if send_ping_request():
            time.sleep(ping_freq)
        else:
            down_time = datetime.datetime.now()
            fail_msg = "Network Connection Unavailable at: " + str(down_time).split(".")[0]
            print(fail_msg)
            with open(FILE, "a") as file:
                file.write(fail_msg + "\n")

                # Check every 1 second to see if network connectivity is restored.
                i = 0
            while not send_ping_request():
                time.sleep(1)
                i += 1

                # For each minute of downtime, log it.
                # The one-minute logs are being used as a proxy to indicate whether the computer lost power,
                # or just the network connectivity was down.

                if i >= 60:
                    i = 0
                    now = datetime.datetime.now()
                    continous_message = "Network Unavailabilty Persistent at: " + str(now).split(".")[0]
                    print(continous_message)
                    with open(FILE, "a") as file:
                        file.write(continous_message + "\n")

            # Record observed time when network connection restored.
            up_time = datetime.datetime.now()
            uptime_message = "Network Connectivity Restored at: " + str(up_time).split(".")[0]

            # Calculate the total duration of the downtime.     
            down_time = cal_time(down_time, up_time)
            downtime_message = "Network Connection was Unavailable for " + down_time

            # Display restoration message to console and record in log file.     
            print(uptime_message)
            print(downtime_message)
     
            with open(FILE, "a") as file:
                file.write(uptime_message + "\n")
                file.write(downtime_message + "\n")
mon_net_con()
