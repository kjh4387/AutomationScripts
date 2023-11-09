import pickle

class Core:
    class data:
        program_data = {
            "address":None,
            "mailservice_host":None,
            "mailservice_port":None
        }   
        contents_data = {
            "template":None,
            "variables":None
        }
        emailer_data = {
            "file_list" : None,
            "receiver_list" : None
        }

    def __init__(self, pickle_path = None):
        if pickle_path is not None:
            self.deserialize_data(pickle_path)
        

    def serialize_data(self, path, data):
        with open(pickle_path, 'wb') as file:
            pickle.dump(data, file)
    def deserialize_data(self):


def add_to_dict(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = value
        return True
    else:
        print(f"Key '{key}' already exists.")
        return False
    
def remove_from_dict(dictionary, key):
    if key in dictionary:
        del dictionary[key]
        return True
    else:
        print(f"Key '{key}' does not exist.")
        return False
    
def update_dict(dictionary, key, value):
    if key in dictionary:
        dictionary[key] = value
        return True
    else:
        print(f"Key '{key}' does not exist. Use add_to_dict to add new key.")
        return False