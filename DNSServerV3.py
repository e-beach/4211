# Fall 2016 CSci4211: Introduction to Computer Networks
# This program serves as the server of DNS query.
# Written in Python v3.

import sys, threading, os
import os
import re
from socket import *

# https://stackoverflow.com/questions/106179/regular-expression-to-match-dns-hostname-or-ip-address
ValidHostnameRegex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"

DNS_Cache = "DNS_mapping.txt"

def main():
    host = "localhost" # Hostname. It can be changed to anything you desire.
    port = os.environ.get("4211_port", 5000)

    #create a socket object, SOCK_STREAM for TCP
    try:
            sSock = socket(AF_INET, SOCK_STREAM)
    except error as msg:
            sSock = None # Handle exception

    # Allow reusing sockets (for convenience)
    sSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    #bind socket to the current address on port 5001
    sSock.bind((host, port))

    #Listen on the given socket maximum number of connections queued is 20
    sSock.listen(20)

    monitor = threading.Thread(target=monitorQuit, args=[])
    monitor.start()

    print("Server is listening...")

    while 1:
        #blocked until a remote machine connects to the local port 5001
        try:
            connectionSock, addr = sSock.accept()
            server = threading.Thread(target=dnsQuery, args=[connectionSock, addr[0]])
            server.start()
        except KeyboardInterrupt:
            sSock.close()
            raise


def dnsQuery(connectionSock, srcAddress):

    def handle():
        hostName = connectionSock.recv(1024).decode() # Receive from client.

        if not re.search(ValidHostnameRegex, hostName):
            return "Invalid hostname"

        open(DNS_Cache, "a") # Create if not exists

        #check the DNS_mapping.txt to see if the host name exists
        for line in open(DNS_Cache):
            if hostName in line.split(":")[0]:
                result = "Local DNS:{}".format(line.strip())
                return result

        try:
            addr = gethostbyname(hostName)
        except error as e: # TODO: gaierror, herror?
            print(error.errno)
            if error.errno == -2:
                addr = "Host Not Found"
            else:
                addr = "resolving DNS failed: {}".format(str(e))

        mapping = '{}:{}'.format(hostName, addr)
        result = 'Root DNS:{}'.format(mapping)
        with open(DNS_Cache, "a") as f:
            f.write(mapping + "\n")

        return result

    result = handle()
    print(result)
    connectionSock.send(result.encode())
    connectionSock.close()

def monitorQuit():
    while 1:
        sentence = input()
        if sentence == "exit":
            os.kill(os.getpid(),9)

main()
