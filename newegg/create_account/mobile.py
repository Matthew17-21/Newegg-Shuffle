import requests
from requests import exceptions as requestsExceptions
import sys
import time
import json
import random
import string
from bs4 import BeautifulSoup
import logging
import colorama
from colorama import Fore, Back, Style
from colorama import init
colorama.init()
init(autoreset=True)
import threading
import datetime
import names
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from . import static_data, Accertify

POSTURL_ticketID = "https://secure.m.newegg.com//Application/UnifiedLogin/Landingpage"



class Create_Account:
    def __init__(self, NeweggParent:object, email):
        self.screenlock = NeweggParent.screenlock
        self.captcha_solver = NeweggParent.captcha_solver

        # Define basic info
        self.current_task = email
        self.email = email
        self.logging_data = {}

        if NeweggParent.settings["password"]["generate_random"]:
            self.password = self.randompassword()
        else:
            self.password = random.choice(NeweggParent.settings["password"]["choices"])

        # Define Headers
        self.session = requests.Session()
        self.HEADERS_getCookies = static_data.HEADERS_getCookies
        self.HEADERS_getTicketID = static_data.HEADERS_getTicketID
        self.HEADERS_getFormKeys = static_data.HEADERS_getFormKeys
        self.HEADERS_createAccount = static_data.HEADERS_createAccount
        self.HEADERS_afterCreate = static_data.HEADERS_afterCreate

    def start(self):
        self.getProxy()
        self.get_ticket_id()
        if self.create_account():
            self.get_cookies()
        return self.logging_data

    def get_ticket_id(self):
        while True:
            try:
                # Get Cookies
                self.screenlock.acquire()
                print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.YELLOW +  "Getting Ticket ID...")
                self.screenlock.release()
                GETURL_getCookies = "https://www.newegg.com/mycountry?CompanyCode=1003&CountryCode=USA&LanguageCode=en-US&RegionCode=USA&t={}".format(round(time.time()))
                self.session.get(GETURL_getCookies, headers=self.HEADERS_getCookies)



                # Get Ticket ID
                payload = "Payload=%7B%22enableGustCheckout%22%3Afalse%2C%22regionCode%22%3A%22USA%22%2C%22LastLoginName%22%3A%22%22%2C%22themeStyle%22%3A0%2C%22userState%22%3A%22%7B%5C%22APPType%5C%22%3A%5C%22ios%5C%22%2C%5C%22path%5C%22%3A%5C%22SignUp%5C%22%7D%22%7D"
                resp = self.session.post(POSTURL_ticketID, headers=self.HEADERS_getTicketID, data=payload, allow_redirects=False)
                self.ticketURL = resp.text.split('"')[1]
                self.ticketID = self.ticketURL.split("tk=")[1]
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
                #self.getProxy()
                continue

    def create_account(self):
        POSTURL_createAccount = f"https://secure.newegg.com/identity/api/SignUp?ticket={self.ticketID}"
        GETURL_tokenData = f"https://secure.newegg.com/identity/api/InitSignUp?ticket={self.ticketID}"
        self.HEADERS_createAccount["Referer"] = self.ticketURL
        self.HEADERS_afterCreate["Referer"] = self.ticketURL
        
        while True:
            try:
                # Get Form ID for payload
                self.screenlock.acquire()
                print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.YELLOW +  "Getting keys for payload...")
                self.screenlock.release()
                signUpPage = self.session.get(self.ticketURL, headers=self.HEADERS_getFormKeys)
                parsedJSON = json.loads(signUpPage.text.split("window.__initialState__ = ")[1].split('</script>')[0])
                soup = BeautifulSoup(signUpPage.text, 'html.parser')
                Tokens = soup.findAll("input")
                firstName_key = Tokens[0].get("name")
                lastName_key = Tokens[1].get("name")
                email_key = Tokens[2].get("name")
                password_key = Tokens[-2].get("name")
                fuzzyChain = parsedJSON["resp"]["FuzzyChain"]
                
                # Get Payload
                self.screenlock.acquire()
                print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.YELLOW +  "Waiting on a captcha token...")
                self.screenlock.release()
                captcha_answer = self.captcha_solver.get_token()
                accertifyFingerprint = Accertify.get_payload(self.ticketURL)
                payload = self.get_payload(self.email, firstName_key, lastName_key, email_key, password_key, fuzzyChain, accertifyFingerprint, captcha_answer)
                response = self.session.post(POSTURL_createAccount, json=payload, headers=self.HEADERS_createAccount)
                
                # Parse Responses
                while "ReCaptchaFailed" in response.text:
                    self.screenlock.acquire()
                    print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.YELLOW +  "Captcha failed. Waiting on a captcha token...")
                    self.screenlock.release()

                    # Get new token and submit
                    captcha_answer = self.captcha_solver.get_token()
                    response = self.session.get(GETURL_tokenData, headers=self.HEADERS_createAccount).json()
                    payload["RecaptchaResponse"] = captcha_answer
                    response = self.session.post(POSTURL_createAccount, json=payload, headers=self.HEADERS_createAccount)
                
                responseJSON = json.loads(response.text)
                if responseJSON["Result"] == "Success":
                    self.GETURL_callBackURL = responseJSON["CallbackPage"]
                    return True
                
                elif responseJSON["Result"] == "ServiceError":
                    self.screenlock.acquire()
                    print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.CYAN +  "Service Error. Restarting.")
                    self.screenlock.release()
                
                elif responseJSON["Result"] == "TicketExpired":
                    self.screenlock.acquire()
                    print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.CYAN +  "Ticket expired. Getting new one.")
                    self.screenlock.release()
                    self.session.cookies.clear()
                    self.get_ticket_id()

                elif "CustomerAddLoginNameDuplicate" in response.text:
                    self.screenlock.acquire()
                    print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.CYAN +  "Email already had an account. Stopping.")
                    self.screenlock.release()
                    self.logging_data = {"error":"Already Had Account"}
                    return False

                else:
                    self.screenlock.acquire()
                    print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.CYAN +  "Unknown erorr. Check file.")
                    self.screenlock.release()
                    with open("Unknown error creating account.json",'w') as outfile:
                        print(json.dumps(responseJSON, indent=2), file=outfile)
                    self.logging_data = {"error":"UNKNOWN ERROR"}
                    return False
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
                continue

    def getProxy(self):
        # Load proxy from file
        with open("./data/proxies.txt", "r") as file:
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

    def get_cookies(self):
        '''
        This methods gets the signed-in cookies once the account is created
        '''
        self.screenlock.acquire()
        print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.YELLOW +  "Created account. Getting cookies...")
        self.screenlock.release()
        while True:
            try:
                response = self.session.get(self.GETURL_callBackURL, headers=self.HEADERS_afterCreate)
                jsonData = json.loads(response.text.split("JSON.stringify(")[1].split("))")[0])



                # Export the cookies for logging
                loginToken = jsonData["LoginToken"]
                self.logging_data = {
                    "password": self.password,
                    "first_name": self.firstname,
                    "last_name": self.lastname,
                    "phone": self.phoneNumber,
                    "desktop": {}, "app": {"login_token":loginToken,"cookies": self.session.cookies.get_dict(), "misc": jsonData }
                }
                self.screenlock.acquire()
                print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.GREEN +  f"Successfully created account for {self.email}!")
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
                self.screenlock.acquire()
                print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.RED +  'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), Fore.RED + "{}".format(type(e).__name__), Fore.RED + "{}".format( e))
                self.screenlock.release()
                #self.getProxy()
                continue

    def get_payload(self,email,firstNameKey,lastNameKey,emailKey,password_key,fuzzyChain, AccertifyPayload, captchaToken):
        self.phoneNumber = str(''.join(random.choices(string.digits, k=10)))
        self.firstname = names.get_first_name()
        self.lastname =  names.get_last_name()
            
        return {
            firstNameKey : self.firstname,
            lastNameKey :self.lastname,
            emailKey : email,
            "MobilePhoneNumber":self.phoneNumber,
            password_key:self.encrypt_data(self.password, static_data.PUBLIC_KEY_PASSWORD),
            "AllowEmail":False,
            "RecaptchaResponse":captchaToken,
            "TextCode":"",
            "FuzzyChain":fuzzyChain,
            "S": self.encrypt_data(  f"S:SignUp:{email}|{self.password}", static_data.PUBLIC_KEY_SIGNATURE ),
            "AccertifyIdentityInfo": AccertifyPayload
        }
    
    @staticmethod
    def encrypt_data(dataToEncrypt, public_key):
        cipher = Cipher_pksc1_v1_5.new(RSA.importKey(public_key))
        cipher_text = base64.b64encode(cipher.encrypt(dataToEncrypt.encode()))
        return cipher_text.decode()

    @staticmethod
    def randompassword():
        specialChars = "!@#$%^&*()_+~"
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        size = random.randint(8, 12)
        return ''.join(random.choice(chars) for x in range(size)) + ''.join(random.choice(specialChars) for x in range(3))