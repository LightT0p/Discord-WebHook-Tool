import requests, random_string, time, json, os, threading
from colorama import Fore
from pystyle import Colorate, Colors

pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
menu = """

            Discord WebHook ToolKit
                By FreakyFDP

              [1] Webhook Spammer
              [2] Webhook Deleter
              [3] Webhook Info
              [4] Webhook bulk creator


"""
banner = Colorate.Diagonal(Colors.red_to_blue, menu, True)

msg_req_sent = 0
msg_sent = 0

def send_request(wbhk, msg, number, amount):
    global msg_req_sent, msg_sent
    try:
        resp = requests.post(wbhk, json={'content': f'{msg}', 'username': '.gg/Cw545PtvHv On Top'})
        with threading.Lock():
            msg_req_sent += 1
            if resp.json()["message"].find("'You are being blocked from accessing our API temporarily due to exceeding our rate limits frequently."):
                time.sleep(5)
            elif resp.json()["message"].find("rate limit"):
                time.sleep(1)
            else:
                print(f"{resp.json()} | (Number: {number} - Message Sent: {msg_sent} / {msg_req_sent} - Total: {amount})")
                msg_sent += 1
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def main():
    os.system("cls")
    global msg_sent, msg_req_sent
    msg_req_sent = 0
    msg_sent = 0
    print(f'{Fore.RESET + banner}')
    bn = Colorate.Diagonal(Colors.red_to_blue, "\nPlease enter your choice (leave empty if you want to quit) >> ", True)
    choice = input(bn)
    os.system("cls")

    if choice == "1":
        wbhk = input(Colorate.Diagonal(Colors.red_to_blue, "Enter the webhook you desire to spam >> ", True))
        check_valid = requests.get(wbhk)
        try:
            if check_valid.json().get("message") == "Unknown Webhook":
                print("This webhook is invalid...")
                input("Press enter to go back to the main menu...")
                main()
        except Exception:
            print("Error checking webhook validity.")
            input("Press enter to go back to the main menu...")
            main()
        
        msg = input(Colorate.Diagonal(Colors.red_to_blue, "Enter the message you desire >> ", True))
        amount = int(input(Colorate.Diagonal(Colors.red_to_blue, "Enter the amount of times you want the webhook to be spammed >> ", True)))
        threads = []

        while msg_sent < amount:
            for _ in range(amount):
                if msg_sent >= amount:
                    break
                thread = threading.Thread(target=send_request, args=(wbhk, msg, msg_sent, amount))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()
        input("Press enter to go back to the main menu...")
        main()

    elif choice == "2":
        file_option = input(Colorate.Diagonal(Colors.red_to_blue, "Do you want to load webhooks from a file? (yes/no) >> ", True)).strip().lower()
        webhooks = []

        if file_option == "yes":
            file_path = input(Colorate.Diagonal(Colors.red_to_blue, "Enter the path to the file containing webhooks >> ", True))
            try:
                with open(file_path, 'r') as file:
                    webhooks = [line.strip() for line in file.readlines() if line.strip()]
                print(f"Loaded {len(webhooks)} webhooks from {file_path}")
            except Exception as e:
                print(f"Failed to read from file: {e}")
                time.sleep(3)
                main()
        elif file_option == "no":
            wbhk = input(Colorate.Diagonal(Colors.red_to_blue, "Enter the webhook you desire to delete >> ", True))
            check_valid = requests.get(wbhk)
            try:
                if check_valid.json()["message"] == "Unknown Webhook":
                    print("This webhook is invalid...")
                    time.sleep(3)
                    main()
            except:
                pass
            webhooks.append(wbhk)
        else:
            print("Invalid option, returning to main menu...")
            input("Press enter to go back to the main menu...")
            main()

        for wbhk in webhooks:
            check_valid = requests.get(wbhk)
            try:
                if check_valid.json()["message"] == "Unknown Webhook":
                    print(f"{wbhk} is invalid...")
                    continue
            except:
                pass
            
            base_url, token = wbhk.rsplit('/', 1)
            censored_id = token[:len(token)//2] + '*' * (len(token) - len(token)//2)
            censored_url = f"{base_url}/{censored_id}"
            
            res = requests.get(wbhk).json()
            deletion = requests.delete(res['url'])

            print(f"Deleted {censored_url}: {'True' if deletion.ok else 'False'}")
        
        input("Press enter to go back to the main menu...")
        main()

    elif choice == "3":
        wbhk = input(Colorate.Diagonal(Colors.red_to_blue, "Enter the webhook you desire to have infos on >> ", True))
        t = requests.get(wbhk)
        print(json.dumps(t.json(), indent=4))
        input("Press enter to go back to the main menu...")
        main()

    elif choice == "4":
        channel_id = input(Colorate.Diagonal(Colors.red_to_blue, "Enter the channel ID you want to create the webhooks in >> ", True))
        webhook_url = f"https://discord.com/api/v9/channels/{channel_id}/webhooks"
        token = input(Colorate.Diagonal(Colors.red_to_blue, "Enter your discord token (NEED TO HAVE THE MANAGE WEBHOOK PERMS) >> ", True))

        resp = requests.get(webhook_url, headers={"authorization": token})
        pp = [t['url'] for t in resp.json()]
        
        number_of_whbk_to_create = input(Colorate.Diagonal(Colors.red_to_blue, f"Enter the number of webhook you want to create\n(you can create a max of {15 - len(pp)} webhook in this channel) >> ", True))

        RATE_LIMIT_DELAY = 5

        def create_webhook(i):
            try:
                response = requests.post(webhook_url, json={"name": f"freakymarketplace_{random_string.generate(6, 6)}"}, headers={"authorization": token})

                if response.status_code == 200:
                    print(Colorate.Diagonal(Colors.red_to_blue, f"Webhook {i} created successfully.", True))
                    return response.json().get("url")
                elif response.status_code == 429:
                    reset_after = response.headers.get("Retry-After")
                    if reset_after:
                        delay = float(reset_after) + 1
                        print(f"Rate limit hit, sleeping for {delay} seconds.")
                        time.sleep(delay)
                    else:
                        print(f"Rate limit hit but no reset time provided. Sleeping for {RATE_LIMIT_DELAY} seconds.")
                        time.sleep(RATE_LIMIT_DELAY)
                    return create_webhook(i)
                else:
                    print(f"Failed to create webhook {i}: {response.status_code} - {response.text}")
                    return None

            except Exception as e:
                print(f"Error creating webhook {i}: {e}")
                return None

        webhook_count = 0

        for i in range(int(number_of_whbk_to_create)):
            url = create_webhook(i)

            if url:
                webhook_count += 1
                print(f"Webhook URL: {url}")
                with open("./webhooks.txt", "a+") as f:
                    f.write(f'{url}\n')

        print(Colorate.Diagonal(Colors.red_to_blue, f"\nTotal webhooks created: {webhook_count}", True))
        input("Press enter to go back to the main menu...")
        main()
    else:
        exit("Exiting the program...")

if __name__ == "__main__":
    os.system("cls")
    main()