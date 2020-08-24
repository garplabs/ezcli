import yaml
from paramiko import SSHClient


class Ezcli:
    def __init__(self, config):
        self.config = config
        self.imported_config = {}
        self.site = ''
        self.gathered_sites = []

    def show_sites(self):
        for site_id in self.gathered_sites:
            print(site_id)

    def show_hosts(self):
        selector = self.imported_config['sites'][self.site]['hosts']
        for host in selector:
            print(host)

    def gather_sites(self):
        for site in self.imported_config['sites']:
            print('Site: ' + site + ' registered.')
            self.gathered_sites.append(site)


    def show_hosts_detail(self):
        selector = self.imported_config['sites'][self.site]['hosts']
        for host in selector:
            print(host)
            print('    IP: ' + selector[host]['ip_address'])
            print('    Connect User: ' + selector[host]['connect_user'])
            try:
                print('    FQDN: ' + selector[host]['fqdn'])
                print('    Description: ' + selector[host]['description'])
            except:
                pass

    def host_connect(self,host):
        # Connect
        selector = self.imported_config['sites'][self.site]['hosts'][host]
        ip = selector['ip_address']
        username = selector['connect_user']
        secret = input('Password:')

        client = SSHClient()
        client.load_system_host_keys()
        client.connect(ip, username=username, password=secret)

        # Run a command (execute PHP interpreter)
        cli_input = ' '
        stdin, stdout, stderr = [' ', ' ', ' ']

        while cli_input != 'ezcli exit':
            cli_input = input('ezcli(' + str(host) + '):')
            stdin, stdout, stderr = client.exec_command(cli_input)
            print(stdout.read().decode("utf8"))

        # Print output of command. Will wait for command to finish.

        # Get return code from command (0 is default for success)

        # Because they are file objects, they need to be closed
        stdin.close()
        stdout.close()
        stderr.close()

        # Close the client itself
        client.close()





    def import_yaml_config(self):
        print('Importing Configuration')
        try:
            with open(self.config, 'r') as yaml_config:
                setup = yaml.full_load(yaml_config)

                self.imported_config = setup

            print('Registering sites...')

            #gather_sites(setup,self.gathered_sites)
            self.gather_sites()

            print('Setup Complete')



        except:
            print('Import function has encountered an error. Please validate YAML syntax')

    def run_ui(self):
        user_input = ''
        while user_input != 'exit':
            user_input = input('EZCLI' + '(' + self.site + ')' + " :")
            if user_input == 'show sites':
                self.show_sites()

            if user_input == ('change site'):
                self.site = input('SITE')

            if user_input == ('show hosts') and self.site != '':
                self.show_hosts()

            if user_input == ('show hosts detail') and self.site != '':
                self.show_hosts_detail()
            if user_input == ('connect') and self.site != '':
                host = input('HOST:')
                self.host_connect(host)









ezcli = Ezcli('testyaml2.yaml')

ezcli.import_yaml_config()
ezcli.run_ui()
