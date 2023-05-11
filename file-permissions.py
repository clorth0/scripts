import os
import sys

# Get the file name from command line argument
if len(sys.argv) < 2:
    print("Usage: python script.py <filename>")
    sys.exit()
    
filename = sys.argv[1]

# Get the full path of the file
file_path = os.path.join(os.path.dirname(__file__), filename)

# Get the file permissions using os.stat
file_mode = os.stat(file_path).st_mode

# Define the permissions and their meanings
permissions = {
    'user': {
        'read': bool(file_mode & 0o400),
        'write': bool(file_mode & 0o200),
        'execute': bool(file_mode & 0o100)
    },
    'group': {
        'read': bool(file_mode & 0o40),
        'write': bool(file_mode & 0o20),
        'execute': bool(file_mode & 0o10)
    },
    'others': {
        'read': bool(file_mode & 0o4),
        'write': bool(file_mode & 0o2),
        'execute': bool(file_mode & 0o1)
    }
}

# Print the permissions and their meanings
print("File permissions for {}: ".format(filename))
for role in permissions:
    for permission in permissions[role]:
        print("{} {} permission: {}".format(role.capitalize(), permission, "Allowed" if permissions[role][permission] else "Not allowed"))
