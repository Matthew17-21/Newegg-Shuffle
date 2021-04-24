import base64
import random
import time
import string
import urllib.parse
import json


def get_payload(signupURL):
    UBASessionID = generate_uba_sessionID()
    pageID = random.randint(1000000000000000, 9999999999999999)
    events = get_events(signupURL, pageID, UBASessionID)

    return {
        "eventSource":"web", # <--- Static
        "deviceTransactionID":"NEWEGG{}".format(''.join(random.choices(string.digits, k=21))), #Accertify2.js
        "uBAID": ''.join(random.choices(string.ascii_lowercase + string.digits, k=36)), #Accertify2.js <---- Need to find how to scrape beacon 
        "uBAEvents":events,
        "uBASessionID":UBASessionID,
        "pageID":pageID
    }


def generate_uba_sessionID():
    temp = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    temp2 = ""
    t = round(time.time()) * 1000
    for _ in range(len(temp)):
        e = int((t + 16 * random.uniform(0, 1)) % 16) | 0
        temp2 += hex(e)[2:]
    return temp2

def get_events(singupURL, pageID, sessionID):
    timeMS = round(time.time() * 1000)
    timeMS2 = round(time.time() * 1000)
    EVENTS = [
        {
            "loc":singupURL,
            "pid":pageID,
            "sid":None,
            "bsid":sessionID,
            "ts":timeMS,
            "type":"mtrk",
            "pay":{
                "t":timeMS,
                "fd":1044.27,
                "sd":1557.69,
                "bb":[
                    random.randint(500,800),
                    random.randint(100,300),
                    random.randint(1000,1400),
                    random.randint(100,300)
                ],
                "s":[
                    {
                    "t":0,
                    "x":1324,
                    "y":274,
                    "fd":945.72,
                    "sd":829.03,
                    "c":15,
                    "a":9139.97,
                    "mx":119066.74,
                    "mn":62.5
                    },
                    {
                    "t":260,
                    "x":771,
                    "y":613,
                    "fd":652.69,
                    "sd":648.64,
                    "c":24,
                    "a":2455.57,
                    "mx":8766.41,
                    "mn":90.91
                    },
                    {
                    "t":551,
                    "x":769,
                    "y":693,
                    "fd":80.32,
                    "sd":80.02,
                    "c":22,
                    "a":330.8,
                    "mx":1004.99,
                    "mn":83.33
                    }
                ],
                "c":50,
                "sc":3
            }
        },
        {
            "loc":singupURL,
            "pid":pageID,
            "sid":None,
            "bsid":sessionID,
            "ts":timeMS2,
            "type":"mclk",
            "pay":{
                "t":timeMS2,
                "m":{
                    "_":[
                    {
                        "t":0,
                        "b":0,
                        "x":random.randint(500,800),
                        "y":random.randint(500,800)
                    }
                    ]
                },
                "c":1
            }
        },
        {
            "loc":singupURL,
            "pid":pageID,
            "sid":None,
            "bsid":sessionID,
            "ts":round(time.time() * 1000),
            "type":"meta",
            "pay":{
                "t":round(time.time() * 1000),
                "m":{
                    "_":{
                    "i":None,
                    "n":None,
                    "t":"submit"
                    }
                }
            }
        }
    ]

    # Start time will be a time before the current time to make it seem more real
    # The ragne will be between 30s-60s
    start = round(time.time()) - random.randint(30,60)
    second = start + random.randint(3,10)
    third = second + random.randint(3,10)
    
    startTime = start * 1000
    secondTime = second * 1000
    thirdTime = third * 1000

    # Update Location, timestamp, pid & bsid
    EVENTS[0]["ts"] = startTime
    EVENTS[0]["pay"]["t"] = startTime

    EVENTS[1]["ts"] = secondTime
    EVENTS[1]["pay"]["t"] = secondTime

    EVENTS[2]["ts"] = thirdTime
    EVENTS[2]["pay"]["t"] = thirdTime


    # URL encode raw array
    urlEncoded = encode(str(json.dumps(EVENTS))).encode("utf-8")
    b64Encoded = base64.b64encode(urlEncoded).decode("utf-8")
    semi = {"ts": round( time.time() * 1000 ), "pay": b64Encoded}
    b64Encoded2 = base64.urlsafe_b64encode(json.dumps(semi).encode()).decode()

    semiFinal = {
       "ts":round( time.time() * 1000 ),
       "pays":[
          b64Encoded2,
          None,
          None
       ]
    }
    final = base64.urlsafe_b64encode(json.dumps(semiFinal).encode()).decode()
    return final

def encode(string):
    return urllib.parse.quote(string)
