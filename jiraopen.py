import sys
import os
import re
import requests
import json
import argparse
from sys import argv

parser = argparse.ArgumentParser(description='open jira ticket and assign it to the current sysops oncall')
parser.add_argument("-t", dest='tixtitle', type=str, default="none", action='store', 
                  help="Server to test against", metavar="DESCRIPTION")
parser.add_argument("-d", dest='descr', type=str, default="none", action='store',
                  help="ticket body", metavar="DESCRIPTION")
args = parser.parse_args()

pagerduty_token = ""
jira_user = 'zabbixapi'
jira_pass = ''

def pull_oncall_user():
 global pagerduty_token
 global level1useremail
 pagerduty_url = "https://org.pagerduty.com/api/v1/escalation_policies/on_call"
 pagerduty_headers = {
 "Content-type":'application/json',
 "Authorization": "Token token=" + pagerduty_token,
 }
 response = requests.get(pagerduty_url,headers=pagerduty_headers)
 oncalldata = response.text
 jsdata = json.loads(oncalldata)
 jsdata_result = jsdata['escalation_policies'][0]['on_call']
 level_1_users = [user_info['user']['email'] for user_info in jsdata_result if user_info['level'] == 1]
 level1useremail =  level_1_users[0]


def open_jira_tix():
 global jira_user
 global jira_pass
 global level1useremail
 jira_url = 'https://util01..net/jira/rest/api/2/issue/'
 jira_headers = {
 "Content-type":'application/json',
 }
 jira_data = '\n\
{\n\
    "fields": {\n\
       "project":\n\
       {\n\
          "key": "SYS"\n\
       },\n\
       "summary": "'+ args.tixtitle +'",\n\
       "description": "'+ args.descr +'",\n\
       "issuetype": {\n\
          "name": "Bug"\n\
       },\n\
       "customfield_10850": {\n\
          "value": "Maintenance"\n\
       }\n\
   }\n\
}'
 create = requests.post(jira_url, data=jira_data, headers=jira_headers, auth=(jira_user, jira_pass))
 print create.status_code
 if create.status_code == 201:
  ticketnumber = create.text[
  print ticketnumber  


pull_oncall_user()
open_jira_tix()

