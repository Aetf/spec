from __future__ import absolute_import, division, print_function
import subprocess as sp

from ansible.errors import AnsibleFilterError
from ansible.module_utils._text import to_text


def systemd_escape(value, suffix=None, template=None, path=False, unescape=False, mangle=False, instance=False):
    cmd = ['systemd-escape']
    if suffix is not None:
        cmd += ['--suffix={}'.format(suffix)]
    if template is not None:
        cmd += ['--template={}'.format(template)]
    if path:
        cmd += ['--path']
    if unescape:
        cmd += ['--unescape']
    if mangle:
        cmd += ['--mangle']
    if instance:
        cmd += ['--instance']

    cmd += [value]

    try:
        output = sp.check_output(cmd)
        return to_text(output.strip())
    except Exception as e:
        raise AnsibleFilterError(e)
    pass


class FilterModule(object):
    """Ansible filter for passing the string through systemd-escape"""

    def filters(self):
        return {
            "systemd_escape": systemd_escape,
        }
