// Orato AI Single Page Application
class OratoApp {
    constructor() {
        this.currentTab = 'home';
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

        // Feature card clicks on home tab
        document.querySelectorAll('.feature-card').forEach(card => {
            card.addEventListener('click', (e) => {
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
        }

        // STT functionality
        const sttProcessBtn = document.getElementById('stt-process');
        if (sttProcessBtn) {
            sttProcessBtn.addEventListener('click', () => {
                this.processSTT();
            });
        }

        // Batch functionality
        const batchProcessBtn = document.getElementById('batch-process');
        if (batchProcessBtn) {
            batchProcessBtn.addEventListener('click', () => {
                this.processBatch();
            });
        }

        // Audio player
        const playBtn = document.getElementById('play-btn');
        if (playBtn) {
            playBtn.addEventListener('click', () => {
                this.toggleAudioPlayback();
            });
        }

        // Progress bar
        const progressBar = document.getElementById('progress-bar');
        if (progressBar) {
            progressBar.addEventListener('click', (e) => {
                this.seekAudio(e);
            });
        }

        // Download button
        const downloadBtn = document.getElementById('download-btn');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => {
                this.downloadAudio();
            });
        }

        // Batch download button
        const batchDownloadBtn = document.getElementById('batch-download');
        if (batchDownloadBtn) {
            batchDownloadBtn.addEventListener('click', () => {
                this.downloadBatch();
            });
        }
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
        
        if (sttUploadArea && sttFileInput) {
            sttUploadArea.addEventListener('click', () => {
                sttFileInput.click();
            });

            sttFileInput.addEventListener('change', (e) => {
                if (e.target.files && e.target.files.length > 0) {
                    this.updateUploadArea(sttUploadArea, e.target.files[0].name);
                    const processBtn = document.getElementById('stt-process');
                    if (processBtn) {
                        processBtn.disabled = false;
                    }
                }
            });
        }

        // Batch file upload
        const batchUploadArea = document.getElementById('batch-upload-area');
        const batchFileInput = document.getElementById('batch-file');
        
        if (batchUploadArea && batchFileInput) {
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
    }

    setupAudioPlayer() {
        // Initialize audio context when needed
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    }

    switchTab(tabName) {
        console.log('Switching to tab:', tabName);
        
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        const activeBtn = document.querySelector(`[data-tab="${tabName}"]`);
        if (activeBtn) {
            activeBtn.classList.add('active');
        }

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        const activeContent = document.getElementById(`${tabName}-tab`);
        if (activeContent) {
            activeContent.classList.add('active');
        }

        this.currentTab = tabName;
    }

    toggleProviderFields(type, provider) {
        const azureFields = document.querySelectorAll(`#${type}-tab .azure-only`);
        const elevenlabsFields = document.querySelectorAll(`#${type}-tab .elevenlabs-only`);

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
        if (content) {
            content.innerHTML = `
                <i class="fas fa-check-circle" style="color: #4ecdc4;"></i>
                <h3>File Selected</h3>
                <p>${fileName}</p>
            `;
        }
    }

    async processTTS() {
        const text = document.getElementById('tts-text').value;
        const language = document.getElementById('tts-language').value;
        const provider = document.querySelector('input[name="tts-provider"]:checked').value;
        
        if (!text.trim()) {
            alert('Please enter text to convert');
            return;
        }

        let apiKey, region, voice, elevenlabsVoice;
        
        if (provider === 'azure') {
            voice = document.getElementById('tts-voice').value;
            apiKey = document.getElementById('tts-api-key').value;
            region = document.getElementById('tts-region').value;
            
            if (!voice) {
                alert('Please enter a voice name for Azure');
                return;
            }
            if (!apiKey) {
                alert('Please enter your Azure API key');
                return;
            }
        } else {
            apiKey = document.getElementById('tts-elevenlabs-key').value;
            elevenlabsVoice = document.getElementById('tts-elevenlabs-voice').value;
            
            if (!apiKey) {
                alert('Please enter your ElevenLabs API key');
                return;
            }
            if (!elevenlabsVoice) {
                alert('Please enter ElevenLabs Voice ID');
                return;
            }
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
                    text: text,
                    language: language,
                    voice_name: provider === 'azure' ? voice : undefined,
                    provider: provider,
                    api_key: apiKey,
                    region: provider === 'azure' ? region : undefined,
                    elevenlabs_voice: provider === 'elevenlabs' ? elevenlabsVoice : undefined
                })
            });

            const result = await response.json();
            
            if (result.success) {
                this.loadAudio(result.download_url);
                document.getElementById('tts-result').style.display = 'block';
            } else {
                alert('Error: ' + (result.error || 'Unknown error occurred'));
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Error generating speech: ' + error.message);
        } finally {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }

    async processSTT() {
        const fileInput = document.getElementById('stt-file');
        const language = document.getElementById('stt-language').value;
        const apiKey = document.getElementById('stt-api-key').value;
        const region = document.getElementById('stt-region').value;

        if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
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
                document.getElementById('stt-text').textContent = result.text;
                document.getElementById('stt-result').style.display = 'block';
            } else {
                alert('Error: ' + (result.error || 'Unknown error occurred'));
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Error processing audio: ' + error.message);
        } finally {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }

    async processBatch() {
        const fileInput = document.getElementById('batch-file');
        const language = document.getElementById('batch-language').value;
        const provider = document.querySelector('input[name="batch-provider"]:checked').value;
        const batchType = document.querySelector('input[name="batch-type"]:checked').value;
        
        if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
            alert('Please select a JSON file first');
            return;
        }

        let apiKey, region, voice, elevenlabsVoice;
        
        if (provider === 'azure') {
            voice = document.getElementById('batch-voice').value;
            apiKey = document.getElementById('batch-api-key').value;
            region = document.getElementById('batch-region').value;
            
            if (!voice) {
                alert('Please enter a voice name for Azure');
                return;
            }
            if (!apiKey) {
                alert('Please enter your Azure API key');
                return;
            }
        } else {
            apiKey = document.getElementById('batch-elevenlabs-key').value;
            elevenlabsVoice = document.getElementById('batch-elevenlabs-voice').value;
            
            if (!apiKey) {
                alert('Please enter your ElevenLabs API key');
                return;
            }
            if (!elevenlabsVoice) {
                alert('Please enter ElevenLabs Voice ID');
                return;
            }
        }

        const button = document.getElementById('batch-process');
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        button.disabled = true;

        try {
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            formData.append('language', language);
            if (provider === 'azure') {
                formData.append('voice', voice);
                formData.append('region', region);
            }
            formData.append('provider', provider);
            formData.append('api_key', apiKey);
            if (provider === 'elevenlabs') {
                formData.append('elevenlabs_voice', elevenlabsVoice);
            }
            formData.append('batch_type', batchType);

            const response = await fetch('/api/batch', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.success) {
                document.getElementById('batch-text').textContent = result.message;
                document.getElementById('batch-result').style.display = 'block';
                
                // Show download link for ZIP file
                const downloadLink = document.getElementById('batch-download-link');
                downloadLink.href = result.download_url;
                downloadLink.style.display = 'block';
            } else {
                alert('Error: ' + (result.error || 'Unknown error occurred'));
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Error processing batch: ' + error.message);
        } finally {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }

    loadAudio(url) {
        console.log('Loading audio from URL:', url);
        
        if (this.currentAudio) {
            this.currentAudio.pause();
        }
        
        this.currentAudio = new Audio(url);
        
        this.currentAudio.addEventListener('loadedmetadata', () => {
            console.log('Audio metadata loaded');
            this.initializeWaveform();
            this.updateProgress();
        });
        
        this.currentAudio.addEventListener('timeupdate', () => {
            this.updateProgress();
            this.updateWaveformIntensity();
        });
        
        this.currentAudio.addEventListener('ended', () => {
            console.log('Audio ended');
            this.isPlaying = false;
            this.updatePlayButton();
            this.pauseWaveform();
        });
        
        this.currentAudio.addEventListener('error', (e) => {
            console.error('Audio loading error:', e);
            alert('Error loading audio: ' + e.message);
        });
    }

    initializeWaveform() {
        const bars = document.querySelectorAll('.wave-bar');
        bars.forEach(bar => {
            const height = Math.random() * 60 + 20;
            bar.style.height = height + '%';
        });
    }

    updateWaveformIntensity() {
        if (!this.currentAudio) return;
        
        const bars = document.querySelectorAll('.wave-bar');
        const progress = this.currentAudio.currentTime / this.currentAudio.duration;
        
        bars.forEach((bar, index) => {
            const intensity = Math.sin((progress * Math.PI * 2) + (index * 0.3)) * 0.5 + 0.5;
            const height = 20 + (intensity * 60);
            bar.style.height = height + '%';
        });
    }

    playWaveform() {
        const bars = document.querySelectorAll('.wave-bar');
        bars.forEach(bar => {
            bar.style.animation = 'wavePulse 0.5s ease-in-out infinite alternate';
        });
    }

    pauseWaveform() {
        const bars = document.querySelectorAll('.wave-bar');
        bars.forEach(bar => {
            bar.style.animation = 'none';
        });
    }

    toggleAudioPlayback() {
        if (!this.currentAudio) return;
        
        if (this.isPlaying) {
            this.currentAudio.pause();
            this.isPlaying = false;
            this.pauseWaveform();
        } else {
            this.currentAudio.play();
            this.isPlaying = true;
            this.playWaveform();
        }
        this.updatePlayButton();
    }

    updatePlayButton() {
        const playBtn = document.getElementById('play-btn');
        if (playBtn) {
            const icon = playBtn.querySelector('i');
            icon.className = this.isPlaying ? 'fas fa-pause' : 'fas fa-play';
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

    seekAudio(e) {
        if (!this.currentAudio) return;
        
        const rect = e.currentTarget.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const width = rect.width;
        const seekTime = (clickX / width) * this.currentAudio.duration;
        
        this.currentAudio.currentTime = seekTime;
    }

    downloadAudio() {
        if (this.currentAudio) {
            const link = document.createElement('a');
            link.href = this.currentAudio.src;
            link.download = 'generated_speech.wav';
            link.click();
        }
    }

    downloadBatch() {
        const downloadLink = document.getElementById('batch-download-link');
        if (downloadLink && downloadLink.href) {
            downloadLink.click();
        } else {
            alert('No file available for download');
        }
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
    new OratoApp();
});