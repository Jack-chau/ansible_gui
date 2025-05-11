import yaml 
import json
from typing import Any, List, Dict

data1 : dict[ str, any ] = {
    'Name' : 'Jack Chau' ,
    'Position' : 'Rubbish' ,
    'Location' : 'VTC' ,
    'Age' : '27' ,
    'Experience' : 'Nothing useful' ,
    'Language' : { 'Programming' : [ 'Youtube', 'ChatGPT', 'Deepseek' ] }
}

yaml_output = yaml.dump( data1, sort_keys=False )

with open( './output/data1.yaml', 'w' ) as file :
    file.write( yaml_output )

#print( yaml_output )

data2 : dict[ dict[ str, any ] ] = [

    {
        'Name' : 'Jack Chau' ,
        'Position' : 'Rubbish' ,
        'Location' : 'VTC' ,
        'Age' : '27' ,
        'Experience' : 'Nothing useful' ,
        'Language' : { 'Programming' : [ 'Youtube', 'ChatGPT', 'Deepseek' ] }
    },
    {
        'Name' : 'Jack Chau' ,
        'Position' : 'Rubbish' ,
        'Location' : 'VTC' ,
        'Age' : '27' ,
        'Experience' : 'Nothing useful' ,
        'Language' : { 'Programming' : [ 'Youtube', 'ChatGPT', 'Deepseek' ] }
    }
]

yaml_output2 = yaml.dump_all( data2, sort_keys=False )

with open( './output/data2.yml', 'w' ) as f :
    f.write( yaml_output2 )
# print( yaml_output2 )









