from flask import Flask, render_template, jsonify, request
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

IMAGGA_API_KEY = os.environ.get('IMAGGA_API_KEY', 'acc_a8fb70652b8aeb8')
IMAGGA_API_SECRET = os.environ.get('IMAGGA_API_SECRET', '5b8d87121d05a5b67830c1afddb409ff')
IMAGGA_API_URL = 'https://api.imagga.com/v2/tags'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_images():
    data = request.get_json()
    image_urls = data.get('image_urls', [])

    if not image_urls or len(image_urls) != 3:
        return jsonify({
            'success': False,
            'error': 'Debes proporcionar exactamente 3 URLs de imágenes.'
        }), 400

    results = []

    for image_url in image_urls:
        try:
            response = requests.get(
                IMAGGA_API_URL,
                auth=(IMAGGA_API_KEY, IMAGGA_API_SECRET),
                params={'image_url': image_url, 'language': 'es'}
            )

            if response.status_code == 200:
                api_data = response.json()
                tags = api_data.get('result', {}).get('tags', [])
                top_tags = sorted(tags, key=lambda x: x['confidence'], reverse=True)[:5]

                result = {
                    'image_url': image_url,
                    'image_name': os.path.basename(image_url),
                    'tags': [
                        {
                            'name': tag['tag']['es'],
                            'confidence': round(tag['confidence'], 2)
                        }
                        for tag in top_tags
                    ],
                    'success': True
                }
            else:
                result = {
                    'image_url': image_url,
                    'image_name': os.path.basename(image_url),
                    'error': f'Error en la API de Imagga: {response.status_code}',
                    'success': False
                }
            results.append(result)

        except requests.exceptions.RequestException as e:
            results.append({
                'image_url': image_url,
                'image_name': os.path.basename(image_url),
                'error': f'Error de conexión: {str(e)}',
                'success': False
            })
        except Exception as e:
            results.append({
                'image_url': image_url,
                'image_name': os.path.basename(image_url),
                'error': f'Ocurrió un error inesperado: {str(e)}',
                'success': False
            })

    return jsonify({
        'success': True,
        'results': results
    })

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)