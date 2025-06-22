# auto gen inventory.ini
import yaml
import ipaddress

class WriteFile( ) :
    def __init__( self ) :
        pass

    def is_valid_ip( self, ip_address ) : 
        try :
            ipaddress.ip_address( ip_address )
            return True
        except ValueError :
            print( 'Please input valid ip address!\n')
            return False

    def write_inventory( self, 
                         file_name = './inventory/hosts.yml', 
                         ip_address = None, 
                         user = None, 
                         sudo_password = None
                        ):
        if ip_address is None:
            raise ValueError("IP address is required")
            
        if not self.is_valid_ip( ip_address ) :
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
            yaml.dump(inventory, f, default_flow_style = False, sort_keys = False)
        return True
if __name__ == "__main__":
    writer = WriteFile()
    writer.write_inventory( ip_address='172.18.0.11', user='ubuntu01', sudo_password='Ubuntu01' )
    # writer.write_inventory( ip_address='256.168.1.1', user='admin', sudo_password='secret' )
