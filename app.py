from flask import Flask, render_template, request, send_file, jsonify
import os
import tempfile
import subprocess
from pathlib import Path

app = Flask(__name__)

# Get the Downloads folder path
DOWNLOADS_FOLDER = str(Path.home() / "Downloads")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        if not request.form.get('url'):
            return jsonify({'error': 'No URL provided'}), 400

        soundcloud_url = request.form['url']
        print(f"Received URL: {soundcloud_url}")
        
        # Create a temporary directory for intermediate files
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"Created temp directory: {temp_dir}")
            
            # Step 1: Download MP3 using scdl
            try:
                print("Downloading MP3...")
                mp3_result = subprocess.run([
                    'scdl',
                    '-l', soundcloud_url,
                    '--path', temp_dir,
                    '--onlymp3',
                    '--addtofile'
                ], capture_output=True, text=True)
                
                print("MP3 Download Output:", mp3_result.stdout)
                if mp3_result.returncode != 0:
                    return jsonify({'error': f'MP3 download failed: {mp3_result.stderr}'}), 500
                
                # Step 2: Find the downloaded MP3
                mp3_files = [f for f in os.listdir(temp_dir) if f.endswith('.mp3')]
                if not mp3_files:
                    return jsonify({'error': 'No MP3 file was downloaded'}), 400
                
                mp3_path = os.path.join(temp_dir, mp3_files[0])
                temp_artwork_path = os.path.join(temp_dir, 'artwork.jpg')
                final_mp4_path = os.path.join(DOWNLOADS_FOLDER, os.path.splitext(mp3_files[0])[0] + '.mp4')
                
                # Step 3: Extract artwork from MP3 metadata
                print("Extracting artwork...")
                extract_cmd = [
                    'ffmpeg',
                    '-i', mp3_path,
                    '-an',
                    '-vcodec', 'copy',
                    '-y',
                    temp_artwork_path
                ]
                
                subprocess.run(extract_cmd, capture_output=True, check=True)
                
                # If no artwork found, create black image
                if not os.path.exists(temp_artwork_path):
                    print("No artwork found, creating black background...")
                    subprocess.run([
                        'ffmpeg',
                        '-f', 'lavfi',
                        '-i', 'color=c=black:s=1920x1080',
                        '-frames:v', '1',
                        '-y',
                        temp_artwork_path
                    ], check=True, capture_output=True)
                
                # Step 4: Generate MP4
                print("Converting to MP4...")
                ffmpeg_cmd = [
                    'ffmpeg',
                    '-loop', '1',  # Loop the image
                    '-i', temp_artwork_path,  # Image input
                    '-i', mp3_path,  # Audio input
                    '-c:v', 'libx264',  # Video codec
                    '-tune', 'stillimage',  # Optimize for still image
                    '-c:a', 'aac',  # Audio codec
                    '-b:a', '192k',  # Audio bitrate
                    '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
                    '-vf', 'scale=-1:1080,pad=1920:1080:(1920-iw)/2:0:black',  # Scale and center
                    '-shortest',  # Match video length to audio length
                    '-y',  # Overwrite output
                    final_mp4_path
                ]
                
                result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
                print("FFmpeg Output:", result.stdout)
                print("FFmpeg Error:", result.stderr)
                
                if result.returncode != 0:
                    return jsonify({'error': 'MP4 conversion failed'}), 500
                
                # Step 5: Verify and return the final MP4
                if not os.path.exists(final_mp4_path):
                    return jsonify({'error': 'MP4 file was not created'}), 500
                
                print(f"Successfully created MP4: {final_mp4_path}")
                return jsonify({'success': 'MP4 file created successfully'})
                
            except subprocess.CalledProcessError as e:
                print(f"Process error: {e.stderr}")
                return jsonify({'error': f'Process failed: {str(e)}'}), 500
            except Exception as e:
                print(f"Error: {str(e)}")
                return jsonify({'error': str(e)}), 500
            
    except Exception as e:
        print(f"General error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)