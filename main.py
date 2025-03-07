from colorama import Fore, init
from pystyle import Colors, Colorate
import requests, os, threading, random_string, json, time, random

init(autoreset=True)
os.system("cls")

title = Colorate.Diagonal(Colors.white_to_blue, r"""
______ _                       _   _    _      _     _   _             _
|  _  (_)                     | | | |  | |    | |   | | | |           | |
| | | |_ ___  ___ ___  _ __ __| | | |  | | ___| |__ | |_| | ___   ___ | | __
| | | | / __|/ __/ _ \| '__/ _` | | |/\| |/ _ \ '_ \|  _  |/ _ \ / _ \| |/ /
| |/ /| \__ \ (_| (_) | | | (_| | \  /\  /  __/ |_) | | | | (_) | (_) |   < 
|___/ |_|___/\___\___/|_|  \__,_|  \/  \/ \___|_.__/\_| |_/\___/ \___/|_|\_\
                             _   _ _   _ _
                            | | | | | (_) |
                            | | | | |_ _| |___
                            | | | | __| | / __|
                            | |_| | |_| | \__ \
                             \___/ \__|_|_|___/

""", 1)

features = Colorate.Diagonal(Colors.white_to_blue, """

                                Choices:
                          [1] WebHook Spammer
                          [2] WebHook Deleters
                          [3] Webhook Info
                          [4] Webhook bulk creator
""", 1)

print_lock = threading.Lock()
msg_sent = 0
valid_wbhks = []
dead_proxies = []

def check_wbhk(wbhk, length):
    check_valid = requests.get(wbhk)
    try:
        if check_valid.json().get("message") == "Unknown Webhook":
            print(f" |_{Fore.RED}WebHook invalid. ({wbhk})")
            return False
    except Exception:
        print("Error checking webhook validity.")
        return False
    return True

def webhook_spammer():
    global msg_sent, valid_wbhks, dead_proxies

    os.system("cls")
    print(f"{title}\n |\n |")
    mult_wbhks = input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Do you want to spam multiple webhooks (./webhooks.txt) <y/n> >> ").lower()

    if mult_wbhks == "y":
        with open("webhooks.txt", "r") as f:
            wbhks = f.read().strip().splitlines()
        for wbhk in wbhks:
            if check_wbhk(wbhk, len(wbhks)):
                valid_wbhks.append(wbhk)
    else:
        wbhk = input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Enter the webhook you desire to spam >> ")
        if not check_wbhk(wbhk, 1):
            print(f" |_{Fore.RED}WebHook Spammer --> Invalid webhook.")
            return
        valid_wbhks.append(wbhk)

    usrnm = input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Enter the username you desire to use >> ")

    send_msg = input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Do you want to send a message (y/n) >> ").lower()
    do_send_msg = send_msg == "y"
    
    msg = None
    if do_send_msg:
        msg = input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Enter the message you want to send >> ")

    send_file = input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Do you want to send a file (y/n) >> ").lower()
    do_send_file = send_file == "y"
    
    path = None
    if do_send_file:
        path = input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Enter the path of the file you want to send >> ")

    msg_number = int(input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Enter how many messages you want to send to each webhook >> "))
    thread_number = int(input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Enter how many threads you want to use >> "))
    use_proxies = input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Do you want to use proxies <y/n> >> ").lower()

    do_use_proxies = True if use_proxies == "y" else False

    def send_request(url, send_msg, msg, send_file, path):
        global msg_sent, dead_proxies
        messages_sent = 0
        while messages_sent < msg_number:
            proxies = open("./proxies.txt", "r").readlines()
            prx = str(random.choice(proxies)).replace("\n", "")
            proxy = {'http': prx, 'https': prx}
            try:
                if send_file:
                    with open(path, "rb") as f:
                        files = {"file": f}
                        resp = requests.post(url, json={"content": str(msg) if send_msg else "", "username": str(usrnm)}, proxies=proxy if do_use_proxies else None)
                        resp = requests.post(url, data={"username": str(usrnm)}, files=files, proxies=proxy if do_use_proxies else None)
                else:
                    resp = requests.post(url, json={"content": str(msg) if send_msg else "", "username": str(usrnm)}, proxies=proxy if do_use_proxies else None)

                wbhk = url.split("/")
                new_wbhk = wbhk[0] + wbhk[1] + wbhk[2] + wbhk[3] + wbhk[4] + wbhk[5] + "/" + "*" * random.randint(6, 12)
                with print_lock:
                    if resp.status_code >= 200 and resp.status_code <= 204:
                        msg_sent += 1
                        messages_sent += 1
                        print(f" |_{Fore.GREEN}WebHook Spammer [{resp.status_code}] --> Message sent successfully to {new_wbhk} ({msg_sent}th message sent)")
                    elif resp.status_code == 429:
                        print(f" |_{Fore.RED}WebHook Spammer [{resp.status_code}] --> Rate limit reached for {new_wbhk}.")
                    elif resp.status_code == 407:
                        print(f" |_{Fore.RED}WebHook Spammer [{resp.status_code}] --> Proxy error: Authentification {proxy}.")
                    else:
                        print(f" |_{Fore.RED}WebHook Spammer [{resp.status_code}] --> Error: {resp.text}.")
            except Exception as e:
                if str(e).find("'Unable to connect to proxy'"):
                    if proxy not in dead_proxies:
                        dead_proxies.append(proxy)
                    print(f" |_{Fore.RED}WebHook Spammer --> Proxy error: Unable to connect {proxy}.")
                else:
                    print(e)

    threads = []
    for wbhk in valid_wbhks:
        for _ in range(thread_number):
            thread = threading.Thread(target=send_request, args=(wbhk, do_send_msg, msg, do_send_file, path))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    print(f" |_{Fore.GREEN}All messages sent according to specified limits. Total messages sent: {msg_sent}")
    print(f" |_{Fore.RED}All dead proxies: {[dead_proxy for dead_proxy in dead_proxies]}")
    input("Press enter to continue...")
    msg_sent = 0
    valid_wbhks.clear()
    dead_proxies.clear()
    menu()


def webhook_deleter():
    os.system("cls")
    print(title + "\n |\n |")
    
    mult_wbhks = input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Do you want to delete multiple webhooks (from ./webhooks.txt) <y/n> >> ").lower()
    msg = input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Enter the message you want to send before deleting webhook >> ")
            
    if mult_wbhks == "y":
        with open("webhooks.txt", "r") as f:
            wbhks = f.read().strip().splitlines()
        for wbhk in wbhks:
            resp = requests.post(wbhk, json={"content": str(msg)})
            if resp.status_code == 204:
                print(f" |\n{Fore.GREEN} |_WebHook Deleter --> Message sent successfully to {wbhk}")
            elif resp.status_code == 429:
                print(f" |\n{Fore.RED} |_WebHook Deleter --> Rate limit reached for {wbhk}.")
            
            resp = requests.delete(wbhk)
            
            if resp.status_code == 204:
                print(f" |\n{Fore.GREEN} |_WebHook Deleter --> Webhook {wbhk} successfully deleted")
            elif resp.status_code == 429:
                print(f" |\n{Fore.RED} |_WebHook Deleter --> Rate limit reached while deleting {wbhk}.")

    else:
        wbhk = input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Enter the webhook you desire to delete >> ")

        resp = requests.post(wbhk, json={"content": str(msg)})
        if resp.status_code == 204:
            print(f" |\n{Fore.GREEN} |_WebHook Deleter --> Message sent successfully")
        elif resp.status_code == 429:
            print(f" |\n{Fore.RED} |_WebHook Deleter --> Rate limit reached.")

        resp = requests.delete(wbhk)
        
        if resp.status_code == 204:
            print(f" |\n{Fore.GREEN} |_WebHook Deleter --> Webhook successfully deleted")
        elif resp.status_code == 429:
            print(f" |\n{Fore.RED} |_WebHook Deleter --> Rate limit reached.")

    input("Press enter to continue...")
    menu()

def webhook_bulk_creator():
    channel_id = input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Enter the channel id you want to the webhooks in >> ")
    webhook_url = f"https://discord.com/api/v9/channels/{channel_id}/webhooks"
    token = input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Enter your discord token (NEED TO HAVE THE MANAGE WEBHOOK PERMS) >> ")

    resp = requests.get(webhook_url, headers={"authorization": token})
    pp = [t['url'] for t in resp.json()]
    
    number_of_whbk_to_create = input(f" |\n{Fore.LIGHTBLACK_EX} ╰┈➤Enter the number of webhook you want to create\n(you can create a max of {15 - len(pp)} webhook in this channel) >> ")

    RATE_LIMIT_DELAY = 5

    def create_webhook(i):
        try:
            response = requests.post(webhook_url, json={"name": f"freakymarketplace_{random_string.generate(6, 6)}"}, headers={"authorization": token})

            if response.status_code == 200:
                print(f" |\n{Fore.GREEN} |_WebHook Bulk Creator --> Webhook {i} created successfully.")
                return response.json().get("url")
            elif response.status_code == 429:
                reset_after = response.headers.get("Retry-After")
                if reset_after:
                    delay = float(reset_after) + 1
                    time.sleep(delay)
                else:
                    time.sleep(RATE_LIMIT_DELAY)
            else:
                print(f" |\n{Fore.RED} |_WebHook Bulk Creator --> Failed to create webhook {i}: {response.status_code} - {response.text}.")
                return None

        except Exception as e:
            print(f" |\n{Fore.RED} |_WebHook Bulk Creator --> Error during creation: {e}.")
            return None

    webhook_count = 0

    for i in range(int(number_of_whbk_to_create)):
        url = create_webhook(i)

        if url:
            webhook_count += 1
            print(f"Webhook URL: {url}")
            with open("./created_webhooks.txt", "a+") as f:
                f.write(f'{url}\n')

    print(Colorate.Diagonal(Colors.red_to_blue, f"\nTotal webhooks created: {webhook_count}", True))

def menu():
    os.system("cls")
    print(title + features + "\n|\n|")
    try:
        choice = int(input(f"|\n|\n{Fore.BLUE}╰┈➤{Fore.LIGHTBLUE_EX}Enter {Fore.LIGHTBLACK_EX}a {Fore.LIGHTWHITE_EX}choice {Fore.WHITE}>> "))
    except ValueError:
        input("Enter a number. Press enter to continue...")
        menu()
    if choice == 0:
        exit()
    elif choice == 1:
        webhook_spammer()
    elif choice == 2:
        webhook_deleter()
    elif choice == 3:
        wbhk = input(Colorate.Diagonal(Colors.red_to_blue, "Enter the webhook you desire to have infos on >> ", True))
        t = requests.get(wbhk)
        print(json.dumps(t.json(), indent=4))
        menu()

    elif choice == 4:
        webhook_bulk_creator()
    else:
        input("Wrong choice, press enter to continue...")
        menu()

if __name__ == "__main__":
    menu()