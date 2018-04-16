#!/usr/bin/env python

import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C

class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))

Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
# initialize needed objects
loader = DataLoader()
options = Options(connection='local', module_path=['/path/to/mymodules'], forks=100, become=None, become_method=None, become_user=None, check=False,diff=False)
passwords = dict(vault_pass='secret')

# Instantiate our ResultCallback for handling results as they come in
results_callback = ResultCallback()

# create inventory and pass to var manager
# use path to host config file as source or hosts in a comma separated string
inventory = InventoryManager(loader=loader, sources='localhost,')
variable_manager = VariableManager(loader=loader, inventory=inventory)

vm_vmname='dev-test-xh'
vm_hostname='dev-test-xh'
vm_template='CentOS6.8-ecs-2c4m50g-qj'
#vm_datastore=str(get_free_hostinfo['volumes'])
vm_datastore='qj1e2'
#vm_esxi_hostname=str(get_free_hostinfo['ip'])
vm_esxi_hostname='192.16'
vm_datacenter='qianjiang-dc'
vm_netname='VM Network'
vm_guest_id='rhel6_64Guest'

dic_args={ 'hostname': 'vc..work',
            'username': 'ad',
            'password': 'Ld',
            'validate_certs': 'no',
            'folder': '/',
            'datacenter': '%s'%vm_datacenter,
            'esxi_hostname': '%s'%vm_esxi_hostname,
            'name': '%s'%vm_vmname,
            'annotation': 'ansible auto created',
            'state': 'poweredoff',
            'guest_id': '%s'%vm_guest_id,
            'disk': [ { 'size_gb': 56, 'type': 'thin', 'datastore': '%s' %vm_datastore} ],
            'networks': [ { 'name': '%s' %vm_netname} ],
            'template': '%s'%vm_template,
            'wait_for_ip_address': 'no' }

dic_mod='vmware_guest'

print dic_args

# create play with tasks
play_source =  dict(
        name = "Ansible Play",
        hosts = 'localhost',
        gather_facts = 'no',
	connection='local',
        tasks = [
            dict(action=dict(module='vmware_guest', args=dic_args), register='deploy',delegate_to='localhost'),
            dict(action=dict(module='debug', args=dict(msg='{{deploy.stdout}}')))
         ]
    )

print play_source
play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

# actually run it
tqm = None
try:
    tqm = TaskQueueManager(
              inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,
              options=options,
              passwords=passwords,
              stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
          )
    result = tqm.run(play)
finally:
    if tqm is not None:
        tqm.cleanup()

     # Remove ansible tmpdir
print C.DEFAULT_LOCAL_TMP
     #shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
