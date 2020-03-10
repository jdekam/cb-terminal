# Check for a valid user by UMID.
# Create new account if needed and from scan.
@view_config(route_name='terminal_umid_check',
             request_method='POST',
             renderer='json',
             permission='service')
def terminal_umid_check(request):
    try:
        # if card was scanned, can create new account if needed
        create = bool(request.POST['scanned'])
        # get user
        user = User.from_umid(request.POST['umid'], create_if_never_seen=create)
        # make sure someone can't create an admin account from terminal
        if user.role == 'serviceaccount':
            # n.b. don't expose a different error path here
            raise User.InvalidUserException

        request.response_status = 200
        return {
            'umid': request.POST['UMID']
        }
    except:
        request.response_status = 400
        return {
            'error': get_localizer(request).translate(('mcard-keypad-error',
                default='First time using Betty? You need to swipe your M-Card the first time you log in.'))
        }


## Main terminal page with purchase/cash deposit.
@view_config(route_name='terminal',
             renderer='templates/terminal/terminal.jinja2',
             permission='service')
def terminal(request):
    try:
        if len(request.matchdict['umid']) != 8:
            raise __user.InvalidUserException()

        with transaction.manager:
            user = User.from_umid(request.matchdict['umid'], create_if_never_seen=True)
        user = DBSession.merge(user)
        if not user.enabled:
            request.session.flash(get_localizer(request).translate(_(
                'user-not-enabled',
                default='User is not enabled. Please contact ${email}.',
                mapping={'email':request.registry.settings['chezbetty.email']},
                )), 'error')
            return HTTPFound(location=request.route_url('index'))

        # Handle re-instating archived user
        if user.archived:
            if user.archived_balance != 0:
                datalayer.adjust_user_balance(user,
                                              user.archived_balance,
                                              'Reinstated archived user.',
                                              request.user)
            user.balance = user.archived_balance
            user.archived = False

        # NOTE TODO (added on 2016/05/14): The "name" field in this temp
        # table needs to be terminal specific. That is, if there are multiple
        # terminals, items and money shouldn't be able to move between them.

        # If cash was added before a user was logged in, credit that now
        deposit = None
        in_flight_deposit = Ephemeron.from_name('deposit')
        if in_flight_deposit:
            amount = Decimal(in_flight_deposit.value)
            deposit = datalayer.deposit(user, user, amount)
            DBSession.delete(in_flight_deposit)

        # For Demo mode:
        items = DBSession.query(Item)\
                         .filter(Item.enabled == True)\
                         .order_by(Item.name)\
                         .limit(6).all()

        # Determine initial wall-of-shame fee (if applicable)
        purchase_fee_percent = Decimal(0)
        if user.balance <= Decimal('-5.0') and user.role != "administrator":
            purchase_fee_percent = 5 + (math.floor((user.balance+5) / -5) * 5)

        # Figure out if any pools can be used to pay for this purchase
        purchase_pools = []
        for pool in Pool.all_by_owner(user, True):
            if pool.balance > (pool.credit_limit * -1):
                purchase_pools.append(pool)

        for pu in user.pools:
            if pu.enabled and pu.pool.enabled and pu.pool.balance > (pu.pool.credit_limit * -1):
                purchase_pools.append(pu.pool)

        # Get the list of tags that have items without barcodes in them
        tags_with_nobarcode_items = Tag.get_tags_with_nobarcode_items();

        return {'user': user,
                'items': items,
                'purchase_pools': purchase_pools,
                'purchase_fee_percent': purchase_fee_percent,
                'good_standing_discount': round((datalayer.good_standing_discount)*100),
                'good_standing_volunteer_discount': round((datalayer.good_standing_volunteer_discount)*100),
                'good_standing_manager_discount': round((datalayer.good_standing_manager_discount)*100),
                'admin_discount': round((datalayer.admin_discount)*100),
                'tags_with_nobarcode_items': tags_with_nobarcode_items,
                'nobarcode_notag_items': Item.get_nobarcode_notag_items(),
                'deposit': deposit}

    except __user.InvalidUserException as e:
        request.session.flash(get_localizer(request).translate(_(
            'mcard-error',
            default='Failed to read M-Card. Please try swiping again.',
            )), 'error')
        return HTTPFound(location=request.route_url('index'))
