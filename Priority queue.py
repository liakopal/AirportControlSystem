import queue
from random import choice
import numpy as np
from datetime import datetime
from time import sleep
import threading

class Plane:
    """
    Represents a plane with its flight number, request type, and priority.

    Attributes:
        flight_number (str): The flight number of the plane.
        request_type (str): The type of request associated with the plane.
        priority (int, optional): The priority level of the plane. Defaults to 0.
    """

    def __init__(self, flight_number, request_type, priority=0):
        self.flight_number = flight_number
        self.request_type = request_type
        self.priority = priority

class AirportControlSystem:
    """
    A class representing an airport control system.

    Attributes:
        landing_queue (Queue): A queue to store planes requesting landing.
        takeoff_queue (Queue): A queue to store planes requesting takeoff.
        emergency_queue (Queue): A queue to store planes requesting emergency landing.

    Methods:
        generate_requests(flight_numbers, n=5): Generates n random plane requests.
        process_request(flight_number, request_type): Processes a plane request and adds it to the appropriate queue.
    """

    def __init__(self):
        self.landing_queue = queue.Queue()
        self.takeoff_queue = queue.Queue()
        self.emergency_queue = queue.Queue()

    def generate_requests(self, flight_numbers, n=5):
        """
        Generate n random plane requests.

        Parameters:
        - flight_numbers (list): A list of flight numbers.
        - n (int): The number of requests to generate (default is 5).

        Returns:
        None

        This method generates n random plane requests by randomly selecting a flight number from the given list
        and choosing a request type ('landing', 'takeoff', or 'emergency') with specified probabilities.
        It then prints the request details and processes the request using the `process_request` method.
        A random delay is added to mimic the arrival times of the requests.
        """
        for _ in range(n):
            flight_number = choice(flight_numbers)
            request_type = np.random.choice(['landing', 'takeoff', 'emergency'], p=[0.4, 0.4, 0.2])
            print(f"{current_timestamp()} [REQUEST] Flight {flight_number} requests {request_type.upper()}.")
            self.process_request(flight_number, request_type)
            sleep(np.random.exponential(0.5))  # Random delay to mimic request arrival times

    def process_request(self, flight_number, request_type):
        """
        Process a request for a plane with the given flight number and request type.

        Args:
            flight_number (str): The flight number of the plane.
            request_type (str): The type of request, which can be 'landing', 'takeoff', or 'emergency'.

        Returns:
            None
        """
        plane = Plane(flight_number, request_type)
        if request_type == 'landing':
            self.landing_queue.put(plane)
        elif request_type == 'takeoff':
            self.takeoff_queue.put(plane)
        elif request_type == 'emergency':
            self.emergency_queue.put(plane)

from datetime import datetime

def current_timestamp():
    """
    Returns the current timestamp in the format HH:MM:SS.
    """
    return datetime.now().strftime("%H:%M:%S")

def process_control_operations(acs):
    """
    Process the requests in the control system queues.

    This function continuously checks the control system queues for incoming requests and performs the necessary operations.
    It first checks the emergency queue, then the landing queue, and finally the takeoff queue.
    If there is an emergency request, it clears the flight for immediate landing.
    If there is a landing request, it clears the flight to land.
    If there is a takeoff request, it clears the flight for takeoff.

    Parameters:
    acs (object): An instance of the control system containing the queues.

    Returns:
    None
    """
    while True:
        if not acs.emergency_queue.empty():
            plane = acs.emergency_queue.get()
            print(f"{current_timestamp()} [CONTROLLER] Emergency: Flight {plane.flight_number} is cleared for immediate landing.")
        elif not acs.landing_queue.empty():
            plane = acs.landing_queue.get()
            print(f"{current_timestamp()} [CONTROLLER] Flight {plane.flight_number} is cleared to land.")
        elif not acs.takeoff_queue.empty():
            plane = acs.takeoff_queue.get()
            print(f"{current_timestamp()} [CONTROLLER] Flight {plane.flight_number} is cleared for takeoff.")
        sleep(1)  # Adjust based on the desired pace of control operations

def main():
    """
    Entry point of the program.
    
    This function initializes the AirportControlSystem, starts the control operations in a separate thread,
    and continuously generates requests until interrupted by the user.
    """
    acs = AirportControlSystem()
    flight_numbers = [f"{i}" for i in range(100, 200)]

    # Start the control operations in a separate thread
    control_thread = threading.Thread(target=process_control_operations, args=(acs,))
    control_thread.start()

    # Continuously generate requests
    try:
        while True:
            acs.generate_requests(flight_numbers, n=np.random.randint(1, 5))
            sleep(np.random.exponential(2))  # Wait a random time before generating more requests
    except KeyboardInterrupt:
        print("\nSimulation ended by user.")

if __name__ == "__main__":
    main()
