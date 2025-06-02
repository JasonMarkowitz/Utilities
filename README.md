# Utilities
General Utilties

## jiraopen.py
Designed to be used with Zabbix, Pagerduty, and Jira, opens a ticket in Jira based on who's on call based on zabbix alerts/actions. 

## prompt.txt

Bash Prompt I typically use

## webhook_gitpull/
Small python service meant to act as a post-commit endpoint that allows for auto-pushing of simple HTML/JS websites. Exposes a simple api endpoint ``https://<url>/webhook?dir=<dir>&key=<key>' -H X-PSK: <psk>``
Designed to be securely configured as a github post-commit hook and security is IP based off allowing only your git providers post-commit IPs. Use with caution. 
Get the hook ip range from ``https://api.github.com/meta``




