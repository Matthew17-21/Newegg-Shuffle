global IOS_VERSION
IOS_VERSION = "6.23.0"

global GETURL_HOMEPAGE
GETURL_HOMEPAGE = "https://www.newegg.com/"

global POSTURL_ticketID
POSTURL_ticketID = "https://secure.m.newegg.com//Application/UnifiedLogin/Landingpage"

global v3_sitekey
v3_sitekey = "6LfgV6wUAAAAAJitb3pPw0WP9q8zACyxczUZk-P7"
global v2_sitekey
v2_sitekey = "6Lcv-WUUAAAAAA9hyir8HPKZ44OvDLg1oZqnq_9d"

global PUBLIC_KEY_SIGNATURE
PUBLIC_KEY_SIGNATURE = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0YEMbfbEuUrYV9Y8CrPw\ncfz8O2AbRif5kSZddMSfZdrkvLYN\u002Fu+NxJbNyWshbO0KJGRH\u002FDm5RXEwBjGbYb0n\nf9vUCrAr28xkOwb+CbAMVrIEMmvwqir+Do7PVW0g+bJ0ROvX09wiW7pLS887AjA4\n3jGE2F1wwOv3EqdYhX3eaIniuMKAmLIEvBXpS9ZtJAJL9lB6bfSMkUiwPKwSzzMG\nbDq689Kp7WuZzoKgryTSLPMaU3EvTav2R\u002F+H12UxQsZGnPQ2JDsFUJIBdt7Es5wI\nKJuxuMP8EbfG47eB4ns56iCmg5Gf+9u0yBXwJZVXzrRaRpzMSjt4jL1j6BUQYlMO\n6wIDAQAB\n-----END PUBLIC KEY-----\n"
global PUBLIC_KEY_PASSWORD
PUBLIC_KEY_PASSWORD  = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnMoWEfo0MxvCGBFL\u002FXBY\n0qHGlbo83tJC+SgDhAf2lKCD8f+LqnsncA7NPmpz36RXwR\u002F9vEKc4Op0TqFGTdI2\nc5pUYhdpBw6HNOLYwRvYK8AkfqxOCe88mwohsBpg3rgup+dIOc81cg9mDTAdGSbk\naKye1w8AlSYqJDxVkl4e8W9ZoPRtNDcnfO8qAvwpQJ25iNGD62hwl7IqeBgSk00m\nNQsq96SmSqI58hYwKqN3nKXW5Q7MS0sYByuAC24BYDBTHaE0tGbSkdiHz0aQzvdq\njOI380xQVq55AlEtryz0rnao7vEBOvYtjjMFuSlujeWMO7ij3RPXi0oBtKufjc3W\nYwIDAQAB\n-----END PUBLIC KEY-----\n"


# Desktop  Headers
global HEADERS_getPages
HEADERS_getPages = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en;q=0.9",
    "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": ""
}
global HEADERS_createAccountPOST
HEADERS_createAccountPOST = {
    "accept": "application/json, text/plain, */*",
    'accept-encoding': "gzip, deflate",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://secure.newegg.com",
    "referer": "",
    "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "",
    "x-ua-pki": "ne200508|ne200509"
}

# Mobile Headers

global HEADERS_getCookies
HEADERS_getCookies = {
    "Host": "www.newegg.com",
    "Accept": "application/json",
    "x-login-status": "0",
    "x-client-useragent": f"iPhone Version {IOS_VERSION}",
    "Content-Type": "application/json",
    "User-Agent": f"Newegg iPhone App / {IOS_VERSION}",
    "Accept-Language": "en-us",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}

global HEADERS_getTicketID
HEADERS_getTicketID = {
    "Host": "secure.m.newegg.com",
    "Connection": "close",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Origin": "null",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "X-Requested-With": "com.newegg.app",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate",
    'Accept-Language': "en-US,en;q=0.9",
}

global HEADERS_getFormKeys
HEADERS_getFormKeys = {
    "Host": "secure.newegg.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "",
    "Accept-Language": "en-us",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}

global HEADERS_createAccount
HEADERS_createAccount = {
    "Host": "secure.newegg.com",
    "Accept": "application/json, text/plain, */*",
    "x-ua-pki": "ne200508|ne200509",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-us",
    "Content-Type": "application/json",
    "Origin": "https://secure.newegg.com",
    "User-Agent": "",
    "Connection": "keep-alive",
    "Referer": ""
}

global HEADERS_afterCreate
HEADERS_afterCreate = {
    "Host": "secure.m.newegg.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
    "User-Agent": "",
    "Accept-Language": "en-us",
    "Referer": "",
    "Accept-Encoding": "gzip, deflate"
}