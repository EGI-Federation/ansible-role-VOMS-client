import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

@pytest.mark.parametrize("OS","package", 
    [("centos6"),("voms","fetch-crl")]
)

def test_packages(host, package):
    assert host.package(package).is_installed


@pytest.mark.parametrize("directory",
    [("/etc/vomses"), "/etc/grid-security/vomsdir"]
)
def test_voms_dir(host, directory):
    
    assert host.file(directory).exists
    assert host.file(directory).is_directory



    