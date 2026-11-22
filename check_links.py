"""Link checker for the well inventory. Standard library only.

Every source of every inventory row must resolve. A DOI is checked
against the doi.org handle registry (publishers often refuse scripted page
reads, the registry does not); any other URL must answer a GET below 400.
Needs the network, so it is a script with a dated record, not a unit test:

    python3 check_links.py [record.json]
"""
import csv
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
INVENTORY = HERE / 'inventory.csv'
AGENT = {'User-Agent': 'Mozilla/5.0 (link check)'}


def inventory_links(path=INVENTORY):
    """(row label, url) for every source of every row; a row without a source is returned with url None."""
    out = []
    with open(path, newline='') as handle:
        for row in csv.DictReader(handle):
            urls = row['sources'].split()
            out += [(row['well'], url) for url in urls] or [(row['well'], None)]
    return out


def _unused(path=None):
    sources = json.loads(Path(path).read_text())['sources']
    out = []
    for key, source in sources.items():
        if 'doi' in source:
            out.append((key, 'https://doi.org/' + source['doi']))
        out.append((key, source.get('url')))
    return out


def doi_of(url):
    for prefix in ('https://doi.org/', 'http://doi.org/', 'https://dx.doi.org/'):
        if url.startswith(prefix):
            return url[len(prefix):]
    return None


def check(url, timeout=40):
    """(ok, detail) for one URL."""
    if not url:
        return False, 'no source'
    doi = doi_of(url)
    target = 'https://doi.org/api/handles/' + doi if doi else url
    try:
        with urllib.request.urlopen(urllib.request.Request(target, headers=AGENT), timeout=timeout) as reply:
            if doi:
                code = json.loads(reply.read().decode()).get('responseCode')
                return code == 1, 'doi registry code %s' % code
            return reply.status < 400, 'http %s' % reply.status
    except urllib.error.HTTPError as error:
        return False, 'http %s' % error.code
    except Exception as error:  # network errors are reported, not hidden
        return False, type(error).__name__


def main(argv):
    seen, rows = {}, []
    for label, url in inventory_links():
        if url not in seen:
            seen[url] = check(url)
        ok, detail = seen[url]
        rows.append({'row': label, 'url': url, 'ok': ok, 'detail': detail})
    failed = [r for r in rows if not r['ok']]
    record = {'record_type': 'well_record_link_check', 'checked': len(rows), 'distinct_urls': len(seen),
              'failed': failed, 'pass': not failed, 'rows': rows}
    if len(argv) > 1:
        Path(argv[1]).write_text(json.dumps(record, indent=1) + '\n')
    for r in failed:
        print('FAIL', r['row'], r['url'], r['detail'])
    print('%d links, %d distinct, %d failed' % (len(rows), len(seen), len(failed)))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
