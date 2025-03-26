"""
Requirements

Some possible questions to ask:

Will there be multiple levels in the parking lot?
What kinds of vehicles will be parked? Will their sizes differ?
Will there be special spots for certain vehicles?
Will the parking lot have a payment system? If so, how will it work?
Will parking spots be reserved or can the driver choose any spot?
How much functionality will the driver have beyond parking and paying?
Basics

Multiple levels in the parking lot
Possible vehicle types: car, limo, semi-truck
We will have a payment system, with a single entrance and exit
Drivers will be assigned a parking spot after paying
Vehicles and Parking Spots

Vehicles can be of different sizes (car = 1, limo = 2, truck = 3)
Each parking spot will have a size of 1
A vehicle must fully take up each spot assigned to it (no fractional spots)
Vehicles will automatically be assigned the next available parking spot on the lowest floor
Payment System

Drivers will pay for parking and be assigned the next available spot on the lowest floor
Drivers can pay for a variable number of hours and they are charged after they remove their vehicle based on an hourly rate
We can assume vehicles can be parked for a variable number of hours
If there is no capacity, the system should not assign a spot and should notify the driver
Design

High-level

We will have a base Vehicle class, and Car, Limo, and Truck classes that inherit from it
Each of these will have a predefined size
A Driver class will have a vehicle that belongs to it, and a total payment due
We will have a ParkingGarage which will be made up of multiple ParkingFloors
A ParkingFloor will be made up of multiple Parking Spots, which can simply be represented by an array (0 = empty, 1 = occupied)
The ParkingSystem will be the main controller of the ParkingGarage and will be responsible for tracking parking hours and charging drivers
"""


# A Vehicle class will be the base class for all vehicles. It will have a size attribute that will be used to determine how many spots it will take up.
class Vehicle:
    def __init__(self, spot_size):
        self._spot_size = spot_size

    def get_spot_size(self):
        return self._spot_size


# A Driver class will have a vehicle that belongs to it, and a total payment due. It will also have a method to charge the driver for parking.
class Driver:
    def __init__(self, id, vehicle):
        self._id = id
        self._vehicle = vehicle
        self._payment_due = 0

    def get_vehicle(self):
        return self._vehicle

    def get_id(self):
        return self._id

    def charge(self, amount):
        self._payment_due += amount


# Cars, Limos, and SemiTrucks will inherit from the Vehicle class. Each will have a predefined size.
class Car(Vehicle):
    def __init__(self):
        super().__init__(1)


class Limo(Vehicle):
    def __init__(self):
        super().__init__(2)


class SemiTruck(Vehicle):
    def __init__(self):
        super().__init__(3)


# A ParkingFloor will be the container for parking spots, which will be represented by an array. It will also keep track of which vehicles are parked in which spots, where [l, r] represents the range of spots occupied by a vehicle.
class ParkingFloor:
    def __init__(self, spot_count):
        self._spots = [0] * spot_count
        self._vehicle_map = {}

    def park_vehicle(self, vehicle):
        size = vehicle.get_spot_size()
        l, r = 0, 0
        while r < len(self._spots):
            if self._spots[r] != 0:
                l = r + 1
            if r - l + 1 == size:
                # we found enough spots, park the vehicle
                for k in range(l, r + 1):
                    self._spots[k] = 1
                self._vehicle_map[vehicle] = [l, r]
                return True
            r += 1
        return False

    def remove_vehicle(self, vehicle):
        start, end = self._vehicle_map[vehicle]
        for i in range(start, end + 1):
            self._spots[i] = 0
        del self._vehicle_map[vehicle]

    def get_parking_spots(self):
        return self._spots

    def get_vehicle_spots(self, vehicle):
        return self._vehicle_map.get(vehicle)


# A ParkingGarage will contain an arbitrary number of ParkingFloors.
# Notice how spots_per_floor is passed into the ParkingFloor constructor. This is because we want to be able to have different sized parking floors. But what if each floor had a varying number of parking spots? We could pass in an array of spots_per_floor instead.


class ParkingGarage:
    def __init__(self, floor_count, spots_per_floor):
        self._parking_floors = [
            ParkingFloor(spots_per_floor) for _ in range(floor_count)
        ]

    def park_vehicle(self, vehicle):
        for floor in self._parking_floors:
            if floor.park_vehicle(vehicle):
                return True
        return False

    def remove_vehicle(self, vehicle):
        for floor in self._parking_floors:
            if floor.get_vehicle_spots(vehicle):
                floor.remove_vehicle(vehicle)
                return True
        return False


# The ParkingSystem will be the main controller of the ParkingGarage. It will be responsible for tracking parking hours and charging drivers.
import datetime
import math


class ParkingSystem:
    def __init__(self, parkingGarage, hourlyRate):
        self._parkingGarage = parkingGarage
        self._hourlyRate = hourlyRate
        self._timeParked = {}  # map driverId to time that they parked

    def park_vehicle(self, driver):
        currentHour = datetime.datetime.now().hour
        isParked = self._parkingGarage.park_vehicle(driver.get_vehicle())
        if isParked:
            self._timeParked[driver.get_id()] = currentHour
        return isParked

    def remove_vehicle(self, driver):
        if driver.get_id() not in self._timeParked:
            return False
        currentHour = datetime.datetime.now().hour
        timeParked = math.ceil(currentHour - self._timeParked[driver.get_id()])
        driver.charge(timeParked * self._hourlyRate)

        del self._timeParked[driver.get_id()]
        return self._parkingGarage.remove_vehicle(driver.get_vehicle())


# Finally, we can test it out by parking a few vehicles.
parkingGarage = ParkingGarage(3, 2)
parkingSystem = ParkingSystem(parkingGarage, 5)

driver1 = Driver(1, Car())
driver2 = Driver(2, Limo())
driver3 = Driver(3, SemiTruck())

print(parkingSystem.park_vehicle(driver1))  # true
print(parkingSystem.park_vehicle(driver2))  # true
print(parkingSystem.park_vehicle(driver3))  # false

print(parkingSystem.remove_vehicle(driver1))  # true
print(parkingSystem.remove_vehicle(driver2))  # true
print(parkingSystem.remove_vehicle(driver3))  # false
