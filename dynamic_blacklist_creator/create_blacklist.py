# Creates a blacklist.json from a pre-created pipe-seperated coinlist

import os, sys
import blacklist_prefix as first
import blacklist_suffix as second

# Get template strings
blacklist_template_first = first.string
blacklist_template_second = second.string

# Get blacklist coins
with open(os.path.join(sys.path[0], 'to_blacklist.txt'), 'r') as file:
    coinlist = file.read()

# Create blacklist-string
string_to_file = blacklist_template_first + coinlist + blacklist_template_second

# Write blacklist to file_object
# TODO: Create filename dynamically (eg. exchange/currency/strategy)
blacklist_file = open(os.path.join(sys.path[0], 'a_new_blacklist.json'), 'w')
blacklist_file.write(string_to_file)
blacklist_file.close()

# empty to_blacklist.txt
open(os.path.join(sys.path[0], 'to_blacklist.txt'), 'w').close()