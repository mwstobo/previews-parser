import collections
import re

regexes = {
    'release': re.compile('(\w{3}\d{6})\s*(.*)\s*\$(\d+\.\d+|pi)', re.IGNORECASE),
    'publisher': re.compile('^(dc comics|dark horse comics|idw publishing|image comics|marvel comics)$', re.IGNORECASE),
    'series': re.compile('(.*?)#\d+'),
    'issue_no': re.compile('#(\d+)'),
    'mature': re.compile('\(MR\)'),
    'printing': re.compile('(\d+)\w{2}\s+(printing|ptg)', re.IGNORECASE)
}

publisher_keys = {
    'DARK HORSE COMICS': 'dark_horse',
    'DC COMICS': 'dc',
    'IDW PUBLISHING': 'idw',
    'IMAGE COMICS': 'image',
    'MARVEL COMICS': 'marvel'
}

def parse(string):
    lines = string.split("\n")
    lines = collections.deque(filter(None, lines))
    output = collections.defaultdict(list)
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
                    extra_info = {
                        'mature':  release_info['mature'] or False,
                        'printing': release_info['printing'] or 1
                    }
                    comic = {
                        'code': match.group(1),
                        'series': release_info['series'],
                        'issue': release_info['issue'],
                        'price': float(match.group(3)),
                        'extra_info': extra_info
                    }
                    output[current_publisher].append(comic)
                    seen_issues.append((release_info['series'], release_info['issue']))
            else:
                under_publisher = False
                lines.appendleft(l)
    return output



def parse_names(string):
    return

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
