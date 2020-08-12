from class_plc import ModbusPLC as plc
from class_firebase import FirebaseConnection as conn
from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')        

while True:
    print('Simulasi untuk plant Ketinggian Air')
    ip_plc = input('Enter the IP address of PLC: ')
    level_plc = plc(ip_plc, 502)
    if level_plc.try_connect() == True: break

firebase = conn(credKey='key.json', databaseURL='https://capstone-plc.firebaseio.com/') 

rr = level_plc.read_register(0x00, 1)
print('Ketinggian air: %s' %rr)

def pungsi(opsi):   
    global rr    
    level_plc.write_register(0, opsi)          
    
while True:    
    print('Input ketinggian air dari 0 sampai 100')
    opsi = input('Masukkan pilihan: ')
    opsi = int(opsi)    
    pungsi(opsi)
    
    clear()
    rt = level_plc.read_coil(6, 5)[0:5] 
    print(rt)