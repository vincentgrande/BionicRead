from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import configparser
from epubToBionic import create_bionic_epub

# Lire la clé API à partir du fichier de configuration
config = configparser.ConfigParser()
config.read('config.ini')
API_KEY = config['security']['api_key']


# Dossier où les fichiers téléchargés seront stockés temporairement
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app = Flask(__name__)
CORS(app)

# Route racine de l'API
@app.route('/')
def home():
    return "Bienvenue à l'API Flask!"


# Route pour transformer un fichier EPUB en lecture Bionic
@app.route('/epub-to-bionic', methods=['POST'])
def post_data():
    #Vérification de la clé API dans les en-têtes de la requête
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized access"}), 401

    if 'file' not in request.files:
        return {"error": "Aucun fichier trouvé dans la requête."}, 400
    
    file = request.files['file']
    
    if file.filename == '':
        return {"error": "Aucun fichier sélectionné."}, 400

    if not file.filename.endswith('.epub'):
        return {"error": "Le fichier n'est pas un EPUB."}, 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(UPLOAD_FOLDER, "Bionic - "+file.filename)

    file.save(input_path)
    
    create_bionic_epub(input_path, output_path)
    
    response = send_file(output_path, as_attachment=True)
    
    # Vider le dossier uploads après l'envoi du fichier
    clear_upload_folder(UPLOAD_FOLDER) 

    return response

# Fonction pour vider le dossier uploads
def clear_upload_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005,debug=True)
