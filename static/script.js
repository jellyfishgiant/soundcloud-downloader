document.getElementById('downloadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const statusDiv = document.getElementById('status');
    const url = document.getElementById('soundcloudUrl').value;
    
    if (!url) {
        statusDiv.textContent = 'Please enter a SoundCloud URL';
        return;
    }
    
    statusDiv.textContent = 'Downloading...';
    
    try {
        // Using URLSearchParams for simpler data formatting
        const data = new URLSearchParams();
        data.append('url', url);
        
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: data
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || 'Download failed');
        }
        
        const blob = await response.blob();
        
        // Create and trigger download
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = 'soundcloud_track.mp3';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(downloadUrl);
        
        statusDiv.textContent = 'Download complete!';
    } catch (error) {
        console.error('Error details:', error);
        statusDiv.textContent = 'Error: ' + error.message;
    }
});