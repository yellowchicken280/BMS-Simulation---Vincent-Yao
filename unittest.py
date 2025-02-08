from bmsclass import Battery

# Scenario 1: Charging default charge current is 10
print("Scenario 1: Charging (OFF → INIT → CHARGING → OFF)")
battery1 = Battery(voltage=3.8, temp=25, soc=50, vdev=0.08, charger_connected=True)
battery1.start_init()  # Goes INIT → CHARGING → OFF

# Scenario 2: Driving (No charger, normal car startup)
print("\nScenario 2: Driving (OFF → INIT → PRECHARGING → IDLE → DISCHARGING → IDLE → OFF)")
battery2 = Battery(voltage=3.8, temp=25, soc=80, vdev=0.05, charger_connected=False)
battery2.start_init()  
battery2.discharge(discharge_current=50, discharge_time=0.5, discharge_type=2)
battery2.display_status()
battery2.shutdown()

# Scenario 3: Fault Detection (Voltage too high on INIT)
print("\nScenario 3: Fault Detection (Voltage too high on INIT, should trigger FAULT)")
battery3 = Battery(voltage=4.5, temp=25, soc=80, vdev=0.05, charger_connected=False)
try:
    battery3.start_init()  # Expected FAULT
except SystemExit:
    print("FAULT detected, continuing with next test case.")

# Scenario 4: Balancing After Charging 
print("\nScenario 4: Balancing (After Charging, SOC High, Voltage Deviation Above Threshold)")
battery4 = Battery(voltage=3.9, temp=25, soc=85, vdev=0.12, charger_connected=True)
battery4.start_init() 
battery4.start_init()  
battery4.balance_cells() 

# Scenario 5: Overcurrent Fault During Discharge
print("\nScenario 5: Overcurrent Fault During Discharge (DISCHARGING → FAULT)")
battery5 = Battery(voltage=3.8, temp=25, soc=50, vdev=0.05, charger_connected=False)
battery5.start_init()  
try:
    battery5.discharge(discharge_current=250, discharge_time=0.5, discharge_type=3) 
except SystemExit:
    print("FAULT detected, continuing with next test case.") 

# Scenario 6: Normal Usage with Charge, Discharge, and Balancing
print("\nScenario 6: Full Cycle (Charging → Discharge → Balancing → OFF)")
battery6 = Battery(voltage=3.7, temp=25, soc=60, vdev=0.09, charger_connected=True)
battery6.start_init() #charges and then shuts down
battery6.start_init()
battery6.discharge(discharge_current=40, discharge_time=0.8, discharge_type=2)
battery6.balance_cells()
battery6.shutdown()

# Scenario 7: Too much current while charging
print("\nScenario 7: Too much current while charging (FAULT)")
battery7 = Battery(voltage=3.7, temp=25, soc=60, vdev=0.09, charger_connected=False)
try:
    battery7.charge(charge_current=100, charge_time=1, charge_type=2)
except SystemExit:
    print("FAULT detected.")

print("\nAll test cases executed.")