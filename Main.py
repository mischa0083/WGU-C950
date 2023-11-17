# Name: Michael Lee
# Student ID: 010219381
# Date: 2022-12-11

# C.  Write an original program to deliver all the packages, meeting all requirements, using the attached supporting documents “Salt Lake City Downtown Map,” “WGUPS Distance Table,” and the “WGUPS Package File.”
#   1.  Create an identifying comment within the first line of a file named “main.py” that includes your first name, last name, and student ID.
#   2.  Include comments in your code to explain the process and the flow of the program.

import csv
import re
import Package
import HashTable
import Truck

# D.  Identify a self-adjusting data structure, such as a hash table, that can be used with the algorithm identified in part A to store the package data.
#   1.  Explain how your data structure accounts for the relationship between the data points you are storing.
#   ANSWER: The hash table accounts for the relationship between the data points by using the package ID as the key and the package object as the value.
#       The package ID is unique and can be used as the key to access the package object.

# Program's overall space-time complexity is O(n^2) because of the for loop nested in the while loop


def create_packages_hash_table():
    packages_hash_table = HashTable.HashTable()

    # Read packages.csv
    with open('packages.csv', mode='r', encoding='utf-8-sig') as csv_packages_file:
        csv_packages = csv.reader(csv_packages_file, delimiter=',')
        csv_packages = list(csv_packages)

        # Add packages to hash table
        for package in csv_packages:
            package_id = package[0]
            package_address = package[1]
            package_city = package[2]
            package_state = package[3]
            package_zip = package[4]
            package_deadline = package[5]
            package_weight = package[6]
            package_note = package[7]
            packages_hash_table.add(package_id, Package.Package(package_id, package_address, package_city,
                                    package_state, package_zip, package_deadline, package_weight, package_note))

    return packages_hash_table

# Create addresses list, space-time complexity O(n) because of for loop


def create_addresses_list():
    with open('addresses.csv', mode='r', encoding='utf-8-sig') as csv_addresses_file:
        csv_addresses = csv.reader(csv_addresses_file)
        return list(csv_addresses)

# Create distances list, space-time complexity O(n) because of for loop


def create_distances_list():
    with open('distances.csv', mode='r', encoding='utf-8-sig') as csv_distances_file:
        csv_distances = csv.reader(csv_distances_file)
        return list(csv_distances)


# Create packages hash table
packages_hash_table = create_packages_hash_table()

# Create addresses list
addresses_list = create_addresses_list()

# Create distances list
distances_list = create_distances_list()

# print_packages_hash_table(packages_hash_table)

# Create and load first truck
first_truck = Truck.Truck(
    1, 16, ["1", "2", "4", "5", "13", "14", "15", "16", "19", "20", "29", "30", "31", "34", "37", "40"], 0, 0, "4001 South 700 East", "Salt Lake City", "UT", "84107")

# Set package truck id to 1, space-time complexity O(n) because of for loop
for package in first_truck.packages:
    packages_hash_table.get(package).delivery_truck = 1

# Create and load second truck
second_truck = Truck.Truck(
    2, 16, ["3", "6", "7", "8", "10", "11", "12", "17", "18", "21", "22", "28", "32", "36", "38", "39"], 0, 0, "4001 South 700 East", "Salt Lake City", "UT", "84107")

# Set package truck id to 2, space-time complexity O(n) because of for loop
for package in second_truck.packages:
    packages_hash_table.get(package).delivery_truck = 2

# Create and load third truck
third_truck = Truck.Truck(
    3, 16, ["9", "23", "24", "25", "26", "27", "33", "35", "39"], 0, 0, "4001 South 700 East", "Salt Lake City", "UT", "84107")

# Set package truck id to 3, space-time complexity O(n) because of for loop
for package in third_truck.packages:
    packages_hash_table.get(package).delivery_truck = 3

# Get address id from address, space-time complexity O(n) because of for loop


def get_address_id(address):
    for item in addresses_list:
        if address in item[2]:
            return int(item[0])

# Get distance between two addresses, space-time complexity O(n) because of for loop


def get_distance(start_address, end_address):
    start_address_id = get_address_id(start_address)
    end_address_id = get_address_id(end_address)
    distance = distances_list[start_address_id][end_address_id]
    if distance == "":
        return float(distances_list[end_address_id][start_address_id])
    return float(distances_list[start_address_id][end_address_id])

# Method for delivering packages on trucks, space-time complexity O(n^2) because of nested for loops


def deliver_packages(truck):
    # Set current address to hub
    current_address = truck.current_address

    # If truck 1, set departure offset time as 8:00 AM
    if truck.id == 1:
        truck.float_time += 480
    # If truck 2, set departure offset time as 9:05 AM
    elif truck.id == 2:
        truck.float_time += 545

    # Print truck id
    print("Delivering packages on truck " + str(truck.id) +
          " at " + '{0:02.0f}:{1:02.0f}'.format(
        *divmod(truck.float_time, 60)) + "...")

    # Correct package 9 address to 410 S State St for truck 3
    if truck.id == 3:
        print("\tCorrecting package 9 address to 410 S State St...")
        packages_hash_table.get("9").address = "410 S State St"
        packages_hash_table.get("9").city = "Salt Lake City"
        packages_hash_table.get("9").state = "UT"
        packages_hash_table.get("9").zip = "84111"

    # Set package status to "en route", space-time complexity O(n) because of for loop
    for package in truck.packages:
        packages_hash_table.get(package).status = "en route"

    # Deliver packages, space-time complexity O(n^2) because of nested for loops
    while truck.packages:
        # Get shortest distance between current address and next package
        shortest = 1000
        next_package = ""
        for package in truck.packages:
            if shortest > get_distance(current_address, packages_hash_table.get(package).address):
                shortest = get_distance(
                    current_address, packages_hash_table.get(package).address)
                next_package = package

        # Add distance to package delivery distance
        packages_hash_table.get(next_package).delivery_distance += shortest
        # Add distance to truck distance
        truck.distance += shortest
        # Calculate time
        time = (shortest / 18) * 60
        # Add time to truck float time
        truck.float_time += time
        # Set package status to "Delivered"
        packages_hash_table.get(next_package).status = "delivered"
        # Set package delivery time
        # Convert float time to time
        package_delivery_time = '{0:02.0f}:{1:02.0f}'.format(
            *divmod(truck.float_time, 60))
        packages_hash_table.get(
            next_package).delivery_time = package_delivery_time
        # Deliver package
        print("\t" + package_delivery_time + " - Delivering package " + next_package + " at " +
              packages_hash_table.get(next_package).address + ".")
        # Remove package from truck
        truck.packages.remove(next_package)
        # Set current address to next package address
        current_address = packages_hash_table.get(next_package).address

    # Print total distance traveled
    print("\nTruck " + str(truck.id) + " delivered all packages at " +
          str(round(truck.distance, 2)) + " miles.")

    # Print total time elapsed
    time = '{0:02.0f}:{1:02.0f}'.format(*divmod(truck.float_time, 60))
    print("Truck " + str(truck.id) + " delivered all packages at " +
          time + ".\n")

    # Return total distance traveled
    return truck.distance


# Deliver packages on trucks
total_distance = 0
total_distance += deliver_packages(first_truck)
total_distance += deliver_packages(second_truck)
# Create variable for third truck departure time
if first_truck.float_time < second_truck.float_time:
    third_truck.float_time = first_truck.float_time
else:
    third_truck.float_time = second_truck.float_time
total_distance += deliver_packages(third_truck)

# Print total distance traveled across all trucks
print("Total distance traveled: " + str(total_distance) + " miles.")

# Print total time accumulated in travel time minus 8:00 AM offset time for truck
# 1 and 9:05 AM offset time for truck 2 and 10:20 AM offset time for truck 3
# (480, 545, 620)
time = '{0:02.0f}:{1:02.0f}'.format(
    *divmod(first_truck.float_time + second_truck.float_time + third_truck.float_time - 1645, 60))
print("Total time elapsed across all trucks: " + time + ".")

# Line divider for readability in console
print("\n" + "-" * 80 + "\n")

# Console interface to take user input for package lookup or time to show all package statuses at that time along with distance traveled across all trucks
while True:
    # Package lookup or time lookup
    lookup_input = input(
        "Enter 'P' to look up PACKAGE by package id or enter 'T' to show all package statuses at a specific TIME formatted HH:MM \n> ")

    # F.  Develop a look-up function that takes the following components as input and returns the corresponding data elements:
    # •   package ID number
    # •   delivery address
    # •   delivery deadline
    # •   delivery city
    # •   delivery zip code
    # •   package weight
    # •   delivery status (i.e., “at the hub,” “en route,” or “delivered”), including the delivery time

    # If package lookup
    if lookup_input == "P":
        # Package lookup by package id, space-time complexity O(n) because of hash table (because of for loop in hash table)
        package_id_input = input(
            "Enter a package ID to look up package \n> ")
        # If package id is valid
        if packages_hash_table.get(package_id_input) is not None:
            # Print package information
            print("\nPackage ID " + package_id_input + ":")
            print("\tAddress: " + packages_hash_table.get(
                package_id_input).address)
            print("\tDeadline: " + packages_hash_table.get(
                package_id_input).deadline)
            print("\tCity: " + packages_hash_table.get(
                package_id_input).city)
            print("\tState: " + packages_hash_table.get(
                package_id_input).state)
            print("\tZip: " + packages_hash_table.get(
                package_id_input).zip)
            print("\tWeight: " + packages_hash_table.get(
                package_id_input).weight)
            print("\tStatus: " + packages_hash_table.get(
                package_id_input).status)
            print("\tDelivery time: " + packages_hash_table.get(
                package_id_input).delivery_time)
        else:
            print("Invalid package ID")

    #     G.  Provide an interface for the user to view the status and info (as listed in part F) of any package at any time,
    #       and the total mileage traveled by all trucks. (The delivery status should report the package as at the hub, en route,
    #       or delivered. Delivery status must include the time.)
    #       1.  Provide screenshots to show the status of all packages at a time between 8:35 a.m. and 9:25 a.m.
    #       2.  Provide screenshots to show the status of all packages at a time between 9:35 a.m. and 10:25 a.m.
    #       3.  Provide screenshots to show the status of all packages at a time between 12:03 p.m. and 1:12 p.m.
    #       ANSWER: For Screenshots, see WGUPS Routing Program Overview.docx file in submission

    # If time lookup, space-time complexity O(n) because of for loop to iterate through all packages
    elif lookup_input == "T":
        # Get time input
        time_input = input(
            "Enter a time in HH:MM format to show all package statuses at that time along with distance traveled across all trucks \n> ")
        # Track total distance traveled
        total_distance = 0
        # If time input is valid perform time lookup
        if re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", time_input):
            # Convert user input to float time
            time_input = time_input.split(":")
            time_input = (int(time_input[0]) * 60) + int(time_input[1])

            # Print all package statuses on all trucks user input time
            print("\nPackage statuses at " + '{0:02.0f}:{1:02.0f}'.format(
                *divmod(time_input, 60)) + ":")
            for package in range(1, packages_hash_table.size + 1):
                # If package delivery time is less than or equal to user input time
                str_package = str(package)
                # If package is not None
                if packages_hash_table.get(str_package) is not None:
                    # If package delivery time is not N/A
                    if packages_hash_table.get(str_package).delivery_time != "N/A":
                        delivery_time = packages_hash_table.get(
                            str_package).delivery_time
                        delivery_time = delivery_time.split(":")
                        delivery_time = (
                            int(delivery_time[0]) * 60) + int(delivery_time[1])
                        if delivery_time <= time_input:
                            print("\tPackage " + str_package + " - " +
                                  packages_hash_table.get(str_package).status + " at " + packages_hash_table.get(str_package).delivery_time +
                                  " by truck " + str(packages_hash_table.get(str_package).delivery_truck) + " to " +
                                  addresses_list[int(get_address_id(packages_hash_table.get(str_package).address))][1] +
                                  ", " + packages_hash_table.get(str_package).address + ".")
                            # Add package delivery distance to total distance
                            total_distance += packages_hash_table.get(
                                str_package).delivery_distance
                        # If package delivery time is greater than user input time
                        else:
                            # If time_input is less than 8:00 AM all packages are at the hub
                            if time_input < 480:
                                print("\tPackage " + str_package + " - at the hub " + " on truck " +
                                      str(packages_hash_table.get(str_package).delivery_truck) + " at " +
                                      addresses_list[0][1] + ", " + addresses_list[0][2] + ".")
                            # If time_input is equal to or greater than 8:00 AM but less than 9:05 AM
                            elif time_input >= 480 and time_input < 545:
                                # Truck 1 packages are en route
                                if packages_hash_table.get(str_package).delivery_truck == 1:
                                    print("\tPackage " + str_package + " - en route on truck " +
                                          addresses_list[int(get_address_id(packages_hash_table.get(str_package).address))][1] +
                                          ", " + str(packages_hash_table.get(str_package).delivery_truck) + " to " +
                                          packages_hash_table.get(str_package).address + ".")
                                # All other packages are at the hub
                                else:
                                    print("\tPackage " + str_package + " - at the hub on truck " +
                                          str(packages_hash_table.get(str_package).delivery_truck) + " at " +
                                          addresses_list[0][1] + ", " + addresses_list[0][2] + ".")
                            # If time_input is equal to or greater than 9:05 AM but less than 10:20 AM
                            elif time_input >= 545 and time_input < 620:
                                # Truck 2 packages are en route
                                if packages_hash_table.get(str_package).delivery_truck == 2:
                                    print("\tPackage " + str_package + " - en route on truck " +
                                          addresses_list[int(get_address_id(packages_hash_table.get(str_package).address))][1] +
                                          ", " + str(packages_hash_table.get(str_package).delivery_truck) + " to " +
                                          packages_hash_table.get(str_package).address + ".")
                                # All other packages are at the hub
                                else:
                                    print("\tPackage " + str_package + " - at the hub on truck " +
                                          str(packages_hash_table.get(str_package).delivery_truck) + " at " +
                                          addresses_list[0][1] + ", " + addresses_list[0][2] + ".")
                            # If time_input is equal to or greater than whenever truck 3 departs
                            elif time_input >= third_truck.float_time:
                                # Truck 3 packages are en route
                                if packages_hash_table.get(str_package).delivery_truck == 3:
                                    print("\tPackage " + str_package + " - en route on truck " +
                                          addresses_list[int(get_address_id(packages_hash_table.get(str_package).address))][1] +
                                          ", " + str(packages_hash_table.get(str_package).delivery_truck) + " to " +
                                          packages_hash_table.get(str_package).address + ".")
                                # All other packages are at the hub
                                else:
                                    print("\tPackage " + str_package + " - at the hub on truck " +
                                          str(packages_hash_table.get(str_package).delivery_truck) + " at " +
                                          addresses_list[0][1] + ", " + addresses_list[0][2] + ".")
            # Print total distance traveled
            print("\nTotal distance traveled across all trucks at " +
                  '{0:02.0f}:{1:02.0f}'.format(
                      *divmod(time_input, 60)) + " is " + str(round(total_distance, 2)) + " miles.")
        # If time input is invalid
        else:
            print("Invalid time. Please try again.")

    # Line divider for readability in console
    print("\n" + "-" * 80 + "\n")
