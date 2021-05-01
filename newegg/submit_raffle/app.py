import datetime
import logging
import json
import urllib.parse
import random
import requests
from requests import exceptions as requestsExceptions
import sys
import colorama
from colorama import Fore
from colorama import init
colorama.init()
init(autoreset=True)
from . import raffle_data

# Get the current date and use that as the log file name
log_file_name = "{} entries.log".format(datetime.datetime.now().strftime("%m-%d-%Y"))
logging.basicConfig(filename=log_file_name, level=logging.INFO)

DO_NOT_ENCODE_KEYS =[
    "LoginToken",
    "CustomerNumber",
    "LoginName",
    "EncryptLoginName"
]

class SubmitRaffle:
    def __init__(self, NeweggParent:object, email, sessionJSON):
        self.screenlock = NeweggParent.screenlock
        self.PRODUCTS_TO_ENTER = NeweggParent.PRODUCTS_TO_ENTER
        self.captcha_solver = NeweggParent.captcha_solver
        self.captcha_solver.captcha_url =  raffle_data.App.RAFFLE_URL
        

        # Define task specific data
        self.email = email
        self.current_task = email
        self.logging_data = sessionJSON
        self.session  = requests.Session()
        self.HEADERS_general = raffle_data.App.HEADERS_general.copy()
        self.HEADERS_submit = raffle_data.App.HEADERS_submitEntry.copy()

        # Update User Agents
        user_agent = random.choice(NeweggParent.settings["user_agents"]["mobile"])
        self.HEADERS_general["User-Agent"] = user_agent
        self.HEADERS_submit["User-Agent"] = user_agent

        # Create the mobile cookie
        cookiesJSON = self.logging_data["app"]["cookies"]
        for cookie in cookiesJSON:
            self.session.cookies.set(cookie, cookiesJSON[cookie])
        appData =  self.logging_data["app"]
        NV_NeweggApp={
            "LoginToken":appData["login_token"],
            "CustomerNumber":appData["misc"]["CustomerLoginInfo"]["EncryptCustomerNumber"],
            "LoginName":appData["misc"]["CustomerLoginInfo"]["LoginName"],
            "EncryptLoginName":appData["misc"]["CustomerLoginInfo"]["EncryptLoginName"],
            "ContactWith":appData["misc"]["CustomerLoginInfo"]["ContactWith"],
            "IsCANB2BCustomer":False,
            "IsEggXpert":False,
            "UserAgent":"Newegg iPhone App / {}".format(NeweggParent.settings["ios_app_version"])
        }

        cookiesTemp = []
        for cookie in NV_NeweggApp:
            # URL encode the key & value
            # DO NOT ENCODE IF COOKIE_KEY = LoginToken, CustomerNumber, LoginName, EncryptLoginName, 
            keyEncoded = self.encode('"{}"'.format(cookie))
            if cookie in DO_NOT_ENCODE_KEYS:
                valueEncoded = "%22{}%22".format(NV_NeweggApp[cookie])
            else:
                if NV_NeweggApp[cookie] == False:
                    valueEncoded = self.encode('false')
                else:
                    valueEncoded = self.encode('"{}"'.format(NV_NeweggApp[cookie]))
            temp = '{}:{}'.format(keyEncoded, valueEncoded)
            cookiesTemp.append(temp)
        
        string = ""
        string += self.encode('{')
        temp = ",".join(cookiesTemp)
        string += temp
        string += self.encode('}')
        NCTC = cookiesJSON["NVTC"]
        self.HEADERS_submit["Cookie"] = f"NV%5FNeweggApp={string}; NVTC={NCTC};"

        # Start the bot
        self.start()


    def start(self):
        self.getProxy()
        self.get_lottery_id()
        self.submit_entries()

        logging.info("{}:{}".format(
            self.email,
            json.dumps(self.logging_data)
        ))
        return 

    def get_lottery_id(self):
        while True:
            try:
                self.screenlock.acquire()
                print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.YELLOW +  "Getting Lottery ID...")
                self.screenlock.release()

                # Get Lottery ID
                response = self.session.get(raffle_data.App.RAFFLE_URL, headers=self.HEADERS_general)
                HTML_Splitted = json.loads(response.text.split("window.__initialState__ = ")[1].split("</script>")[0])
                self.lotteryID = HTML_Splitted["lotteryData"]["LotteryID"]
                self.screenlock.acquire()
                print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.YELLOW +  "Lottery ID: {}".format(self.lotteryID))
                self.screenlock.release()
                return

            except requestsExceptions.ConnectTimeout:
                self.screenlock.acquire()
                print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.MAGENTA +  "Connection timedout.")
                self.screenlock.release()
                continue
            except requestsExceptions.ProxyError:
                self.screenlock.acquire()
                print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.MAGENTA +  "Proxy error.")
                self.screenlock.release()
                self.getProxy()
                continue
            
            except Exception as e:
                print(e)
                self.screenlock.acquire()
                print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.RED +  'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), Fore.RED + "{}".format(type(e).__name__), Fore.RED + "{}".format( e))
                self.screenlock.release()
                continue
    
    def submit_entries(self):
        while True:
            try:
                # Solve Captcha
                self.screenlock.acquire()
                print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.YELLOW +  "Waiting on Captcha...")
                self.screenlock.release()
                captcha_answer = self.captcha_solver.get_token()



                # Submit Entry
                self.screenlock.acquire()
                print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.YELLOW +  "Submitting entry...")
                self.screenlock.release()
                payload = self.getPayload(self.lotteryID, "v2", captcha_answer, self.PRODUCTS_TO_ENTER)
                submit = self.session.post(raffle_data.POSTURL_submitEntry, headers=self.HEADERS_submit, json=payload)

                # Parse Response
                response = json.loads(submit.text)
                if response["Result"] == "Success":
                    self.screenlock.acquire()
                    print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.GREEN +  f"Successfully entered raffle!")
                    self.screenlock.release()

                    self.logging_data["app"]["cookies"] = json.dumps(self.session.cookies.get_dict())
                    return
                elif response["Result"] == "ReChaptCha Invalid":
                    self.screenlock.acquire()
                    print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.MAGENTA +  "Invalid captcha token.")
                    self.screenlock.release()                    
                elif response["Result"] == "UnAccess" or response["Result"] == "UnSuccess":
                    self.screenlock.acquire()
                    print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.CYAN +  "UnAccess. Stopping.")
                    self.screenlock.release()

                    self.logging_data["error"] = True
                    self.logging_data["error_msg"] = "UnAccess"
                    self.logging_data["app"]["cookies"] = json.dumps(self.session.cookies.get_dict())
                    return
                elif response["Code"] == "111":
                    self.screenlock.acquire()
                    print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.CYAN +  "Proxy banned. Switiching.")
                    self.screenlock.release()
                    self.getProxy()
                else:
                    self.screenlock.acquire()
                    print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.CYAN +  "Unknown response while entering. Check text file")
                    self.screenlock.release()
                    with open("Failed to enter - {}.json".format(self.email),'w') as outfile:
                        print(json.dumps(response, indent=2), file=outfile)
                    
                    self.logging_data["error"] = True
                    self.logging_data["error_msg"] = "Unknown error"
                    self.logging_data["app"]["cookies"] = json.dumps(self.session.cookies.get_dict())
                    return


            except requestsExceptions.ConnectTimeout:
                self.screenlock.acquire()
                print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.MAGENTA +  "Connection timedout.")
                self.screenlock.release()
                continue
            except requestsExceptions.ProxyError:
                self.screenlock.acquire()
                print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.MAGENTA +  "Proxy error.")
                self.screenlock.release()
                self.getProxy()
                continue
            
            except Exception as e:
                self.screenlock.acquire()
                print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.RED +  'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), Fore.RED + "{}".format(type(e).__name__), Fore.RED + "{}".format( e))
                self.screenlock.release()
                self.getProxy()
                continue

    def getProxy(self):
        # Load proxy from file
        with open(self.PATH_PROXIES, "r") as file:
            proxies = file.readlines()
        if len(proxies) > 0:
            line = proxies[random.randint(0, len(proxies) - 1)].strip("\n").split(":")
            if len(line) == 2: #if proxy length is ==2, its an IP Auth proxy
                line = proxies[random.randint(0, len(proxies) - 1)].strip("\n")
                proxy= {
                    'http':line,
                    'https':line,
                    }
            
            else:#if proxy length is anything else, its an USER:PASS
                proxy = {'http': 'http://' + line[2] + ":" + line[3] + "@" + line[0] + ":" + line[1] + "/",
                        'https': 'https://' + line[2] + ":" + line[3] + "@" + line[0] + ":" + line[1] + "/"}
            self.session.proxies.update(proxy)
        return

    @staticmethod
    def encode(string):
        return urllib.parse.quote(string)

    @staticmethod
    def getPayload(lotteryID, captchaType, captchaToken, PRODUCTS_TO_ENTER):
        return {
            "LoginToken":"",
            "LotteryID":lotteryID,
            "LotteryInfos":PRODUCTS_TO_ENTER,
            "version":captchaType,
            "token":captchaToken,
            # This URL is typically static. Feel free to change it to another Shuffle URL
            "url":"https://www.newegg.com/product-shuffle?template=1&cm_sp=Promo_Banner-_-mobile_promo_shuffle-_-%252f%252fc1.neweggimages.com%252fnewegg%252ftool%252fshuffle_promo_banner.jpg&icid=612023"
        }