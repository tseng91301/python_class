t_data={
        "basic":{
            "name":"",
            "email":"",
            "phone":"",
            "address":""
        },
        "education":{
            "num":0,
            "info":[]
        },
        "professional":{
            "num":0,
            "info":[]
        },
        "leadership":{
            "num":0,
            "info":[]
        },
        "skill":{
            "num":0,
            "info":[]
        },
        "additional":{
            "num":0,
            "info":[]
        },
        "certification":{
            "num":0,
            "info":[]
        }
        
    }

def data_i():
    return t_data

def dict_contains(parent_dict:dict, child_dict:dict):
    for key, value in parent_dict.items():
        if isinstance(value,dict):
            if(dict_contains(value,child_dict[key])):
                continue
            else:
                return False
        if key not in child_dict:
            return False
    return True

def check_available(inp:dict,valid=t_data):
    return dict_contains(valid,inp)