from __future__ import absolute_import, division, print_function


def ensure_list(value):
    if isinstance(value, list):
        return value
    else:
        return [value]


class FilterModule(object):
    """Ansible filter for passing the string through systemd-escape"""

    def filters(self):
        return {
            "ensure_list": ensure_list,
        }
