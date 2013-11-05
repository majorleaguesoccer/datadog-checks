open_handles
==============

Ruffness level: high

This check looks for open file handles for a specified process and returns the count. It is pretty rough and was created as a quick hack for us to run our node.js app instances. It will need some additional work to make it easily handle other processes. The main limitation is being able to grab the pid of the target process using pidof. Some additional manipulation using ps could likely fix this issue.

__Config Example__

init_config:

instances:
    - process_name: node
      stat_prefix: node
      ps_filters: [sed 's/.*our_app/our_app/g', sed 's/\.js//']

process_name: The name of the process you want to monitor (this must be findable with the pidof command)
stat_prefix: The first part of the stat name (e.g. node.our_app.open_handles). This will default to the process_name.
ps_filters: An array of commands to pipe the output of ps through. This can be used to santize output from the ps command. 