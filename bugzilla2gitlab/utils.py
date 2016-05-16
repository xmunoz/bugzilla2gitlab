import requests
import dateutil.parser
from xml.etree import ElementTree

def _perform_request(url, method, data={}, params={}, headers={}, files={}, json=True,
                     dry_run=False):
    '''
    Utility method to perform an HTTP request.
    '''
    if dry_run:
        msg = "{} {} dry_run".format(url, method)
        print(msg)
        return 0

    func = getattr(requests, method)

    if files:
        result = func(url, files=files, headers=headers)
    else:
        result = func(url, params=params, data=data, headers=headers)

    if result.status_code in [200, 201]:
        if json:
            return result.json()
        else:
            return result

    raise Exception("{} failed requests: {}".format(result.status_code, result.reason))


def markdown_table_row(key, value):
    '''
    Create a row in a markdown table.
    '''
    return "| {} | {} |\n".format(key, value)


def format_datetime(datestr, formatting):
    '''
    Apply a dateime format to a string, according to the formatting string.
    '''
    parsed_dt = dateutil.parser.parse(datestr)
    return parsed_dt.strftime(formatting)


def get_bugzilla_bug(bugzilla_url, bug_id):
    '''
    Read bug XML, return all fields and values in a dictionary.
    '''
    bug_xml = _fetch_bug_content(bugzilla_url, bug_id)
    tree = ElementTree.fromstring(bug_xml)

    bug_fields = {
        "long_desc" : [],
        "attachment": [],
        "cc": [],
    }
    for bug in tree:
        for field in bug:
            if field.tag in ("long_desc", "attachment"):
                new = {}
                for data in field:
                    new[data.tag] = data.text
                bug_fields[field.tag].append(new)
            elif field.tag == "cc":
                bug_fields[field.tag].append(field.text)
            else:
                bug_fields[field.tag] = field.text

    return bug_fields

def _fetch_bug_content(url, bug_id):
    url = "{}/show_bug.cgi?ctype=xml&id={}".format(url, bug_id)
    response = _perform_request(url, "get", json=False)
    return reponse.content

def validate_list(integer_list):
    '''
    Ensure that the user-supplied input is a list of integers, or a list of strings 
    that can be parsed as integers.
    '''
    if not integer_list:
        raise Exception("No bugs to migrate! Call `migrate` with a list of bug ids.")

    if not isinstance(integer_list, list):
        raise Exception("Expected a list of integers. Instead recieved "
                            "a(n) {}".format(type(integer_list)))

        for i in integer_list:
            try:
                int(i)
            except ValueError:
                raise Exception("{} is not able to be parsed as an integer, "
                                "and is therefore an invalid bug id.".format(i))
