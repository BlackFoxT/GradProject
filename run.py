from app import app, db
import os

if __name__ == "__main__":
    # Uygulama ortamını ayarla
    env = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(f'config.{env.capitalize()}Config')

    # Veritabanını oluştur
    with app.app_context():
        db.create_all()

    # Sunucuyu başlat
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
