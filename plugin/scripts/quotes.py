"""Normalize observed quotes, without fetching or inventing tariffs."""
from decimal import Decimal, ROUND_HALF_UP
from common import fields, require, number, text, instant, public_url, now

COMPONENTS = ('goods', 'domestic_shipping', 'handling', 'international_shipping', 'mandatory_options', 'tax')


def compare(data, at=None):
    at = at or now()
    fields(data, ('context', 'fx', 'quotes'), ('context', 'quotes'))
    context = data['context']
    fields(context, ('product_key', 'quantity', 'destination', 'package'), ('product_key', 'quantity', 'destination', 'package'))
    text(context['product_key'])
    require(type(context['quantity']) is int and context['quantity'] > 0, 'invalid quantity')
    text(context['destination'])
    pack = context['package']
    fields(pack, ('weight_g', 'dimensions_cm', 'basis'), ('weight_g', 'dimensions_cm', 'basis'))
    require(pack['basis'] in ('assumed', 'measured', 'unknown'), 'invalid package basis')
    if pack['basis'] != 'unknown':
        require(number(pack['weight_g']) > 0, 'invalid weight')
        require(isinstance(pack['dimensions_cm'], list) and len(pack['dimensions_cm']) == 3, 'three dimensions required')
        require(all(number(v) > 0 for v in pack['dimensions_cm']), 'invalid dimensions')
    fx = data.get('fx')
    if fx:
        fields(fx, ('krw_per_100_jpy', 'source_url', 'basis_date', 'observed_at', 'expires_at', 'kind'), ('krw_per_100_jpy', 'source_url', 'basis_date', 'observed_at', 'expires_at', 'kind'))
        require(number(fx['krw_per_100_jpy']) > 0, 'invalid FX')
        public_url(fx['source_url']); text(fx['kind']); text(fx['basis_date'])
        require(instant(fx['observed_at']) <= at < instant(fx['expires_at']), 'stale or future FX')
    rows, providers = [], set()
    require(isinstance(data['quotes'], list) and data['quotes'], 'quotes required')
    for quote in data['quotes']:
        fields(quote, ('provider', 'method', 'context', 'status', 'source_url', 'observed_at', 'expires_at', 'components', 'tracking', 'compensation', 'benefits'), ('provider', 'method', 'context', 'status', 'source_url', 'observed_at', 'expires_at', 'components'))
        provider = text(quote['provider']); providers.add(provider)
        text(quote['method']); public_url(quote['source_url'])
        require(quote['status'] in ('available', 'unavailable', 'unverified'), 'invalid availability')
        require(instant(quote['observed_at']) <= at, 'future observation')
        require(instant(quote['expires_at']) > instant(quote['observed_at']), 'invalid validity window')
        issues = []
        if quote['context'] != context: issues.append('comparison_conditions_differ')
        if at >= instant(quote['expires_at']): issues.append('stale_quote')
        if quote['status'] != 'available': issues.append(quote['status'])
        if pack['basis'] == 'unknown': issues.append('unknown_package')
        costs = quote['components']
        fields(costs, COMPONENTS, COMPONENTS)
        total = Decimal(0)
        for label, cost in costs.items():
            if cost is None:
                issues.append('unknown_' + label); continue
            fields(cost, ('amount', 'currency', 'basis'), ('amount', 'currency', 'basis'))
            require(cost['basis'] in ('quoted', 'estimated', 'confirmed_zero'), 'invalid cost basis')
            amount = number(cost['amount'])
            require(cost['currency'] in ('JPY', 'KRW'), 'unsupported currency; obtain conversion first')
            if cost['currency'] == 'KRW':
                require(fx is not None, 'KRW conversion needs sourced FX')
                amount = amount / number(fx['krw_per_100_jpy']) * 100
            total += amount
        rows.append({'provider': provider, 'method': quote['method'], 'known_cost_jpy': str(total.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)), 'comparable_estimate_jpy': None if issues else str(total.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)), 'issues': issues, 'components': costs, 'source_url': quote['source_url'], 'observed_at': quote['observed_at'], 'tracking': quote.get('tracking', 'unverified'), 'compensation': quote.get('compensation', 'unverified'), 'benefits': quote.get('benefits', 'unverified')})
    valid = [r for r in rows if not r['issues']]
    valid.sort(key=lambda r: Decimal(r['comparable_estimate_jpy']))
    return {'context': context, 'fx': fx, 'providers_attempted': len(providers), 'three_providers_attempted': len(providers) >= 3, 'valid_provider_count': len({r['provider'] for r in valid}), 'three_valid_providers': len({r['provider'] for r in valid}) >= 3, 'lowest_comparable_estimate': valid[0] if valid else None, 'quotes': rows, 'notice': 'Estimate only. Excludes actual card FX/fees unless separately accounted for. Unknown costs are not zero.'}
