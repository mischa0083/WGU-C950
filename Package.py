# Name: Michael Lee
# Student ID: 010219381
# Date: 2022-12-11
# This file contains the Package class, which represents a package

# Package class
class Package():

    # Constructor
    def __init__(self, id, address, city, state, zip, deadline, weight, note, delivery_status="at the hub", delivery_time="N/A", delivery_truck="N/A", delivery_distance=0):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.note = note
        self.delivery_status = delivery_status
        self.delivery_time = delivery_time
        self.delivery_truck = delivery_truck
        self.delivery_distance = delivery_distance

    # Returns a string representation of the package
    def __str__(self):
        return f"Package ID: {self.id} Address: {self.address} {self.city}, {self.state} {self.zip} Deadline: {self.deadline} Weight: {self.weight} Note: {self.note} Delivery Status: {self.delivery_status} Delivery Time: {self.delivery_time} Delivery Truck: {self.delivery_truck}"
