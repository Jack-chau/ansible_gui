import docker

class DockerFunctions( ) :
	
	def __init__( self ):
		self.client = docker.from_env()
	# Ping
	def check_connection( self ) :
		try :
			self.client.ping( )
			welcome = rf"""
				       🫧
				     🫧🫧🫧          
				  🫧🫧🫧🫧🫧🫧     
				🫧🫧🫧🫧🫧🫧🫧🫧
				################"\___/ ===
				{{    /  ====	\___/ 
				\____ o         __/
				 \    \       __/
				  \    \    ___/
				   \____\____/
				
				DOCKER: 🐳Yea!!!🐳
		🔥🔥🔥Docker are successfully connected!🔥🔥🔥
				"""
			print(welcome)
		except Exception as e :
			print( f"❌Failed to connect to Docker: {str( e ) }❌" )
	
	# List all containers
	def list_all_containers( self ) :
		containers = self.client.containers.list( all = all )
		containers_list = list( )
		for container in containers :
			containers_list.append(
				{
					'id' : container.short_id,
					'name' : container.name,
					'status' : container.status,
					'newtwork_name' : list( container.attrs['NetworkSettings']['Networks'].keys())[0],
					'ip_addr' : container.attrs['NetworkSettings']['IPAddress'],
					'port' : container.attrs['NetworkSettings']['Ports']
				}
			)
		if len( containers_list ) > 0 :
			self.show_container_info( containers_list )
		else :
			print( "No running container" )


	def list_runing_containers( self ) :
		running_containers = self.client.containers.list( all = False )
		running_containers_list = list( )
		for container in running_containers :
			network_settings = container.attrs['NetworkSettings']['Networks']
			# Get network if exists
			if network_settings :
				network_info = dict()
				for network_name, network_setting in network_settings.items( ) :
					network = self.client.networks.get( network_setting[ 'NetworkID' ] )
					network_info[network_name] = {
						'driver' : network.attrs['Driver'],
						'network_id' : network.id,
						'ip_address' : network_setting['IPAddress'],
					}

			running_containers_list.append(
				{
					'id' : container.short_id,
					'name' : container.name,
					'status' : container.status,
					'newtwork_name' : list( network_info.keys())[0],
					'network_type' : network_info[network_name]['driver'],
					'ip_addr' : network_info[network_name]['ip_address'] ,
					'ports' : ', '.join( container.attrs['NetworkSettings']['Ports'].keys() )
				}
			)
		if len( running_containers_list ) > 0 :
			self.show_container_info( running_containers_list )
			# print( running_containers_list )
		else :
			print( "No running containers" )

	
	def show_container_info( self, data_list ) :
		id = True
		name = True
		status = True
		network_type = True
		newtwork_name = True
		ip_addr = True
		port = True
		num_of_container = 1
		for i in data_list:
			print( f"The NO:{num_of_container} container status:")
			if i['id'] and id == True :
				keys = f"{'id'}\t"
				values = f"{i['id']}\t"

			if i['name'] and name == True :
				keys += f"\t{'name'}\t\t"
				values += f"{i['name']}\t"

			if i['status'] and status == True :
				keys += f"{'status'}\t\t" 
				values += f"{i['status']}\t\t"
			
			if i['network_type'] and newtwork_name == True :
				keys += f"{'network_type'}\t" 
				values += f"{i['network_type']}\t\t"  

			if i['newtwork_name'] and newtwork_name == True :
				keys += f"{'newtwork_name'}\t\t" 
				values += f"{i['newtwork_name']}\t" 

			if i['ip_addr'] and ip_addr == True :
				keys += f"{'ip_addr'}\t\t" 
				values += f"{i['ip_addr']}\t" 

			if i['ports'] and port == True :
				keys += f"{'port'}\t\t" 
				values += f"{i['ports']}\t" 
			num_of_container += 1
			print( keys )
			print( values )
			print( '\n' )

	
	def run_container( self, image, command = None, detach = True, ports = None, name = None, network = None, static_ip = None ) :
		try :
			container = self.client.containers.run( 
				image = image,
				command = command,
				detach = detach,
				ports = ports,
				name = name,
				network = network,
				static_ip = static_ip
			)
			if detach :
				print( f"container {container.id} is running with detach mode" )
			else :
				print( f"container {container.id} is running without detach mode" )
			if network:
				net = self.client.networks.get( network )
				net.connect(
					container = container.id,
					ipv4_address = static_ip
				)
		
		except Exception as e :
			print( f"❌Fail to run container")
		
	def stop_container( self, container_id ) :
		try :
			container = self.client.container.get( container_id )
			container.stop()
			print( f"{container.id} is stoped." )
		except Exception as e :
			print( e )
	
	def remove_container( self, container_id , force = False ) :
		try :
			container = self.client.container.get( container_id )
			container.remove( force = force )
		except Exception as e :
			print( e )

	def list_image( self ) :
		return self.client.imgaes.list( )
	
	def pull_image( self, repository, tag = "latest" ) :
		return self.client.imgaes.pull( f"{repository} : {tag}" )

	def remove_image( self, image_id, force = False ) : #If force=true, it force the removeal of image even it is currently in use.
		to_remove = input( f"Do you want to remove the image {image_id} ?")
		if to_remove :
			self.client.imgaes.remove( image_id, force = force )
			return f"The image {image_id} has been removed."
		else :
			return f"The action has been cancled."
 
	def list_network( self ):
		return self.client.network.list()
	
	def create_network( self, name, driver = "bridge" ) :
		return self.client.networks.create( name, driver=driver )
	
	def set_static_ip( self, container_id, network_name, ip_addr ) :
		try :
			# Get the container
			container = self.client.container.get( container_id )

			# Get the network
			network = self.client.networks.get( network_name )

			# Disconnect if network already added
			if network_name in container.attrs[ 'NetworkSettings' ][ 'Networks' ]:
				network.disconnect( container )
			
			# Assign network and set static IP
			self.client.api.connect_container_to_network(
				container.id,
				network_name,
				ipv4_address = ip_addr
			)
			
			# Verify the container was assigned static IP
			container.reload()
			assigned_ip = container.attrs[ 'NetworkSettings' ][ 'Networks' ] [ network_name ][ "IPAddress" ]
			
			if assigned_ip == ip_addr :
				print( f"Sucessfully assigned static IP {ip_addr} to container { container_id }." )
				return
			else :
				print( f"Failed to assign static IP." )
				return
		except Exception as e :
			print( f"Unexpected error: {str( e )}" )

a = DockerFunctions()
print(a.check_connection())
# a.run_container( image="nginx:alpine", name="my_web_server", ports={'80/tcp':8080}, network="my-docker-network" )
# print( a.list_all_containers() )
# a.run_container( image = 'alpine', command = [ 'echo', 'hello', 'world'], name = 'alpine3', detach=True )
# print( a.list_runing_containers( ) )