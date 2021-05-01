# Use this file as a config

global POSTURL_submitEntry
POSTURL_submitEntry = "https://www.newegg.com/events/api/GoogleRecaptCha"

class App:
    '''
    The attributes in this object is everything needed for App
    '''
    RAFFLE_URL = "https://www.newegg.com/product-shuffle?template=1&cm_sp=Promo_Banner-_-mobile_promo_shuffle-_-%252f%252fc1.neweggimages.com%252fnewegg%252ftool%252fshuffle_promo_banner.jpg&icid=612023"
    HEADERS_general = {
        "Host": "www.newegg.com",
        "Content-Type": "application/json",
        "Origin": "https://www.newegg.com",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "",
        "Accept-Language": "en-us"
    }
    HEADERS_submitEntry = {    
        "Host": "www.newegg.com",
        "Content-Type": "application/json",
        "Origin": "https://www.newegg.com",
        "Accept-Encoding": "gzip, deflate",
        "Cookie" : "", # Certain cookie will distinguish it from the desktop
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "",
        "Referer": RAFFLE_URL,
        "Accept-Language": "en-us"
    }


class Desktop:
    '''
    The attributes in this object is everything needed for Desktop entries
    '''
    RAFFLE_URL = "https://www.newegg.com/product-shuffle"
    HEADERS_general = {
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

    HEADERS_submitEntry = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://www.newegg.com",
        'referer': "https://www.newegg.com/product-shuffle",
        "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        "sec-ch-ua-mobile": '?0',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        'user-agent': ""
    }
