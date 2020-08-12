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
    turb_plc = plc(ip_PLC, 502)
    if turb_plc.client.connect() != False: break
    
firebase = conn(credKey='key.json', databaseURL='https://capstone-plc.firebaseio.com/')

# --------------------------------------------------------------------------- #
# Pemeriksaan nilai awal turbin dr PLC
# --------------------------------------------------------------------------- #
try:
    rr = turb_plc.read_coil(0x03, 3)
    plc_turb_value = rr[0:3]
    print('Value of turbine HP, MP, LP: ', plc_turb_value)
except Exception as e:
    print('Error: %s' %str(e))

# --------------------------------------------------------------------------- #
# Fungsi yang dikerjakan bila terjadi event pada firebase
# --------------------------------------------------------------------------- #
def listen_function(event, turb_plc=turb_plc, firebase=firebase):                 
    resp_flag = 0
    try:        
    # ------------------------------------------------------------------------#
    # Preproccesing data dari event firebase
    # ------------------------------------------------------------------------#        
        event_null = list(event.data.keys())
        # print(event_null)               #debugging
        if len(event_null) == 1:
            event_data_keys = list(event.data[event_null[0]])
            event_data = event.data[event_null[0]]
            # print(event_data)
        else:
            event_data_keys = []
            event_data = []
        # print(event_data_keys, type(event_data_keys))          #debugging
    # ------------------------------------------------------------------------#
    # Preproccesing data dari event firebase
    # ------------------------------------------------------------------------#            
        turb_type_key = event_data_keys[4]           
        turb_value_key = event_data_keys[2]
        turb_type = event_data[turb_type_key]          ## tipe turbin        
        turb_value = event_data[turb_value_key]         ## nilai boolean dari turbin        
        if turb_type in ['hp', 'mp', 'lp']:
            print('Processing turbine', turb_type, 'to value', turb_value)
    
    # ------------------------------------------------------------------------#
    # Proses pengiriman input ke switch PLC sesuai tipe turbin dan membaca output
    # ------------------------------------------------------------------------#
        if turb_type == 'hp' and plc_turb_value[0] != turb_value:            
            turb_plc.write_coil(0x00, turb_value)    
            rr = turb_plc.read_coil(0x03, 1)            
            plc_turb_value[0] = rr[0]
            print('Value of HP turbine output: ', rr[0])       
            resp_flag = 1
        elif turb_type == 'mp' and plc_turb_value[1] != turb_value:        
            turb_plc.write_coil(0x01, turb_value)              
            rr = turb_plc.read_coil(0x04, 1)
            plc_turb_value[1] = rr[0]
            print('Value of MP turbine output: ', rr[0])
            resp_flag = 1
        elif turb_type == 'lp' and plc_turb_value[2] != turb_value:        
            turb_plc.write_coil(0x02, turb_value)
            rr = turb_plc.read_coil(0x05, 1)
            plc_turb_value[2] = rr[0]
            print('Value of LP turbine output: ', rr[0])        
            resp_flag = 1
            
    except Exception as e:
        print('Error: %s' %e)   

    # ------------------------------------------------------------------------#
    # Proses pengiriman respon ke firebase
    # ------------------------------------------------------------------------#
    if resp_flag == 1:            
        resp_msg = 'Turbine '+turb_type+' successfully switched'
        resp_id_key = event_data_keys[0]
        resp_id = event_data[resp_id_key]        
        currentDT = datetime.datetime.now()
        resp_time = currentDT.strftime('%d/%m/%Y %H:%M:%S.%f')
        print('Response sent: ', resp_time)
        resp_dic = {'id' : resp_id, 'message' : "Success", 'response' : resp_msg, 'time' : resp_time}       
        firebase.response('activity/response', resp_dic)
    

firebase.database_listen('activity/history/turbine', listen_function)
