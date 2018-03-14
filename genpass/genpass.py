#!/usr/bin/env python
#-*- conding: utf-8 -*-

import string, random

try:
    input = raw_input
except NameError:
    pass

def generate_password(password_length, special):

    password_length = int(password_length)

    a_list = list(string.ascii_lowercase)
    b_list = list(string.ascii_uppercase)
    c_list = list(range(10))
    d_list = [ '%', '*', ')', '(', '?', '@', '#', '$', '~' ]

    if special == 's':
        full_list = [ a_list, b_list, c_list, d_list ]
    else:
        full_list = [ a_list, b_list, c_list ]

    n_1 = random.randrange(len(full_list))
    character_type = full_list[n_1]
    n_2 = random.randrange(len(full_list[n_1]))
    charachter = full_list[n_1][n_2]

    password = ''

    for i in range(password_length):
        n_1 = random.randrange(len(full_list))
        character_type = full_list[n_1]
        n_2 = random.randrange(len(full_list[n_1]))
        charachter = full_list[n_1][n_2]
        password = password + str(charachter)

    print ("Password: " + password)
    input("Press 'Enter' to exit\n>")

def generate_password_no_special(password_length):
    password = generate_password(password_length, 'ns')

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3:
        generate_password(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        if sys.argv[1] == '--help':
            print ('Usage: genpass <password length> [<s>]\
            \n  <password length>   - integer number\
            \n  <s>         - use special characters in password')
        else:
            generate_password_no_special(sys.argv[1])
    else:
        print ('Wrong number of arguments!\
        \nUsage: genpass <password length> [<s>]\
        \n  <password length>   - integer number\
        \n  <s>         - use special characters in password')
