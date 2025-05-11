import yaml
import random
import getpass

with open( 'game_conf.yml', 'r' ) as f:
    config = yaml.safe_load( f )

range_min = config[ 'range' ][ 'min' ]
range_max = config[ 'range' ][ 'max' ]
guesses_allowed = config[ 'guesses' ]
mode = config[ 'mode' ]

solved = False

if mode == 'single':
    correct_number = random.randint( range_min, range_max )
elif mode == 'multi':
    correct_number = int( getpass.getpass( "player 2, please enter the number to guess: "))
else:
    print( 'invalid config' )
    exit( )

for i in range( guesses_allowed ):
    guess = int( input( 'Enter your guess: ' ) )

    if guess == correct_number:
        print( f"Correct! You needed {i + 1 } tries" )
    elif guess < correct_number :
        print( "too low!" )
    else :
        print( 'too high' )

if not solved:
    print( 'You lost. The number was' , correct_number )