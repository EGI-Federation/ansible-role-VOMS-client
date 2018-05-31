import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_voms_dir(host):
    vomses_dir = host.file('/etc/vomses')
    voms_dir = host.file('/etc/grid-security/vomsdir')
    
    assert vomses_dir.exists



    