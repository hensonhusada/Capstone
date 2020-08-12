from class_plc import ModbusPLC as plc
from class_firebase import FirebaseConnection as conn
from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')        

while True:
    print('Simulasi untuk plant Turbin')
    ip_plc = input('Enter the IP address of PLC: ')
    level_plc = plc(ip_plc, 502)
    if level_plc.try_connect() == True: break

firebase = conn(credKey='key.json', databaseURL='https://capstone-plc.firebaseio.com/') 

rr = level_plc.read_coil(0x00, 3)
print('State Switch PLC: %s' %rr[0:3])
rt = level_plc.read_coil(3, 3)[0:3]
print('Kondisi Turbin PLC: %s' %rt[0:3])

def pungsi(opsi):   
    global rr
    opsi = opsi-1    
    if rr[opsi]==True:
        level_plc.write_coil(opsi, False)        
        rr[opsi] = level_plc.read_coil(opsi, 1)[0]        
    else:
        level_plc.write_coil(opsi, True)
        rr[opsi] = level_plc.read_coil(opsi, 1)[0]        
    
while True:    
    print('Input:  1. Switch Turbin HP\n\t2. Switch Turbin MP\n\t3. Switch Turbine LP')
    opsi = input('Masukkan pilihan: ')    
    if opsi == 'cls':
        clear()
    else:
        opsi = int(opsi)
        pungsi(opsi)        
        rt = level_plc.read_coil(3, 3)[0:3]
        rr = level_plc.read_coil(0x00, 3)
    print('State Switch PLC: %s' %rr[0:3])
    print('Kondisi Turbin PLC: %s' %rt[0:3])