import time as t
import sys
import random

voltage = 0
discharge = 0
charge = 0
impedance = 5.4
temp = 0
vdev = 0
state = "OFF" ##states: OFF, PRECHARGING, INIT, IDLE, CHARGING, BALANCING, DISCHARGING, FAULT

soc = 0
soh = 100*5.4/impedance

print ("Welcome to the BMS simulator. Activating the machine...")
print ("Please enter the initial conditions/sensor inputs of the battery")
print ("Enter initial voltage (acceptable range is 2.5 to 4.2 volts)")
voltage = float(input()) #initial voltage
            

print ("Enter initial temp")
temp = float(input()) #initial temp

print ("Enter initial SOC as an number 1 to 100")
soc = float(input()) #initial SOC
if soc <0 or soc > 100: #input validation
    print ('invalid input, enter again')
    soc = float(input())

print ('Enter the degree of deviation between battery cells, 0.1 and 80% SOC is the threshold for balancing')
vdev = float(input())
while True:
    print ("Enter ON to turn the the car on, or C to plug in a charger, or EXIT to turn off the bms")
    on = input()
    if on == "ON":
        state = "INIT"
        print ('entering INIT state, performing self checks')
        if voltage > 4.2 or voltage <= 2.5:
            state = "FAULT"
            print ("Voltage is out of accpetable range, machine is in fault state")
            print('shutdown circut activated')
            sys.exit()
        if temp >=60 or temp <= -20:
            state = "FAULT"
            print ("Temp is out of acceptable range, machine is in fault state")
            print('shutdown circut activated')
            sys.exit()
        print ('initialization complete, now in pre charging state')
        print ("powering up high voltage system...")
        t.sleep(3)
        print ("Enter YES to indicate successful power up")
        if input() != "YES":
            state = "FAULT"
            print ("power up failed, machine is in fault state")
            print('shutdown circut activated')
            sys.exit()
        print ("low voltage system powered up successfully, state is now idle")
        state = "IDLE"
        while True:
            if vdev >= 0.1 and soc >= 80:
                state = "BALANCING"
                print ("STATE: ", state)
                print ("Balancing cells")
                t.sleep(5)
                vdev = random.uniform(0, 0.05)
                print ("Balancing complete, back to IDLE state, deviation is now ", round(vdev, 4))
                state = "IDLE"
            print("current state: ", state, "current state of charge: ", round(soc, 2), "current voltage: ", voltage, "current Temp: ", temp)
            if state == "FAULT" or state == "OFF":
                break
            print ("Enter command,  A to accelerate the car, V, T, I, and D to change the voltage, temprature, impedance, and degree of deviation respectively, enter OFF to turn car off")
            command = input()

            if command == 'A': #accelerate, discharge state
                if voltage > 4.2 or voltage <= 2.5:
                    state = "FAULT"
                    print ("Voltage is out of accpetable range, machine is in fault state")
                    print('shutdown circut activated')
                    break
                if temp >=60 or temp <= -20:
                    state = "FAULT"
                    print ("Temp is out of acceptable range, machine is in fault state")
                    print('shutdown circut activated')
                    break
                print("type 1,2,3 for (1) No cooling, in a pack (2) Forced air cooling, (3) 10 sec. pulse, fuse limited, respectively")
                i = 0
                i = int(input())
                while not (0<i<4): #input validation
                    print('invalid input')
                    i = int(input())
                limit = 60*i
                print ('enter discharge current in amps (per module)')
                discharge = float(input())
                while discharge <= 0: #input validation
                    print ('invalid input, enter again')
                    discharge = float(input())
                if discharge > limit:
                    print ("discharge current exceeds limit, it will be set to ", round(limit, 2))
                    discharge = limit

                print ('enter how long you want to discharge in hours (e.g. 1 hr 20 mins u enter 1.33)')
                time = float(input())
                
                if soc <=2:
                    print ("SOC below threshold, you cannot discharge")
                    discharge = 0
                else:
                    state = "DISCHARGING"
                if state == "DISCHARGING" and soc-time*discharge*10000/(soh*10.2)<=2:
                    print ("discharge will exceed SOC limit, time will be set to ", round(time, 2))
                    time = (soc-2)*(soh*10.2)/(discharge*10000)
                soc -= time*discharge*10000/(soh*10.2)
                soc = max(0, soc)
                print ("New state: ", state)
                if state == "DISCHARGING":
                    t.sleep(time*10)
                    print ("discharging complete new SOC: ", round(soc, 2))
                    state = "IDLE"
                    discharge = 0
                    print ("New state: ", state)
            
            
            elif command == 'V':
                print ("Enter new Voltage (acceptable range is 2.5 to 4.2 volts)")
                voltage = float(input())
                if voltage > 4.2 or voltage <= 2.5:
                    state = "FAULT"
                    print ("Voltage is out of acceptable range, machine is in fault state")
                    print('shutdown circut activated')
                    break
                print ("New state: ", state)
            elif command == 'T':
                print ("Enter new Temp")
                temp = float(input())
                if temp >=60 or temp <= -20:
                    state = "FAULT"
                    print ("Temp is out of acceptable range, machine is in fault state")
                    print('shutdown circut activated')
                    break
                print ("New state: ", state)
            elif command == 'I':
                print ("Enter new Impedance, current impedance is, ", impedance)
                newimpedance = float(input())
                assert newimpedance >= 5.4
                soh = 5.4/newimpedance
                soc = soc*newimpedance/impedance
                impedance = newimpedance
                print ('new soh: ', soh)
                print ('now your maximum charge is ', round(soh*10.2, 2), " amp hours")
                print ("New state: ", state)
            elif command == 'OFF':
                state = "OFF"
                print ('machine is now off')
                break
            elif command == "D":
                print ('Enter new degree of deviation between cells')
                vdev = float(input())
                print ("New state: ", state)
            else:
                print ('invalid input, enter again')
    elif on == "C":
        if voltage > 4.2 or voltage <= 2.5:
            state = "FAULT"
            print ("Voltage is out of acceptable range, machine is in fault state")
            print('shutdown circut activated')
            break
        if temp >=45 or temp <= 0:
            state = "FAULT"
            print ("Temp is out of range, machine is in fault state")
            print('shutdown circut activated')
            break
        print("type 1,2,3 for (1) No cooling, in a pack (2) Forced air cooling, (3) 10 sec. pulse, 50% SOC, respectively")
        i = 0
        i = int(input())
        while not (0<i<4): #input validation
            print('invalid input')
            i = int(input())
        if (i==1):
            limit = 15
        elif (i==2):
            limit = 20
        else:
            limit = 120
        print ('enter charge current in amps (per module)')
        charge = float(input())
        while charge <= 0: #input validation
            print ('invalid input, enter again')
            charge = float(input())
        if charge > limit:
            print ("charge current exceeds limit, overcurrent detected, FAULT state will be activated")
            break

        print ('enter how long you want to charge in hours (e.g. for 1 hr 20 mins u enter 1.33)')
        time = float(input())
        if soc >= 100:
            print ("SOC above threshold, you cannot charge")
            charge = 0
        else:
            state = "CHARGING"
        if state == 'CHARGING' and soc+time*charge*10000/(soh*10.2)>100:
            time = (100-soc)*(soh*10.2)/(charge*10000)
            print ("charge will exceed SOC limit, time will be set to ", round(time, 2))

        soc += time*charge*10000/(soh*10.2)
        soc = min(100, soc)
        print ("New state: ", state)
        if state == "CHARGING":
            t.sleep(time*10)
            print ("charging complete new SOC: ", round(soc, 2))
            state = "OFF"
            charge = 0
            print ("Enter new Voltage (acceptable range is 2.5 to 4.2 volts)")
            voltage = float(input())
            if voltage > 4.2 or voltage <= 2.5:
                state = "FAULT"
                print ("Voltage is out of acceptable range, machine is in fault state")
                print('shutdown circut activated')
                break
            print ("New state: ", state)
    elif on == "EXIT":
        print ("turning off the machine")
        break
    else:
        print ('invalid input, try again')
        
        
        
    
