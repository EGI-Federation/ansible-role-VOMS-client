import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_certificiates_dir(host):
    cert_dir = host.file('/etc/grid-security/certificates')

    assert cert_dir.exists
    assert cert_dir.is_directory


def test_role_exists(host):
    
    result = host.get_host("local://").run_expect('EGI-Foundation.VOMS-client-ansible','ansible-galaxy search voms')
    print result