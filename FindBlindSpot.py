#!/usr/bin/python

from lib.blindfuzzer import blindSeeker
import socket
import sys

# Target Parameters
Server = '192.168.56.101'
Port = 80
Index = 1
Method = 'GET'

# Provide files with tests for fuzzing
Headerfile = "fuzz-data/headers/default_headers.txt"
injectionfile = "fuzz-data/payloads/mysql_time.txt"

try:
    # Data to Fuzz our Target (in the format required)
    target_params = {
        'server': Server,
        'port': Port,
        'index': Index,
        'headersFile': Headerfile,
        'injectionFile': injectionfile,
        'method': Method
    }

    # Use blindfuzzer methods to find a Timebased Blind-Sql Injection
    vulns = blindSeeker(target_params)
    vulns.fuzz()

except Exception as err:
    print("Check Your Conection/Setup!")
    print("Hint: ")
    print(err)
