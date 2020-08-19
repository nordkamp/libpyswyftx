"""libpyswyftx.py v0.1: Python 3 bindings for the Swyftx web API
The GNU Public License (GPL) version 3.0 applies to this module and all other modules
written as a part of this software.

Copyright (C) 2020 Matthew Hoffman

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>."""

__author__ = "Matthew Hoffman"
__copyright__ = "Copyright 2020, Matthew Hoffman"
__credits__ = ["Matthew Hoffman"]
__version__ = "0.1"

from json import dumps
from requests import get, post

SUPPORTED_STANDARDS = ("AUD", "USD", "BTC")
SUPPORTED_COMPARISON_EXCHANGES = ("swyftx", "coinspot")

ROUTE_BASE = "https://api.swyftx.com.au/"

ROUTE_ORDERS = "orders/"
ROUTE_EXCHANGE_PAIRS = f"{ROUTE_ORDERS}rate/"

ROUTE_ACC_BALANCES = "user/balance/"
ROUTE_SET_CRNCY = "user/currency/"

ROUTE_WITHDRWL_LIMIT = "limits/withdrawal/"
ROUTE_DETAILED_INFO = "markets/info/detail/"

ROUTE_MESSAGES_LATEST = "messages/latest/"
ROUTE_ANNOUNCEMENTS_LATEST = "messages/announcements/"

ROUTE_INFO = "info/"
ROUTE_COMPARISON = "compare/"

ASSET_ID_LOOKUP = {
    "AUD": "1",
    "BTC": "3",
    "USD": "36"
}

ACC_TKN = ""
HEADERS = {
    "Content-Type": "application/json",
    'Authorization': f'Bearer {ACC_TKN}',
}

def main():
    """Alert the user to import instead of run directly."""
    print("This library is not meant to be run directly. Please import into your program instead.")

def get_account_balance():
    """Returns account balance as a json."""
    return get(f"{ROUTE_BASE}{ROUTE_ACC_BALANCES}", headers=HEADERS).json()

def get_withdrawal_limits():
    """Returns withdrawal limits as a json."""
    return {key:float(value) for (key, value) in \
        get(f"{ROUTE_BASE}{ROUTE_WITHDRWL_LIMIT}", headers=HEADERS).json()["limits"].items()}

def set_currency(asset):
    """Sets the default currency for the user, if that currency is supported.
    Parameters:
        asset (str): 3 letter asset code to change to. See SUPPORTED_ASSETS constant for values."""
    if asset not in SUPPORTED_STANDARDS:
        raise Exception("Unsupported currency! No changes were made.")
    return post(f"{ROUTE_BASE}{ROUTE_SET_CRNCY}", headers=HEADERS,\
        data=dumps({"profile": {"defaultAsset": ASSET_ID_LOOKUP[asset]}})).text

def get_orders(asset):
    """Returns all placed orders.
    Parameters:
        asset (str): 3 letter asset code to get orders for."""
    return get(f"{ROUTE_BASE}{ROUTE_ORDERS}{asset}", headers=HEADERS).json()["orders"]

def place_order(asset, standard, amount, target_price):
    """Place an order on Swyftx.
    Parameters:
        asset (str): 3 letter asset code to purchase
        standard (str): 3 letter standard currency to buy with
        amount (int): Integer value of standard to buy asset with
        target_price (int): Target price to buy at"""
    return post(f"{ROUTE_BASE}{ROUTE_ORDERS}", headers=HEADERS,\
        data=dumps({"primary":f"{standard}","secondary":f"{asset}","assetQuantity":f"{standard}",\
            "orderType":1,"quantity":amount,"trigger":f"{target_price}"})).text

def get_buy_price(asset, standard):
    """Returns the price of an asset relative to a standard. See SUPPORTED_STANDARDS
    constant for standards.
    Parameters:
        asset (str): 3 letter asset code to get the price relative to standard for.
        standard (str): 3 letter standard code used to evaluate the price of the asset."""
    return float(post(f"{ROUTE_BASE}{ROUTE_EXCHANGE_PAIRS}",\
        headers=HEADERS, data=dumps({"buy": f"{asset}", "sell": f"{standard}"}), timeout=2).json()["price"])

def get_sell_price(asset, standard):
    """Returns the selling price of an asset relative to a standard. See SUPPORTED_STANDARDS
    constant for standards.
    Parameters:
        asset (str): 3 letter asset code to get the selling price relative to standard for.
        standard (str): 3 letter standard code used to evaluate the selling price of the asset."""
    # Do simple mathematics to convert the asset into the standard based on value from API.
    return 1 / float(post(f"{ROUTE_BASE}{ROUTE_EXCHANGE_PAIRS}",\
        headers=HEADERS, data=dumps({"buy": f"{standard}", "sell": f"{asset}"}), timeout=2).json()["price"])

def get_detailed_info(asset):
    """Returns a dump of detailed info as a json.
    Parameters:
        asset (str): 3 letter asset code to get detailed info for"""
    return get(f"{ROUTE_BASE}{ROUTE_DETAILED_INFO}{asset}").json()

def get_messages(limit=""):
    """Returns latest messages as a json.
    Parameters:
        limit (int) or (str): Number of messages to limit output to"""
    return get(f"{ROUTE_BASE}{ROUTE_MESSAGES_LATEST}{limit}", headers=HEADERS).json()

def get_announcements(limit=""):
    """Returns latest announcements as a json.
    Parameters:
        limit (int) or (str): Number of messages to limit output to"""
    return get(f"{ROUTE_BASE}{ROUTE_ANNOUNCEMENTS_LATEST}{limit}", headers=HEADERS).json()

def get_info():
    """Returns API info as a json."""
    return get(f"{ROUTE_BASE}{ROUTE_INFO}", headers=HEADERS).json()

def compare_exchange(exchange):
    """Returns comparison prices for a supported exchange as a json."""
    if exchange.lower() not in SUPPORTED_COMPARISON_EXCHANGES:
        raise Exception("Unsupported exchange!")
    return get(f"{ROUTE_BASE}{ROUTE_COMPARISON}{exchange.lower()}").json()

if __name__ == "__main__":
    main()
