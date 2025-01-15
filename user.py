#Veritabanına ürün ekleme, ürün silme, kullanıcı silme, kayıt alma, veritabanı bağlantısı ve son olarak kullanıcı varlığını 'user.py' dosyasına tanımlar.
from database import add_product, delete_product, delete_user, log_action, connect_db, user_exists

# Kullanıcıların ve Adminlerin yapabileceği işlemleri gösterir.
class User:
    def __init__(self, user_id, username, role):
        self.user_id = user_id
        self.username = username
        self.role = role

    # Ürün ekleme ve kaydının tutulmasını sağlar.
    def add_product(self, name, price):
        # Ürüne isim, fiyat ve ID belirleyen koddur.
        add_product(name, price, self.user_id)
        # Eklenen ürünlerin kaydını tutar.
        log_action(self.user_id, f"Added product: {name}")

    # Ürün kaldırır ve kaydının tutulmasını sağlar.
    def delete_product(self, product_id):
        # Ürün IDsi ile silinmesini sağlar.
        delete_product(product_id)
        # Ürün IDsi ile silinmesini sağlar.
        log_action(self.user_id, f"Deleted product ID: {product_id}")

        # Kullanıcının kendi log kayıtlarını almasını sağlar.
    def get_own_logs(self):
        # Veritabanına bağlar.
        conn = connect_db()
        cursor = conn.cursor()
        # Kullanıcının kendi IDsi ile log kayıtlarını seçer.
        cursor.execute('SELECT * FROM logs WHERE user_id = ?', (self.user_id,))
        # Seçilen kayıtları alır.
        logs = cursor.fetchall()
        # Veritabanı ile bağlantıyı keser.
        conn.close()
        # Kayıtları döndürür.
        return logs

    # Sadece adminler için geçerli işlemler:
    def generate_report(self, target_user_id):
        if self.role != 'admin':
            print("Bu işlem için yetkiniz yok.")
            return []
        # Veritabanına bağlar.
        conn = connect_db()
        cursor = conn.cursor()
        # Seçilen kullanıcı IDsi ile işlem kayılarını seçer.
        cursor.execute('SELECT * FROM logs WHERE user_id = ?', (target_user_id,))
        # Seçilen kayıtları alır.
        logs = cursor.fetchall()
        # Veritabanı ile bağlantıyı keser.
        conn.close()
        # Kayıtları döndürür.
        return logs
    
    # Admin Seçilen bir kullanıcıyı ID kullanarak siler.
    def delete_user(self, user_id):
        if self.role != 'admin':
            print("Bu işlem için yetkiniz yok.")
            return False
        # Girilen kullanıcının varlığını sorgular.
        if user_exists(user_id):
            # Kullanıcıyı siler.
            delete_user(user_id)
            # Silme işlemini kayıt eder.
            log_action(self.user_id, f"Deleted user ID: {user_id}")
            return True
        # Kullanıcının olmadığı veya bulunmadığı durumdur.
        else:
            return False
