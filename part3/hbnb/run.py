import os
from app import create_app

# Obtiene la configuración desde la variable de entorno (por defecto, usa 'development')
config_name = os.getenv('FLASK_ENV', 'default')

app = create_app(config_name)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
