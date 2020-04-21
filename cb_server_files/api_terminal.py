# NOTES on API: 
# - This code is more or less a copy from the views_terminal.py file. I'm not sure
# what large parts of the models do, so better to play it safe.
#
# - Security is handled with a token that's set locally within the Electron App's ENV 
# and in the server. Currently, I'm just letting all requests from any origin go to a
# handler which will check for the existence of the correct token and refuse the
# request otherwise. There's probably a better way of doing this with cookies or something...
#
# - Copied the imports from views_terminal.py entirely.

from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config

from pyramid.i18n import TranslationStringFactory, get_localizer
_ = TranslationStringFactory('betty')

from sqlalchemy.sql import func
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound

from .models import *
from .models.model import *
from .models import user as __user
from .models.user import User
from .models.item import Item
from .models.box import Box
from .models.transaction import Transaction, BTCDeposit, PurchaseLineItem
from .models.account import Account, VirtualAccount, CashAccount
from .models.event import Event
from .models.announcement import Announcement
from .models.btcdeposit import BtcPendingDeposit
from .models.pool import Pool
from .models.tag import Tag
from .models.ephemeron import Ephemeron
from .models.badscan import BadScan

from .utility import user_password_reset
from .utility import send_email

from pyramid.security import Allow, Everyone, remember, forget

import chezbetty.datalayer as datalayer
import transaction

import math


# debt threshold at which emails start to be sent
global debtor_email_theshold
debtor_email_theshold = Decimal(-5.00)

# token used to verify requests to api
global token 
token = 'ABC123'

# headers to return to OPTIONS requests
global options_headers
options_headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST',
    'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Max-Age': '1728000',
}


# custom exception
class DepositException(Exception):
    pass


# fetch data used to render /login
@view_config(
    route_name='api_terminal_login',
    renderer='json',
)
def api_terminal_login(request):
    if request.method == 'OPTIONS':
        request.response.headers.update(options_headers)
        return {}

    request.response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
    })

    if request.method != 'POST':
        request.response.status = 400
        return {'error': 'request-not-post'}

    body = request.json_body

    if body['token'] != token:
        request.response.status = 401
        return {}
    
    announcements = []
    for announcement in Announcement.all_enabled():
        announcements.append(announcement.announcement)

    return {
        'announcements': announcements,
        'debt': str(User.get_amount_owed()),
    }


# helper function for api_terminal_umid()
def terminal_initial(user):
    # if cash was added before a user was logged in, credit that now
    deposit = None
    in_flight_deposit = Ephemeron.from_name('deposit')
    if in_flight_deposit:
        amount = Decimal(in_flight_deposit.value)
        deposit = datalayer.deposit(user, user, amount)
        DBSession.delete(in_flight_deposit)

    # determine initial wall-of-shame fee (if applicable)
    purchase_fee_percent = Decimal(0)
    if user.balance <= Decimal('-5.00') and user.role != 'administrator':
        purchase_fee_percent = 5 + (math.floor((user.balance + 5) / -5) * 5)

    # determine what discounts or fees, if any, to apply
    discount_type = ''
    discount = 0
    if user.role == 'administrator':
        discount_type = 'Admin Discount'
        discount = 20
    else:
        if purchase_fee_percent != 0:
            discount_type = "Debtor's Fee"
            discount = purchase_fee_percent
        elif user.balance > 20:
            discount_type = 'Good Standing Discount'
            if user.role == 'manager':
                discount = 15
            elif user.role == 'volunteer':
                discount = 10
            else:
                discount = 5

    # get list of purchase pools available for user
    tmp = []
    for pool in Pool.all_by_owner(user, True):
        if pool.balance > (pool.credit_limit * -1):
            tmp.append(pool)

    for pu in user.pools:
        if pu.enabled and pu.pool.enabled and pu.pool.balance > (pu.pool.credit_limit * -1):
            tmp.append(pu.pool)

    purchase_pools = {}
    for pool in tmp:
        pool_dict = {
            'id': pool.id,
            'name': pool.name,
            'balance': str(pool.balance),
        }
        purchase_pools[pool.id] = pool_dict


    # get list of tags that have items without barcodes in them
    tag_list = Tag.get_tags_with_nobarcode_items()
    tags_with_nobarcode_items = {}
    for tag in tag_list:
        tag_dict = {
            'id': tag.id,
            'name': tag.name,
        }
        tags_with_nobarcode_items[tag.id] = tag_dict

    # pull list of recently purchased items (ALERT: THIS NEEDS TO BE ADDED FOR FINAL DEMO)
    user_recent_items = user.get_recent_items(limit=5)

    # return terminal data
    return {
        'user_name': user.name,
        'user_balance': str(user.balance),
        'user_umid': user.umid,
        'user_role': user.role,
        'purchase_pools': purchase_pools,
        'discount': discount,
        'discount_type': discount_type,
        'tags_with_nobarcode_items': tags_with_nobarcode_items,
    }


# validate umid then return user data if successful
# inputs: token (str), umid (str), scanned (bool)
@view_config(
    route_name='api_terminal_umid',
    renderer='json',
)
def api_terminal_umid(request):
    # handle preflight header, validate request
    if request.method == 'OPTIONS':
        request.response.headers.update(options_headers)
        return {}

    request.response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
    })

    if request.method != 'POST':
        request.response.status = 400
        return {'error': 'request-not-post'}

    body = request.json_body

    if body['token'] != token:
        request.response.status = 401
        return {}

    # handle request
    if body['scanned']:
        try:
            # check length before trying to fetch umid
            if len(body['umid']) != 8:
                raise __user.InvalidUserException()

            # get user, create if needed
            with transaction.manager:
                user = User.from_umid(body['umid'], create_if_never_seen=True)

            # add user to database / fetch user data
            user = DBSession.merge(user)

            # return special error if user is disabled
            if not user.enabled:
                request.response.status = 400
                return {'error': 'user-not-enabled'}

            # unarchive user if previously archived
            if user.archived:
                if user.archived_balance != 0:
                    datalayer.adjust_user_balance(
                        user,
                        user.archived_balance,
                        'Reinstated archived user.',
                        request.user
                    )
                user.balance = user.archived_balance
                user.archived = False

            # umid checks out, fetch data needed to display terminal
            try:
                request.response.status = 200
                return terminal_initial(user)

            except:
                request.response.status = 400
                return {'error': 'terminal-fetch-failed'}

        except:
            request.response.status = 400
            return {'error': 'user-not-found'}

    # umid entered w/ keypad
    else:
        try:
            # try to fetch user, will throw exception on failure
            user = User.from_umid(body['umid'])

            # check user is valid
            if user.role == 'serviceaccount':
                raise User.InvalidUserException

            # umid checks out, fetch data needed to display terminal
            try:
                request.response.status = 200
                return terminal_initial(user)

            except:
                request.response.status = 400
                return {'errors': 'terminal-fetch-failed'}

        except:
            request.response.status = 400
            return {'error': 'mcard-keypad-error'}


# get all items without barcodes in a tag
# inputs: token (str), tag_id (int)
@view_config(
    route_name='api_terminal_tag',
    renderer='json',
)
def terminal_purchase_tag(request):
    # handle preflight header, validate request
    if request.method == 'OPTIONS':
        request.response.headers.update(options_headers)
        return {}

    request.response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
    })

    if request.method != 'POST':
        request.response.status = 400
        return {'error': 'request-not-post'}

    body = request.json_body

    if body['token'] != token:
        request.response.status = 401
        return {}

    # handle request
    nobarcode_items = {}
    try:
        if body['id'] == 'Other':
            tag = { 'nobarcode_items': Item.get_nobarcode_notag_items()}
            
            for item in tag['nobarcode_items']:
                item_dict = {
                    'id': item.id,
                    'name': item.name,
                    'price': str(item.price),
                }
                nobarcode_items[item.id] = item_dict
        else:
            tag = Tag.from_id(int(body['id']))

            for item in tag.nobarcode_items:
                item_dict = {
                    'id': item.id,
                    'name': item.name,
                    'price': str(item.price),
                }
                nobarcode_items[item.id] = item_dict

    except:
        request.response.status = 400
        return {'error': 'Unable to parse TAG ID'}

    request.response.status = 200
    return nobarcode_items


# handle bill deposits
# inputs: umid (str), token(str), amount (str), method (str)
@view_config(
    route_name='api_terminal_deposit',
    renderer='json',
)
def api_terminal_deposit(request):
    # handle preflight header, validate request
    if request.method == 'OPTIONS':
        request.response.headers.update(options_headers)
        return {}

    request.response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
    })

    if request.method != 'POST':
        request.response.status = 400
        return {'error': 'request-not-post'}

    body = request.json_body

    if body['token'] != token:
        request.response.status = 401
        return {}

    # handle request
    try:
        if body['umid'] == '':
            # User was not logged in when deposit was made. We store
            # this deposit temporarily and give it to the next user who
            # logs in.
            user = None
        else:
            user = User.from_umid(body['umid'])

        amount = Decimal(body['amount'])
        method = body['method']

        if amount <= 0.0:
            raise DepositException('Deposit amount must be greater than $0.00')
        
        # Now check the deposit method. We trust anything that comes from the
        # bill acceptor, but double check a manual deposit
        if method == 'manual':
            # Check if the deposit amount is too great.
            if amount > 2.0:
                # Anything above $2 is blocked
                raise DepositException('Deposit amount of ${:,.2f} exceeds the limit'.format(amount))

        elif method == 'acceptor':
            # Any amount is OK
            pass

        else:
            raise DepositException('"{}" is an unknown deposit type'.format(method))

        # At this point the deposit can go through
        ret = {}

        if user:
            response.response.status = 200
            deposit = datalayer.deposit(user, user, amount, method != 'manual')
            ret['type'] = 'user'
            ret['amount'] = float(deposit['amount'])
            ret['event_id'] = deposit['event'].id
            ret['user_balance'] = float(user.balance)

        else:
            # No one was logged in. Need to save this temporarily
            # total_stored = datalayer.temporary_deposit(amount);
            # ret['type'] = 'temporary'
            # ret['new_amount'] = float(amount)
            # ret['total_amount'] = float(total_stored)

            print('GOT NON-LOGGED IN DEPOSIT')
            print('GOT NON-LOGGED IN DEPOSIT')
            print('GOT NON-LOGGED IN DEPOSIT')
            print('AMOUNT: {}'.format(amount))
            print('IGNORING THIS FOR NOW.')
            request.response.status = 200           
            ret['error'] = 'Must be logged in to deposit'

        return ret

    except __user.InvalidUserException as e:
        request.status.code = 400
        return {'error': 'Error finding user.'}

    except ValueError as e:
        request.status.code = 400
        return {'error': 'Error understanding deposit amount.'}

    except DepositException as e:
        request.status.code = 400
        return {'error': str(e)}

    except Exception as e:
        request.status.code = 400
        return {'error': str(e)}


# helper function to fetch items from db by barcode
def get_item_from_barcode(barcode):
    try:
        item = Item.from_barcode(barcode)
    except:
        # Could not find the item. Check to see if the user scanned a box
        # instead. This could lead to two cases: a) the box only has 1 item in it
        # in which case we just add that item to the cart. This likely occurred
        # because the individual items do not have barcodes so we just use
        # the box. b) The box has multiple items in it in which case we throw
        # an error for now.
        try:
            box = Box.from_barcode(barcode)
            if box.subitem_number == 1:
                item = box.items[0].item
            else:
                return 'Cannot add that entire box to your order. Please scan an individual item.'
        except:
            badscan = BadScan(barcode)
            DBSession.add(badscan)
            DBSession.flush()

            return 'Could not find that item.'

    if not item.enabled:
        return 'That product is not currently for sale.'

    return item


# Get details about an item based on a barcode. This can be used to add to a cart or as a price check.
# inputs: token (str), barcode (str)
@view_config(
    route_name='api_terminal_item_barcode',
    renderer='json',
)
def api_terminal_item_barcode(request):
    # handle preflight header, validate request
    if request.method == 'OPTIONS':
        request.response.headers.update(options_headers)
        return {}

    request.response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
    })

    if request.method != 'POST':
        request.response.status = 400
        return {'error': 'request-not-post'}

    body = request.json_body

    if body['token'] != token:
        request.response.status = 401
        return {}

    # handle request
    item = get_item_from_barcode(body['barcode'])

    if type(item) is str:
        request.response.status = 400
        return {'error': item}

    request.response.status = 200
    return {
        'id': item.id,
        'name': item.name,
        'price': float(item.price),
    }


# Get details about an item based on an item ID. This can be used to add to a cart or as a price check.
# inputs: token (str), item_id (str)
@view_config(
    route_name='api_terminal_item_id',
    renderer='json',
)
def api_terminal_item_id(request):
    # handle preflight header, validate request
    if request.method == 'OPTIONS':
        request.response.headers.update(options_headers)
        return {}

    request.response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
    })

    if request.method != 'POST':
        request.response.status = 400
        return {'error': 'request-not-post'}

    body = request.json_body

    if body['token'] != token:
        request.response.status = 401
        return {}

    # handle request
    try:
        item = Item.from_id(body['item_id'])

    except:
        request.response.status = 400
        return {'error': 'Could not find that item.'}

    if not item.enabled:
        request.response.status = 400
        return {'error': 'That product is not currently for sale.'}

    request.response.status = 200
    return {
        'id': item.id,
        'name': item.name,
        'price': float(item.price),
    }


# Make a purchase from the terminal.
# params: token (str), umid (str), pool_id (int/str, IF SELECTED), item(s)_id (int/str), item(s)_quantity (int)
@view_config(
    route_name='api_terminal_purchase',
    renderer='json',
)
def api_terminal_purchase(request):
    # handle preflight header, validate request
    if request.method == 'OPTIONS':
        request.response.headers.update(options_headers)
        return {}

    request.response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
    })

    if request.method != 'POST':
        request.response.status = 400
        return {'error': 'request-not-post'}

    body = request.json_body

    if body['token'] != token:
        request.response.status = 401
        return {}

    # handle request
    try:
        user = User.from_umid(body['umid'])

        # Bundle all purchase items
        items = {}
        for item_id in body['items']:
            item = Item.from_id(int(item_id))
            items[item] = body['items'][item_id]['amount']

        # What should pay for this?
        # Note: should do a bunch of checking to make sure all of this
        # is kosher. But given our locked down single terminal, we're just
        # going to skip all of that.
        if 'pool_id' in body and body['pool_id'] != None:
            pool = Pool.from_id(int(body['pool_id']))
            purchase = datalayer.purchase(user, pool, items)
        else:
            purchase = datalayer.purchase(user, user, items)

        # Create a order complete view
        order = {
            'total': str(purchase.amount),
            'discount': str(purchase.discount),
            'items': []
        }

        for subtrans in purchase.subtransactions:
            item = {}
            item['name'] = subtrans.item.name
            item['quantity'] = subtrans.quantity
            item['price'] = str(subtrans.item.price)
            item['total_price'] = str(subtrans.amount)
            order['items'].append(item)

        if purchase.fr_account_virt_id == user.id:
            account_type = 'user'
            pool = None
        else:
            account_type = 'pool'
            pool = Pool.from_id(purchase.fr_account_virt_id)

        # Email the user if they are currently in debt
        if float(user.balance) < debtor_email_theshold:
            send_email(
                TO=user.uniqname+'@umich.edu',
                SUBJECT='Please Pay Your Chez Betty Balance',
                body=render('templates/terminal/email_user_in_debt.jinja2',
                {'user': user})
            )

        summary = {
            'user_umid': user.umid,
            'event_id': purchase.event.id,
            'order': order,
            # 'transaction': purchase,
            'account_type': account_type,
            'pool': pool
        }

        # Return the committed transaction ID
        request.response.status = 200
        return {
            'order_table': summary,
            'user_balance': str(user.balance)
        }

    except __user.InvalidUserException as e:
        request.response.status = 400
        return {'error': get_localizer(request).translate(_('invalid-user-error',
                           default='Invalid user error. Please try again.'))
               }

    except ValueError as e:
        request.response.status = 400
        return {'error': 'Unable to parse Item ID or quantity'}

    except NoResultFound as e:
        # Could not find an item
        request.response.status = 400
        return {'error': 'Unable to identify an item.'}


# Delete a just completed purchase.
# params: token (string), umid (str), event_id(str / int)
@view_config(
    route_name='api_terminal_purchase_delete',
    renderer='json',
)
def api_terminal_purchase_delete(request):
    # handle preflight header, validate request
    if request.method == 'OPTIONS':
        request.response.headers.update(options_headers)
        return {}

    request.response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
    })

    if request.method != 'POST':
        request.response.status = 400
        return {'error': 'request-not-post'}

    body = request.json_body

    if body['token'] != token:
        request.response.status = 401
        return {}

    # handle request
    try:
        user = User.from_umid(body['umid'])
        old_event = Event.from_id(body['old_event_id'])

        if old_event.type != 'purchase' or \
           old_event.transactions[0].type != 'purchase' or \
           (old_event.transactions[0].fr_account_virt_id != user.id and \
            old_event.user_id != user.id):
           # Something went wrong, can't undo this purchase
           raise DepositException('Cannot undo that purchase')

        # Now undo old deposit
        datalayer.undo_event(old_event, user)

        request.response.status = 200
        return {'user_balance': float(user.balance)}

    except __user.InvalidUserException as e:
        request.response.status = 400
        return {'error': 'Invalid user error. Please try again.'}

    except DepositException as e:
        request.response.status = 400
        return {'error': str(e)}
