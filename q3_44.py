# ~~~ This is a template for question 3  ~~~

#Imports:
import pandas as pd

#Path for data:
path='data.xlsx'

#Implement HashTable class:
class HashTable:
    def __init__(self, size=int , hash_function_method=str, collision_handling=str,m=int,A=float,m_2=None,A_2=None): #Initiate all the parameter for the hash table.
        if not isinstance(size, (int)):  # check if  size is an int
            raise ValueError('size should be an int')
        if not isinstance((hash_function_method), (str)):  # check if  hash_function_method is an str
            raise ValueError('hash_function_method should be an str')
        if not isinstance((collision_handling), (str)):  # check if  collision_handling is an str
            raise ValueError('collision_handling should be an str')

        if not isinstance(m, (int)):  # check if  m is an int
            raise ValueError('m should be an int')
        if not isinstance(A, (float,int)):  # check if  A is an float
            raise ValueError('A should be an float')

        if m_2 is not None:
            if not isinstance(m_2, (int)):  # check if  m_2 is an int
                raise ValueError('m_2 should be an int')

        if A_2 is not None:
            if not isinstance(A_2, (float, int)):  # check if  A_2 is an float
                raise ValueError('A_2 should be an float')

        self.hash_function_method=hash_function_method
        self.collision_handling=collision_handling
        self.size = size
        self.keys =[[] for _ in range(size)] #Data structure for keys.
        self.data = [[] for _ in range(size)]#Data structure for values.
        self.m=m
        self.A=A
        self.m_2=m_2
        self.A_2=A_2
        self.num_keys=0
        #Check that all the parameters are given for a specific configuration of the hash table:
        if self.hash_function_method=="multiplication" and self.A ==float:
            raise ValueError('Need to define A')
        if self.collision_handling=="OA_Double_Hashing" and self.m_2 ==int:
            raise ValueError('Need to define m_2')
        if self.collision_handling=="OA_Double_Hashing" and self.hash_function_method=="multiplication" and self.A_2 ==float:
            raise ValueError('Need to define A_2')

###Part A###

    def hash_function(self,key):                #Logic of hash function.
        """
        Primary hash function:
        - if "mod"            : h(k) = k mod m
        - if "multiplication": h(k) = floor(m * ( (k*A) - floor(k*A) ))
        """
        if self.hash_function_method == "mod":
            return key % self.m
        elif self.hash_function_method == "multiplication":
            # fractional part of k*A
            frac = (key * self.A) - int(key * self.A)
            return int(self.m * frac)
        else:
            raise ValueError(f"Unknown hash_function_method: {self.hash_function_method}")


    def hash_function_2(self,key):              #Logic of hash function, when using OA_Double_Hashing.
        """
        Secondary hash function (only used in double hashing):
        - if "mod"            : h2(k) = m_2 – (k mod m_2)
        - if "multiplication": h2(k) = floor(m_2 * ((k*A_2) - floor(k*A_2)))
        """
        if self.hash_function_method == "mod":
            # Standard “division” second hash
            return (self.m_2 - (key % self.m_2))
        elif self.hash_function_method == "multiplication":
            frac = (key * self.A_2) - int(key * self.A_2)
            return int(self.m_2 * frac)
        else:
            raise ValueError(f"Unknown hash_function_method: {self.hash_function_method}")


    def insert(self,key=int,value=str):
        if not isinstance(key, (int)):  # check if  key is an int
            raise ValueError('key should be an int')
        if not isinstance(value, (str)):  # check if  str is an int
            raise ValueError('value should be an str')

        counter=0                           #We will use the counter later to create our metric of efficiency.
        place= self.hash_function(key)
        if self.keys[place]==[] or self.keys[place]==[-1] :            #If we did not have any collision.
            self.keys[place]=[key]
            self.data[place]=[value]
            counter+=1
            self.num_keys += 1
            return counter
        elif self.keys[place]==[key]:       #Replacing the value.
            self.data[place]=[value]
            counter+=1
            return counter
        #hendeling collisions:
        elif self.collision_handling=="Chain":
            counter+=1
            for i in range(1,len(self.keys[place])):
                counter+=1
                if self.keys[place][i]==key:        #Replacing the value.
                    self.data[place][i]=value
                    self.num_keys += 1
                    return counter                  #Returns the amount of operations.
            self.keys[place].append(key)            #Using 'Chain'.
            self.data[place].append(value)
            self.num_keys += 1
            return counter                          #Returns the amount of operations.

        elif self.collision_handling=="OA_Quadratic_Probing":
            if self.num_keys==self.size:
                return "Hash Table is full"             #In open addressing, we can not have more keys then the size of the data structure.
            counter+=1
            for i in range(1,self.size):
                counter+=1

###Part B###
                new_place = (place + i * i) % self.m

                if self.keys[new_place]==[key]:         #Replacing the value.
                    self.data[new_place]=[value]
                    return counter                      #Returns the amount of operations.
                elif self.keys[new_place]==[] or self.keys[new_place]==[-1]:
                    self.keys[new_place]=[key]          #Using 'OA_Quadratic_Probing'.
                    self.data[new_place]=[value]
                    self.num_keys+=1
                    return counter                      #Returns the amount of operations.

        elif self.collision_handling=="OA_Double_Hashing":
            if self.num_keys==self.size:
                return "Hash Table is full"             #In open addressing, we can not have more keys then the size of the data structure.
            counter+=1
            for i in range(1,self.size):
                counter+=1
                new_place=(self.hash_function(key)+i*self.hash_function_2(key))%self.m
                if self.keys[new_place] == [key]:       #Replacing the value.
                    self.data[new_place] = [value]
                    return counter                      #Returns the amount of operations.
                elif self.keys[new_place]==[] or self.keys[new_place]==[-1]:
                    self.keys[new_place]=[key]
                    self.data[new_place]=[value]        #Using 'OA_Double_Hashing'.
                    self.num_keys+=1
                    return counter                      #Returns the amount of operations.

    def delete(self,key=int):
        if not isinstance(key, (int)):  # check if  key is an int
            raise ValueError('key should be an int')

        counter = 0                                     #We will use the counter later to create our metric of efficiency.
        place = self.hash_function(key)
        if self.keys[place] == [key]:
            self.keys[place]==[-1]
            del self.data[place]
            counter += 1                                #If we did not have any collision.
            self.num_keys -= 1                          #Update the number of keys in the hash table.
            return counter                              #Returns the amount of operations.

        elif self.collision_handling == "Chain":
            if self.keys[place] == []:
                counter += 1
                return "Data is not in Hash Table",counter  #Data is not in Hash Table, Returns the amount of operations.
            counter+=1
            for i in range(1,len(self.keys[place])):
                counter += 1
                if self.keys[place][i] == key:
                    del self.keys[i]                   #Go over all keys in a specific place in the hash table.
                    del self.data[place][i]
                    self.num_keys -= 1                 #Update the number of keys in the hash table.
                    return counter                     #Found and deleted, Returns the amount of operations.
            return "Data is not in Hash Table",counter #Data is not in Hash Table, Returns the amount of operations.

        elif self.collision_handling == "OA_Quadratic_Probing":
            counter+=1
            for i in range(1, self.size):
                counter += 1
                new_place = self.hash_function(place + i * i)
                if self.keys[new_place] == []:              #If we have an empty slot, this means that we do not have the key in the table.
                    break
                if self.keys[new_place] == [key]:
                    self.keys[new_place]=-1
                    del self.data[new_place]                #Go over all places the key can be - using OA Quadratic Probing.
                    self.num_keys -= 1                      #Update the number of keys in the hash table.
                    return counter                          #Found and deleted, Returns the amount of operations.
            return "Data is not in Hash Table",counter      #Data is not in Hash Table, Returns the amount of operations.

        elif self.collision_handling == "OA_Double_Hashing":
            counter+=1
            for i in range(1, self.size):
                counter += 1

###Part C###
                new_place = (self.hash_function(key) + i * self.hash_function_2(key)) % self.m

                if self.keys[new_place] == []:              #If we have an empty slot, this means that we do not have the key in the table.
                    break
                if self.keys[new_place] == [key]:
                    self.keys[new_place]=-1                #Go over all places the key can be - using OA Double Hashing.
                    del self.data[new_place]
                    self.num_keys -= 1                      #Update the number of keys in the hash table.
                    return counter                          #Found and deleted, Returns the amount of operations.
            return "Data is not in Hash Table"  ,counter    #Data is not in Hash Table, Returns the amount of operations.

    def member(self, key=int):
        if not isinstance(key, (int)):  # check if  key is an int
            raise ValueError('key should be an int')

        counter = 0                                         #We will use the counter later to create our metric of efficiency.
        place = self.hash_function(key)
        if self.keys[place] == [key]:                       #If we did not have any collision.
            counter += 1
            return True, counter                            #Returns True and the amount of operations.

        elif self.collision_handling == "Chain":
            if self.keys[place] == [] or self.keys[place] == [-1] :
                counter += 1
                return False, counter                       #Go over all keys in a specific place in the hash table,
                                                            #if the key is in it return True and the amount of operations,
            counter+=1                                      #elsr False and the amount of operations
            for i in range(1,len(self.keys[place])):
                counter += 1
                if self.keys[place][i] == key:
                    return True,counter
            return False,counter

        elif self.collision_handling == "OA_Quadratic_Probing":
            counter+=1
            for i in range(1, self.size):

                counter += 1                                    #Go over all places the key can be - using OA Quadratic Probing,
                new_place = self.hash_function(place + i * i)   #if the key is in it return True and the amount of operations,
                if self.keys[new_place] == []:                  #If we have an empty slot, this means that we do not have the key in the table.
                    break
                if self.keys[new_place] == [key]:               #else False and the amount of operations.
                    return True,counter
            return False,counter

        elif self.collision_handling == "OA_Double_Hashing":
            counter+=1
            for i in range(1, self.size):                                                          #Go over all places the key can be - using OA Double Hashing,
                counter += 1                                                                       #if the key is in it return True and the amount of operations,
                new_place = (self.hash_function(key) + i * self.hash_function_2(key)) % self.m     #else False and the amount of operations.
                if self.keys[new_place] == []:                                                     #If we have an empty slot, this means that we do not have the key in the table.
                    break
                if self.keys[new_place] == [key]:
                    return True,counter
            return False,counter

def compute_efficiency(results_d):
    """
    Given `results_d` from Part D (returned by data_hashing),
    compute efficiency = total_probes / n_records for each config.
    """
    efficiencies = {}
    for sheet_name, (n_records, sheet_probes) in results_d.items():
        eff_dict = {}
        for label, total_probes in sheet_probes.items():
            eff_dict[label] = total_probes / n_records if n_records > 0 else float("inf")
        efficiencies[sheet_name] = eff_dict
    return efficiencies

def data_hashing(path):
    ### Part D: build & insert into each hash‐table configuration

    # 1. Read all sheets at once (keys in first column, cast to int):
    all_sheets = pd.read_excel(path, sheet_name=None)

    # 2. Define the six (m, hash, collision) configurations exactly as in EX2:
    configs = {
        "mod_chain": {
            "size": 149, "hash_meth": "mod", "collision": "Chain",
            "m": 149, "A": 0.0, "m_2": None, "A_2": None
        },
        "mod_quad": {
            "size": 149, "hash_meth": "mod", "collision": "OA_Quadratic_Probing",
            "m": 149, "A": 0.0, "m_2": None, "A_2": None
        },
        "mod_double": {
            "size": 149, "hash_meth": "mod", "collision": "OA_Double_Hashing",
            "m": 149, "A": 0.0, "m_2": 97, "A_2": None
        },
        "mul_chain": {
            "size": 149, "hash_meth": "multiplication", "collision": "Chain",
            "m": 149, "A": 0.589, "m_2": None, "A_2": None
        },
        "mul_quad": {
            "size": 149, "hash_meth": "multiplication", "collision": "OA_Quadratic_Probing",
            "m": 149, "A": 0.589, "m_2": None, "A_2": None
        },
        "mul_double": {
            "size": 149, "hash_meth": "multiplication", "collision": "OA_Double_Hashing",
            "m": 149, "A": 0.589, "m_2": 97, "A_2": 0.405
        },
    }

    # 3. For each sheet, extract all integer keys and insert into each config:
    results = {}
    for sheet_name, df in all_sheets.items():
        keys = df.iloc[:, 0].dropna().astype(int).tolist()
        n_records = len(keys)

        # Keep (n_records, total_probes_for_each_config) together:
        sheet_probes = {}
        for label, params in configs.items():
            H = HashTable(
                size=params["size"],
                hash_function_method=params["hash_meth"],
                collision_handling=params["collision"],
                m=params["m"],
                A=params["A"],
                m_2=params["m_2"],
                A_2=params["A_2"]
            )
            total_probes = 0
            for k in keys:
                total_probes += H.insert(k, str(k))
            sheet_probes[label] = total_probes

        results[sheet_name] = (n_records, sheet_probes)

    ###Part E###
    #efficiency value

    return compute_efficiency(results)


print(data_hashing(path))




#part f- sanity check
def compute_efficiency(results_d):
    """
    Given `results_d` from Part D (returned by data_hashing),
    compute efficiency = total_probes / n_records for each config.
    """
    efficiencies = {}
    for sheet_name, (n_records, sheet_probes) in results_d.items():
        eff_dict = {}
        for label, total_probes in sheet_probes.items():
            eff_dict[label] = total_probes / n_records if n_records > 0 else float("inf")
        efficiencies[sheet_name] = eff_dict
    return efficiencies

def data_hashing(path):
    ### Part D: build & insert into each hash‐table configuration

    # 1. Read all sheets at once (keys in first column, cast to int):
    all_sheets = pd.read_excel(path, sheet_name=None)

    # 2. Define the six (m, hash, collision) configurations exactly as in EX2:
    configs = {
        "mod_chain": {
            "size": 149, "hash_meth": "mod", "collision": "Chain",
            "m": 149, "A": 0.0, "m_2": None, "A_2": None
        },
        "mod_quad": {
            "size": 149, "hash_meth": "mod", "collision": "OA_Quadratic_Probing",
            "m": 149, "A": 0.0, "m_2": None, "A_2": None
        },
        "mod_double": {
            "size": 149, "hash_meth": "mod", "collision": "OA_Double_Hashing",
            "m": 149, "A": 0.0, "m_2": 97, "A_2": None
        },
        "mul_chain": {
            "size": 149, "hash_meth": "multiplication", "collision": "Chain",
            "m": 149, "A": 0.618, "m_2": None, "A_2": None
        },
        "mul_quad": {
            "size": 149, "hash_meth": "multiplication", "collision": "OA_Quadratic_Probing",
            "m": 149, "A": 0.618, "m_2": None, "A_2": None
        },
        "mul_double": {
            "size": 149, "hash_meth": "multiplication", "collision": "OA_Double_Hashing",
            "m": 149, "A": 0.618, "m_2": 97, "A_2": 0.405
        },
    }

    # 3. For each sheet, extract all integer keys and insert into each config:
    results = {}
    for sheet_name, df in all_sheets.items():
        keys = df.iloc[:, 0].dropna().astype(int).tolist()
        n_records = len(keys)

        # Keep (n_records, total_probes_for_each_config) together:
        sheet_probes = {}
        for label, params in configs.items():
            H = HashTable(
                size=params["size"],
                hash_function_method=params["hash_meth"],
                collision_handling=params["collision"],
                m=params["m"],
                A=params["A"],
                m_2=params["m_2"],
                A_2=params["A_2"]
            )
            total_probes = 0
            for k in keys:
                total_probes += H.insert(k, str(k))
            sheet_probes[label] = total_probes

        results[sheet_name] = (n_records, sheet_probes)

    ###Part E###
    #efficiency value

    return compute_efficiency(results)
print(data_hashing(path))
#as we can see we got 1.0 in sheet 3 as the best effciency while for sheet 1 our effeciency got lower, in contarst to what we predicted, probaly dew to low amounts of data.
#thus we will try increasing m
def compute_efficiency(results_d):
    """
    Given `results_d` from Part D (returned by data_hashing),
    compute efficiency = total_probes / n_records for each config.
    """
    efficiencies = {}
    for sheet_name, (n_records, sheet_probes) in results_d.items():
        eff_dict = {}
        for label, total_probes in sheet_probes.items():
            eff_dict[label] = total_probes / n_records if n_records > 0 else float("inf")
        efficiencies[sheet_name] = eff_dict
    return efficiencies

def data_hashing(path):
    ### Part D: build & insert into each hash‐table configuration

    # 1. Read all sheets at once (keys in first column, cast to int):
    all_sheets = pd.read_excel(path, sheet_name=None)

    # 2. Define the six (m, hash, collision) configurations exactly as in EX2:
    configs = {
        "mod_chain": {
            "size": 248, "hash_meth": "mod", "collision": "Chain",
            "m": 248, "A": 0.0, "m_2": None, "A_2": None
        },
        "mod_quad": {
            "size": 248, "hash_meth": "mod", "collision": "OA_Quadratic_Probing",
            "m": 248, "A": 0.0, "m_2": None, "A_2": None
        },
        "mod_double": {
            "size": 248, "hash_meth": "mod", "collision": "OA_Double_Hashing",
            "m": 248, "A": 0.0, "m_2": 97, "A_2": None
        },
        "mul_chain": {
            "size": 248, "hash_meth": "multiplication", "collision": "Chain",
            "m": 248, "A": 0.618, "m_2": None, "A_2": None
        },
        "mul_quad": {
            "size": 248, "hash_meth": "multiplication", "collision": "OA_Quadratic_Probing",
            "m": 248, "A": 0.618, "m_2": None, "A_2": None
        },
        "mul_double": {
            "size": 248, "hash_meth": "multiplication", "collision": "OA_Double_Hashing",
            "m": 248, "A": 0.618, "m_2": 97, "A_2": 0.405
        },
    }

    # 3. For each sheet, extract all integer keys and insert into each config:
    results = {}
    for sheet_name, df in all_sheets.items():
        keys = df.iloc[:, 0].dropna().astype(int).tolist()
        n_records = len(keys)

        # Keep (n_records, total_probes_for_each_config) together:
        sheet_probes = {}
        for label, params in configs.items():
            H = HashTable(
                size=params["size"],
                hash_function_method=params["hash_meth"],
                collision_handling=params["collision"],
                m=params["m"],
                A=params["A"],
                m_2=params["m_2"],
                A_2=params["A_2"]
            )
            total_probes = 0
            for k in keys:
                total_probes += H.insert(k, str(k))
            sheet_probes[label] = total_probes

        results[sheet_name] = (n_records, sheet_probes)

    ###Part E###
    #efficiency value

    return compute_efficiency(results)
print(data_hashing(path))
#because sheet 1 contains ids which are close numbers then making m, the amount of places in the output vector, bigger makes the hashing more effecient