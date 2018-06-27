import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("package_name,os_type,os_release", [
    ("fetch-crl", "redhat", "6"),
    ("fetch-crl", "redhat", "7"),
    ("voms-clients3", "redhat", "6"),
    ("voms-clients-cpp", "redhat", "7"),
    ("voms-clients-java", "redhat", "7")
])
def test_packages(host, package_name, os_type, os_release):
    if (host.system_info.release == os_release and
            host.system_info.distribution):
            assert host.package(package_name).is_installed


@pytest.mark.parametrize("executable", [
    "/usr/bin/voms-proxy-info",
    "/usr/bin/voms-proxy-init",
    "/usr/bin/voms-proxy-destroy"]
)
def test_voms_executables(host, executable):
    assert host.file(executable).exists
    # assert host.file(executable).mode == '511'


@pytest.mark.parametrize("directory", [
    "/etc/vomses",
    "/etc/grid-security/vomsdir"])
def test_voms_dir(host, directory):
    assert host.file(directory).exists
    assert host.file(directory).is_directory


# Check that sample VO data is correct
@pytest.mark.parametrize("voname,voms_server,dn,ca_dn", [
    ("ops",
     "lcg-voms2.cern.ch",
     '/DC=ch/DC=cern/OU=computers/CN=lcg-voms2.cern.ch',
     '/DC=ch/DC=cern/CN=CERN Grid Certification Authority'),
    ("dteam",
     "voms2.hellasgrid.gr",
     '/C=GR/O=HellasGrid/OU=hellasgrid.gr/CN=voms2.hellasgrid.gr',
     '/C=GR/O=HellasGrid/OU=Certification Authorities/CN=HellasGrid CA 2016'),
    ("demo.fedcloud.egi.eu",
     "voms1.grid.cesnet.cz",
     '/DC=cz/DC=cesnet-ca/O=CESNET/CN=voms1.grid.cesnet.cz',
     '/DC=cz/DC=cesnet-ca/O=CESNET CA/CN=CESNET CA 3'),
    ("fedcloud.egi.eu",
     "voms1.grid.cesnet.cz",
     '/DC=cz/DC=cesnet-ca/O=CESNET/CN=voms1.grid.cesnet.cz',
     '/DC=cz/DC=cesnet-ca/O=CESNET CA/CN=CESNET CA 3')
])
def test_vo_configuration(host, voname, voms_server, dn, ca_dn):
    vomses_filename = '/etc/vomses/' + voname + '-' + voms_server
    vomses_file = host.file(vomses_filename)
    assert vomses_file.exists
    assert vomses_file.contains(voname)
    assert vomses_file.contains(dn)
    assert vomses_file.contains(voms_server)
