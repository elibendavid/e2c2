# -*- coding: utf-8 -*-
# @Author: Eli Ben-David
# @Date:   2017-09-21 11:33:48
# @Last Modified by:   Eli Ben-David
# @Last Modified time: 2018-09-17 17:17:38
import os

_colors = {
    "running_color": 'magenta',
    "conf_key_color": 'cyan',
    "conf_val_color": 'yellow',
    "error_color": 'red',
    "warning_color": 'yellow',
    "help_color": 'white',
}


# this is the default configuration
# replace YOUR_SSH_KEY and YOUR_SSH_USER with real life values
# e.g. {"key":"mykeyfile.pem" , "user":"ubuntu"}
_default_config = {
    "ssh_path": "~/.ssh",
    "default_key": {
        "key": "YOUR_SSH_KEY",  # replace this
        "user": "YOUR_SSH_USER" # replace this
    },
}

#
# Sample Configuration
#
sample_config1 =  {
    # *mandatory*
    #
    # define a path for your ssh keys
    "ssh_path": "~/.ssh",

    # define the default key to user if to set for an instance,
    # *mandatory* if no keys are defined in instances
    "default_key": {
        "key": "YOUR_SSH_KEY",  # replace this
        "user": "YOUR_SSH_USER"  # replace this
    },


    # this defines instances of interest, these will show when doing 'list', or 'list running' ( as opposed to 'list all', 'list all-running' that will show all instances, and not just those of interest)
    "instances" : {
        "YOUR_INSTANCE_ID1" : {
            # this key will be used when connecting this instance
            "key" : "YOUR_INSTANCE_SPECIFIC_SSH_KEY1",
            "user": "YOUR_INSTANCE_SPECIFIC_SSH_USER1",
        },
        "YOUR_INSTANCE_ID2": {
            # this key will be used when connecting this instance
            "key": "YOUR_INSTANCE_SPECIFIC_SSH_KEY2",
            "user": "YOUR_INSTANCE_SPECIFIC_SSH_USER2",
        },
        "YOUR_INSTANCE_ID3": {
            # the default key will be used when connecting to this instance
        }

    }

}


#
# OPTIONAL :
#
# this dictionary is used for automatically loading different configurations according to AWS_DEFAULT_PROFILE env var
# if not set or not found, _default_config is loaded
# _aws_profile_auto_load = {
#     "YOUR_AWS_PROFILE_1": sample_config1,
#     "YOUR_AWS_PROFILE_1": sample_config2,
# }


_aws_profile_auto_load  = {}
_active_configuration = {}


def auto_load():
    global _active_configuration
    profile = os.getenv("AWS_DEFAULT_PROFILE")

    if profile in _aws_profile_auto_load:
        print("auto-loading configuration for aws profile " + os.getenv("AWS_DEFAULT_PROFILE"))
        _active_configuration = _aws_profile_auto_load[profile]
    else:
        print("no auto load info found or AWS_DEFAULT_PROFILE not set, loading default configuration")
        _active_configuration = _default_config
