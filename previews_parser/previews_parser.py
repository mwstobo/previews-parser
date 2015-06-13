import collections
import datetime
import re

regexes = {
    'release': re.compile('(\w{3}\d{6})\s*(.*)\s*(\$(\d+\.\d+)|pi)', re.IGNORECASE),
    'publisher': re.compile('^(dc comics|dark horse comics|idw publishing|image comics|marvel comics)$', re.IGNORECASE),
    'series': re.compile('(.*?)#\d+(?!(.*poster)|.*(combo pack))', re.IGNORECASE),
    'issue_no': re.compile('#(\d+)(?!-)'),
    'mature': re.compile('\(MR\)'),
    'printing': re.compile('(\d+)\w{2}\s+(printing|ptg)', re.IGNORECASE),
    'date': re.compile('(\d+)/(\d+)/(\d+)', re.IGNORECASE),
}

publisher_keys = {
    'DARK HORSE COMICS': 'Dark Horse Comics',
    'DC COMICS': 'DC Comics',
    'IDW PUBLISHING': 'IDW Publishing',
    'IMAGE COMICS': 'Image Comics',
    'MARVEL COMICS': 'Marvel Comics'
}

def parse(string):
    lines = string.split("\n")
    lines = collections.deque([l.strip() for l in lines if l.strip()])
    output = []
    under_publisher = False
    current_publisher = None
    seen_issues = []
    while len(lines) > 0:
        if not under_publisher:
            l = lines.popleft()
            match = regexes['publisher'].match(l)
            if match:
                under_publisher = True
                current_publisher = publisher_keys[match.group(0)]
        else:
            l = lines.popleft()
            match = regexes['release'].match(l)
            if match:
                release_info = parse_release_info(match.group(2))
                if release_info != {}:
                    if (release_info['series'], release_info['issue']) in seen_issues:
                        continue
                    try:
                        price = float(match.group(4))
                    except:
                        continue
                    comic = {
                        'code': match.group(1),
                        'series': release_info['series'],
                        'issue': release_info['issue'],
                        'price': price,
                        'publisher': current_publisher,
                        'printing': release_info['printing'] or 1,
                        'mature':  release_info['mature'] or False,
                    }
                    output.append(comic)
                    seen_issues.append((release_info['series'], release_info['issue']))
            else:
                under_publisher = False
                lines.appendleft(l)
    return output

def parse_release_info(string):
    output = collections.defaultdict(lambda: None)
    series_match = regexes['series'].search(string)
    if series_match:
        title = series_match.group(1).title().strip()
        output['series'] = title
        string = re.sub(title, '', string).strip()
    else:
        return {}

    issue_match = regexes['issue_no'].search(string)
    if issue_match:
        output['issue'] = int(issue_match.group(1))
    else:
        return {}

    mature_match = regexes['mature'].search(string)
    if mature_match:
        output['mature'] = True

    printing_match = regexes['printing'].search(string)
    if printing_match:
        output['printing'] = int(printing_match.group(1))

    return output

def parse_date(string):
    lines = string.split("\n")
    lines = collections.deque([l.strip() for l in lines if l.strip()])
    while len(lines) > 0:
        l = lines.popleft()
        match = regexes['date'].search(l)
        if match:
            month = int(match.group(1))
            day = int(match.group(2))
            year = int(match.group(3))
            return datetime.date(year, month, day)
