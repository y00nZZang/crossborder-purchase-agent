"""Pure validation utilities. No network, credentials, or external mutations."""
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from urllib.parse import urlsplit
import hashlib
import json


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def fields(obj, allowed, required=()):
    require(isinstance(obj, dict), 'expected object')
    require(not set(obj) - set(allowed), 'unsupported fields')
    require(set(required) <= set(obj), 'missing fields')


def text(value):
    require(isinstance(value, str) and 0 < len(value) <= 1000, 'expected nonempty text')
    return value


def number(value):
    require(isinstance(value, (str, int)) and not isinstance(value, bool), 'amount must be decimal string or integer')
    try:
        d = Decimal(value)
    except InvalidOperation:
        raise Invalid('invalid decimal') from None
    require(d.is_finite() and 0 <= d <= Decimal('1e12'), 'invalid amount')
    return d


def instant(value):
    try:
        t = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        raise Invalid('invalid timestamp') from None
    require(t.tzinfo is not None, 'timestamp needs timezone')
    return t


def now():
    return datetime.now(timezone.utc)


def public_url(value):
    text(value)
    u = urlsplit(value)
    require(u.scheme == 'https' and u.hostname and not u.username and not u.password, 'expected public HTTPS URL')
    # Product option query parameters are preserved. Session URLs must never be supplied.
    require(not any(x in value.lower() for x in ['checkout', 'token=', 'session=', 'temp_id=', 'cid=']), 'use public product/source URL')
    return value


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
