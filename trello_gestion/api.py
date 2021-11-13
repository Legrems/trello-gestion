from . import settings
from .decorators import debug_verbose


import json
import os
import re
import requests
import urllib.parse
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tqdm import tqdm


ALLOWED_RESOURCES = [
    "board",
    "cards", 
    "checklists", 
    "labels", 
    "lists", 
]


class TrelloApi:

    @classmethod
    @debug_verbose(False)
    def url(self, resource_type, *args, **kwargs):

        if resource_type not in ALLOWED_RESOURCES:
            raise ValueError("Wrong resource type: {}".format(resource_type))

        return "{}/{}?{}".format(
            settings.TRELLO_API_URL.rstrip("/"),
            "{}/{}".format(resource_type, "/".join(args)),
            urllib.parse.urlencode({
                "key": settings.TRELLO_API_KEY,
                "token": settings.TRELLO_TOKEN,
                **kwargs,
            })
        )

    @classmethod
    @debug_verbose(True, lambda x: '')
    def get_board(cls, board_id, *args, **kwargs):

        return requests.get(cls.url(
            "board",
            board_id,
            *args,
            **kwargs,
            cards="all",
            labels="all",
            lists="all",
            members="all",
        )).json()

    @classmethod
    @debug_verbose(True, lambda x: '')
    def delete(cls, resource_type, resource_id):
        return requests.delete(cls.url(resource_type, resource_id)).json()

    @classmethod
    @debug_verbose(True, lambda x: '')
    def update_card(cls, card_id, *args, **kwargs):
        return requests.put(cls.url('cards', card_id, *args, **kwargs))


class Board:

    def __init__(self, name, board_settings, *args, **kwargs):
        self.name = name
        self.board_settings = board_settings
        self.board_id = self.board_settings["board_id"]
        self.start_date = datetime.fromisoformat("{}{}".format(self.board_settings["start_date"], settings.TIMEZONE))

        self.label_todo = None

    def build_labels(self, card_labels):

        label_to_keep = []

        if self.label_todo:
            label_to_keep.append(self.label_todo["id"])

        delta_options = {}
        for label in card_labels:

            delta_type = None

            if "heure" in label["name"].lower():
                delta_type = "hours"
            
            elif "jour" in label["name"].lower():
                delta_type = "days"

            elif "semaine" in label["name"].lower():
                delta_type = "weeks"

            elif "mois" in label["name"].lower():
                delta_type = "months"

            if "logistique" in label["name"].lower():
                label_to_keep.append(label["id"])

            # If it is a time-label
            if delta_type:

                amount = int(re.search("^[0-9]*", label["name"])[0])

                if "avant" in label["name"].lower():
                    delta_options[delta_type] = -amount

                else:
                    delta_options[delta_type] = amount

                label_to_keep.append(label["id"])

        return ",".join(label_to_keep), delta_options

    def restore(self, update_labels=False, update_duedate=False, fake=True, specific_card_names=[], *args, **kwargs):

        self.board = TrelloApi.get_board(self.board_id, *args, **kwargs)
        print("Restoring Board {} ...".format(self.board["name"]))

        print("Searching \"TODO\" label ...")
        for label in tqdm(self.board["labels"]):
            if kwargs.get("verbose"):
                print(label)
            if "todo" in label["name"].lower():
                self.label_todo = label

                if kwargs.get("verbose"):
                    print("todo in", label)

        if not self.label_todo:
            print("No \"TODO\" label found, skipping")

        print("Updating all the {} cards ...".format(len(self.board["cards"])))
        for card in tqdm(self.board["cards"]):

            if specific_card_names and card["name"].lower() not in specific_card_names:
                continue

            card_labels, date_options = self.build_labels(card["labels"])

            card_options = {
                "closed": "false",
                "idList": card["idList"],
            }

            if update_labels:
                card_options["idLabels"] = card_labels

            if update_duedate:
                card_options["due"] = (self.start_date + relativedelta(**date_options)).isoformat() if date_options else 'null'

            if kwargs.get("verbose") or True:
                print(card["name"])
                print(card_options)

            if not fake:
                r = TrelloApi.update_card(card["id"], **card_options)
                if r.status_code != 200:
                    print(r.text)
                    raise Exception

        print("Board restored !")
            

