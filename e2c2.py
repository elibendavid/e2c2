#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Eli Ben-David
# @Date:   2017-09-21 11:43:41
# @Last Modified by:   Eli Ben-David
# @Last Modified time: 2018-09-20 15:44:05

import os
import boto3
import cmd
from termcolor import colored
from terminaltables import AsciiTable
import e2c2config
from e2c2config import _colors

"""
e2c2 - A shell tool for managing from EC2 instances.
"""


# dependencies :
#
# cmd, terminaltables, termcolor
#
# pip install them
#


# TODO : output to text file

class ec2_controller(cmd.Cmd):
    menu = {}
    ec2 = 0
    prompt = "e2c2> "
    config = {}

    def get_entry(self, menu_index):
        try:
            return self.menu[int(menu_index)]
        except Exception as e:
            return False

    def do_config(self, param):
        """
        Usage :

        config - dump e2c2 configuaton ( instances , keys etc )

        e.g. config
        """
        _instances = self.config['instances']
        _default_key = self.config['default_key']
        _ssh_path = self.config['ssh_path']
        print("")
        print ("%s: %s" % (colored("ssh keys path", _colors["conf_key_color"]), _ssh_path ))
        print ("%s: %s" % (colored("instances", _colors["conf_key_color"]), _instances.keys()))
        print ("%s: " % (colored("ssh keys", _colors["conf_key_color"])))

        for k in _instances:
            ins = _instances[k]
            if 'key' not in ins or 'user' not in ins:
                continue
            _user = ins['user']
            _key = ins['key']
            print ("\tinstance [%s] user [%s] key [%s] " % (
                colored(k, _colors["conf_val_color"]),
                colored(_user, _colors["conf_val_color"]),
                colored(_key, _colors["conf_val_color"]))
                   )

        print ("%s: %s" % (colored("default ssh key", _colors["conf_key_color"]), _default_key))
        print("")

    def do_quit(self, param):
        """
        Usage :

        quit - quits e2c2

        e.g. quit
        """
        return True

    def print_error(self, err_str):
        print (colored("error: %s" % err_str, _colors["error_color"]))
        return False

    def print_warning(self, err_str):
        print (colored("warning: %s" % err_str, _colors["warning_color"]))

    def do_ssh(self, menu_index):
        """
        Usage :

        ssh <#> -  start interactive ssh session to instance

        e.g. ssh 0
        """
        keys = {}

        if not self.valid_menu_index(menu_index):
            self.do_help("ssh")
            return

        # ins = _instances[self.menu[int(menu_index)]['id']]
        _instances      = self.config['instances']
        _default_key    = self.config['default_key']
        _ssh_path       = self.config['ssh_path']
        try:
            ins = _instances[self.menu[int(menu_index)]['id']]
            k = ins['key']
            keys['user'] = ins['user']
            keys['key'] = ins['key']
        except Exception as e:
            self.print_warning("ssh access info not configured for this entry, trying default ssh details")
            keys['user'] = _default_key['user']
            keys['key'] = _default_key['key']

        current_state = self.menu[int(menu_index)]['state']
        print ("status %s" % (current_state))
        if current_state != colored("RUNNING", _colors["running_color"]):
            self.print_error("machine is not running, start it first")
            return

        ip = self.menu[int(menu_index)]['pub_ip']
        ssh_string = "ssh {0}@{1} -i {2}/{3}".format(keys['user'], ip, _ssh_path, keys['key'])
        print ("ssh> %s" % ssh_string)
        os.system(ssh_string)

    def valid_menu_index(self, menu_index):
        if not menu_index or not menu_index.isdigit() or not self.get_entry(menu_index=menu_index):
            self.print_error("bad or missing menu item index")
            return False
        return True

    def do_stop(self, menu_index):
        """
        Usage :

        stop  <#> -  stop an instance

        e.g. stop 0
        """
        if not self.valid_menu_index(menu_index):
            self.do_help("stop")
            return

        current_state = self.menu[int(menu_index)]['state']

        if current_state != colored("RUNNING", _colors["running_color"]):
            self.print_error("machine is not running, start it first [ state = |%s| ] " % current_state)
            return

        print ("stopping menu item %s" % menu_index)
        entry = self.get_entry(menu_index)
        instance = self.ec2.Instance(entry['id'])
        result = instance.stop()
        print("HTTP %s" % result['ResponseMetadata']['HTTPStatusCode'])

    def do_start(self, menu_index):
        """
        Usage:

        start <#> -  start an instance

        e.g. start 0
        """
        if not self.valid_menu_index(menu_index):
            self.do_help("start")
            return

        current_state = self.menu[int(menu_index)]['state']

        if current_state == colored("RUNNING", _colors["running_color"]):
            self.print_error("machine is already running, stop it first [ state = |%s| ] " % current_state)
            return

        print ("starting menu item %s" % menu_index)
        entry = self.get_entry(menu_index)
        instance = self.ec2.Instance(entry['id'])
        result = instance.start()
        print("HTTP %s" % result['ResponseMetadata']['HTTPStatusCode'])

    def help_config(self):
        print ("")
        print (colored("config - dump e2c2 configuration", _colors['help_color']))
        print ("")

    def help_ssh(self):
        print ("")
        print (colored("ssh <#> - open interactive ssh session to instance ", _colors['help_color']))
        print ("")
        print (
            colored("note: this option requires ssh setup for this machine or default key compatibility in e2c2config ",
                    _colors['help_color']))
        print ("examples:")
        print ("")
        print(colored("\tssh 0\t\t# ssh session to instance at list row 0", _colors['help_color']))

    def help_start(self):
        print ("")
        print (colored("start <#> - start an instance ", _colors['help_color']))
        print ("")
        print ("examples:")
        print ("")
        print(colored("\tstart 0\t\t# start instance at list row 0", _colors['help_color']))

    def help_stop(self):
        print ("")
        print (colored("stop <#> - start an instance ", _colors['help_color']))
        print ("")
        print ("examples:")
        print ("")
        print(colored("\tstop 0\t\t# stop instance at list row 0", _colors['help_color']))

    def help_list(self):
        print ("")
        print (colored("list <opt> - retrieve list of all relevant instances from EC2", _colors['help_color']))
        print ("")
        print ("examples:")
        print ("")
        print(colored("\tlist	\t\t# list all instances configured in e2c2config", _colors['help_color']))
        print(colored("\tlist running\t\t# list all instances configured in e2c2config that are running",
                      _colors['help_color']))
        print(colored("\tlist %s\t\t# list all instances available in account" % "all", _colors['help_color']))
        print(colored("\tlist %s\t# list all instances available in account that are running" % "all-running",
                      _colors['help_color']))

    def do_list(self, param1="no"):
        """
        list <opt> - retrieve list of all relevant instances from EC2

        examples:

        list	# all instances configured in e2c2config
        list running	# all instances configured in e2c2config that are running
        list all	# all instances available in account
        list all-running	# all instances available in account that are running

        """
        self.menu = {}
        all_instances = {}
        _instances = self.config['instances']
        if param1 == "all":
            print ("retrieving all instances info..")
            all_instances = self.ec2.instances.all()
        elif param1 == "all-running":
            print ("retrieving all running instances info..")
            all_instances = self.ec2.instances.filter(Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['running']
                }
            ])
        elif param1 == "running":
            if not _instances:
                self.print_warning("no instances of interest specified in configuration, showing all instances ('list all-running')")
                all_instances = self.ec2.instances.filter(Filters=[
                    {
                        'Name': 'instance-state-name',
                        'Values': ['running']
                    }
                ])
            else:
                print ("retrieving running instances info..")
                all_instances = self.ec2.instances.filter(Filters=[
                    {
                        'Name': 'instance-id',
                        'Values': _instances.keys()
                    },
                    {
                        'Name': 'instance-state-name',
                        'Values': ['running']
                    }
                ])
        else:
            print ("retrieving instances info..")
            if not _instances:
                self.print_warning("no instances of interest specified in configuration, showing all instances ('list all')")
                all_instances = self.ec2.instances.all()
            else:
                all_instances = self.ec2.instances.filter(Filters=[
                    {
                        'Name': 'instance-id',
                        'Values': _instances.keys()
                    },
                ])

        menu_index = 0

        for i in all_instances:
            state = i.state['Name']
            pub_ip = i.public_ip_address
            instance_id = i.id
            instance_type = i.instance_type

            idict = {
                "state": state,
                "pub_ip": pub_ip,
                "id": instance_id,
                "type": instance_type
            }
            idict['state'] = idict['state'].upper()
            if idict['state'] == "RUNNING":
                idict['state'] = colored(idict['state'], _colors["running_color"])

            if not i.tags:
                self.print_warning("no tags for this entry [instance-id:%s]" % i.id)
                idict['name'] = "UNKNOWN"
            else:
                for idx, tag in enumerate(i.tags, start=1):
                    if (tag['Key'] == "Name"):
                        idict['name'] = tag['Value']
            self.menu[menu_index] = idict
            menu_index += 1

        table_data = [
            ['#', 'NAME', 'STATE', 'PUB_IP', 'TYPE', 'ID'],
        ]

        for index in self.menu:
            entry = self.menu[index]
            entry['list_index'] = "%s" % index
            table_data.append(entry.values())

        table = AsciiTable(table_data)

        print (table.table)


    def validate_configuration(self):
        error = 0;

        if not self.config:
            self.print_error("configuration object is empty, please specify your settings in e2c2config.py")
            return False

        if 'ssh_path' not in self.config:
            self.print_error("ssh_path not found in configuration. this field is mandatory")
            error = 1

        if 'instances' not in self.config:
            self.print_warning("configuration does not contain any instance info, you will only be able use 'all' functions (list all, list all-running)")
            self.config['instances'] = {}
            if 'default_key' not in self.config:
                error = 1
                self.print_error("no instances are configured (allowed), but no default key found")
        else:
            _instances = self.config['instances']
            for i in _instances:
                if 'key' not  in i:
                    if 'default_key' not in self.config:
                        error = 1
                        self.print_error("no key was specified for image {0} and 'default_key' is not found")

        if error:
            self.print_error("error(s) encountered while validating configuration, please fix and try again")
            return False

        print("configuration OK")
        return True

    def preloop(self):
        # fill the array once before everything
        print ("")
        print ("e2c2 - a cli shell tool for managing EC2 instances")
        print ("==================================================")
        print ("connecting to EC2..")
        self.ec2 = boto3.resource('ec2')
        e2c2config.auto_load()
        self.config = e2c2config._active_configuration
        if not self.validate_configuration():
            os._exit(-1)
        self.do_list("")
        self.do_help("")


if __name__ == '__main__':
    ec2_controller().cmdloop()
