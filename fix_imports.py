import os

def create_init_files():
    # Projedeki tüm klasörleri tara
    for root, dirs, files in os.walk("."):
        # 'logs', 'docker', 'tests', '__pycache__' gibi klasörleri atla
        if any(x in root for x in ["logs", "docker", "tests", "__pycache__"]):
            continue
            
        for d in dirs:
            # Her klasörün içine __init__.py ekle
            init_path = os.path.join(root, d, "__init__.py")
            if not os.path.exists(init_path):
                with open(init_path, 'w') as f:
                    pass # Boş dosya oluştur
                print(f"✅ Oluşturuldu: {init_path}")

if __name__ == "__main__":
    print("Sistem paketleri taranıyor ve __init__.py dosyaları ekleniyor...")
    create_init_files()
    print("\n🚀 İşlem tamamlandı! Şimdi tekrar 'python -m app.main' deneyebilirsin.")
