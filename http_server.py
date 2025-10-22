try:
    from flask import Flask, request, jsonify
    USE_FLASK = True
except ImportError:
    USE_FLASK = False
    Flask = None
    request = None
    jsonify = None

import io

if USE_FLASK:
    app = Flask(__name__)

    @app.route('/voices', methods=['GET'])
    def get_voices():
        from voice import list_voices
        voices = list_voices()
        return jsonify([{'name': v.name, 'gender': v.gender, 'locale': v.locale} for v in voices])

    @app.route('/synth', methods=['POST'])
    def synth():
        from cli import run_cli
        data = request.json
        text = data.get('text', '')
        voice = data.get('voice', 'narrator')
        # Run synth
        args = ['synth', '--text', text, '--voice', voice, '--out', '/tmp/temp.mp3']
        run_cli(args)
        # Read file and return
        with open('/tmp/temp.mp3', 'rb') as f:
            mp3_data = f.read()
        return mp3_data, 200, {'Content-Type': 'audio/mpeg'}

    @app.route('/status', methods=['GET'])
    def status():
        return jsonify({'status': 'running'})

def start_http_server(port=8080):
    if USE_FLASK:
        app.run(host='0.0.0.0', port=port)
    else:
        print("Flask not available, cannot start HTTP server")