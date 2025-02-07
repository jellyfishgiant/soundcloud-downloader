from flask import Flask, render_template, request, send_file, jsonify
import os
import tempfile
import subprocess
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        if not request.form.get('url'):
            return jsonify({'error': 'No URL provided'}), 400

        soundcloud_url = request.form['url']
        print(f"Received URL: {soundcloud_url}")  # Debug print
        
        # Create a temporary directory to store the download
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"Created temp directory: {temp_dir}")  # Debug print
            
            # Use subprocess to call scdl command line tool
            try:
                result = subprocess.run([
                    'scdl',
                    '-l', soundcloud_url,
                    '--path', temp_dir,
                    '--onlymp3'
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"SCDL Error: {result.stderr}")
                    return jsonify({'error': f'Download failed: {result.stderr}'}), 500
                
            except Exception as e:
                print(f"Download error: {str(e)}")
                return jsonify({'error': f'Download failed: {str(e)}'}), 500
            
            print(f"Files in directory: {os.listdir(temp_dir)}")  # Debug print
            
            # Find the downloaded file
            downloaded_files = [f for f in os.listdir(temp_dir) if f.endswith('.mp3')]
            if not downloaded_files:
                return jsonify({'error': 'No MP3 file was downloaded'}), 400
                
            downloaded_file = downloaded_files[0]
            file_path = os.path.join(temp_dir, downloaded_file)
            
            print(f"Sending file: {downloaded_file}")  # Debug print
            
            try:
                return send_file(
                    file_path,
                    as_attachment=True,
                    download_name=downloaded_file,
                    mimetype='audio/mpeg'
                )
            except Exception as e:
                print(f"Send file error: {str(e)}")
                return jsonify({'error': f'Failed to send file: {str(e)}'}), 500
            
    except Exception as e:
        print(f"General error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

if __name__ == '__main__':
    app.run(debug=True)