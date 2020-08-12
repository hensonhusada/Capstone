"""
    class_plc     
"""

# --------------------------------------------------------------------------- #
# 
# --------------------------------------------------------------------------- #
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

class ModbusPLC:    
    '''
        Proses penyambungan PLC menggunakan ModbusTCP, pengguna hanya perlu menyediakan 
        alamat IP serta port dimana PLC berjalan dalam menginstansi class.
        
        Contoh:
        plc = plc('192.168.100.1')
        atau
        plc = plc('192.168.100.1', 502)
    '''
    
    def __init__(self, ip_address, port=502):
        '''
            Menginisialisasi pengaturan koneksi PLC.
            
            Argumen
                ip_address
                port
        '''        
        self.client = ModbusClient(ip_address, port=port)        
    
    def try_connect(self):
        '''
            Mencoba koneksi ke PLC.
            
            Return: boolean
        '''
        if self.client.connect()==False:        
            print('Connection invalid. Please try again.')            
            return(False)
        else:
            print('Successfully connect to PLC.')
            return(True)
            
    def read_coil(self, addr, quan, slave_id=0x00):
        '''
            Membaca memori coil pada protokol Modbus PLC.
            
            Argumen
                addr: alamat coil mula(hex atau int)
                quan: jumlah coil yang dibaca
                slave_id: default 0x00 untuk broadcast
            
            Return: sebuah list sepanjang kelipatan delapan
        '''
        try:
            self.client.connect()
            rr = self.client.read_coils(addr, quan, unit=slave_id)
            self.client.close()
            return(rr.bits)            
        except Exception as e:
            print('An error occured while trying to read coils: %s' %str(e))
            return(None)
    
    def write_coil(self, addr, val, slave_id=0x00):
        '''
            Menulis memori coil pada protokol Modbus PLC.
            
            Argumen
                addr: alamat coil mula(hex atau int)
                val: nilai yang dituliskan
                     (untuk menuliskan satu nilai, cukup int atau bool)
                     (untuk menuliskan banyak nilai, gunakan list int atau list bool)
                slave_id: default 0x00 untuk broadcast
                        
        '''        
        try:
            self.client.connect()
            if type(val)==bool:
                rr = self.client.write_coil(addr, val, unit=slave_id)   
                print('Coil', str(addr), 'written successfully!')
            else:
                rr = self.client.write_coils(addr, val, unit=slave_id)
                print('Coils written successfully!')
            self.client.close()
        except Exception as e:
            print('An error occured while trying to write coils: %s' %str(e))            
        
    def read_register(self, addr, quan, slave_id=0x00):
        '''
            Membaca memori register pada protokol Modbus PLC.
            
            Argumen
                addr: alamat register mula(hex atau int)
                quan: jumlah register yang dibaca
                slave_id: default 0x00 untuk broadcast
            
            Return: sebuah list sepanjang jumlah nilai yang diminta
        '''
        try:
            self.client.connect()
            rr = self.client.read_holding_registers(addr, quan, unit=slave_id)
            return(rr.registers)
            self.client.close()
        except Exception as e:
            print('An error occured while trying to read registers: %s' %str(e))
            return(None)
        
    def write_register(self, addr, val, slave_id=0x00):
        '''
            Menulis memori register pada protokol Modbus PLC.
            
            Argumen
                addr: alamat register mula(hex atau int)
                val: nilai yang dituliskan
                     (untuk menuliskan satu nilai, cukup int)
                     (untuk menuliskan banyak nilai, gunakan list int)
                slave_id: default 0x00 untuk broadcast
        '''   
        try:
            self.client.connect()
            if type(val)==list:
                rr = self.client.write_registers(addr, val, unit=slave_id)
                print('Registers written successfully!')
            else:
                rr = self.client.write_register(addr, val, unit=slave_id)
                print('Registers written successfully!')
            self.client.close()
        except Exception as e:
            print('An error occured while trying to write registers: %s' %str(e))            