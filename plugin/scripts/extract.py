"""Extract candidate products from supplied public HTML; never select a variant silently."""
from html.parser import HTMLParser
import json
from common import public_url


class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.blocks = []; self.buf = None
    def handle_starttag(self, tag, attrs):
        if tag == 'script' and dict(attrs).get('type', '').lower() == 'application/ld+json': self.buf = []
    def handle_data(self, data):
        if self.buf is not None: self.buf.append(data)
    def handle_endtag(self, tag):
        if tag == 'script' and self.buf is not None:
            self.blocks.append(''.join(self.buf)); self.buf = None


def extract(html, url):
    public_url(url)
    parser = Page(); parser.feed(html)
    products, failures = [], 0
    def walk(node):
        if isinstance(node, list):
            for v in node: walk(v)
        elif isinstance(node, dict):
            types = node.get('@type', [])
            if isinstance(types, str): types = [types]
            if 'Product' in types:
                products.append({k: node[k] for k in ('name', 'sku', 'mpn', 'gtin', 'gtin13', 'brand', 'offers', 'color', 'size', 'weight') if k in node})
            for k, v in node.items():
                if k != 'offers': walk(v)
    for block in parser.blocks:
        try: walk(json.loads(block))
        except (ValueError, TypeError): failures += 1
    return {'source_url': url, 'candidates': products, 'parse_failures': failures, 'requires_visible_page_verification': True, 'notice': 'Untrusted metadata; verify seller, variant, price and availability against visible page. No match is not no product.'}
