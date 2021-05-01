import sys
try:
    import os
    import platform
    import logging
    import json
    import threading
    from threading import Semaphore
    import colorama
    from colorama import Fore
    from colorama import init
    colorama.init()
    init(autoreset=True)
    from captchatools import captcha_harvesters
    from newegg.create_account import static_data
    import time
except ModuleNotFoundError:
    print("Make sure you ran pip3 install -r requirements.txt")
    time.sleep(999)
    sys.exit(0)



class Newegg:
    def __init__(self):
        self.screenlock = Semaphore(value=1)

        # Load config
        settings = self.load_settings()
        self.settings = settings
        if settings["captcha"]["captcha_solver"] == 1 or str( settings["captcha"]["captcha_solver"]).lower() == "capmonster":
            api_key = settings["captcha"]["keys"]["capmonster"]
        elif settings["captcha"]["captcha_solver"] == 2 or str( settings["captcha"]["captcha_solver"]).lower() == "anticaptcha":
            api_key = settings["captcha"]["keys"]["anticaptcha"]
        elif settings["captcha"]["captcha_solver"] == 3 or str( settings["captcha"]["captcha_solver"]).lower() == "2captcha":
            api_key = settings["captcha"]["keys"]["2captcha"]
        
        if settings["captcha"]["version"].lower() == "v3":
            sitekey = static_data.v3_sitekey
        elif settings["captcha"]["version"].lower() == "v2":
            sitekey = static_data.v2_sitekey
        

        self.captcha_solver = captcha_harvesters(
                                solving_site=settings["captcha"]["captcha_solver"], 
                                api_key=api_key, 
                                sitekey=sitekey,
                                captcha_url="https://secure.newegg.com/identity/signup?tk=",
                                min_score=0.7, action="Register", captcha_type=settings["captcha"]["version"]
        )

        # Start the bot when initialized.
        self.main()
    
    def main(self):
        '''
        Main method.

        This method will be called (automatically) when the bot starts.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '''

        # Get user input for what they want to do
        print()
        print(Fore.CYAN + '1' ,Fore.MAGENTA + "=", Fore.YELLOW +  "Create Accounts")
        print(Fore.CYAN + '2' ,Fore.MAGENTA + "=", Fore.YELLOW +  "Submit Entries")
        choice = eval(input("{}".format(Fore.MAGENTA + "Enter your choice: " + Fore.CYAN)))
        if choice == 1:
            self.create_accounts()
        elif choice == 2:
            self.submit_entries()
    
    def load_settings(self):
        # Some users said their program couldn't find the files
        # So this is a quick fix to that.
        original_path = os.getcwd()
        os.chdir("./data/")
        self.PATH_EMAILS  = os.getcwd() + "\\emails.txt"
        self.PATH_PROXIES  = os.getcwd() + "\\proxies.txt"
        if platform.system() == "Linux" or platform.system() == "Darwin":
            self.PATH_EMAILS  = self.PATH_EMAILS.replace("\\", "/")
            self.PATH_PROXIES  = self.PATH_PROXIES.replace("\\", "/")
        

        # Open settings file
        settings_file_path = os.getcwd() + "/settings.json"
        os.chdir(original_path)
        with open(settings_file_path) as settingsFile:
            try:
                return json.load(settingsFile)
            except json.JSONDecodeError:
                print(Fore.RED + "There is an error in your settings.json file." +
                    "Make sure the commas are correct and there aren't any extra commas!")
                time.sleep(999)
                sys.exit(0)

    def create_accounts(self):
        '''
        This method will be called when the user wants to create Newegg Accounts.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        It will pull emails from the /data/emails.txt folder and use those
        to create the accounts
        '''
        from newegg.create_account import desktop, app, static_data

        # Prompt for how many tasks
        num_tasks = eval(input(Fore.BLUE + "\nEnter amount of tasks at a time: " + Fore.WHITE + " "))
        self.sema = threading.Semaphore(value=num_tasks)
        threads = []

        # Start to create create accounts
        with open(self.PATH_EMAILS) as email_file:
            for line in email_file.readlines():
                email = line.split(':')[0].strip("\n")
                self.sema.acquire()
                thread = threading.Thread(target=desktop.Create_Account,args=(self,email))
                threads.append(thread)
                thread.start()
    
    def submit_entries(self):
        '''
        This method will be called when the user wants to enter the Newegg raffle.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        It'll pull sessions from the file that the user used to create accounts
        '''
        from newegg.submit_raffle import raffles, app, desktop
        path_to_created_accounts = os.getcwd() + "\\{}".format(self.settings["output_filename"]) if \
            platform.system == "Windows"  else os.getcwd() + "/{}".format(self.settings["output_filename"])

        # Because Newegg still has V2 captcha enabled for submitting entries,
        # we'll use that over V3. If for whatever reason you want to use V3,
        # you would have to change this line of code. 
        self.captcha_solver.sitekey = "6Lcv-WUUAAAAAA9hyir8HPKZ44OvDLg1oZqnq_9d"
        self.captcha_solver.captcha_type = "v2"

        # Scrape & display raffle items
        print()
        print(Fore.YELLOW + "Getting items in raffle...")
        items = raffles.get_items()
        index = 0
        for item in items:
            print(Fore.GREEN + str(index) ,Fore.MAGENTA + "=", Fore.CYAN + "{} (${})".format( item["name"], item["price"]))
            index +=1


        # Get user choice(s) for the items they want to enter for
        self.PRODUCTS_TO_ENTER = [] # This will be the array used to submit entries
        choices = input(Fore.MAGENTA + "Enter the numbers of all the products you'd like to enter for, seperated by a space. (Example: 1 5 7 9 ): " + Fore.GREEN)
        for choice in choices.split():
            try:
                self.PRODUCTS_TO_ENTER.append({"ItemNumber": items[eval(choice)]["id"]})
            except Exception:
                print(Fore.RED + f"There was an error with item: #{choice}. Skipping that item.")


        # Show how many accounts have been made / are about to enter the raffle
        print()
        try:    
            with open(path_to_created_accounts) as email_file:
                print( Fore.BLUE + "Amount of accounts loaded: {} ({})".format(
                    Fore.CYAN + str(len(email_file.readlines())), 
                    self.settings["output_filename"])
                )
        except (FileExistsError, FileNotFoundError):
            print(Fore.RED + "Could not find the file with sessions. Check repo fore help.")
            time.sleep(100)
            return


        # Prompt how many tasks
        num_tasks = eval(input(Fore.BLUE + "Enter amount of tasks at a time: " + Fore.WHITE + " "))
        self.sema = threading.Semaphore(value=num_tasks)
        threads = []


        # Enter raffle
        with open(path_to_created_accounts) as email_file: # Get the emails from the file the user named
            for line in email_file.readlines():
                if "error" not in line:
                    self.sema.acquire()
                    email = line.split(':')[2].strip("\n")
                    sessionData = json.loads(":".join(line.split(":")[3:]))

                    # If the acct was created via desktop, it will enter via that way
                    # If the acct was created via app, it will enter via that way
                    if sessionData["desktop"] == {}: # If there are no desktop cookies, means it was created via APP
                        task = threading.Thread(target=app.SubmitRaffle,args=(self,email, sessionData))
                    else:
                        task = threading.Thread(target=desktop.SubmitRaffle,args=(self,email, sessionData))
                    threads.append(task)
                    task.start()


Newegg()