# Newegg Shuffle
Python module(s) to help you with the Newegg raffle

# How to use
```
$ git clone https://github.com/Matthew17-21/Newegg-Shuffle
$ cd Newegg-Raffle
$ pip3 install -r requirements.txt
$ python3 main.py
```
- **Checkout the [file structure](https://github.com/Matthew17-21/Newegg-Shuffle#file-structure) below on how to enter & change data**

# File Structure
### /data
- emails.txt
    * Enter the emails you'd like to create accounts for.
- proxies.txt
    * Proxies that'll be used when creating accounts.
- settings.json

| Key | Type | Description | Options |
| :--:| :---:| :---------: | :-----: |
| output_filename | String | File name where the sessions will be saved | - |
| version | String | Type of captcha you want to solve to create the account | v2 or v3 |
| captcha_solver | String or int | Captcha solving site | Checkout the [documentation.](https://github.com/Matthew17-21/Captcha-Tools#how-to-use) |
| keys | dict | dict containing keys to solving sites | - |
| generate_random | bool | Should the program generate random password. | `true` or `false` |
| choices | array | Array of password choices | - |
| user_agents| array | Array of user-agents for mobile & desktop | - |

### /newegg/*
- Contains the core software code. 

# Creating Accounts
- If you want to create accounts via mobile, change line 93 in `main.py` from `desktop.Create_Account(self, email)` to `mobile.Create_Account(self, email)`
    * And vice versa 
- MAKE SURE YOU STORE YOUR SESSIONS SOMEWHERE (Don't delete the `.log` file)

# Submitting Entries
- In order to submit entries, you must make sure:
    * The program will pull accounts/sessions from the filename that was used to create accounts (`output_filename` in the settings.json file).
    * Your .log file is in the main directory (alongside with `main.py`)
    * Accounts/Sessions are still in the .log file
    * The program will automatically enter on the same platform as the account was created (Desktop or App)
    * MAKE SURE YOU KEEP YOUR SESSIONS (Don't delete the `.log` file)

# Recommendations
1. **MAKE SURE YOU STORE YOUR SESSIONS SOMEWHERE (Don't delete the `.log` file)**
2. Althought not completely necessary, but you should add/delete/randomify events for accertify.
3. Make sure iOS app version is up to date
4. Handle exceptions better
    * There are some exceptions, such as those from [captchatools](https://github.com/Matthew17-21/Captcha-Tools#exceptions), that I did not handle.
5. Use proxies (But they aren't required to run the script)
6. If V2 Recaptcha pops up again, use that over V3


# Notes
- Failed captchas are normal.
- Newegg disabled their V2 Recaptcha for creating accounts, making V3 the only option. Because all 3rd party solvers aren't the best at V3 captchas, there will be lots of failed captchas.
    * I recommend using anticaptcha for V3, but Capmonster & 2Captcha is also available.
- Only tested on Python 3.7
    * *Should* work on other versions, but I can't promise anything.
- This is intended for devs. If you aren't familiar with python, try not to change too much code as it might break something.
- This isn't a reflection of how I actually write code so pls don't judge too hard :joy:
    * I've been writing in Go lately, hence the structure of the whole thing.
- There are lots of ways to make this better, cleaner and better on memory. If I find time, I'll update this repo.


# Maintenance
- This bot is fully functional with success. I won't be working on it much. I'll only work on it when:
    * They make some massive change
    * Have *loads* of free time and can complete the [to do list](https://github.com/Matthew17-21/Newegg-Shuffle#to-do)
- Pull requests are always welcome
- If any issues were to arise, [open an issue](https://github.com/Matthew17-21/Newegg-Shuffle/issues/new)
    * Please incude:
        * Python version
        * Error
        * How to replicate
- You may also contact me on discord - `Matthew#6937` with any questions or concerns

# FAQ
1. Does this work out of the box?
    * Yes, however, you do need change some info.
2. Can I use these accounts for the raffle?
    * Yes.
3. Should I use the mobile or desktop module?
    * Use the same mode you'll be using to enter raffles.
        * Entering raffle via app, use the mobile version to create account.
        * Entering raffle via desktop, use the desktop version to create account.
4. How do I use the captchatools?
    * Checkout the [documentation.](https://github.com/Matthew17-21/Captcha-Tools)

# Success
![Genning](https://i.imgur.com/lvrTp36.png)
![Running](https://i.imgur.com/r8gPUIq.png)
![Success](https://i.imgur.com/8csUoqR.png)

# TO DO 
1. [] Clean up & document code
2. [] Release GUI version
3. [] Maybe a folder for logs?
4. [] Release in Go
5. [] Inherit, don't pass.