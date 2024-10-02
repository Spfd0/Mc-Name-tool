import random
import string
import requests
import os
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style
from tqdm import tqdm

init(autoreset=True)

ASCII_ART = """
███╗   ███╗██╗███╗   ██╗███████╗ ██████╗██████╗  █████╗ ███████╗████████╗
████╗ ████║██║████╗  ██║██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
██╔████╔██║██║██╔██╗ ██║█████╗  ██║     ██████╔╝███████║█████╗     ██║   
██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██║     ██╔══██╗██╔══██║██╔══╝     ██║   
██║ ╚═╝ ██║██║██║ ╚████║███████╗╚██████╗██║  ██║██║  ██║██║        ██║   
╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   
                USERNAME AVAILABILITY CHECKER
"""

def generate_username(length):
    characters = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choices(characters, k=length))

def generate_usernames(count, length):
    usernames = set()
    with tqdm(total=count, desc=f"{Fore.BLUE}Generating usernames", unit="username", 
              colour="green", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]") as pbar:
        while len(usernames) < count:
            username = generate_username(length)
            if username not in usernames:
                usernames.add(username)
                pbar.update(1)
    return usernames

def check_username(username):
    url = f'https://api.mojang.com/users/profiles/minecraft/{username}'
    try:
        response = requests.get(url, timeout=5)
        return username, response.status_code == 404
    except requests.RequestException:
        return username, False

def check_usernames(usernames):
    with ThreadPoolExecutor(max_workers=40) as executor:
        results = list(tqdm(executor.map(check_username, usernames), 
                            total=len(usernames), desc=f"{Fore.BLUE}Checking usernames", unit="username",
                            colour="green", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"))
    return results

def read_usernames_from_file(filename):
    possible_paths = [
        filename,
        os.path.join(os.getcwd(), filename),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), filename),
        os.path.abspath(filename)
    ]

    for path in possible_paths:
        try:
            with open(path, 'r') as file:
                usernames = [line.strip() for line in file if line.strip()]
                print(f"Successfully read {len(usernames)} usernames from file.")
                return usernames
        except IOError:
            continue

    print(f"Error: Could not read file '{filename}' from any possible location.")
    return []

def display_menu():
    print(Fore.LIGHTBLUE_EX + "\nChoose an option:")
    print(Fore.BLUE + "1. Enter usernames manually")
    print(Fore.BLUE + "2. Read usernames from a file")
    print(Fore.BLUE + "3. Generate random usernames")
    print(Fore.BLUE + "4. Generate maximum usernames for a specific length")
    print(Fore.RED + "5. Exit")
    choice = input(Fore.WHITE + "Enter your choice (1-5): ")
    clear_screen(7)  # Clear the menu, including "Choose an option:" and input
    return choice

def get_usernames_manually():
    usernames = input(Fore.WHITE + "Enter usernames separated by spaces: ").split()
    clear_screen(1)  # Clear only the input line
    return usernames

def get_usernames_from_file():
    filename = input(Fore.WHITE + "Enter the filename containing usernames: ")
    clear_screen(1)  # Clear only the input line
    return read_usernames_from_file(filename)

def get_generated_usernames():
    count = int(input(Fore.WHITE + "Enter the number of usernames to generate: "))
    length = int(input(Fore.WHITE + "Enter the desired length for usernames: "))
    clear_screen(2)  # Clear both input lines
    return list(generate_usernames(count, length))

def get_max_usernames():
    print(Fore.CYAN + Style.BRIGHT + "\nChoose username length:")
    print(Fore.LIGHTBLUE_EX + "1. " + Fore.WHITE + "1-letter usernames " + Fore.YELLOW + "(26 usernames)")
    print(Fore.LIGHTBLUE_EX + "2. " + Fore.WHITE + "2-letter usernames " + Fore.YELLOW + "(676 usernames)")
    print(Fore.LIGHTBLUE_EX + "3. " + Fore.WHITE + "3-letter usernames " + Fore.YELLOW + "(17,576 usernames)")
    print(Fore.LIGHTBLUE_EX + "4. " + Fore.WHITE + "4-letter usernames " + Fore.YELLOW + "(456,976 usernames)")
    print(Fore.LIGHTBLUE_EX + "5. " + Fore.WHITE + "5-letter usernames " + Fore.YELLOW + "(11,881,376 usernames)")
    print(Fore.LIGHTBLUE_EX + "6. " + Fore.WHITE + "6-letter usernames " + Fore.YELLOW + "(308,915,776 usernames)")
    length_choice = input(Fore.GREEN + Style.BRIGHT + "Enter your choice (1-6): " + Style.RESET_ALL)
    clear_screen(8)  # Clear the menu and input
    
    length = int(length_choice)
    max_count = 26 ** length
    return list(generate_usernames(max_count, length))

def clear_screen(lines=1):
    # Move cursor up 'lines' lines and clear from cursor to end of screen
    print(f"\033[{lines}A\033[0J", end="")

def print_header():
    print(Fore.LIGHTBLUE_EX + ASCII_ART)
    print(Fore.WHITE + "Welcome to the Minecraft Username Availability Checker!")
    print(Fore.WHITE + "This tool allows you to check the availability of Minecraft usernames.")
    print(Fore.WHITE + "You can enter usernames manually, read them from a file, or generate random ones.")

def main():
    print_header()

    while True:
        choice = display_menu()

        if choice == '1':
            usernames = get_usernames_manually()
        elif choice == '2':
            usernames = get_usernames_from_file()
        elif choice == '3':
            usernames = get_generated_usernames()
        elif choice == '4':
            usernames = get_max_usernames()
        elif choice == '5':
            print(Fore.YELLOW + "Goodbye!")
            break
        else:
            print(Fore.YELLOW + "Invalid choice. Please try again.")
            continue

        if not usernames:
            print(Fore.YELLOW + "No usernames provided. Please try again.")
            continue

        results = check_usernames(usernames)

        print("\n" + Fore.WHITE + Style.BRIGHT + "Scan complete! Results:" + Style.RESET_ALL)
        print(Fore.LIGHTBLUE_EX + "=" * 40)

        available_usernames = [username for username, is_available in results if is_available]
        unavailable_count = len(usernames) - len(available_usernames)

        print(Fore.BLUE + f"Total usernames checked: {len(usernames)}")
        print(Fore.RED + f"Unavailable usernames: {unavailable_count}")
        print(Fore.GREEN + f"Available usernames: {len(available_usernames)}")

        if available_usernames:
            print(Fore.WHITE + "\nAvailable usernames:" + Style.RESET_ALL)
            for username in available_usernames:
                print(Fore.GREEN + f"  {username}")

        print(Fore.LIGHTBLUE_EX + "=" * 40)

        input(Fore.WHITE + "\nPress Enter to continue...")
        
        # Clear everything except the header
        clear_screen(100)  # Clear a large number of lines to ensure everything is cleared
        print_header()

if __name__ == "__main__":
    main()
