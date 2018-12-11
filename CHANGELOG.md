# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


<!-- For an easy way to do this see 
https://stackoverflow.com/questions/7387612/git-changelog-how-to-get-all-changes-up-to-a-specific-tag
git shortlog --oneline --decorate <last tag>
 -->
## [Unreleased]

### Added

### Changed
<!-- Changed for changes in existing functionality. -->
### Deprecated
<!-- Deprecated for soon-to-be removed features. -->
### Removed
<!-- Removed for now removed features. -->
### Fixed 
<!-- Fixed for any bug fixes. -->
### Security
<!-- Security in case of vulnerabilities. -->

## [0.1.2] - EGI Trust Anchor 1.95

### Added

- b76c6a9 (dh_vos_update) Add changelog.
- 93792d7 DIH VOS update (#21)
- a3294d1 (origin/dh_vos_update) Update voms1 and voms2.pd certs from https://operations-portal.egi.eu/broadcast/archive/2275
- 8fc8889 Use free strategy for provisioning
- 1567ca9 Update DIH voucher vo configs
- f8c58ef Add the innovation hub vouchers
- ab511f2 Add container badge


### Changed
<!-- Changed for changes in existing functionality. -->
### Deprecated
<!-- Deprecated for soon-to-be removed features. -->
### Removed
<!-- Removed for now removed features. -->
### Fixed 
<!-- Fixed for any bug fixes. -->
### Security
<!-- Security in case of vulnerabilities. -->

## [0.1.1] - EGI Trust Anchor 1.94

This is the release of the Ansible VOMS clients role corresponding to EGI Trust Anchor version 1.94-1.

### Added

- c316cdb Actually commit the images and push them
- 3b8582c Update for 1.94
- 075b34a Proper formatting of vomses files
- 968e63b Add mathematical-softare VO and change French CA DN
- fcbd796 Merge pull request #16 from enolfc/pythonic
- 10064b4 python 3 support and pep8 fixes
- d1e246a Push to quay  on success

### Changed

- 88e424b Switch to umd base image
- 
### Deprecated
<!-- Deprecated for soon-to-be removed features. -->
### Removed
<!-- Removed for now removed features. -->
### Fixed 
<!-- Fixed for any bug fixes. -->
### Security
<!-- Security in case of vulnerabilities. -->


## [0.1.0] - 2018-07-04

### Added

The first release of the role which configures all VOs from the Operations Portal data.

- e5015cc Change source of UMD dependency
- 65cf550 Update README to explain why we cache data
- 6596848 Remove verbosity on testing
- f9a8ab0 Update requirements to change python docker module (docker)
- 892ec4f New task to configure from cached data
- 52ac706 Configuration done with cached data.
- 4f369d4 Add install tasks for RedHat-based machines
- 772a9da Add python script to filter
- f3ffa3a Add community health files and update readme
- 4c65028 Merge pull request #6 from EGI-Foundation/fix_travis_timeout
- a7f595c Passing tests for vomses file content
- ce7ccff Add failing tests on VOMSes file assertions
- ecc1ad7 Add variable for excluding VOs with no VOMS info
- 3d44c92 Update vomses task to write proper format
- 1dcabf8 briefly describe the Ansible role and what it does
- 20a5c7a changed the endpoint for the data
- b4bce34 Update README to describe how we ingest data
- 96324b5 Initial Commit

### Changed
<!-- Changed for changes in existing functionality. -->
### Deprecated
<!-- Deprecated for soon-to-be removed features. -->
### Removed
<!-- Removed for now removed features. -->
### Fixed 
<!-- Fixed for any bug fixes. -->
### Security
<!-- Security in case of vulnerabilities. -->