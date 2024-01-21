
'''

This software contains the definition of the class LabHashing, which implements several hashing algorithms such as division hashing, 
linear probing, and quadratic probing. Chaining is sometimes used as a hashing technique. There is also an insert method, 
a custom_hash_function, and a string representation method in the LabHashing class. The file contains routines for reading data 
from files, writing results to files, and creating and using hash tables. The get_hash_table function receives data from an input 
file, generates a hash table using the supplied parameters, inserts the data into the hash table, and writes the results to an output 
file. The custom_hash_wrapper function wraps the LabHashing class's custom_hash_function method so that it may be used as a custom 
hash function for the hash table.
'''

import time

'''
A class Node is defined with an initializer method that takes in a key parameter and initializes two instance variables key 
and next to None.
'''
class Node:
    def __init__(self, key):
        self.key = key
        self.next = None
'''
Another class HashTable is defined, which takes four parameters with default values: bucket_size, divisor, probing_type, and 
custom_hash. An instance variable total_slots is initialized with the value 120, and another instance variable table is 
initialized as a list of None with length total_slots. The initializer method sets the instance variables with the passed parameters
or default values.
'''
class LabHashing:
    def __init__(self, bucket_size=3, divisor=120, probing_type="linear", custom_hash=None):
        self.bucket_size = bucket_size
        self.divisor = divisor
        self.probing_type = probing_type
        self.custom_hash = custom_hash
        self.total_slots = self.bucket_size * self.divisor
        self.table = [None] * self.total_slots

    '''
    A method division_hash is defined that takes a key parameter and returns the remainder of key divided by divisor.
    '''

    def division_hash(self, key):
        try:
            return key % self.divisor
        except TypeError:
            print(f"Error: key '{key}' is not a valid integer.")
            return None

    '''
    Another method linear_probing is defined that takes two parameters, key and step (default value is 1).
    The method first calculates the index using division_hash method and checks if the table at that index is not None.
    If the table is not None, it calculates the next index using index + step and modulo with total_slots.
    It continues to do so until it finds an empty slot, and returns the index of that empty slot.
    '''

    def linear_probing(self, key, step=1):
        try:
            index = self.division_hash(key)
        except TypeError:
            print(f"Error: {key} is not a valid key. Keys must be integers.")
            raise

        while self.table[index] is not None:
            index = (index + step) % self.total_slots
        return index

    '''
    A third method quadratic_probing is defined that takes three parameters, key, c1 (default value is 0.5), and c2 
    (default value is 0.5). The method first calculates the index using division_hash method and checks if the table at that 
    index is not None. If the table is not None, it calculates the next index using the formula (index + int(c1 * i + c2 * i * i)) 
    % self.total_slots, where i starts from 1. It continues to do so until it finds an empty slot, and returns the index of that 
    empty slot.
    '''

    def quadratic_probing(self, key, c1=0.5, c2=0.5):
        try:
            index = self.division_hash(key)
        except ValueError as e:
            raise e
        i = 1
        while self.table[index] is not None:
            index = (index + int(c1 * i + c2 * i * i)) % self.total_slots
            i += 1
            if i == self.total_slots:
                raise ValueError("Hash table is full.")
        return index

    '''
    A method chaining is defined that takes a key parameter.
    The method first calculates the index using division_hash method and checks if the table at that index is None.
    If the table is None, it sets the table at that index to a new instance of the Node class with the key parameter.
    If the table is not None, it traverses the linked list at that index until it finds the last node and appends a new node 
    with the key parameter to the end of the linked list.
    '''

    def chaining(self, key):
        try:
            index = self.division_hash(key)
        except ZeroDivisionError:
            raise ValueError("Divisor cannot be zero.")
        if self.table[index] is None:
            self.table[index] = Node(key)
        else:
            node = self.table[index]
            while node.next is not None:
                node = node.next
            node.next = Node(key)

    '''
    A static method custom_hash_function is defined that takes two parameters, self and key.
    The method demonstrates an example of mid-square hashing by first calculating the square of the key.
    It then converts the square to a string and gets the middle two digits of the string.
    It returns the integer value of the middle two digits.
    '''

    @staticmethod
    def custom_hash_function(self, key):
        square = key * key
        str_square = str(square)
        mid_index = len(str_square)//2-1
        if mid_index < 0:
            print("Warning: Key is too small for custom hash function.")
        mid_digits = str_square[mid_index:mid_index+2]
        return int(mid_digits)

    '''
    A method insert is defined that takes a key parameter.
    The method initializes a dictionary result with keys 'collisions', 'comparisons', and 'not_inserted', and values 0.
    If the custom_hash parameter is not None and is callable, it uses the custom hash function to calculate the index, otherwise, 
    it uses the probing method based on the probing_type parameter to calculate the index. If the probing_type parameter is "chaining", 
    it sets the index to the result of the chaining method, which already stores the key in the table.
    If the slot at the index is not empty, it increments the 'collisions' key of the result dictionary by 1.
    It sets the table at the index to the key parameter and returns the result dictionary.
    '''

    def insert(self, key):
        result = {'collisions': 0, 'comparisons': 0, 'not_inserted': 0}

        if not isinstance(key, int):
            raise TypeError("Key must be an integer.")

        if self.custom_hash and callable(self.custom_hash):
            index = self.custom_hash(key) % self.total_slots  # Call the custom_hash function here
        else:
            if self.probing_type == "linear":
                index = self.linear_probing(key)
            elif self.probing_type == "quadratic":
                index = self.quadratic_probing(key)
            elif self.probing_type == "chaining":
                self.chaining(key)  # Directly call the chaining function
                return result

        # If the slot is not empty, it means there was a collision
        if self.table[index] is not None:
            result['collisions'] += 1

        self.table[index] = key

        return result

    '''
    A special method __str__ is defined that returns a string representation of the HashTable object.
    It initializes an empty list output.
    It loops through each slot in the table.
    If the slot is not None, it checks if the slot contains a Node instance or an integer.
    If the slot contains a Node instance, it initializes an empty list node_values and a node variable pointing to the slot.
    It then traverses the linked list at that slot, appending the key of each node to the node_values list.
    It joins the node_values list with "->" and appends the resulting string to the output list.
    If the slot contains an integer, it appends the string representation of the integer to the output list.
    If the slot is None, it appends the string "None" to the output list.
    Finally, it returns the output list joined by ", ".
    '''

    def __str__(self):
        output = []
        for slot in self.table:
            try:
                if slot is not None:
                    if isinstance(slot, Node):  # Check if the slot contains a Node
                        node_values = []
                        node = slot
                        while node is not None:
                            node_values.append(str(node.key))
                            node = node.next
                        output.append("->".join(node_values))
                    else:  # If the slot contains an integer
                        output.append(str(slot))
                else:
                    output.append("None")
            except AttributeError:
                output.append("Error: Invalid input type")
        return ", ".join(output)

'''
A function read_data_from_file is defined that takes a file_path parameter.
The function initializes an empty list data.
It opens the file at the file_path in read mode.
It loops through each line in the file.
It strips the line and checks if the stripped line is not empty and is a digit.
If the stripped line is a digit, it appends the integer value of the stripped line to the data list.
Finally, it returns the data list containing the integers from the file.
'''

def read_data_from_file(file_path):
    data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                stripped_line = line.strip()
                if stripped_line and stripped_line.isdigit():
                    data.append(int(stripped_line))
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
    return data

'''
This function takes in the output file path, a hash table instance, the start time of the program, and the number of collisions, 
comparisons, and not_inserted items. It writes the results of the program to a file, including the runtime, the size of the hash 
table, the bucket size, the number of collisions, comparisons, and not_inserted items, the load factor, and the resulting hash table.
It determines the maximum length of the numbers in the hash table and formats the resulting hash table with the appropriate spacing
between elements.
'''
def write_result_to_file(output_file, hash_table, start_time, collisions, comparisons, not_inserted):
    end_time = time.perf_counter()
    runtime = (end_time - start_time) * 1000

    # Determine the maximum length of the numbers in the table
    max_length = max([len(str(slot.key)) if isinstance(slot, Node) else len(str(slot)) for slot in hash_table.table if slot is not None])

    try:
        with open(output_file, 'w') as file:
            file.write(f"Runtime: {runtime:.7f}ms\n")
            file.write("=========================\n")
            file.write(f"Hash table size: {hash_table.total_slots}\n")
            file.write(f"Bucket Size: {hash_table.bucket_size}\n")
            file.write(f"Number of collisions: {collisions}\n")
            file.write(f"Number of comparisons: {comparisons}\n")
            file.write(f"Number of items not inserted: {not_inserted}\n")
            file.write(f"Load factor: {len(hash_table.table) / hash_table.total_slots:.1f}\n\n")
            file.write("Resulting hash table:\n")

            for i in range(0, len(hash_table.table), 5):
                row_elements = []
                for j in range(i, min(i + 5, len(hash_table.table))):
                    slot = hash_table.table[j]
                    if slot is None:
                        row_elements.append("[" + " " * (max_length + 2) + "]")
                    elif isinstance(slot, Node):
                        node_values = []
                        node = slot
                        while node is not None:
                            node_values.append(str(node.key).rjust(max_length))
                            node = node.next
                        row_elements.append("[" + " -> ".join(node_values) + "]")
                    else:
                        row_elements.append("[" + str(slot).rjust(max_length) + "]")
                file.write(" ".join(row_elements) + "\n")

    except IOError:
        print("Error writing to output file.")


'''
This function takes in a file path, an output file path, and optional parameters for the bucket size, divisor, probing type, and 
custom hash function. It reads data from the file and creates a hash table instance with the given parameters. It then iterates 
through the data and inserts each item into the hash table. It also tracks the number of collisions, comparisons, and not_inserted 
items. Finally, it calls the write_result_to_file function to write the results of the program to a file.
'''
def get_hash_table(file_path, output_file, bucket_size=1, divisor=120, probing_type="linear", custom_hash=None):
    data = read_data_from_file(file_path)
    if not data:
        print("Error: input file is empty")
        return

    hash_table = LabHashing(bucket_size=1, divisor=divisor, probing_type=probing_type, custom_hash=custom_hash)
    
    # Add variables to track collisions, comparisons, and not_inserted
    collisions = 0
    comparisons = 0
    not_inserted = 0

    start_time = time.perf_counter()
    for key in data:
        try:
            key = int(key)
            if key < 0 or key > 99999:
                raise ValueError(f"{key} is not a valid key. Keys must be integers between 0 and 99999.")
        except ValueError as e:
            print(f"Error: {e}")
            not_inserted += 1
            continue
        result = hash_table.insert(key)
        collisions += result['collisions']
        comparisons += result['comparisons']
        not_inserted += result['not_inserted']

    write_result_to_file(output_file, hash_table, start_time, collisions, comparisons, not_inserted)

"""
This function takes an integer key and a divisor as input, and returns a custom hash value.
The custom hash value is calculated by converting the integer key to a string, then computing
the sum of the ASCII values of each character in the string. Finally, the sum is divided by the
divisor, and the remainder is returned as the custom hash value.

:param key: The integer key to be hashed
:param divisor: The divisor used to calculate the hash value
:return: The custom hash value for the given key
"""

def custom_hash_wrapper(key, divisor):
    try:
        key_str = str(key)  # Convert the integer key to a string
        key_hash = sum(ord(c) for c in key_str)  # Simple sum of ASCII values of characters in the key
        return key_hash % divisor
    except Exception as e:
        print(f"Error: {e}")
        return None

"""
    This function generates hash tables for the given input file using the specified hashing scheme(s).
    If probing_type is "all", it generates hash tables using linear, quadratic, and chaining probing schemes,
    and generates a separate output file for each scheme. Otherwise, it generates a single output file
    for the specified probing scheme.

    :param input_file: The name of the input file containing keys to be hashed
    :param output_file: The base name of the output file(s) to be generated
    :param divisor: The divisor used in the hash function
    :param probing_type: The type of probing scheme to use (linear, quadratic, chaining, or all)
    :return: None
    """

def run_hashing_schemes(input_file, output_file, divisor, probing_type):
    try:
        # If probing_type is "all", loop over all probing types and generate output files for each
        if probing_type == "all":
            probing_types = ["linear", "quadratic", "chaining"]
            for pt in probing_types:
                output_file_name = f"{output_file}_{pt}.txt"
                get_hash_table(input_file, output_file_name, divisor=divisor, probing_type=pt, custom_hash=lambda key: custom_hash_wrapper(key, divisor))
        # Otherwise, generate a single output file for the given probing type
        else:
            output_file_name = f"{output_file}_{probing_type}.txt"
            get_hash_table(input_file, output_file_name, divisor=divisor, probing_type=probing_type, custom_hash=lambda key: custom_hash_wrapper(key, divisor))
    except Exception as e:
        # If an exception is raised, print the error message and re-raise the exception
        print(f"Error: {e}")
        raise

"""
    This function prompts the user to enter the name of the input file and the base name of the output file,
    with default values provided if no input is provided. It then returns the input and output file names.

    :return: A tuple containing the input file name and the output file base name
"""
def get_input_files():
    try:
        # Prompt the user to enter the input file and output file names, with defaults provided
        input_file = input("Enter the name of the input file (default: LabHashingInput.txt): ").strip() or 'LabHashingInput.txt'
        output_file = input("Enter the base name of the output file (default: LabHashingOutput): ").strip() or 'LabHashingOutput'
        return input_file, output_file
    except Exception as e:
        # If an exception is raised, print the error message and re-raise the exception
        print(f"Error: {e}")
        raise

"""
    This function prompts the user to enter the divisor and probing type for the hash function,
    with default values provided if no input is provided. It then returns the divisor and probing type.

    If a non-integer value is entered for the divisor, a ValueError is raised.

    :return: A tuple containing the divisor and probing type
    """

def get_divisor_and_probing_type():
    try:
        # Prompt the user to enter the divisor and probing type, with defaults provided
        divisor = int(input("Enter the divisor (default: 113): ").strip() or 113)
        probing_type = input("Enter the probing type (linear, quadratic, chaining) or 'all' to run all schemes (default: all): ").strip().lower() or "all"
        return divisor, probing_type
    except ValueError as e:
        # If a ValueError is raised (e.g. if a non-integer value is entered for the divisor), print a custom error message and re-raise the exception
        print(f"Error: {e}. Please enter a valid integer for the divisor.")
        raise
    except Exception as e:
        # If an exception other than a ValueError is raised, print the error message and re-raise the exception
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    # Get the input and output file names from the user
    input_file, output_file = get_input_files()
    # Get the divisor and probing type from the user
    divisor, probing_type = get_divisor_and_probing_type()
    # Generate hash tables using the specified hashing scheme(s)
    run_hashing_schemes(input_file, output_file, divisor, probing_type)

