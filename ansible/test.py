import yaml
import ipaddress

def is_valid_ip( ip_address ) : 
    try :
        ip_address= ipaddress.ip_address( ip_address )
        return True
    except ValueError :
        print( 'Please input valid ip address!\n')

def write_inventory( file_name='./inventory/hosts', ip_address=None, user=None, sudo_password=None):
    if ip_address is None:
        raise ValueError("IP address is required")
        
    if not is_valid_ip( ip_address ) :
        return False
        
    inventory = {
        'servers': {
            'hosts': {
                ip_address: {
                    'ansible_user': user,
                    'ansible_become_pass': sudo_password
                }
            }
        }
    }
    
    with open( file_name, 'w' ) as f:
        yaml.dump(inventory, f)
    return True

write_inventory( ip_address='192.168.1.1', user='admin', sudo_password='secret' )