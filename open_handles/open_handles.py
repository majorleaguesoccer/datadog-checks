from checks import AgentCheck
import subprocess

class openFileHandleCheck(AgentCheck):
    def check(self, instance):
        if not instance['process_name']:
            self.log.error('process_name is not defined')
            return

        process_name = instance['process_name']
        stat_prefix = self.init_config.get('stat_prefix', process_name)
        filter = ''

        if 'ps_filters' in instance:
            filter = '| ' + '| '.join(instance['ps_filters'])

        process_pids = subprocess.check_output('pidof -x %s' % process_name, shell=True).rstrip().split()

        for pid in process_pids:
            process_name_command = "ps -o cmd -p %s --no-headers %s" % (pid, filter)

            process_name = subprocess.check_output(process_name_command, shell=True).rstrip().split()

            open_handles = subprocess.check_output('sudo lsof -P -n -p %s | wc -l' % pid, shell=True).rstrip()

            self.log.debug('Found %s handles for process %s with pid %s' % (open_handles, process_name, pid))
            self.gauge('%s.%s.open_handles' % (stat_prefix, process_name), open_handles, tags=[''])