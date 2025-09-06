// Orato AI Application
class OratoApp {
    constructor() {
        this.currentTab = 'stt';
        this.audioContext = null;
        this.audioSource = null;
        this.currentAudio = null;
        this.isPlaying = false;
        
        this.init();
    }

    init() {
        console.log('Initializing OratoApp...');
        this.setupEventListeners();
        this.setupProviderSwitching();
        this.setupFileUploads();
        this.setupAudioPlayer();
        console.log('OratoApp initialized successfully');
    }

    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = e.currentTarget.dataset.tab;
                this.switchTab(tab);
            });
        });

        // TTS functionality
        const ttsGenerateBtn = document.getElementById('tts-generate');
        if (ttsGenerateBtn) {
            ttsGenerateBtn.addEventListener('click', () => {
                this.processTTS();
            });
        } else {
            console.error('TTS generate button not found');
        }

        // STT functionality
        const sttProcessBtn = document.getElementById('stt-process');
        if (sttProcessBtn) {
            sttProcessBtn.addEventListener('click', () => {
                this.processSTT();
            });
        } else {
            console.error('STT process button not found');
        }

        // Batch functionality
        const batchProcessBtn = document.getElementById('batch-process');
        if (batchProcessBtn) {
            batchProcessBtn.addEventListener('click', () => {
                this.processBatch();
            });
        } else {
            console.error('Batch process button not found');
        }

        // Audio player
        document.getElementById('play-btn').addEventListener('click', () => {
            this.toggleAudioPlayback();
        });

        // Progress bar
        document.querySelector('.progress-bar').addEventListener('click', (e) => {
            this.seekAudio(e);
        });
    }

    setupProviderSwitching() {
        // TTS Provider switching
        document.querySelectorAll('input[name="tts-provider"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.toggleProviderFields('tts', e.target.value);
            });
        });

        // Batch Provider switching
        document.querySelectorAll('input[name="batch-provider"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.toggleProviderFields('batch', e.target.value);
            });
        });

        // Batch Type switching
        document.querySelectorAll('input[name="batch-type"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.toggleBatchType(e.target.value);
            });
        });
    }

    setupFileUploads() {
        console.log('Setting up file uploads...');
        
        // STT file upload
        const sttUploadArea = document.getElementById('stt-upload-area');
        const sttFileInput = document.getElementById('stt-file');
        
        console.log('STT Upload Elements:', {
            sttUploadArea: sttUploadArea,
            sttFileInput: sttFileInput
        });
        
        if (!sttUploadArea || !sttFileInput) {
            console.error('STT upload elements not found - retrying in 500ms');
            setTimeout(() => this.setupFileUploads(), 500);
            return;
        }
        
        console.log('STT upload elements found - setting up event listeners');
        
        sttUploadArea.addEventListener('click', () => {
            console.log('STT upload area clicked');
            sttFileInput.click();
        });

        sttFileInput.addEventListener('change', (e) => {
            console.log('STT file input changed:', e.target.files);
            if (e.target.files && e.target.files.length > 0) {
                this.updateUploadArea(sttUploadArea, e.target.files[0].name);
                const processBtn = document.getElementById('stt-process');
                if (processBtn) {
                    processBtn.disabled = false;
                }
            }
        });

        // Batch file upload
        const batchUploadArea = document.getElementById('batch-upload-area');
        const batchFileInput = document.getElementById('batch-file');
        
        if (!batchUploadArea || !batchFileInput) {
            console.error('Batch upload elements not found - retrying in 500ms');
            setTimeout(() => this.setupFileUploads(), 500);
            return;
        }
        
        batchUploadArea.addEventListener('click', () => {
            batchFileInput.click();
        });

        batchFileInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files.length > 0) {
                this.updateUploadArea(batchUploadArea, e.target.files[0].name);
                const processBtn = document.getElementById('batch-process');
                if (processBtn) {
                    processBtn.disabled = false;
                }
            }
        });
    }

    setupAudioPlayer() {
        // Initialize audio context when needed
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');

        this.currentTab = tabName;
    }

    toggleProviderFields(type, provider) {
        const azureFields = document.querySelectorAll(`.${type} .azure-only`);
        const elevenlabsFields = document.querySelectorAll(`.${type} .elevenlabs-only`);

        if (provider === 'azure') {
            azureFields.forEach(field => field.style.display = 'block');
            elevenlabsFields.forEach(field => field.style.display = 'none');
        } else {
            azureFields.forEach(field => field.style.display = 'none');
            elevenlabsFields.forEach(field => field.style.display = 'block');
        }
    }

    toggleBatchType(type) {
        const voiceField = document.querySelector('#batch-voice').parentElement;
        if (type === 'tts') {
            voiceField.style.display = 'block';
        } else {
            voiceField.style.display = 'none';
        }
    }

    updateUploadArea(area, fileName) {
        const content = area.querySelector('.upload-content');
        content.innerHTML = `
            <i class="fas fa-check-circle" style="color: #4ecdc4;"></i>
            <h3>File Selected</h3>
            <p>${fileName}</p>
        `;
    }

    async processTTS() {
        const text = document.getElementById('tts-text').value;
        const language = document.getElementById('tts-language').value;
        const voice = document.getElementById('tts-voice').value;
        const provider = document.querySelector('input[name="tts-provider"]:checked').value;
        const apiKey = provider === 'azure' ? 
            document.getElementById('tts-api-key').value : 
            document.getElementById('tts-elevenlabs-key').value;
        const region = document.getElementById('tts-region').value;

        if (!text || !apiKey) {
            alert('Please fill in all required fields');
            return;
        }

        const button = document.getElementById('tts-generate');
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        button.disabled = true;

        try {
            const response = await fetch('/api/tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text,
                    language,
                    voice_name: voice,
                    provider,
                    api_key: apiKey,
                    region
                })
            });

            const result = await response.json();

            if (result.success) {
                this.showTTSResult(result.download_url);
            } else {
                alert('Error: ' + (result.error || 'TTS generation failed'));
            }
        } catch (error) {
            console.error('TTS Error:', error);
            alert('Network error: ' + error.message);
        } finally {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }

    async processSTT() {
        console.log('=== PROCESSING STT ===');
        
        // Try multiple ways to find the file input
        let fileInput = document.getElementById('stt-file');
        if (!fileInput) {
            fileInput = document.querySelector('#stt-file');
        }
        if (!fileInput) {
            fileInput = document.querySelector('input[type="file"][id="stt-file"]');
        }
        
        const language = document.getElementById('stt-language').value;
        const apiKey = document.getElementById('stt-api-key').value;
        const region = document.getElementById('stt-region').value;

        console.log('STT Elements Debug:', {
            fileInput: fileInput,
            fileInputType: fileInput ? fileInput.type : 'not found',
            fileInputId: fileInput ? fileInput.id : 'not found',
            language: language,
            apiKey: apiKey ? 'present' : 'missing',
            region: region
        });

        if (!fileInput) {
            console.error('File input element not found with any method');
            alert('File input not found. Please refresh the page.');
            return;
        }

        console.log('File input found:', {
            files: fileInput.files,
            filesLength: fileInput.files ? fileInput.files.length : 'no files',
            fileInputValue: fileInput.value
        });

        if (!fileInput.files || fileInput.files.length === 0) {
            alert('Please select an audio file first');
            return;
        }

        if (!apiKey) {
            alert('Please enter your Azure API key');
            return;
        }

        const button = document.getElementById('stt-process');
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        button.disabled = true;

        try {
            const formData = new FormData();
            formData.append('audio', fileInput.files[0]);
            formData.append('language', language);
            formData.append('api_key', apiKey);
            formData.append('region', region);

            const response = await fetch('/api/stt', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.showSTTResult(result.text);
            } else {
                alert('Error: ' + (result.error || 'STT processing failed'));
            }
        } catch (error) {
            console.error('STT Error:', error);
            alert('Network error: ' + error.message);
        } finally {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }

    async processBatch() {
        const fileInput = document.getElementById('batch-file');
        const language = document.getElementById('batch-language').value;
        const voice = document.getElementById('batch-voice').value;
        const type = document.querySelector('input[name="batch-type"]:checked').value;
        const provider = document.querySelector('input[name="batch-provider"]:checked').value;
        const apiKey = provider === 'azure' ? 
            document.getElementById('batch-api-key').value : 
            document.getElementById('batch-elevenlabs-key').value;
        const region = document.getElementById('batch-region').value;

        if (!fileInput.files || fileInput.files.length === 0) {
            alert('Please select a JSON file first');
            return;
        }

        if (!apiKey) {
            alert('Please enter your API key');
            return;
        }

        const button = document.getElementById('batch-process');
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        button.disabled = true;

        try {
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            formData.append('language', language);
            formData.append('voice', voice);
            formData.append('type', type);
            formData.append('provider', provider);
            formData.append('api_key', apiKey);
            formData.append('region', region);

            const response = await fetch('/api/batch', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.showBatchResult(result);
            } else {
                alert('Error: ' + (result.error || 'Batch processing failed'));
            }
        } catch (error) {
            console.error('Batch Error:', error);
            alert('Network error: ' + error.message);
        } finally {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }

    showTTSResult(downloadUrl) {
        const resultArea = document.getElementById('tts-result');
        const downloadLink = document.getElementById('download-link');
        
        downloadLink.href = downloadUrl;
        resultArea.style.display = 'block';
        resultArea.scrollIntoView({ behavior: 'smooth' });

        // Load audio for playback
        this.loadAudio(downloadUrl);
    }

    showSTTResult(text) {
        const resultArea = document.getElementById('stt-result');
        const textElement = document.getElementById('stt-text');
        
        textElement.textContent = text;
        resultArea.style.display = 'block';
        resultArea.scrollIntoView({ behavior: 'smooth' });
    }

    showBatchResult(result) {
        const resultArea = document.getElementById('batch-result');
        const messageElement = document.getElementById('batch-message');
        const downloadLink = document.getElementById('batch-download');
        
        messageElement.textContent = result.message;
        downloadLink.href = result.download_url;
        resultArea.style.display = 'block';
        resultArea.scrollIntoView({ behavior: 'smooth' });
    }

    async loadAudio(url) {
        try {
            const response = await fetch(url);
            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);
            
            this.currentAudio = new Audio(audioUrl);
            this.currentAudio.addEventListener('loadedmetadata', () => {
                this.updateTimeDisplay();
                this.initializeWaveform();
            });
            this.currentAudio.addEventListener('timeupdate', () => {
                this.updateProgress();
                this.updateWaveformIntensity();
            });
            this.currentAudio.addEventListener('ended', () => {
                this.isPlaying = false;
                this.pauseWaveform();
                this.updatePlayButton();
            });
        } catch (error) {
            console.error('Error loading audio:', error);
        }
    }

    initializeWaveform() {
        const waveBars = document.querySelectorAll('.wave-bar');
        waveBars.forEach((bar, index) => {
            // Set random initial heights for more realistic look
            const randomHeight = Math.random() * 30 + 20;
            bar.style.height = randomHeight + 'px';
        });
    }

    updateWaveformIntensity() {
        if (!this.isPlaying) return;
        
        const waveBars = document.querySelectorAll('.wave-bar');
        const progress = this.currentAudio.currentTime / this.currentAudio.duration;
        
        waveBars.forEach((bar, index) => {
            // Create simple movement based on audio progress
            const intensity = Math.sin(progress * Math.PI * 4 + index * 0.5) * 0.5 + 0.5;
            const height = 20 + (intensity * 40);
            bar.style.height = height + 'px';
        });
    }

    toggleAudioPlayback() {
        if (!this.currentAudio) return;

        if (this.isPlaying) {
            this.currentAudio.pause();
            this.pauseWaveform();
        } else {
            this.currentAudio.play();
            this.playWaveform();
        }
        
        this.isPlaying = !this.isPlaying;
        this.updatePlayButton();
    }

    playWaveform() {
        const waveform = document.getElementById('waveform');
        if (waveform) {
            waveform.classList.remove('paused');
            waveform.classList.add('playing');
        }
    }

    pauseWaveform() {
        const waveform = document.getElementById('waveform');
        if (waveform) {
            waveform.classList.remove('playing');
            waveform.classList.add('paused');
        }
    }

    updatePlayButton() {
        const playBtn = document.getElementById('play-btn');
        const icon = playBtn.querySelector('i');
        
        if (this.isPlaying) {
            icon.className = 'fas fa-pause';
        } else {
            icon.className = 'fas fa-play';
        }
    }

    updateProgress() {
        if (!this.currentAudio) return;

        const progress = document.getElementById('progress');
        const time = document.getElementById('time');
        
        const currentTime = this.currentAudio.currentTime;
        const duration = this.currentAudio.duration;
        
        if (duration) {
            const progressPercent = (currentTime / duration) * 100;
            progress.style.width = progressPercent + '%';
            
            time.textContent = `${this.formatTime(currentTime)} / ${this.formatTime(duration)}`;
        }
    }

    updateTimeDisplay() {
        if (!this.currentAudio) return;

        const time = document.getElementById('time');
        const duration = this.currentAudio.duration;
        
        if (duration) {
            time.textContent = `0:00 / ${this.formatTime(duration)}`;
        }
    }

    seekAudio(e) {
        if (!this.currentAudio) return;

        const progressBar = e.currentTarget;
        const rect = progressBar.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const width = rect.width;
        const seekTime = (clickX / width) * this.currentAudio.duration;
        
        this.currentAudio.currentTime = seekTime;
    }

    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded - Initializing OratoApp');
    
    // Add a small delay to ensure all elements are rendered
    setTimeout(() => {
        // Debug: Check if STT elements exist
        const sttFile = document.getElementById('stt-file');
        const sttUploadArea = document.getElementById('stt-upload-area');
        const sttProcessBtn = document.getElementById('stt-process');
        
        console.log('STT Elements Check (after delay):', {
            sttFile: sttFile ? 'Found' : 'Not Found',
            sttUploadArea: sttUploadArea ? 'Found' : 'Not Found', 
            sttProcessBtn: sttProcessBtn ? 'Found' : 'Not Found'
        });
        
        new OratoApp();
    }, 100);
});
