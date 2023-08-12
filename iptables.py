import argparse
import re
import datetime
import os
import subprocess
import sys

LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

line_format = re.compile(r'(\S+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"')

def format_bytes(bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
def process_logs(log_path):
    if os.path.isfile(log_path):
        files = [log_path]
    else:
        print("Invalid log path")
        return

    ip_counts = {}
    
    for filename in files:
            open_fn = open

            with open_fn(filename, 'rt', encoding='utf-8') as file:
                for line in file:

                    match = line_format.match(line.strip())

                    if match:
                        ip, date_str, request, status, bytes_sent, referrer, user_agent = match.groups()
                        dt_log = datetime.datetime.strptime(date_str, '%d/%b/%Y:%H:%M:%S %z')
                        dt_now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3)
                        try:
                            method, url = request.split()[0], " ".join(request.split()[1:])
                        except IndexError:
                            method, url = request, ''

                        ip_counts[ip] = ip_counts.get(ip, 0) + 1

                        diff = dt_now - dt_log

    for ip, count in sorted(ip_counts.items(), key=lambda x: x[1], reverse=True):
        if datetime.timedelta(seconds=120).seconds > diff.seconds and count > 10:
           print("\033[1m\033[91mIP's for block:\033[0m")
           print(f"IP:{ip}, Age:{diff}, Count: {count}, Desired Delta:{datetime.timedelta(minutes=2)}")
           if os.geteuid() != 0:
              print("Insufficient permissions! Root required. Trying access via sudo.")
              subprocess.run(["sudo", "/usr/sbin/iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
              print("\033[1m\033[91mRules list:\033[0m")
              #print(subprocess.run(["sudo", "/usr/sbin/iptables", "-L", "-v", "-n"]))
        
        if datetime.timedelta(seconds=600).seconds < diff.seconds:
           print("\033[1m\033[91mIP's for unblock:\033[0m")     
           print(f"IP:{ip}, Age:{diff}, Count: {count}, Desired Delta:{datetime.timedelta(minutes=10)}")
           if os.geteuid() != 0:
              print("Insufficient permissions! Root required. Trying access via sudo.")
              subprocess.run(["sudo", "/usr/sbin/iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"])
              print("\033[1m\033[91mRules list:\033[0m")
              #print(subprocess.run(["sudo", "/usr/sbin/iptables", "-L", "-v", "-n"]))      

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process nginx log files.')
    parser.add_argument('--log_path', metavar='LOG_PATH', type=str,
                        help='Path to the log file or directory')
    args = parser.parse_args()
    process_logs(args.log_path)