# makeuser

A script that allows admins to make user accounts easily.

Run `make` to install the script to `/usr/local/bin`.



## User removal

Use `rmuser <username>` to remove a user account and clean up related services:

- Removes user from Helpdesk (`helpdesk_admin.sh del`)
- Removes user from ZNC (`zncdelete.py`)
- Discovers user email from `/var/signups` for Helpdesk/list cleanup
- Comments out matching signup entries in `/var/signups`
- Sends mailing list unsubscribe request when an email is discovered
- Deletes the Unix account and home directory (`userdel -r`)

Run `make` to install `rmuser` and `zncdelete.py` to `/usr/local/bin`.
