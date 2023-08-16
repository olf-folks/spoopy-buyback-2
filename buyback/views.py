# Create your views here.
from django.http import Http404
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from .forms import ItemForm
import re
from .models import EveItemTax  # Import your model
from typing import List
import logging

logger = logging.getLogger(__name__)


# jake
def parse_user_input(form_data):
    lines = form_data.strip().split('\n')
    parsed_input = []
    default_quantity = 1
 
    for line in lines:
        parts = line.split('\t') # split line at first tab
        item_name = parts[0].strip() # get name out of line
 
        if len(parts) > 1:
            quantity = parts[1].strip() # get quantity
            quantity = quantity.replace(',', '') # remove commas
            quantity = quantity.replace('.', '') # non us money format
        else: # if the line dose not have more than 1 parts or is seperated with spaces
            # Check if the line has a quantity by splitting at spaces
            item_parts = item_name.split() # what is this doing?
            if len(item_parts) > 1 and item_parts[-1].isdigit():
                quantity = item_parts[-1] #?
                quantity = quantity.replace(',', '') # remove commas
                quantity = quantity.replace('.', '') # non us money format
                item_name = " ".join(item_parts[:-1]) # what is this doing?
            else:
                quantity = default_quantity # if there is no quanity eg: unpackaged items are 1
        
        if len(str(quantity)) < 1:
            quantity = default_quantity
 
        quantity = int(quantity)
 
        parsed_input.append({
            'name': item_name,
            'quantity': quantity,
        })
 
    return parsed_input

def calculate_buyback_price(item_price, tax_rate):
    tax_deci = tax_rate / 100
    buyback_price = item_price * tax_deci
    return buyback_price

def get_tax_rate_from_database(item_id):
    try:
        tax_entry = EveItemTax.objects.get(type_id=item_id)
        # return tax_entry.jita_buy_percentage / 100.0  # Convert percentage to decimal
        return tax_entry.jita_buy_percentage  # dont Convert percentage to decimal
    except EveItemTax.DoesNotExist:
        return 0.0  # Default tax rate if item not found

def get_flat_rate_from_database(item_id):
    try:
        tax_entry = EveItemTax.objects.get(type_id=item_id)
        
        flat_cost_str = str(tax_entry.flat_cost)
        flat_cost_cleaned = flat_cost_str.replace(',', '')  # Remove commas
        
        if flat_cost_cleaned.isdigit():
            return int(flat_cost_cleaned)
        else:
            return 0  # Default tax rate if not a valid integer
    except EveItemTax.DoesNotExist:
        return 0  # Default tax rate if item not found

def get_haul_fee_bool_from_database(item_id):
    try:
        haul_fee_entry = EveItemTax.objects.get(type_id=item_id)
        # return tax_entry.jita_buy_percentage / 100.0  # Convert percentage to decimal
        return haul_fee_entry.hauling_fee  
    except EveItemTax.DoesNotExist:
        return False # Default to False not found

def getqtys(parsed_user_input):
    qtys = [] 
    for item in parsed_user_input:
        quantity = item['quantity']
        qtys.append(quantity)

    return qtys  # Move the return statement outside the loop

def generate_api_input(parsed_user_input):
    string = ""
    for item in parsed_user_input:
        name = item['name']
        quantity = item['quantity']
        space = " "
        ret = "\n"
        string = string + name + space + str(quantity) + ret
    return string  # Move the return statement outside the loop

def index(request):
    haul_fee_rate_sv = 200 # set value is 200 ISK per m3
    debug = []
    info_right = 2
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            raw_user_input = form.cleaned_data['item_name']  # Get the input text from the form
            parsed_user_input = parse_user_input(raw_user_input)

            logger.debug("parsed_user_input: %s", parsed_user_input)
            api_input = generate_api_input(parsed_user_input)
            quantity = getqtys(parsed_user_input)
            logger.debug("apiinput: %s", api_input)
            janiceurl = 'https://janice.e-351.com/api/rest/v2/pricer?market=2'
            janiceheaders = {"accept": "application/json", "X-ApiKey": "G9KwKq3465588VPd6747t95Zh94q3W2E", "Content-Type": "text/plain"}
            janiceresponse = requests.post(janiceurl, api_input, headers=janiceheaders)
            api_data = janiceresponse.json()
            logger.debug("api_data: %s", api_data)

            # make list of dicts that combines api_data + tax_rate + api_input \\ need to add: hauling fee ###
            processed_items = []
            for item in parsed_user_input:
                
                item_name = item['name']
                item_name_lower = item_name.lower()

                quantity = item['quantity']
                item_data = next((api_item for api_item in api_data if api_item['itemType']['name'].lower() == item_name_lower), None)
            
                if item_data:
                    
                    item_id = item_data['itemType']['eid']
                    item_volume = item_data['itemType']['volume']                    
                    haul_bool = get_haul_fee_bool_from_database(item_id)
                    logger.debug("Is fee for haul?: %s", haul_bool)
                    if haul_bool == True:
                        total_item_vol = item_volume * quantity
                        haul_fee = haul_fee_rate_sv * total_item_vol
                    else:
                        haul_fee = 0
                    logger.debug("haul fee is: %s", haul_fee)
                    tax_deci = get_tax_rate_from_database(item_id)
                    tax_rate = tax_deci * 100
                    flat_rate = get_flat_rate_from_database(item_id)
                    logger.debug("type for flat_rate is: %s", flat_rate)
                    prembuyback_price = calculate_buyback_price(item_data['immediatePrices']['buyPrice5DayMedian'], tax_rate)
                    buyback_price = prembuyback_price + haul_fee
                    logger.debug("bb before flat rate price is: %s", buyback_price)
                    if flat_rate != 0:
                        buyback_price = flat_rate
                    logger.debug("bb price after flat rate price is: %s", buyback_price)
                    buyback_price_itemtotal = quantity * buyback_price
                    market_price = item_data['immediatePrices']['buyPrice5DayMedian']
                    market_price_itemtotal = quantity * market_price
                    processed_items.append({
                        'item_id': item_id,
                        'item_name': item_name,
                        'quantity': quantity,
                        'tax_rate': tax_rate,
                        'buyback_price': buyback_price,
                        'market_price': market_price,
                        'buyback_price_itemtotal': buyback_price_itemtotal,
                        'market_price_itemtotal': market_price_itemtotal,
                        'haul_bool': haul_bool,
                        'item_volume': item_volume,
                        'haul_fee': haul_fee,
                        
                    })  # Include the processed item data
            logger.debug("processed_items: %s", processed_items)
            gtotal_market = sum(item.get('market_price_itemtotal', 0) for item in processed_items)
            logger.debug("gtotal_market: %s", gtotal_market)
            gtotal_buyback = sum(item.get('buyback_price_itemtotal', 0) for item in processed_items)
            logger.debug("gtotal_buyback: %s", gtotal_buyback)
            if gtotal_market != 0 and gtotal_buyback !=0:
                geff_drate = gtotal_buyback / gtotal_market
                geff_rate = geff_drate * 100
            else:
                geff_rate = 0 
            totals_info = [gtotal_buyback, gtotal_market, geff_rate]           
            debug = [api_data]
            debugtog = False
            return render(request, 'buyback/index.html', {'form': form,'processed_items': processed_items, 'totals_info':totals_info, 'debugtog': debugtog, 'debug': debug, 'info_right': info_right})
    else:
        form = ItemForm()
        info_right = 1
    return render(request, 'buyback/index.html', {'form': form, 'debug': debug, 'info_right': info_right})

def all_item_tax_view(request):
    all_items = EveItemTax.objects.all()
    return render(request, 'buyback/all_item_tax.html', {'all_items': all_items})


def collapsible_tree_view(request):
    categories = {}
    items = EveItemTax.objects.all()

    for item in items:
        category_id = item.category_id
        group_id = item.group_id
        item_id = item.taxid
        if category_id not in categories:
            categories[category_id] = {
                'name': item.category_name,
                'groups': {},
            }

        if group_id not in categories[category_id]['groups']:
            categories[category_id]['groups'][group_id] = {
                'name': item.group,
                'items': [],
            }

        categories[category_id]['groups'][group_id]['items'][item_id].append(item)

    return render(request, 'buyback/collapsible_tree.html', {'categories': categories})

def update_inventory(request):
    all_items = EveItemTax.objects.all()
    return render(request, 'buyback/update_inventory.html', {'all_items': all_items})
update_inventory