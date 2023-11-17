# Name: Michael Lee
# Student ID: 010219381
# Date: 2022-12-11
# This file contains the HashTable class, which represents a hash table

# E.  Develop a hash table, without using any additional libraries or classes, that has an insertion
#   function that takes the following components as input and inserts the components into the hash table:
# •   package ID number
# •   delivery address
# •   delivery deadline
# •   delivery city
# •   delivery zip code
# •   package weight
# •   delivery status (e.g., delivered, en route)

# Code is from WGU course tips referenced video (James, 2016),
# modified the hashing algorithm slightly to prevent hash collisions for package ID keys

# HashTable class
class HashTable():

    # Constructor, size of 40 to accommodate 40 packages
    def __init__(self):
        self.size = 40
        self.map = [None] * self.size

    # Returns a hash value for a given key
    def _get_hash(self, key):
        return int(key) % self.size - 1

    # Adds a key-value pair to the hash table, space-time complexity O(n) because of the for loop
    def add(self, key, value):
        key_hash = self._get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[key_hash].append(key_value)
            return True

    # Gets a key-value pair from the hash table, space-time complexity O(n) because of the for loop
    def get(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    # Deletes a key-value pair from the hash table, space-time complexity O(n) because of the for loop
    def delete(self, key):
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True

    # Prints HashTable, space-time complexity O(n) because of the for loop
    def print(self):
        print('--- Packages ---')
        for item in self.map:
            if item is not None:
                print(f"Key: {item[0][0]}, Value: {str(item[0][1])}")
