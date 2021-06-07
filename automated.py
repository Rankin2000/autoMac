import os
import subprocess
import argparse
import plistlib

#system_intergrity_protection"
#"system_info"
#"install_history"
#"gatekeeper_status"
#"established_connections"
#"environment_variables"
#"periodic_scripts"
#"cron_jobs"
#"emond_rules"
#"launch_agents"
#"launch_daemons"
#"applications"
#"event_taps"
#"bash_history"
#"kernel_extensions"
#"chrome_extensions"
#"safari_extensions"

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", type=str, choices=["html", "json"], help="output format")
parser.add_argument("-f", "--file", type=str)
parser.add_argument("-v", "--verbosity", help="increase output verbosity")

results = []
users = []
#Get Users
def getusers():
    allUsers = subprocess.check_output("dscl . list /Users", shell=True).decode().split("\n")
    users = []
    for user in allUsers:
        if not user.startswith('_') and user:
            users.append(user)


getusers()

#SIP
sip = subprocess.check_output("csrutil status", shell=True).decode()
print("SIP = " + sip)


#Launch Agents
launchagents = os.listdir("/Library/LaunchAgents")
for user in users:
    userlaunchagents = os.listdir("/Users/" + user + "/Library/LaunchAgents")
    launchagents.extend(userlaunchagents)
print(launchagents)

#Launch Daemons
launchdaemons = os.listdir("/Library/LaunchDaemons")
print(launchdaemons)

#Periodic Scripts
daily = os.listdir("/etc/periodic/daily/")
weekly = os.listdir("/etc/periodic/weekly/")
monthly = os.listdir("/etc/periodic/monthly/")

print(daily)
print(weekly)
print(monthly)

#Cron
#need to add


#Emond
rules = os.listdir("/etc/emond.d/rules/")
for rule in rules:
    with open("/etc/emond.d/rules/" + rule, "rb") as f:
        pl = plistlib.load(f)
        print(pl)

#Kernel Extensions
extensions = os.listdir("/Library/Extensions")
for extension in extensions:
    for root, dirs, files in os.walk("/Library/Extensions/" + extension):
        for file in files:
            if file == "Info.plist":
                with open(os.path.join(root, file), "rb") as f:
                    kextPlist = plistlib.load(f)
                print(kextPlist)
                if kextPlist:
                    exe = kextPlist.get("CFBundleExecutable")
                    if exe:
                        exepath = root + "/MacOS/" + exe

#connections
processes = subprocess.check_output("lsof -i", shell=True).decode().split('\n')
for process in processes:

    #process = process.split(" ")
    if "(ESTABLISHED)" in process:
        print(process)
