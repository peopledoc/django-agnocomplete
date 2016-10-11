"""
agnocomplete doc checker
"""
import os
from copy import copy
from os.path import abspath, dirname, join, splitext


def grep(rootdir, searched):
    "grep -l <searched>"
    to_inspect = []
    for root, dirs, files in os.walk(rootdir):
        for _file in files:
            if _file.endswith('.rst'):
                to_inspect.append(join(root, _file))

    to_check = ((_file, open(_file, 'r').read()) for _file in to_inspect)
    to_check = filter(lambda item: searched in item[1], to_check)
    to_check = map(lambda item: item[0], to_check)
    return to_check


def get_expected_html_files(rootdir, files):
    html_files = map(lambda _file: splitext(_file), files)
    html_files = map(lambda item: (item[0].replace(rootdir, '')), html_files)
    html_files = map(lambda item: "{}{}.html".format('/_build/html', item), html_files)
    return set(html_files)


if __name__ == '__main__':
    rootdir = abspath(dirname(__file__))
    files = grep(rootdir, 'literalinclude')
    expected_html_files = get_expected_html_files(rootdir, files)

    # Manually fed:
    html_files = ['admin-site.html', 'autocomplete-definition.html']
    # CHECK!
    files = copy(html_files)
    files = map(lambda item: "{}/{}".format("/_build/html", item), files)
    files = set(files)
    diff = expected_html_files.symmetric_difference(files)
    msg = "Have you checked every literalinclude?: {}".format(diff)
    assert files == expected_html_files, msg
    print("Reminder: Check your literalinclude in: {}".format(expected_html_files))
