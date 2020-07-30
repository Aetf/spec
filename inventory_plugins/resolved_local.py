# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
    module: resolved_local
    plugin_type: inventory
    short_description: Returns localhost's real hostname
    description: Returns localhost's real hostname for easier matching in host vars
    options:
      plugin:
          description: Name of the plugin
          required: true
          choices: ['resolved_local']
    extends_documentation_fragment:
      - inventory_cache
'''


import socket

from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable
from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):

    # used internally by Ansible, it should match the file name but not required
    NAME = 'resolved_local'

    def parse(self, inventory, loader, path, cache=True):

        # call base method to ensure properties are available for use with other helper methods
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        # this method will parse 'common format' inventory sources and
        # update any options declared in DOCUMENTATION as needed
        config = self._read_config_data(path)
        cache_key = self.get_cache_key(path)

        # cache may be True or False at this point to indicate if the inventory is being refreshed
        # get the user's cache option too to see if we should save the cache if it is changing
        user_cache_setting = self.get_option('cache')

        # read if the user has caching enabled and the cache isn't being refreshed
        attempt_to_read_cache = user_cache_setting and cache
        # update if the user has caching enabled and the cache is being refreshed; update this value to True if the cache has expired below
        cache_needs_update = user_cache_setting and not cache

        # attempt to read the cache if inventory isn't being refreshed and the user has caching enabled
        hostname = None
        if attempt_to_read_cache:
            try:
                hostname = self._cache[cache_key]
            except KeyError:
                # This occurs if the cache_key is not in the cache or if the cache_key expired, so the cache needs to be updated
                cache_needs_update = True

        if hostname is None:
            # resovle hostname
            try:
                hostname = socket.gethostname()
            except Exception as e:
                raise AnsibleError('Failed to get local hostname: {}'.format(to_native(e)))

        if cache_needs_update:
            # set the cache
            self._cache[cache_key] = hostname

        self.inventory.add_host(hostname)
        # make sure it's connected via local
        self.inventory.set_variable(hostname, 'ansible_connection', 'local')
