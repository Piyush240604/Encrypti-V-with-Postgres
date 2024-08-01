import os
import stat

def get_access_type(file_path):
    try:
        # Get the status of the file or folder
        file_stat = os.stat(file_path)
        
        # Get the permission bits
        permissions = file_stat.st_mode
        
        # Map the permission bits to a string representation
        access_type = {
            'read': {
                'user': 'r' if permissions & stat.S_IRUSR else '-',
                'group': 'r' if permissions & stat.S_IRGRP else '-',
                'others': 'r' if permissions & stat.S_IROTH else '-',
            },
            'write': {
                'user': 'w' if permissions & stat.S_IWUSR else '-',
                'group': 'w' if permissions & stat.S_IWGRP else '-',
                'others': 'w' if permissions & stat.S_IWOTH else '-',
            },
            'execute': {
                'user': 'x' if permissions & stat.S_IXUSR else '-',
                'group': 'x' if permissions & stat.S_IXGRP else '-',
                'others': 'x' if permissions & stat.S_IXOTH else '-',
            }
        }
        
        # Combine the permission strings
        user_permissions = access_type['read']['user'] + access_type['write']['user'] + access_type['execute']['user']
        group_permissions = access_type['read']['group'] + access_type['write']['group'] + access_type['execute']['group']
        others_permissions = access_type['read']['others'] + access_type['write']['others'] + access_type['execute']['others']
        
        access_type_string = user_permissions + group_permissions + others_permissions
        
        return access_type_string
                
    except FileNotFoundError:
        print(f"The file or folder '{file_path}' does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
