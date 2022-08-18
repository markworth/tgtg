from datetime import datetime
from datetime import timedelta

import json
import requests
from tgtg import TgtgClient

chat_ops = "https://hooks.slack.com/services/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"
console_ops = "https://hooks.slack.com/services/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"

def render_items(items):
    for item in items:
        store = f"{item.get('display_name')} "
        if (item.get('items_available') > 0) and item.get('item').get('item_category') != "GROCERIES":
            the_time = datetime.strptime(item.get('pickup_interval').get('start'), "%Y-%m-%dT%H:%M:%SZ")
            the_end_time = datetime.strptime(item.get('pickup_interval').get('end'), "%Y-%m-%dT%H:%M:%SZ")

            output_time = the_time.strftime("%H:%M")
            output_end_time = the_end_time.strftime("%H:%M")

            if the_time.date() == datetime.today().date():
                store += f"TODAY {output_time} - {output_end_time} ({item.get('items_available')})"
            elif the_time.date() == datetime.today().date() + timedelta(days = 1):
                store += f"TOMORROW {output_time} - {output_end_time} ({item.get('items_available')})"
            else:
                store += the_time.strftime("%a %d %H:%M") + " - " + output_end_time + " (" + item.get('items_available') + ")"

            print(store)
            requests.post(chat_ops, json={"text": store})

            if "Lola" in store or "Worth" in store or "Sushi" in store or "Kreme" in store:
                requests.post(console_ops, json={"text": store})
        else:
            print(store)    

def main(event, context):
    client = TgtgClient(email="markpalmer65@gmx.com", password="Picklepants99")


    items = client.get_items(
        favorites_only=False,
        latitude=51.4389,
        longitude=0.2711,
        radius=2
    )

    render_items(items)

    items = client.get_items(
        favorites_only=False,
        latitude=51.4657023,
        longitude=0.1323916,
        radius=2
    )

    render_items(items)