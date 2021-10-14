# Creates a blacklist.json from a pre-created pipe-seperated coinlist

import os, sys
import blacklist_prefix as first
import blacklist_suffix as second
import blacklist_create_config as config

# Get template strings
blacklist_template_first = first.string
blacklist_template_second = second.string

# Get directories
temp_directory = config.temp_directory
BL_directory = config.blacklist_directory

# TODO: Try/catch with empty files? if (os.stat("file").st_size == 0) ...

# Get blacklist coins
with open(os.path.join(temp_directory, 'to_blacklist.txt'), 'r') as file:
    coinlist = file.read()
    file.close()
    
# Get strategy name and currecy
with open(os.path.join(temp_directory, 'stratname.txt'), 'r') as file:
    stratname = file.read().splitlines()
    strategy = stratname[0]
    currency = stratname[1]
    file.close()

# Create blacklist string
string_to_file = blacklist_template_first + coinlist + blacklist_template_second

# Creat blacklist filename
# TODO: Add exchange to filename
filename = 'blacklist-' + currency + '-' + strategy + '.json'

# Write blacklist to file_object
blacklist_file = open(os.path.join(BL_directory, filename), 'w')
blacklist_file.write(string_to_file)
blacklist_file.close()

# empty to_blacklist.txt and stratname.txt
open(os.path.join(temp_directory, 'to_blacklist.txt'), 'w').close()
open(os.path.join(temp_directory, 'stratname.txt'), 'w').close()