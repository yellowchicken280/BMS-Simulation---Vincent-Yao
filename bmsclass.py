import time
import sys
import random

class Battery:
    def __init__(self, voltage=3.8, temp=25, soc=50, vdev=0.08, charger_connected=False):
        """ Initializes the battery with given parameters. """
        self.voltage = voltage
        self.temp = temp
        self.soc = soc
        self.soh = 1.0
        self.impedance = 5.4
        self.vdev = vdev
        self.charge_current = 0
        self.discharge_current = 0
        self.charger_connected = charger_connected
        self.state = "OFF"

    def transition_state(self, new_state):
        """ Changes the battery state """
        print(f"Transitioning: {self.state} → {new_state}")
        self.state = new_state

    def start_init(self):
        """ Starts the car or starts charging"""
        if self.state != "OFF":
            print("System is already active.")
            return
        
        self.transition_state("INIT")

        # input validation
        if not (2.5 <= self.voltage <= 4.2):
            self.trigger_fault("Voltage out of range")
        if not (-20 <= self.temp <= 60):
            self.trigger_fault("Temperature out of range")

        print("INIT checks passed.")

        if self.charger_connected:
            print("Charger detected. Entering CHARGING mode instead of PRECHARGING.")
            self.charge()
        else:
            print("No charger detected. Proceeding to PRECHARGING.")
            self.precharge()

    def precharge(self):
        self.transition_state("PRECHARGING")
        time.sleep(2)  
        print("Precharge complete. Entering IDLE state.")
        self.transition_state("IDLE")

    #can either charge while off state or when the car starts up with the default settings below
    def charge(self, charge_current=10, charge_time=1, charge_type=2):
        if self.state not in  ["INIT", "OFF"]:
            print("Charging can only start from INIT, not IDLE")
            return

        if not (0 <= self.temp <= 45):
            self.trigger_fault("Temperature out of range")

        charge_limits = {1: 15, 2: 20, 3: 120}
        charge_limit = charge_limits.get(charge_type, 15)

        if charge_current > charge_limit:
            self.trigger_fault("Overcurrent detected")

        self.transition_state("CHARGING")

        soc_increase = charge_time * charge_current * 10000 / (self.soh * 10.2)

        if self.soc + soc_increase > 100:
            charge_time = (100 - self.soc) * self.soh * 10.2 / (charge_current * 10000)
        
        self.soc = min(100, self.soc + soc_increase)
        print(f"Charging... New SOC: {self.soc:.2f}%")
        time.sleep(charge_time)
        self.charger_connected = False
        print("Charging complete. Returning to OFF state.")
        self.transition_state("OFF") 

    def discharge(self, discharge_current, discharge_time, discharge_type):
        
        if self.state != "IDLE":
            print("Cannot discharge from current state:", self.state)
            return

        if not (-20 <= self.temp <= 60):
            self.trigger_fault("Temperature out of range")

        discharge_limits = {1: 60, 2: 120, 3: 200}
        discharge_limit = discharge_limits.get(discharge_type, 60)

        if discharge_current > discharge_limit:
            self.trigger_fault("Overcurrent detected")

        self.transition_state("DISCHARGING")

        soc_decrease = discharge_time * discharge_current * 10000 / (self.soh * 10.2)

        if self.soc - soc_decrease < 2:
            discharge_time = (self.soc - 2) * self.soh * 10.2 / (discharge_current * 10000)

        self.soc = max(2, self.soc - soc_decrease)
        print(f"Discharging... New SOC: {self.soc:.2f}%")
        time.sleep(discharge_time)

        self.transition_state("IDLE")

    def balance_cells(self):

        if self.state != "IDLE":
            print("Balancing can only occur from IDLE state.")
            return

        if self.vdev >= 0.1 and self.soc >= 80:
            self.transition_state("BALANCING")
            print("Balancing cells...")
            time.sleep(3)
            self.vdev = random.uniform(0, 0.05)  
            print(f"Balancing complete. New deviation: {self.vdev:.3f}V")
            self.transition_state("IDLE")
        else:
            print("Balancing not required.")

    def trigger_fault(self, reason):
        print(f"FAULT detected: {reason}. Entering FAULT state.")
        self.transition_state("FAULT")
        sys.exit()

    def shutdown(self):
        print("Shutting down the system...")
        self.transition_state("OFF")

    def display_status(self):
        """ Prints the current state and battery conditions. """
        print(f"State: {self.state} | Voltage: {self.voltage:.2f}V | Temp: {self.temp}°C | SOC: {self.soc:.2f}% | SOH: {self.soh:.2f} | Vdev: {self.vdev:.2f}V")


