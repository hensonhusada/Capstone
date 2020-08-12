# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
from class_plc import ModbusPLC as plc
from class_firebase import FirebaseConnection as conn
import datetime

# --------------------------------------------------------------------------- #
# Setup inisiasi koneksi PLC dan firebase
# --------------------------------------------------------------------------- #
while True:
    ip_PLC = input('Enter the IP address of PLC: ')
    error_plc = plc(ip_PLC, 502)    
    if error_plc.client.connect() != False: break
    
firebase = conn(credKey='key.json', databaseURL='https://capstone-plc.firebaseio.com/')

# --------------------------------------------------------------------------- #
# Pemeriksaan nilai awal tiap-tiap level pada PLC
# --------------------------------------------------------------------------- #
try:
    rr = error_plc.read_coil(0x06, 5)
    tmp_type = rr[0:5]
    print('Value of level coils ', tmp_type)
except Exception as e:
    print('Error: %s' %str(e))
    
# --------------------------------------------------------------------------- #
# Fungsi yang dikerjakan bila terjadi event pada firebase
# --------------------------------------------------------------------------- #
def listen_function(event, error_plc=error_plc):      
    resp_flag = 0    
    global tmp_type
    # ------------------------------------------------------------------------#
    # Preproccesing data dari event firebase
    # ------------------------------------------------------------------------#
    try:
        level_value = 0
        event_null = list(event.data.keys())                
        if len(event_null) == 1:
            event_data_keys = list(event.data[event_null[0]])
            event_data = event.data[event_null[0]]            
        else:
            event_data_keys = []
            event_data = []
        level_value_key = event_data_keys[0]                          
        level_value = event_data[level_value_key]       ## nilai level air                
    except Exception as e:        
        print('Error: %s' %str(e))
        
    # ------------------------------------------------------------------------#
    # Proses pengiriman input ke PLC 
    # ------------------------------------------------------------------------#    
    try:               
        if level_value > 0 and level_value <=25 and tmp_type[0] != True:
            print('Processing level to value', level_value)
            error_plc.write_register(0x00, level_value)
            rr = error_plc.read_coil(0x06, 5)
            tmp_type = rr[0:5]
            resp_flag = 1
        elif level_value >25 and level_value <= 50 and tmp_type[1] != True:
            print('Processing level to value', level_value)
            error_plc.write_register(0x00, level_value)
            rr = error_plc.read_coil(0x06, 5)
            tmp_type = rr[0:5]
            resp_flag = 1
        elif level_value > 50 and level_value <= 75 and tmp_type[2] != True:
            print('Processing level to value', level_value)
            error_plc.write_register(0x00, level_value)
            rr = error_plc.read_coil(0x06, 5)
            tmp_type = rr[0:5]
            resp_flag = 1
        elif level_value > 75 and level_value <=100 and tmp_type[3] != True:
            print('Processing level to value', level_value)
            error_plc.write_register(0x00, level_value)
            rr = error_plc.read_coil(0x06, 5)
            tmp_type = rr[0:5]
            resp_flag = 1
        elif tmp_type[4] != True:
            print('Processing level to value', level_value)
            error_plc.write_register(0x00, level_value)
            rr = error_plc.read_coil(0x06, 5)
            tmp_type = rr[0:5]
            resp_flag = 1
            
    except Exception as e:
        print('error: %s' %str(e))          
        
    # ------------------------------------------------------------------------#
    # Proses pengiriman input ke PLC 
    # ------------------------------------------------------------------------# 
    if resp_flag == 1:
        print('Sending response to database')
        resp_msg = 'Water level succefully changed to '+ str(level_value)
        resp_id_key = event_data_keys[3]
        resp_id = event_data[resp_id_key]        
        currentDT = datetime.datetime.now()
        resp_time = currentDT.strftime('%d/%m/%Y %H:%M:%S.%f')
        print(resp_time)        
        resp_dic = {'id' : resp_id, 'message' : "Success", 'response' : resp_msg, 'time' : resp_time}       
        firebase.response('activity/response', resp_dic)    

firebase.database_listen('activity/history/height', listen_function)
