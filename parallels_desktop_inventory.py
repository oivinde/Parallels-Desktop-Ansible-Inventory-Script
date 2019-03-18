#!/usr/bin/env python

import json
import shutil
import argparse
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.errors import AnsibleError
import ansible.constants as C
import os
username = os.environ.get("PARALLELS_USERNAME")
password = os.environ.get("PARALLELS_PASSWORD")
hostname = [os.environ.get("PARALLELS_HOSTNAME"), '']


class ResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = []
        self.host_unreachable = []
        self.host_failed = []

    def v2_runner_on_unreachable(self, result, ignore_errors=False):
        result = result._result
        self.host_unreachable = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        result = result._result
        self.host_ok = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        result = result._result
        self.host_failed = result


class Parallels_Invenory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.list_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print json.dumps(self.inventory)

    def list_inventory(self):
        Options = namedtuple('Options', ['connection',
                                         'module_path',
                                         'remote_user',
                                         'forks',
                                         'become',
                                         'become_method',
                                         'become_user',
                                         'check',
                                         'diff'])

        options = Options(connection='ssh',
                          module_path=['/to/mymodules'],
                          remote_user=username,
                          forks=10,
                          become=None,
                          become_method=None,
                          become_user=None,
                          check=False,
                          diff=False)

        loader = DataLoader()
        passwords = {'conn_pass': password}
        C.INVENTORY_ENABLED = ['host_list', 'script']
        inventory = InventoryManager(loader=loader, sources=','.join(hostname))
        variable_manager = VariableManager(loader=loader, inventory=inventory)
        play_source = dict(
            name="Ansible Play",
            hosts='all',
            gather_facts='no',
            tasks=[
                dict(action=dict(module='shell',
                                 args='/usr/local/bin/prlctl list --all -o name -j'),
                     register='shell_out'),
                dict(action=dict(module='debug',
                                 args=dict(msg='{{shell_out.stdout}}')))
            ]
        )

        play = Play().load(play_source, variable_manager=variable_manager,
                           loader=loader)

        tqm = None
        callback = ResultsCollector()
        try:
            tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=passwords,
            )

            tqm._stdout_callback = callback
            result = tqm.run(play)
            if callback.host_ok:
                inv = {}
                inv['all'] = {}
                inv['all']['hosts'] = []
                for i in callback.host_ok['msg']:
                    #print i['name']
                    inv['all']['hosts'].append(i['name'])
                inv['all']['vars'] = {}
                inv['all']['vars']['ansible_connection'] = 'ssh'
                #print(json.dumps(inv, indent=4))
                return inv
            if callback.host_unreachable:
                raise AnsibleError(callback.host_unreachable['msg'])
            if callback.host_failed:
                raise AnsibleError(callback.host_failed['msg'])

        finally:
            if tqm is not None:
                tqm.cleanup()

            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


Parallels_Invenory()
