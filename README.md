# IPTABLES

This code analyzes a web server (nginx) access log and automatically blocks or unblocks IP addresses based on their activity. Here's what it does:
- Processes the log file, extracting request details.
- Tracks IP addresses and counts the number of requests from each.
- Calculates the time difference between the current moment and the request timestamp in the log.
- Blocks an IP address (using iptables) if it has made more than 10 requests within the last 2 minutes.
- Unblocks an IP address if its activity is old (more than 10 minutes).
- Uses sudo, if the script is run without root privileges.

**This script helps automatically manage traffic, limiting suspicious activity and mitigating potential DDoS attacks.**
