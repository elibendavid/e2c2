# e2c2 - a cli shell for managing aws ec2 instances

## About

**e2c2** is a cli shell tool for managing aws ec2 instances. When you start e2c2 you will see a list menu of instances.
You can then perform operations on these instances like start, stop, ssh, based of their menu index in the list.

You can also define 'instances of interest' ( this is especially useful for account with a large amount of instances )
So when you 	```'list'``` your instances you will only see your instances of interest.
You can also ```'list running'``` to show only the instances of interest that are running.
If you want to see all your instances and not only those of interest you can use ```'list all'```, or ```'list all-running'```


It also possible to define **mutiple configurations**, usually associated with multiple aws accounts.
You can then define different keys, and different instances of interest for each aws account.

**autoload** - you can also load a configuration automatically according to content if environment variable ```AWS_DEFAULT_PROFILE``` is set. This behavior is defined by the ```_aws_profile_auto_load``` dictionary in e2c2config.py


It is recommended to go over e2c2config.py to check whats really going on.

## Install:

copy the files to the same location (aka <install_dir>)


## Setup:

goto e2c2config.py and modify the values in ```_default_config``` to conform with your aws account

**ssh_path** -  location of key files

**key** 	- is the name of the key file
**user** 	- is the user name


```
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
```


### Run
```
$ cd <install_dir>
$ ./e2c2.py
```




## Commands:

**list** 

```
list <opt> - retrieve list of all relevant instances from EC2

examples:

list                # list all instances configured in e2c2config
list running        # list all instances configured in e2c2config that are running
list all            # list all instances available in account
list all-running    # list all instances available in account that are running
```

**start**

```
start <#> - start an instance 

examples:

start 0		# start instance at list row 0
```

**stop**

```
stop <#> - stop an instance 

examples:

stop 0		# stop instance at list row 0
```


**ssh**

```
ssh <#> - open interactive ssh session to instance 

note: this option requires ssh setup for this machine or default key compatibility in e2c2config 
examples:

ssh 0		# ssh session to instance at list row 0
	
```

**Caveats**

* After starting an instance using 'start', you will need to do some 'list's until the instance is in running stat, only then can you start an ssh session to it using 'ssh' command
