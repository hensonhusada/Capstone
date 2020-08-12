import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class FirebaseConnection:
    '''
        Proses inisialisasi pengaturan koneksi google firebase serta fungsi
        sederhana listener dan response.
    '''
    
    def __init__(self, credKey, databaseURL):
        '''
            Inisialisasi pengaturan koneksi dan inisialisasi firebase
            
            Argumen
                credKey = kunci enkripsi yang dibutuhkan untuk akses ke firebase, berformat json
                databaseURL = url dari database pada google firebase
        '''
        self.cred = credentials.Certificate(credKey)
        self.databaseURL = databaseURL
        name = '[DEFAULT]'
        self.firebes = firebase_admin.initialize_app(self.cred, {'databaseURL' : self.databaseURL}, name)         
        
    def database_listen(self, firebase_ref, cb_func):
        '''
            Register event listener pada database
            
            Argumen
                firebase_ref = path pada firebase yang akan diberi listener
                cb_func = function yang dipanggil ketika terjadi event
        '''   
        self.ref = db.reference(firebase_ref).listen(cb_func)
        
    def response(self, firebase_ref, data):
        '''
            Mengirimkan data ke database
            
            Argumen
                firebase_ref = path pada firebase yang akan dikirim kan data
                data = data yang akan dipush dalam bentuk json(dict)
        '''
        self.ref = db.reference(firebase_ref).push(data)