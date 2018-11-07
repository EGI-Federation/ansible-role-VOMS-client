# EGI VOMS Client 

[![Build Status](https://travis-ci.org/EGI-Foundation/ansible-role-VOMS-client.svg?branch=master)](https://travis-ci.org/EGI-Foundation/ansible-role-VOMS-client)
[![Docker Repository on Quay](https://quay.io/repository/egi/voms-client/status "Docker Repository on Quay")](https://quay.io/repository/egi/voms-client)
<!-- A brief description of the role goes here. -->

## General information

### About VOMS and VOs

This is an Ansible role which configures VOMS clients.
VOMS is a web service for managing membership of Virtual Organisations.
VOMS clients are necessary to obtain authorisation (in the form of
short-lived proxies) for interacting with specific services, based on VO
membership.
VOMS clients are set of command-line utilities which send authenticated
requests to the relevant VOMS server in order to request authorisation
from them.

In order to use the VOMS client, an individual needs to

- have a personal x.509 certificate
- be registered in the VO they want to get an authorisation for

VOMS clients are typically installed on the User Interface or Worker Node profiles.

### Configuration

Configuration of the VOMS clients is done with a few files:

  1. `.lsc` files
  2. `vomses` files

See [the VOMS documentation](http://italiangrid.github.io/voms/documentation/voms-clients-guide/3.0.4/#voms-trust) for more detailed information.

For every VO you wish to interact with, the relevant configuration needs
to be in place.
This can be quite a time-consuming task, especially in cases where a
site administrator does not know _a-priori_ which VOs to configure.

To make life bearable, we take a **data-driven** approach.

The necessary data is available via the EGI Operations Portal, which
is used in this role as a data source.
This allows us to configure **all** VOs registered in the Operations Portal
in one foul swoop.
Two approaches could be taken to generating the configuration:

1. configuration from raw data pulled from Lavoisier at Ansible runtime
1. configuration from filtered data pulled from Lavoisier prior to Ansible runtime.

In the former approach, a well-crafted [`json_query`](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#json-query-filter) could be used to iterate over the data returned from Lavoisier.
The query in this case needs to reflect the complexity and structure of the data object returned by Lavoisier, which cannot be assumed to return an array of consistent data.
In the latter approach, a much simpler is used to iterate over a cached data object, which has been filtered to exclude items which do not contain the relevant information.
This cached data can be easily created by a simple python script - `[files/create_clean_vo_data.py](files/create_clean_vo_data.py) which
reads the role vars and creates a local cache of data.
The data format has been chosen to be YAML so that we can add it to the repository and keep track of changes - this would be difficult with JSON, due to the lack of lines.

We have opted for the latter (see [4215026e18c](https://github.com/EGI-Foundation/ansible-role-VOMS-client/commit/52ac706fe059a336244bb2e4af0bdee2f37752a6)) for the following reasons:

  1. It is easier to _maintain_ a well-documented script than a complex json query.
  2. It is easier to _read_ a well-documented script than a complex json query
  3. If the role is added as a dependency to playbooks (as will certainly be the case, since the voms clients are used all over the place), the data needs to be present.

There is however the drawback that the data in the repo can quickly become out of synch with the actual data on Lavoisier. 
This could happen either by individuals editing the cache by hand, or by the maintainer not running the script when necessary.
The only way to overcome this is to maintain a strong test suite.

## Testing

The role is tested with [molecule](https://molecule.readthedocs.io/en/latest/) for the following scenarios:

- `default` (tested with [TestInfra](http://testinfra.readthedocs.io/en/latest/))

Tests cover unit and integration tests, but not functional tests, since
a personal certificate is necessary for using the VOMS client.
Specific tests included are:

- presence of binary executables
- presence of configuration directories
- contents of configuration files for selected VOs

## Requirements

See [`requirements.txt`](requirements.txt)

## Role Variables

Role variables kept on `defaults/main.yml` include:

- `prerequisites` - the prerequisite packages on an OS-basis
- `voms_dir`, `vomses_dir` - directory locations on the target host which contain the voms information
- `lavoisier` - the lavoisier framework endpoints necessary for extracting the data necessary to populate the configuration files.

There is no need to change the default variables.

## Dependencies

Dependencies are not explicitly declared in the metadata, but this role depends on the UMD role:

```yaml
  - { role: brucellino.umd, release: 4 }
```

## Example Playbook

<!--
Including an example of how to use your role (for instance, with variables
passed in as parameters) is always nice for users too:
-->

```yaml
    - hosts: servers
      roles:
         - { role: EGI-Foundation.umd, release: 4 }
         - { role: EGI-Foundation.voms-client}
```

## License

Apache-2.0

## Author Information

See AUTHORS.md
