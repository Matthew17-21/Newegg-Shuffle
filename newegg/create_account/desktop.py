import os
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

from ..utils.get_proxy import return_proxy

colorama.init()
init(autoreset=True)
import threading
import datetime
import names
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from . import static_data, Accertify


class Create_Account:
    def __init__(self, NeweggParent:object, email):
        # I don't like how I'm passing these in. I'm going to change this soon.
        logging.basicConfig(filename=NeweggParent.settings["output_filename"], level=logging.INFO)
        self.screenlock = NeweggParent.screenlock
        self.captcha_solver = NeweggParent.captcha_solver
        self.sema = NeweggParent.sema
        self.PATH_PROXIES  = NeweggParent.PATH_PROXIES

        # Define basic info
        self.current_task = email
        self.email = email
        self.logging_data = {}
        if NeweggParent.settings["password"]["generate_random"]:
            self.password = self.randompassword()
        else:
            self.password = random.choice(NeweggParent.settings["password"]["choices"])

        self.session = requests.Session()
        self.HEADERS_getPages = static_data.HEADERS_getPages.copy()
        self.HEADERS_createAccountPOST = static_data.HEADERS_createAccountPOST.copy()

        # Update Headers
        user_agent = random.choice(NeweggParent.settings["user_agents"]["desktop"])
        self.HEADERS_getPages["user-agent"] = user_agent
        self.HEADERS_createAccountPOST["user-agent"] = user_agent

        self.start()
        


    def start(self):
        self.getProxy()
        self.get_ticket_id()
        if self.create_account():
            self.get_cookies()
        
        logging.info("{}:{}".format(
            self.email,
            json.dumps(self.logging_data)
        ))
        self.sema.release()
        return

    def get_ticket_id(self):
        '''
        The get_ticket_id methods returns an ID that is used in POST URL's to create account
        '''
        self.screenlock.acquire()
        print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.YELLOW +  "Getting Ticket ID...")
        self.screenlock.release()

        while True:
            try:
                response = self.session.get(static_data.GETURL_HOMEPAGE, headers=self.HEADERS_getPages, timeout=15) # Need cookies
                response = self.session.get("https://secure.newegg.com/NewMyAccount/AccountLogin.aspx?nextpage=https%3A%2F%2Fwww.newegg.com%2F", headers=self.HEADERS_getPages, timeout=15)
                self.tkToken = str(response.url).split("tk=")[1]
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
        '''
        The create_account is called once all the info is gather and creates accounts.
        '''
        POSTURL_createAccount = f"https://secure.newegg.com/identity/api/SignUp?ticket={self.tkToken}"
        GETURL_tokenData = f"https://secure.newegg.com/identity/api/InitSignUp?ticket={self.tkToken}"
        GETURL_signUpPage = f"https://secure.newegg.com/identity/signup?tk={self.tkToken}"
        self.HEADERS_createAccountPOST["referer"] = f"https://secure.newegg.com/identity/signup?tk={self.tkToken}"

        self.screenlock.acquire()
        print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.YELLOW +  "Creating account...")
        self.screenlock.release()
        while True:
            try:
                # Get cookies
                self.session.get(GETURL_tokenData, headers=self.HEADERS_getPages, timeout=15)

                # Get Key Forms for sign up
                response = self.session.get(GETURL_signUpPage, headers=self.HEADERS_getPages, timeout=15)
                parsedJSON = json.loads(response.text.split("window.__initialState__ = ")[1].split('</script>')[0]) # <---- Now that im looking at this, should've used Re lmao
                soup = BeautifulSoup(response.text, 'html.parser')
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
                accertifyFingerprint = Accertify.get_payload(GETURL_signUpPage)
                payload = self.get_payload(self.email, firstName_key, lastName_key, email_key, password_key, fuzzyChain, accertifyFingerprint, captcha_answer)
                response = self.session.post(POSTURL_createAccount, json=payload, headers=self.HEADERS_createAccountPOST)

                # Parse Responses
                while "ReCaptchaFailed" in response.text:
                    self.screenlock.acquire()
                    print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.YELLOW +  "Captcha failed. Waiting on a captcha token...")
                    self.screenlock.release()

                    # Get new token and submit
                    captcha_answer = self.captcha_solver.get_token()
                    response = self.session.get(GETURL_tokenData, headers=self.HEADERS_createAccountPOST).json()
                    payload["RecaptchaResponse"] = captcha_answer
                    response = self.session.post(POSTURL_createAccount, json=payload, headers=self.HEADERS_createAccountPOST)
                            
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
                #self.getProxy()
                continue
    
    def get_cookies(self):
        '''
        This methods gets the signed-in cookies once the account is created

        The "NV%5FCUSTOMERLOGIN" cookie is the most important
        '''
        self.screenlock.acquire()
        print(Fore.CYAN + '{}'.format(datetime.datetime.now()),Fore.MAGENTA + "{}".format(self.current_task), Fore.YELLOW +  "Created account. Getting cookies...")
        self.screenlock.release()
        while True:
            try:
                # Go to the Callback URL to complete the sign up process
                self.session.get(self.GETURL_callBackURL, headers=self.HEADERS_createAccountPOST)

                # Export the cookies for logging
                self.logging_data = {
                    "password": self.password,
                    "first_name": self.firstname,
                    "last_name": self.lastname,
                    "phone": self.phoneNumber,
                    "app": {}, "desktop": {"cookies": self.session.cookies.get_dict() }
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

    def getProxy(self):
        self.session.proxies.update(return_proxy())
        return

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