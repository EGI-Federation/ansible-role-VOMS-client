# VOMS Client [![Build Status](https://travis-ci.org/EGI-Foundation/ansible-VOMS-client-role.svg?branch=master)](https://travis-ci.org/EGI-Foundation/ansible-VOMS-client-role)

<!-- A brief description of the role goes here. -->

## Requirements

See [`requirements.txt`](requirements.txt)

## Role Variables

Role variables kept on `defaults/main.yml` include: 

- `prerequisites` - the prerequisite packages on an OS-basis
- `voms_dir`, `vomses_dir` - directory locations on the target host which contain the voms information
- ` lavoisier` - the lavoisier framework endpoints necessary for extracting the data necessary to populate the configuration files.

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
         - { role: brucellino.umd, release: 4, }
         - { role: EGI-Foundation.voms-client, vos: 'atlas' }
```

## License

Apache-2.0

## Author Information

See AUTHORS.md
