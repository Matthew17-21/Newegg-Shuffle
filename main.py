import sys
try:
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
    from newegg.create_account import desktop, mobile, static_data
except ModuleNotFoundError:
    print("Make sure you ran pip3 install -r requirements.txt")
    sys.exit(0)


with open("./data/settings.json") as settingsFile:
    settings = json.load(settingsFile)
logging.basicConfig(filename=settings["output_filename"], level=logging.INFO)

class Newegg:
    def __init__(self):
        self.screenlock = Semaphore(value=1)

        # Load config
        self.settings = settings
        if settings["captcha"]["captcha_solver"] == 1 or str( settings["captcha"]["captcha_solver"]).lower() == "capmonster":
            api_key = settings["captcha"]["keys"]["capmonster"]
        elif settings["captcha"]["captcha_solver"] == 2 or str( settings["captcha"]["captcha_solver"]).lower() == "anticaptcha":
            api_key = settings["captcha"]["keys"]["anticaptcha"]
        elif settings["captcha"]["captcha_solver"] == 3 or str( settings["captcha"]["captcha_solver"]).lower() == "2captcha":
            api_key = settings["captcha"]["keys"]["2captcha"]
        
        if settings["captcha"]["version"] == "v3":
            sitekey = static_data.v3_sitekey
        elif settings["captcha"]["version"] == "v3":
            sitekey = static_data.v2_sitekey
        

        self.captcha_solver = captcha_harvesters(
                                solving_site=settings["captcha"]["captcha_solver"], 
                                api_key=api_key, 
                                sitekey=sitekey,
                                captcha_url="https://secure.newegg.com/identity/signup?tk=",
                                min_score=0.7, action="Register", captcha_type=settings["captcha"]["version"]
        )

        # Start the bot.
        self.main()
    
    def main(self):
        num_tasks = eval(input(Fore.BLUE + "Enter amount of tasks at a time: " + Fore.WHITE + " "))
        self.sema = threading.Semaphore(value=num_tasks)
        threads = []

        with open("./data/emails.txt") as email_file:
            for line in email_file.readlines():
                email = line.split(':')[0].strip("\n")
                self.sema.acquire()
                thread = threading.Thread(target=self.create,args=(email,))
                threads.append(thread)
                thread.start()
    
    def create(self,email):
        task = desktop.Create_Account(self, email)
        data = task.start()

        # Log Data
        logging.info("{}:{}".format(
            email,
            json.dumps(data)
        ))
        self.sema.release()



Newegg()