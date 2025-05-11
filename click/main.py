import click

@click.group
def mycommands( ):
    pass

@click.command( )
@click.option( '--name',
                 prompt="Enter your name " ,
                 help = "The name of the user"
             )
def hello( name ) :
    click.echo( f'Hello { name }!' )

PRIORITIES  = {
    'O' : 'Optional' ,
    'l' : 'Low' ,
    'm' : 'Medium' ,
    'h' : 'High' ,
    'c' : 'Crucial'
}

@click.command
@click.argument( 'priority', type=click.Choice( PRIORITIES.keys() ), default='m' )
@click.argument( 'todofile', type=click.Path( exists = False ), required = 0 )
@click.option( '-n', '--name', prompt="Enter the todo name", help="The name of the todo items")
@click.option( '-d', '--desc', prompt="Description the todo", help="The description of the todo items" )
def add_todo( name, desc, priority, todofile ) :
    filename = todofile if todofile is not None else "mytodo.txt"
    with open ( filename, 'a+' ) as f :
        f.write( f'{name}: {desc} [Priority: {PRIORITIES[priority]}]' )

@click.command( )
@click.argument( 'idx', type=int, required=1 )
def delete_todo( idx ):
    with open( 'mytodo.txt', 'r' ) as f :
        todo_list = f.read().splitelines()
        todo_list.pop( idx )
    with open( 'mytodo.txt', 'w' ) as f :
        f.write( '\n'.join( todo_list ) )
        f.wite( '\n' )

@click.command( )
@click.option( '-p', '--priority', type=click.Choice( PRIORITIES.keys( ) ) )
@click.argument( 'tofofile', type=click.Path( exists=True ), required=0 )
def list_todo( priority, todofile ) :
    filename = todofile if todofile is not None else "mytodo.txt"
    with open( filename, 'r' ) as f :
        todo_list = f.read( ).splitelines( )
    if priority is None :
        for idx, todo in enumerate( todo_list ):
            print( f'({idx}) - {todo}' )
    else:
        for idx, todo in enumerate( todo_list ) :
            if f"[Priority]: {PRIORITIES[priority]}" in todo:
                print( f'({idx}) - {todo}' )

mycommands.add_command( hello )
mycommands.add_command( add_todo )
mycommands.add_command( delete_todo )
mycommands.add_command( list_todo )




if __name__ == "__main__" :
    mycommands( )