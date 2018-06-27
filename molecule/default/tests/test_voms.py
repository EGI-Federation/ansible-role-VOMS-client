import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


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
     "'/DC=ch/DC=cern/OU=computers/CN=lcg-voms2.cern.ch'",
     "'/DC=ch/DC=cern/CN=CERN Grid Certification Authority'"),
    ("dteam",
     "voms2.hellasgrid.gr",
     "'/C=GR/O=HellasGrid/OU=hellasgrid.gr/CN=voms2.hellasgrid.gr'",
     "'/C=GR/O=HellasGrid/OU=Certification Authorities/CN=HellasGrid CA 2016'"),
    ("demo.fedcloud.egi.eu",
     "voms1.grid.cesnet.cz",
     "'/DC=cz/DC=cesnet-ca/O=CESNET/CN=voms1.grid.cesnet.cz'",
     "'/DC=cz/DC=cesnet-ca/O=CESNET CA/CN=CESNET CA 3'"),
    ("fedcloud.egi.eu",
     "voms1.grid.cesnet.cz",
     "'/DC=cz/DC=cesnet-ca/O=CESNET/CN=voms1.grid.cesnet.cz'",
     "'/DC=cz/DC=cesnet-ca/O=CESNET CA/CN=CESNET CA 3'")
])
def test_vo_configuration(host, voname, voms_server, dn, ca_dn):
    vomses_filename = '/etc/vomses/' + voname + '-' + voms_server
    vomses_file = host.file(vomses_filename)

    assert vomses_file.exists
    assert vomses_file.contains(voname)
