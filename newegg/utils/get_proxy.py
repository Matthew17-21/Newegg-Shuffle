import random

from newegg.utils.return_project_root import get_project_root


def return_proxy():
    # Load proxy from file
    with open(f'{get_project_root()}/data/proxies.txt', "r") as file:
        proxies = file.readlines()
    if len(proxies) > 0:
        line = proxies[random.randint(0, len(proxies) - 1)].strip().split(":")
        if len(line) == 2:  # if proxy length is ==2, its an IP Auth proxy
            line = proxies[random.randint(0, len(proxies) - 1)].strip()
            proxy = {
                'http': f'http://{line}',
                'https': f'https://{line}',
            }

        else:  # if proxy length is anything else, its an USER:PASS
            proxy = {'http': 'http://' + line[2] + ":" + line[3] + "@" + line[0] + ":" + line[1] + "/",
                     'https': 'https://' + line[2] + ":" + line[3] + "@" + line[0] + ":" + line[1] + "/"}
    return proxy