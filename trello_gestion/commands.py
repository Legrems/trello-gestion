from . import settings
from .api import Board, TrelloApi


import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--restore", action="store_true", help="Equivalent to '--labels --duedate'")
parser.add_argument("--verbose", action="store_true", help="Print output for debugging")
parser.add_argument("--duedate", action="store_true", help="Update all duedate for each card")
parser.add_argument("--labels", action="store_true", help="Update label (todo and other) on each card")
parser.add_argument("--confirm", action="store_true", help="Confirm action, required")
parser.add_argument("-n", "--names", nargs="+", default=[])
parser.add_argument("-c", "--cards", nargs="+", default=[])

# No change on this action
parser.add_argument("--list-cards", action="store_true", help="See all the cards in the board")


parser_args = parser.parse_args()


def main():

    board_list = parser_args.names

    if not board_list:
        board_list = settings.BOARDS.keys()

    for board_name in board_list:
        if board_name not in settings.BOARDS:
            print(f"{board_name} board not found, skipped")
            continue

        b = Board(board_name, settings.BOARDS[board_name])

        update_labels = False
        update_duedate = False

        if parser_args.restore:
            update_duedate = True
            update_labels = True
        
        if parser_args.labels:
            update_labels = True

        if parser_args.duedate:
            update_duedate = True
        
        b.restore(
            update_labels=update_labels,
            update_duedate=update_duedate,
            fake=not parser_args.confirm,
            specific_card_names=list(map(lambda x: x.lower(), parser_args.cards)),
            verbose=parser_args.verbose
        )
