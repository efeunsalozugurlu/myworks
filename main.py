# 'database.py' kısmındaki rolleri 'main.py' dosyasına tanımlar.
from database import create_tables, add_user, authenticate_user, connect_db, username_exists, export_logs_to_csv
# 'user.py' kısmındaki rolleri 'main.py' dosyasına tanımlar.
from user import User

# Programa giriş ekranını gösteren koddur.
def main():
    print("Çevrimiçi Satış Programına Hoşgeldiniz")
    create_tables()
    
    # Sisteme bir admin tanımlar.
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
    if cursor.fetchone()[0] == 0:
        add_user('efe', 'shazam', 'admin')
    conn.close()
    
    # Giriş veya kayıt ekranına yönlendiren koddur.
    while True:
        print("\n1. Giriş Yap")
        print("2. Yeni Kullanıcı Oluştur")
        print("3. Çıkış")
        choice = input("Seçiminiz: ")

        # Eğer 1 yani giriş seçeneğini seçtikten sonra girilmesi gereken bilgileri gösteren koddur.
        if choice == '1':
            username = input("Kullanıcı Adı: ")
            password = input("Şifre: ")
            user = authenticate_user(username, password)

            # İki tane kullanıcı tipi girilir.
            # Admine kullanıcı ID ve kullanıcı ismi görüntüleme yetkisini tanımlar.
            if user:
                user_id, role = user
                current_user = User(user_id, username, role)
                user_menu(current_user)
            else:
                print("Geçersiz kullanıcı adı veya şifre")

        # Eğer 2 yani kayıt seçeneği seçilirse girilmesi gereken bilgileri temsil eden koddur ve sadece kullanıcı için geçerlidir. Admin hesabı için geçerli değildir..
        elif choice == '2':
            new_username = input("Yeni Kullanıcı Adı: ")
            if  username_exists(new_username):
                print("Bu kullanıcı adına ait hesap var, lütfen farklı bir kullanıcı adı deneyin.")
            else:
                new_password = input("Yeni Şifre: ")
                role = 'user'
                add_user(new_username, new_password, role)
                print(f"Kullanıcı {new_username} başarıyla oluşturuldu.")

        # Eğer 3 yani çıkış seçeneği seçilirse programı durduran koddur.
        elif choice == '3':
            break
        # Verilen seçenekler dışında bir şey seçilirse hatalı olduğunu tanımlar.
        else:
            print("Geçersiz seçim. Tekrar deneyin.")

# Giriş yaptıktan sonra kullanıcının yapabileceği seçenekleri temsil eden koddur.
def user_menu(current_user):
    while True:
        print("\n1. Ürün Ekle")
        print("2. Ürün Kaldır")
        print("3. İşlem Kayıtlarımı Görüntüle")
        # Eğer admin hesabına giriş yaparsanız kullanıcı seçenekleri dışında yeni yetkileri tanımlamak için kullanılan koddur.
        if current_user.role == 'admin':
            print("4. Kullanıcı Raporu Oluştur")
            print("5. Kullanıcı Sil")
            print("6. CSV Dosya Adı: ")
        print("7. Çıkış")
        choice = input("Seçiminiz: ")

        # Eğer 1 yani ürün ekle seçeneği seçilirse ürün adı ve fiyatı yazılan kısma yönlendiren kısımdır.
        if choice == '1':
            name = input("Ürün Adı: ")
            price = float(input("Ürün Fiyatı: "))
            current_user.add_product(name, price)
            print(f"{name} ürünü eklendi.")

        # Eğer 2 yani ürün kaldır seçeneği seçilirse kaldırılacak ürünün seçilmesini sağlayan kısımdır.
        elif choice == '2':
            product_id = int(input("Silinecek Ürün ID: "))
            if current_user.delete_product(product_id):
                print(f"Ürün ID {product_id} kaldırıldı.")
            else:
                print(f"Ürün ID {product_id} olan bir ürün bulunamadı.")

         # Eğer 3 yani log kayıtlarını görüntüleme seçeneği seçilirse kullanıcının kendi log kayıtlarını gösterir.
        elif choice == '3':
            logs = current_user.get_own_logs()
            for log in logs:
                print(log)

        # Eğer 3 yani rapor oluşturma seçeneği seçilirse kullanıcının IDsini isteyen koddur.Bunu sadece admin rolü için görülür.
        elif choice == '4' and current_user.role == 'admin':
            target_user_id = int(input("Rapor Alınacak Kullanıcı ID: "))
            logs = current_user.generate_report(target_user_id)
            for log in logs:
                print(log)

        # Eğer 4 yani kullanıcı silme seçeneği seçilirse kullanıcı ID ile silinmesini sağlar.
        elif choice == '5' and current_user.role == 'admin':
            user_id_to_delete = int(input("Silinecek Kullanıcı ID: "))
            if current_user.delete_user(user_id_to_delete):
                print(f"Kullanıcı ID {user_id_to_delete} başarıyla silindi.")
            else:
                print(f"Kullanıcı ID {user_id_to_delete} bulunamadı.")
                
        # Eğer en son bütün işlemler bitince log kaydı alınmak istenirse bu kod kullanılır. Admine özeldir.
        elif choice == '6' and current_user.role == 'admin':
            csv_filename = input("CSV Dosya Adı: ")
            export_logs_to_csv(csv_filename)
            print(f"Loglar {csv_filename} dosyasına aktarıldı.")

        # Eğer 6 yani çıkış seçeneği seçilirse giriş ekranına yönlendirir.
        elif choice == '7':
            break
        # Verilen seçenekler dışında bir girdi girilirse geçersiz sayılır.
        else:
            print("Geçersiz seçim. Tekrar deneyin.")

# Kod çalıştığında 'main()' fonksiyonunu çağırır.
if __name__ == "__main__":
    main()
