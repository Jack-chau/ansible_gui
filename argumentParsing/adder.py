# This program calculates the volume of a cylinder given the radius and height
# Cylinder volume formula: V = πr^2h
import math
import argparse

parser = argparse.ArgumentParser( description = "Calculate the volume of a cylinder" )
parser.add_argument( "-r", "--radius", metavar = '', required = True ,type = int, help = "The radius of the cylinder" )
parser.add_argument( "-H", "--height", metavar = '', required = True ,type = int, help = "The height of the cylinder" )
group = parser.add_mutually_exclusive_group()
group.add_argument( '-q', '--quiet', action = 'store_true', help = "print quiet" ) 
group.add_argument( '-v', '--verbose', action = 'store_true', help = "print verbose" )


args = parser.parse_args()

def cylinder_volume(radius, height):
    volume = math.pi * radius**2 * height
    return round(volume, 2)

if __name__ == "__main__":
    volume =  cylinder_volume( args.radius, args.height )
    if args.quiet:
        print( volume )
    elif args.verbose:
        print( f"The volume of the cylinder is {volume}" )
    else:
        print( f"The volume of the cylinder is {volume}" )
    