import customtkinter as ctk
import threading
import queue
from features import Clock, Appearance, Textbox, Progressbar
import nmap
# import sqlite3
# from sqlite3 import Error
from datetime import datetime
import psycopg2

class NmapPage( ctk.CTkFrame ) :
    def __init__( self, master ) :
        super( ).__init__( master )
        self.result_queue = queue.Queue( ) # Add queue for thread-safe communication ( for the fucking textbox )
        self.scan_complete_event = threading.Event( )
        self.after( 100, self.process_queue ) # Keep update the fucking queue periodically
        # Configuration
        # self.database = r'sasqdemo.db'
        # self.conn = self.create_connection( self.database )
        # self.data = self.select_all_records( )
        self.scanner = nmap.PortScanner()
        self.font_style = ( "Helventica bold", 15 )

        # Nmap Sidebar Frame
        self.nmap_sidebar = ctk.CTkFrame( 
            master, 
            width = 70, 
            corner_radius = 0 
        )
        self.nmap_sidebar.grid( 
            row = 0, 
            rowspan = 4, 
            column = 2, 
            sticky = 'nsew' 
        )
        # Clock
        self.date_label = Clock( self.nmap_sidebar ).date_label
        self.date_label.pack(
            side = 'top',
            pady = ( 10, 0 )
        )
        self.day_label = Clock( self.nmap_sidebar ).day_label
        self.day_label.pack(
            side = 'top',
        )
        self.time_label = Clock( self.nmap_sidebar ).time_label
        self.time_label.pack(
            side = 'top',
            pady = ( 20 , 0)
        )     
        # Sidebar
        self.page_label = ctk.CTkLabel( 
            self.nmap_sidebar, 
            text = "Nmap Page", 
            font = ctk.CTkFont("Segoe Script", 30 ),
        )
        self.page_label.pack( 
            side = 'top',
            pady = ( 40, 30 ),
        )
        # left sidebar window 1


        self.scan_network = ctk.CTkButton( 
            self.nmap_sidebar, 
            text="Scan Network",
            width = 180,
            height = 50,
            font = ctk.CTkFont( "Segoe Script", 15 ),
            command = self.scan_network
        )
        self.scan_network.pack( 
            side = 'top',
            pady = ( 20, 20 ),
            padx = ( 0, 0 )

        )

        self.save_btn = ctk.CTkButton(
            self.nmap_sidebar, 
            text = "Save Record", 
            width = 180,
            height = 50,
            font = ctk.CTkFont("Segoe Script", 15 ),
            #command = self.save_results 
        )
        self.save_btn.pack(
            side = 'top',
            pady = ( 10 , 50 ),
            padx = ( 0 , 0 ),
        )
        self.clear_btn = ctk.CTkButton(
            self.nmap_sidebar, 
            text = "Clear", 
            width = 180,
            height = 50,
            font = ctk.CTkFont("Segoe Script", 15 ),
            command = self.clear_textbox
        )
        self.clear_btn.pack(
            side = 'top',
            pady = ( 10 , 50 ),
            padx = ( 0 , 0 )
        )

        # Appearance
        self.appearance_label = Appearance( self.nmap_sidebar ).appearance_label
        self.appearance_label.configure( 
            font = ctk.CTkFont("Segoe Script", 20 )
        )
        self.appearance_label.pack( 
            side = 'top',
            pady = ( 150, 20 )
        )

        self.appearance_optionmenu = Appearance( self.nmap_sidebar ).appearance_optionmenu
        self.appearance_optionmenu.configure(
            width = 150,
            height = 40, 
            font = ctk.CTkFont("Segoe Script", 15 ),
            dropdown_font = ctk.CTkFont("Segoe Script", 15 ),
        )
        self.appearance_optionmenu.pack( 
            side = 'top',
            pady = ( 20, 20 )
        )

        self.scale_label = Appearance( self.nmap_sidebar ).scale_label
        self.scale_label.configure( 
            font = ctk.CTkFont("Segoe Script", 20 )
        )
        self.scale_label.pack( 
            side = 'top',
            pady = ( 10, 20 )
        )

        self.scale_optionmenu = Appearance( self.nmap_sidebar ).scale_optionmenu
        self.scale_optionmenu.configure(
            width = 150,
            height = 40,
            font = ctk.CTkFont("Segoe Script", 15 ),
            dropdown_font = ctk.CTkFont("Segoe Script", 15 ),
        )
        self.scale_optionmenu.pack(
            side = 'top',
        )

        # Text Box Frame
        self.nmap_textbox_frame = ctk.CTkFrame( 
            master, 
            width = 70, 
            corner_radius = 0 
        )
        self.nmap_textbox_frame.grid( 
            row = 0, 
            rowspan = 4, 
            column = 4, 
            sticky = 'nsew',
        )
        # Textbox
        self.nmap_textbox = Textbox( self.nmap_textbox_frame ).textbox
        self.nmap_textbox.pack(
            side = 'top',
            padx = ( 0,0 ),
            pady = ( 0, 0 ),
            expand = True,
            fill = 'both',
        )
        # Progress bar
        self.progressbar = Progressbar( self.nmap_textbox_frame ).progressbar
        self.progressbar.pack(
            side = 'top',
            fill = 'both',
            padx = (10,10),
            pady = (10,10),
        )
        self.progressbar.set( 0 )
        # self.progressbar.forget()

        # Configuration Frame
        self.config_frame = ctk.CTkFrame( 
            master, 
            width = 300,
            border_width = 10,
        )
        self.config_frame.grid( 
            row = 0, 
            column = 6, 
            rowspan = 2,
            sticky = 'nsew',
        )
        self.nmap_tab = ctk.CTkTabview(
            self.config_frame,
            width = 80,
            height = 400,
        )
        self.nmap_tab.pack(
            side = 'top',
        )
        self.nmap_tab.add( 'Scan Config' )
        self.nmap_tab.add( 'Scan Log' )
        self.ip_label = ctk.CTkLabel(
            self.nmap_tab.tab( 'Scan Config' ), 
            text = "Target IP : ",
            font = ( "Comic Sans MS", 20 ),
        )
        self.ip_label.grid(
            row = 0, 
            column = 0, 
            padx = (10, 0), 
            pady = (20, 5), 
            sticky = "ew"
        )
        self.ip_entry = ctk.CTkEntry(
            self.nmap_tab.tab( 'Scan Config' ), 
            placeholder_text = "IP address",
            width= 200,
        )
        self.ip_entry.grid(
            row=0, 
            column=1, 
            padx=(10,10), 
            pady=(25, 10), 
            sticky="ew"
        )

        # Scan Options
        self.nmap_version_radio_var = ctk.StringVar( value = "off" )
        self.nmap_version_radio = ctk.CTkCheckBox(
            self.nmap_tab.tab( 'Scan Config' ), 
            text="Nmap Version",
            variable = self.nmap_version_radio_var,
            onvalue = "on",
            offvalue = "off",
            font = ( "Comic Sans MS", 15 )
        )
        self.nmap_version_radio.grid(
            row=1, 
            column=0, 
            padx=(30, 30), 
            pady=(30, 20), 
            sticky="nsew"
        )

        self.number_of_host_radio_var = ctk.StringVar( value = "off" )
        self.number_of_host_radio = ctk.CTkCheckBox(
            self.nmap_tab.tab( 'Scan Config' ), 
            text="Number of Hosts",
            variable = self.number_of_host_radio_var,
            onvalue = "on",
            offvalue = "off",
            font = ( "Comic Sans MS", 15 )
        )
        self.number_of_host_radio.grid(
            row=1, 
            column=1, 
            padx=(30,0), 
            pady=(40, 30), 
            sticky="nsew"
        )

        self.ip_radio_var = ctk.StringVar( value = "off" )
        self.ip_radio = ctk.CTkCheckBox(
            self.nmap_tab.tab( 'Scan Config' ), 
            text="IP addresses",
            variable = self.ip_radio_var,
            onvalue = "on",
            offvalue = "off",
            font = ( "Comic Sans MS", 15 )
        )
        self.ip_radio.grid(
            row=2, 
            column=0, 
            padx=(30,30), 
            pady=(30, 20), 
            sticky="nsew"
        )

        self.service_radio_var = ctk.StringVar( value = "off" )
        self.service_radio = ctk.CTkCheckBox(
            self.nmap_tab.tab( 'Scan Config' ), 
            text="Running Service",
            variable = self.service_radio_var,
            onvalue = "on",
            offvalue = "off",
            font = ( "Comic Sans MS", 15 )
        )
        self.service_radio.grid(
            row=2, 
            column=1, 
            padx = ( 30, 0 ), 
            pady = ( 30, 30 ), 
            sticky="nsew"
        )

        self.os_radio_var = ctk.StringVar( value = "off" )
        self.os_radio = ctk.CTkCheckBox(
            self.nmap_tab.tab( 'Scan Config' ), 
            text="OS Version",
            variable = self.os_radio_var,
            onvalue = "on",
            offvalue = "off",
            font = ( "Comic Sans MS", 15 )
        )
        self.os_radio.grid(
            row=3,
            column=0,
            padx=( 30, 30),
            pady=( 30, 0 ),
            sticky="nsew"
        )

        self.server_name_radio_var = ctk.StringVar( value = "off" )
        self.server_name_radio = ctk.CTkCheckBox(
            self.nmap_tab.tab( 'Scan Config' ), 
            text="Server Name" ,
            variable = self.server_name_radio_var,
            onvalue = "on",
            offvalue = "off",
            font = ( "Comic Sans MS", 15 )
        )
        self.server_name_radio.grid(
            row=3,
            column=1,
            padx=( 30, 0 ),
            pady=( 30, 0 ),
            sticky="nwse"
        )

        # History Box
        self.display_button = ctk.CTkButton(
            self.nmap_tab.tab( 'Scan Log' ), 
            text = "Display Records",
            font = ( "Comic Sans MS", 20 ),
            width = 250,
            height = 50,
            #command = self.display_to_text
            #command = lambda: self.display_to_text( self.data ),
        )
        self.display_button.grid(
            row=2, 
            column=0,
            columnspan = 2,
            rowspan = 2,
            padx=( 10, 10 ), 
            pady=( 30, 20), 
            sticky="nwse"
        )

        self.del_id_label = ctk.CTkLabel(
            self.nmap_tab.tab( 'Scan Log' ), 
            text = "Delete ID : ",
            font = ( "Comic Sans MS", 20 ),
        )
        self.del_id_label.grid( 
            row=5, 
            column=0,
            padx=(0, 0), 
            pady=( 40, 20 ), 
            sticky="nwse" 
        )

        self.del_id_box = ctk.CTkEntry(
            self.nmap_tab.tab( 'Scan Log' ), 
            placeholder_text = "data id", 
            font = ( "Comic Sans MS", 20 ),
            width = 220,
            justify = 'center'
        )
        self.del_id_box.grid(
            row=5, 
            column=1, 
            padx = ( 0, 20 ), 
            pady=( 20, 0), 
            sticky="nwse"
        )

        self.del_data_label = ctk.CTkLabel(
            self.nmap_tab.tab( 'Scan Log' ), 
            text = "Delete Data : ",
            font = ( "Comic Sans MS", 20 ),
        )
        self.del_data_label.grid( 
            row=7, 
            column=0,
            padx=( 10, 0), 
            pady=( 40,0 ), 
            sticky="nwse" 
        )

        self.del_data_btn = ctk.CTkButton(
            self.nmap_tab.tab( 'Scan Log' ),
            text = "Delete Data", 
            font = ( "Comic Sans MS", 20 ),
            width=100,
            height=50,
            fg_color= 'orange',
            hover_color = 'red'
            # command = self.delete_data 
        )
        self.del_data_btn.grid(
            row=7, 
            column=1, 
            padx=( 10, 0 ), 
            pady=( 40, 0 ) ,
            sticky="nwse",
        )
        # Remark Frame
        self.remark_frame = ctk.CTkFrame( 
            master, 
            width = 300,
            border_width = 20,
            corner_radius = 10,
        )
        self.remark_frame.grid( 
            row = 2, 
            column = 6,
            rowspan = 2,
            sticky = 'nsew',
        )
        self.remark_box = ctk.CTkTextbox(
            self.remark_frame,
            font = ( "Comic Sans MS", 20 ),
            border_width = 10,
        )
        self.remark_box.pack(
            side = 'top',
            expand = True,
            fill = 'both'
    
        )
        self.remark_box.insert( 
            "0.0",
            "\nRemarks:\n\n"
            "1. Number of hosts:\n    Scan all the hosts in the target network.\n"
            "2. IP addresses:\n    Shows the IP addresses of the hosts.\n"
            "3. Running Service:\n    Shows hosts running service.\n"
            "4. OS Version:\n    Shows hosts OS Version\n"
            "5. Server name:\n    Server name (If server was found)\n"
            "6. Nmap Version:\n    Shows Nmap version"
        )

    def process_queue( self ) :
        try :
            while True :
                result = self.result_queue.get_nowait( ) # get result from the queur
                self.nmap_textbox.insert( 'end', str( result ) )
        except queue.Empty :
            pass
        self.after( 100, self.process_queue ) # keep update queue

    def run_in_thread( self, target, args=( ) ):
        def wrapper( ) :
            try :
                result = target( *args ) # host_list
                self.result_queue.put( str( result ) ) # put host from host_list in queue
            except Exception as e :
                self.result_queue.put( f"Error: { str( e ) }\n" )
            finally :
                self.scan_complete_event.set()

        thread = threading.Thread( target = wrapper )
        thread.start( )
        return thread

    def clear_textbox(self):
        self.nmap_textbox.delete( '0.0', 'end' )

    def show_command_executed( self ):
        return f"Command executed:\n{ self.scanner.command_line( ) }\n"

    def get_nmap_version( self ):
        return f"\nNmap Version:\t{ self.scanner.nmap_version( )[0] }.{ self.scanner.nmap_version()[1] }\n"

    def get_number_of_host( self, host_list ) :
        return f"\nTotal number of Hosts: { str( len( host_list ) ) }"
    
    def nmap_getIp( self, host_list ) :
        ip_list = '\nThe hosts ip are:\n'
        for num, host in enumerate( host_list, start = 1 ) :
            ip_list += f"{num} . {host}\n"
        return ip_list

    def scan_services( self, host_list ):
        display_service = ''
        for host in host_list :
            self.scanner.scan( host, arguments='-v -sS -Pn' ) # sudo = True
            display_service += f"command executed: \n{ self.scanner.command_line( ) }\n"
            if 'tcp' in self.scanner[host] :
                open_ports = self.scanner[host]['tcp'].keys( )
                scanned_results = self.scanner[host]['tcp']
                display_service += f"\nOpen Port\t\tService\t\tScan Type"
            
                for port in open_ports :
                    service_name = scanned_results[port]['name']
                    scan_type = scanned_results[port]['reason']
                    display_service += f"\n{port}\t\t{service_name}\t\t{scan_type}"
            else :
                display_service += f"No open TCP ports found for host {host}.\n"
        return display_service

    def get_server_version( self, host_list ) :
        display_os_info = ''
        for host in host_list: 
            self.scanner.scan( host, arguments='-O' ) #sudo = True
            self.run_in_thread( self.show_command_executed )
            if 'osmatch' in self.scanner[host]:
                for osmatch in self.scanner[host]['osmatch']:
                    if 'osclass' in osmatch:
                        for osclass in osmatch['osclass']:
                            display_os_info += f"\nIp Address : {host}\n"
                            display_os_info += f"OS name : {osmatch['name']}\n"
                            display_os_info += f"OS type : {osclass['type']}\n"
                            display_os_info += f"OS vendor : {osclass['vendor']}\n"
                            display_os_info += f"OS family : {osclass['osfamily']}\n"
        return display_os_info

    def get_server_name(self, host_list):
        display_server_name = ''
        for host in host_list:
            self.scanner.scan(host, arguments='-A')  # Perform an aggressive scan
            self.run_in_thread( self.show_command_executed )
            print( self.scanner.scan(host, arguments='-A') )
            if 'hostscript' in self.scanner[host]:
                for d in self.scanner[host]['hostscript'] :
                    for key, value in d.items():
                        if "NetBIOS name" in value:
                            script_output = value
                            name = script_output.split( ':' )
                            name = name[1].split(',')
                            server_name = f"The Server Name is: {name[0]}"
                            display_server_name += server_name
            else :
                display_server_name += "This is not a server!"
        return display_server_name

    def scan_network( self ) :
        try :
            target_ip = self.ip_entry.get( )
            if not target_ip:
                self.result_queue.put( "Please enter target IP.\n" )
                return
            self.scan_complete_event.clear()
            self.run_in_thread( self.clear_textbox )
            # Show command executed
            self.result_queue.put( "Starting scan...\n")

            #Perform Scan
            self.scanner.scan( target_ip, arguments = '-sS -Pn' ) #, sudo = True )
            self.run_in_thread( self.show_command_executed ) 
            host_list = self.scanner.all_hosts( )
            # Update progressbar :
            self.progressbar.set( 0.2 )

            threads= list( )

            # 1. Show Nmap Version
            if self.nmap_version_radio.get( ) == 'on' :
                thread = self.run_in_thread( self.get_nmap_version )
                threads.append( thread )
                self.result_queue.put( "\n" )
            
                # Update progressbar :
                self.progressbar.set( 0.3 )

            # 2. Show Numner of Hosts    
            if self.number_of_host_radio.get( ) == "on" :
                thread = self.run_in_thread( self.get_number_of_host, args=( host_list, ) )
                threads.append( thread )
                self.result_queue.put( "\n" )

            # 3.Show Target Ip
            if self.ip_radio.get( ) == 'on' :
                thread = self.run_in_thread( self.nmap_getIp, args=( host_list, ) )
                threads.append( thread )
            
                # Update progressbar :
                self.progressbar.set( 0.4 )

            # 4. Show running services
            if self.service_radio.get() == 'on' :
                thread = self.run_in_thread( self.scan_services, args = ( host_list, ) )
                threads.append( thread )
                self.result_queue.put( "\n")
            
                # Update progressbar :
                self.progressbar.set( 0.6 )

            # 5. Show operation system
            if self.os_radio.get( ) == 'on' :
                thread = self.run_in_thread( self.get_server_version, args = ( host_list, ) )
                threads.append( thread )
                self.result_queue.put( "\n")
            
                # Update progressbar :
                self.progressbar.set( 0.8 )

            # 6. Show Server name
            if self.server_name_radio.get() == 'on' :
                thread = self.run_in_thread( self.get_server_name, args = ( host_list, ) )
                threads.append( thread )
                # Update progressbar :
                self.progressbar.set( 1 )

            # for thread in threads :
            #     thread.join( ) # until all thread finished
                
            self.result_queue.put( "\nScan completed.\n" )
            self.progressbar.set( 1 )

        except nmap.PortScannerError as e :
            self.result_queue.put( f"Nmap PortScannerError: { str( e )}\n" )
            self.progressbar.set( 0 )

        except Exception as e :
            self.result_queue.put( f"An error occurred: { str( e )}\n" )
            self.progressbar.set( 0 )



    # def insert_record( self, new_data ) :
    #     self.new_data = new_data
    #     cur = self.conn.cursor( )
    #     sql = "INSERT INTO scanning_history ( scanning_target, )"