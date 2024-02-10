from shop.enum import Currency


def all_currencies(request):
    return {'all_currencies': [curr for curr in Currency],
            'current_currency': request.session.get("currency") or Currency.USD.value}
