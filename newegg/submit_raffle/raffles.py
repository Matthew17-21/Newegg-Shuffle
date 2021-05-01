import re
import json
import requests



def get_items():
    temp = []
    while True:
        try:
            s = requests.Session()
            res = s.get("https://www.newegg.com/product-shuffle")
            raffle_products =  json.loads(re.findall(r"{.+[:,].+}", res.text)[1].split("</script>")[0])
            for products in raffle_products["lotteryData"]["LotteryItems"]:
                for raffle_item in products["ChildItem"]:
                    # Get the item(s) in the combo
                    combo_items = [] # Products that you can select to enter the raffle for
                    for item in raffle_item["ComboItems"]:
                        combo_items.append(item["Title"])
                    items_name = " & ".join(combo_items)

                    # Get the ID of the combo/item to enter the raffle & price
                    item_id= raffle_item["ItemNumber"] # This is used to enter the raffle
                    combo_price = raffle_item["FinalPrice"]


                    temp.append({
                        "name": items_name,
                        "id": item_id,
                        "price": combo_price
                    })
            return temp
        except Exception:
            print("[ERROR GETTING RAFFLES]")