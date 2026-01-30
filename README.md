## Description

A collection of scripts, which analyze and report different kind of anomalies, based on real-time reading different linux logs from **/var/log/** directory.
Current available notification methods are:
* Desktop notification
* Sound alarm
* Terminal notification (a terminal should be open for this)
  
Can be added as a daemon, or run as a separate python script.

## Contents

- **auth_log** - analyzing */var/log/auth.log*.
  Checks:
  * *too_many_sudos()* - three consecutive (< 5 min) failed *sudo* attempts.
