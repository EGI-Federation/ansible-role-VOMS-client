import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

@pytest.mark.parametrize("directory",
    [("/etc/vomses"), "/etc/grid-security/vomsdir"]
)
def test_voms_dir(host, directory):
    
    assert host.file(directory).exists
    assert host.file(directory).is_directory
