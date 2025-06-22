import subprocess

# with open( 'output.txt', 'w' ) as f :
    # p1 = subprocess.run( ['ls', '-la' ], capture_output = True ) # need decode -> p1.stdout.decode( )
    # p1 = subprocess.run( ['ls', '-la' ], stdout=subprocess.PIPE, text=True ) #no need decode
    # p1 = subprocess.run( ['ls', '-la' ], stdout=f, text=True ) # write to file
    # print( p1.args )
    # print( p1.returncode ) # show error
    # print( p1.stdout )

# Error handling
# p1 = subprocess.run( ['ls', '-la' , 'dne'], capture_output = True, text=True, check=True )
# print( p1.returncode )
# print( p1.stderr )

# p1 = subprocess.run( ['ls', '-la' , 'dne'], stderr=subprocess.DEVNULL, check=True )
# print( p1.stderr )

# Read from input
p1 = subprocess.run( ['cat', 'test.txt'], capture_output=True, text=True )
# print( p1.stdout )
p2 = subprocess.run( ['grep', '-n' , 'is'], 
                        capture_output=True, text=True, input=p1.stdout )
print( p2.stdout )
