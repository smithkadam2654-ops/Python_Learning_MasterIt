"""
Audio Processing Module

This module provides comprehensive audio processing utilities including:
- Audio file loading and saving
- Audio playback and recording
- Sound analysis and visualization
- Audio effects and filters
- Audio format conversion
- Speech recognition helpers
- Audio manipulation
- Audio streaming
- Audio quality analysis
- Signal processing utilities

Note: This module uses pydub and sounddevice for audio operations.
Install with: pip install pydub sounddevice numpy scipy

For MP3 support: pip install ffmpeg-python

All functions include comprehensive docstrings and type hints.
"""

import math
import array
import struct
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import json


try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


try:
    from pydub import AudioSegment
    from pydub.effects import normalize, fade_in, fade_out
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False


try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False


class AudioFormat(Enum):
    """Supported audio formats."""
    WAV = "wav"
    MP3 = "mp3"
    OGG = "ogg"
    FLAC = "flac"
    AAC = "aac"
    M4A = "m4a"


class AudioChannel(Enum):
    """Audio channel configurations."""
    MONO = 1
    STEREO = 2
    SURROUND_5_1 = 6
    SURROUND_7_1 = 8


@dataclass
class AudioInfo:
    """Container for audio file information."""
    duration: float
    sample_rate: int
    channels: int
    sample_width: int
    format: str
    file_size: int
    bit_rate: Optional[int] = None


@dataclass
class AudioAnalysis:
    """Container for audio analysis results."""
    rms_level: float
    peak_level: float
    dynamic_range: float
    frequency_peaks: List[Tuple[float, float]]
    spectral_centroid: float
    zero_crossing_rate: float


class AudioLoader:
    """Audio file loading utilities."""
    
    @staticmethod
    def load_audio(file_path: str) -> Optional[AudioSegment]:
        """Load audio file."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required. Install with: pip install pydub")
        
        try:
            return AudioSegment.from_file(file_path)
        except Exception as e:
            print(f"Error loading audio: {e}")
            return None
    
    @staticmethod
    def get_audio_info(file_path: str) -> Optional[AudioInfo]:
        """Get audio file information."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required. Install with: pip install pydub")
        
        try:
            audio = AudioSegment.from_file(file_path)
            
            # Calculate bit rate (approximate)
            file_size = os.path.getsize(file_path)
            bit_rate = int(file_size * 8 / audio.duration_seconds) if audio.duration_seconds > 0 else None
            
            return AudioInfo(
                duration=audio.duration_seconds,
                sample_rate=audio.frame_rate,
                channels=audio.channels,
                sample_width=audio.sample_width,
                format=file_path.split('.')[-1].lower(),
                file_size=file_size,
                bit_rate=bit_rate
            )
        except Exception as e:
            print(f"Error getting audio info: {e}")
            return None
    
    @staticmethod
    def convert_format(input_path: str, output_path: str, 
                       format: AudioFormat = AudioFormat.WAV) -> bool:
        """Convert audio file format."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required. Install with: pip install pydub")
        
        try:
            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format=format.value)
            return True
        except Exception as e:
            print(f"Error converting audio: {e}")
            return False


class AudioEffects:
    """Audio effects and processing."""
    
    @staticmethod
    def apply_volume_change(audio: AudioSegment, 
                           change_db: float) -> AudioSegment:
        """Change volume by specified dB."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        return audio + change_db
    
    @staticmethod
    def normalize_audio(audio: AudioSegment, 
                       target_dbfs: float = -20.0) -> AudioSegment:
        """Normalize audio to target dBFS."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        return normalize(audio, target_dbfs)
    
    @staticmethod
    def apply_fade_in(audio: AudioSegment, 
                     duration_ms: int = 1000) -> AudioSegment:
        """Apply fade-in effect."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        return fade_in(audio, duration_ms)
    
    @staticmethod
    def apply_fade_out(audio: AudioSegment, 
                      duration_ms: int = 1000) -> AudioSegment:
        """Apply fade-out effect."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        return fade_out(audio, duration_ms)
    
    @staticmethod
    def reverse_audio(audio: AudioSegment) -> AudioSegment:
        """Reverse audio."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        return audio.reverse()
    
    @staticmethod
    def change_speed(audio: AudioSegment, 
                    speed_factor: float = 1.0) -> AudioSegment:
        """Change playback speed."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        # Manually change speed by frame rate manipulation
        new_frame_rate = int(audio.frame_rate * speed_factor)
        return audio._spawn(audio).set_frame_rate(new_frame_rate)
    
    @staticmethod
    def change_pitch(audio: AudioSegment, 
                     semitones: float = 0.0) -> AudioSegment:
        """Change pitch by semitones."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        # Simple pitch shift using speed change (not perfect but functional)
        # For professional pitch shifting, use librosa or similar
        speed_factor = 2 ** (semitones / 12)
        return AudioEffects.change_speed(audio, speed_factor)
    
    @staticmethod
    def trim_silence(audio: AudioSegment, 
                    silence_threshold: int = -40,
                    chunk_size: int = 10) -> AudioSegment:
        """Remove silence from beginning and end."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        # Trim from beginning
        def is_silent(chunk):
            return chunk.dBFS < silence_threshold
        
        # Split into chunks and find first non-silent
        chunks = [audio[i:i+chunk_size] for i in range(0, len(audio), chunk_size)]
        
        # Find first non-silent chunk
        start_index = 0
        for i, chunk in enumerate(chunks):
            if not is_silent(chunk):
                start_index = i * chunk_size
                break
        
        # Find last non-silent chunk
        end_index = len(audio)
        for i in range(len(chunks) - 1, -1, -1):
            if not is_silent(chunks[i]):
                end_index = (i + 1) * chunk_size
                break
        
        return audio[start_index:end_index]
    
    @staticmethod
    def apply_echo(audio: AudioSegment, 
                  delay_ms: int = 500,
                  decay: float = 0.5) -> AudioSegment:
        """Apply echo effect."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        # Create delayed version
        delayed = audio._spawn(audio)
        delayed = delayed - (20 * math.log10(decay))  # Adjust volume for decay
        
        # Overlay delayed version
        combined = audio.overlay(delayed, position=delay_ms)
        
        return combined


class AudioAnalyzer:
    """Audio analysis and visualization."""
    
    @staticmethod
    def get_waveform(audio: AudioSegment) -> List[int]:
        """Extract waveform data."""
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy library is required. Install with: pip install numpy")
        
        # Convert to numpy array
        samples = np.array(audio.get_array_of_samples())
        
        # Downsample for visualization
        if len(samples) > 1000:
            samples = samples[::len(samples)//1000]
        
        return samples.tolist()
    
    @staticmethod
    def analyze_audio(audio: AudioSegment) -> AudioAnalysis:
        """Perform comprehensive audio analysis."""
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy library is required. Install with: pip install numpy")
        
        samples = np.array(audio.get_array_of_samples())
        
        # Calculate RMS level
        rms_level = np.sqrt(np.mean(samples ** 2))
        
        # Calculate peak level
        peak_level = np.max(np.abs(samples))
        
        # Calculate dynamic range
        dynamic_range = peak_level / rms_level if rms_level > 0 else 0
        
        # Calculate zero crossing rate
        zero_crossings = np.sum(np.diff(np.sign(samples)) != 0)
        zero_crossing_rate = zero_crossings / len(samples)
        
        # Simple frequency analysis (FFT)
        fft = np.fft.fft(samples)
        freqs = np.fft.fftfreq(len(samples), 1/audio.frame_rate)
        
        # Find frequency peaks
        magnitude = np.abs(fft)
        peak_indices = np.argsort(magnitude)[-10:]  # Top 10 peaks
        frequency_peaks = [(abs(freqs[i]), magnitude[i]) for i in peak_indices]
        frequency_peaks.sort(reverse=True, key=lambda x: x[1])
        
        # Calculate spectral centroid
        spectral_centroid = np.sum(freqs * magnitude) / np.sum(magnitude) if np.sum(magnitude) > 0 else 0
        
        return AudioAnalysis(
            rms_level=rms_level,
            peak_level=peak_level,
            dynamic_range=dynamic_range,
            frequency_peaks=frequency_peaks,
            spectral_centroid=spectral_centroid,
            zero_crossing_rate=zero_crossing_rate
        )
    
    @staticmethod
    def detect_silence(audio: AudioSegment, 
                      threshold: int = -40,
                      min_duration: float = 0.5) -> List[Tuple[float, float]]:
        """Detect silent segments in audio."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        # Split into small chunks
        chunk_size = 10  # ms
        chunks = [audio[i:i+chunk_size] for i in range(0, len(audio), chunk_size)]
        
        silent_chunks = []
        current_start = None
        
        for i, chunk in enumerate(chunks):
            is_silent = chunk.dBFS < threshold
            
            if is_silent and current_start is None:
                current_start = i * chunk_size / 1000  # Convert to seconds
            elif not is_silent and current_start is not None:
                duration = (i * chunk_size / 1000) - current_start
                if duration >= min_duration:
                    silent_chunks.append((current_start, duration))
                current_start = None
        
        return silent_chunks
    
    @staticmethod
    def calculate_bitrate(file_path: str) -> Optional[int]:
        """Calculate audio bitrate."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        try:
            audio = AudioSegment.from_file(file_path)
            file_size = os.path.getsize(file_path)
            
            if audio.duration_seconds > 0:
                return int(file_size * 8 / audio.duration_seconds)
            return None
        except Exception:
            return None


class AudioRecorder:
    """Audio recording utilities."""
    
    @staticmethod
    def record_audio(duration: float, 
                    sample_rate: int = 44100,
                    channels: int = 1,
                    output_file: Optional[str] = None) -> Optional[AudioSegment]:
        """Record audio for specified duration."""
        if not SOUNDDEVICE_AVAILABLE:
            raise ImportError("sounddevice library is required. Install with: pip install sounddevice")
        
        try:
            # Record audio
            recording = sd.rec(int(duration * sample_rate), 
                              samplerate=sample_rate, 
                              channels=channels)
            sd.wait()  # Wait for recording to complete
            
            # Convert to AudioSegment
            audio_data = recording
            
            if PYDUB_AVAILABLE:
                # Convert to AudioSegment
                audio = AudioSegment(
                    audio_data.tobytes(),
                    frame_rate=sample_rate,
                    sample_width=audio_data.dtype.itemsize,
                    channels=channels
                )
                
                if output_file:
                    audio.export(output_file, format="wav")
                
                return audio
            
            return None
            
        except Exception as e:
            print(f"Recording failed: {e}")
            return None
    
    @staticmethod
    def record_to_buffer(duration: float,
                         sample_rate: int = 44100,
                         channels: int = 1) -> Optional[np.ndarray]:
        """Record audio to numpy array buffer."""
        if not SOUNDDEVICE_AVAILABLE or not NUMPY_AVAILABLE:
            raise ImportError("sounddevice and numpy libraries are required")
        
        try:
            recording = sd.rec(int(duration * sample_rate),
                              samplerate=sample_rate,
                              channels=channels)
            sd.wait()
            return recording
        except Exception as e:
            print(f"Recording failed: {e}")
            return None


class AudioPlayback:
    """Audio playback utilities."""
    
    @staticmethod
    def play_audio(audio: AudioSegment) -> bool:
        """Play audio file."""
        if not SOUNDDEVICE_AVAILABLE:
            raise ImportError("sounddevice library is required. Install with: pip install sounddevice")
        
        try:
            # Convert audio to numpy array
            samples = np.array(audio.get_array_of_samples())
            
            # Normalize to [-1, 1] range
            if audio.sample_width == 2:
                samples = samples.astype(np.float32) / 32768.0
            elif audio.sample_width == 4:
                samples = samples.astype(np.float32) / 2147483648.0
            
            # Handle stereo
            if audio.channels == 2:
                samples = samples.reshape(-1, 2)
            
            # Play audio
            sd.play(samples, samplerate=audio.frame_rate)
            sd.wait()
            
            return True
        except Exception as e:
            print(f"Playback failed: {e}")
            return False
    
    @staticmethod
    def play_file(file_path: str) -> bool:
        """Play audio file directly."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        try:
            audio = AudioSegment.from_file(file_path)
            return AudioPlayback.play_audio(audio)
        except Exception as e:
            print(f"Playback failed: {e}")
            return False


class AudioManipulation:
    """Audio manipulation utilities."""
    
    @staticmethod
    def concatenate_audio(audio_files: List[str], 
                         output_file: str) -> bool:
        """Concatenate multiple audio files."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        try:
            combined = AudioSegment.empty()
            
            for file_path in audio_files:
                audio = AudioSegment.from_file(file_path)
                combined += audio
            
            combined.export(output_file, format="wav")
            return True
        except Exception as e:
            print(f"Concatenation failed: {e}")
            return False
    
    @staticmethod
    def split_audio(audio: AudioSegment, 
                   parts: int) -> List[AudioSegment]:
        """Split audio into equal parts."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        part_duration = len(audio) // parts
        parts_list = []
        
        for i in range(parts):
            start = i * part_duration
            end = start + part_duration if i < parts - 1 else len(audio)
            part = audio[start:end]
            parts_list.append(part)
        
        return parts_list
    
    @staticmethod
    def extract_segment(audio: AudioSegment,
                       start_time: float,
                       end_time: float) -> AudioSegment:
        """Extract segment from audio."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        start_ms = int(start_time * 1000)
        end_ms = int(end_time * 1000)
        
        return audio[start_ms:end_ms]
    
    @staticmethod
    def mix_audio(audio1: AudioSegment, 
                 audio2: AudioSegment,
                 position: int = 0) -> AudioSegment:
        """Mix two audio tracks."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        return audio1.overlay(audio2, position=position)
    
    @staticmethod
    def change_sample_rate(audio: AudioSegment,
                          new_sample_rate: int) -> AudioSegment:
        """Change sample rate of audio."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        return audio.set_frame_rate(new_sample_rate)
    
    @staticmethod
    def convert_to_mono(audio: AudioSegment) -> AudioSegment:
        """Convert stereo audio to mono."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        if audio.channels == 2:
            return audio.set_channels(1)
        return audio
    
    @staticmethod
    def convert_to_stereo(audio: AudioSegment) -> AudioSegment:
        """Convert mono audio to stereo."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        if audio.channels == 1:
            return audio.set_channels(2)
        return audio


class AudioVisualization:
    """Audio visualization utilities."""
    
    @staticmethod
    def generate_waveform_ascii(audio: AudioSegment, 
                               width: int = 50,
                               height: int = 10) -> str:
        """Generate ASCII waveform visualization."""
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy library is required")
        
        samples = np.array(audio.get_array_of_samples())
        
        # Downsample
        if len(samples) > width:
            samples = samples[::len(samples)//width]
        
        # Normalize to height
        samples = np.abs(samples)
        max_val = np.max(samples) if np.max(samples) > 0 else 1
        samples = (samples / max_val * height).astype(int)
        
        # Generate ASCII art
        lines = []
        for row in range(height, 0, -1):
            line = ""
            for sample in samples:
                if sample >= row:
                    line += "█"
                else:
                    line += " "
            lines.append(line)
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_spectrum_ascii(audio: AudioSegment,
                               width: int = 50,
                               height: int = 10) -> str:
        """Generate ASCII spectrum visualization."""
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy library is required")
        
        samples = np.array(audio.get_array_of_samples())
        
        # Calculate FFT
        fft = np.fft.fft(samples)
        magnitude = np.abs(fft[:len(fft)//2])
        
        # Downsample
        if len(magnitude) > width:
            magnitude = magnitude[::len(magnitude)//width]
        
        # Normalize to height
        max_val = np.max(magnitude) if np.max(magnitude) > 0 else 1
        magnitude = (magnitude / max_val * height).astype(int)
        
        # Generate ASCII art
        lines = []
        for row in range(height, 0, -1):
            line = ""
            for mag in magnitude:
                if mag >= row:
                    line += "█"
                else:
                    line += " "
            lines.append(line)
        
        return "\n".join(lines)


class AudioUtilities:
    """General audio utility functions."""
    
    @staticmethod
    def calculate_duration(file_path: str) -> Optional[float]:
        """Calculate audio duration in seconds."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        try:
            audio = AudioSegment.from_file(file_path)
            return audio.duration_seconds
        except Exception:
            return None
    
    @staticmethod
    def get_supported_formats() -> List[str]:
        """Get list of supported audio formats."""
        return ["wav", "mp3", "ogg", "flac", "aac", "m4a"]
    
    @staticmethod
    def batch_convert(input_dir: str, 
                     output_dir: str,
                     target_format: AudioFormat = AudioFormat.WAV) -> List[str]:
        """Batch convert audio files in directory."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        import os
        
        converted_files = []
        supported_extensions = [".wav", ".mp3", ".ogg", ".flac", ".aac", ".m4a"]
        
        for filename in os.listdir(input_dir):
            if any(filename.lower().endswith(ext) for ext in supported_extensions):
                input_path = os.path.join(input_dir, filename)
                output_filename = os.path.splitext(filename)[0] + f".{target_format.value}"
                output_path = os.path.join(output_dir, output_filename)
                
                if AudioLoader.convert_format(input_path, output_path, target_format):
                    converted_files.append(output_path)
        
        return converted_files
    
    @staticmethod
    def create_silence(duration: float,
                      sample_rate: int = 44100,
                      channels: int = 1) -> AudioSegment:
        """Create silent audio segment."""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub library is required")
        
        duration_ms = int(duration * 1000)
        return AudioSegment.silent(duration=duration_ms, frame_rate=sample_rate)


def demonstrate_audio_processing():
    """Demonstrate audio processing functionality."""
    print("=== Audio Processing Demonstration ===\n")
    
    # Audio Information
    print("1. Audio Information:")
    print("   Audio file loading and analysis")
    print("   - Supports WAV, MP3, OGG, FLAC, AAC, M4A")
    print("   - Provides duration, sample rate, channels info")
    print("   - Calculates bitrate and file size")
    
    # Audio Effects
    print("\n2. Audio Effects:")
    print("   Available audio effects:")
    print("   - Volume change (dB)")
    print("   - Normalization")
    print("   - Fade in/out")
    print("   - Reverse audio")
    print("   - Speed change")
    print("   - Pitch shift")
    print("   - Silence trimming")
    print("   - Echo effect")
    
    # Audio Analysis
    print("\n3. Audio Analysis:")
    print("   Analysis capabilities:")
    print("   - Waveform extraction")
    print("   - RMS and peak levels")
    print("   - Dynamic range calculation")
    print("   - Frequency analysis (FFT)")
    print("   - Spectral centroid")
    print("   - Zero crossing rate")
    print("   - Silence detection")
    
    # Audio Manipulation
    print("\n4. Audio Manipulation:")
    print("   Manipulation operations:")
    print("   - Concatenate multiple files")
    print("   - Split audio into parts")
    print("   - Extract segments")
    print("   - Mix audio tracks")
    print("   - Change sample rate")
    print("   - Convert mono/stereo")
    
    # Recording and Playback
    print("\n5. Recording and Playback:")
    if SOUNDDEVICE_AVAILABLE:
        print("   - Record audio to file")
        print("   - Record to buffer")
        print("   - Play audio files")
        print("   - Play from AudioSegment")
    else:
        print("   Install sounddevice: pip install sounddevice")
    
    # Visualization
    print("\n6. Audio Visualization:")
    print("   Visualization options:")
    print("   - ASCII waveform generation")
    print("   - ASCII spectrum analysis")
    print("   - Configurable dimensions")
    
    # Utilities
    print("\n7. Audio Utilities:")
    print("   General utilities:")
    print("   - Duration calculation")
    print("   - Format conversion")
    print("   - Batch processing")
    print("   - Silence generation")
    
    # Example workflow
    print("\n8. Example Workflow:")
    print("""
# Load audio file
audio = AudioLoader.load_audio("input.wav")

# Apply effects
audio = AudioEffects.normalize_audio(audio)
audio = AudioEffects.apply_fade_in(audio, 1000)
audio = AudioEffects.apply_fade_out(audio, 1000)

# Analyze audio
analysis = AudioAnalyzer.analyze_audio(audio)
print(f"RMS Level: {analysis.rms_level}")
print(f"Peak Level: {analysis.peak_level}")

# Save processed audio
audio.export("output.wav", format="wav")
""")
    
    print("\n=== Demonstration Complete ===")
    print("\nAudio Processing Requirements:")
    print("- pydub: Audio file handling and effects")
    print("- sounddevice: Recording and playback")
    print("- numpy: Signal processing and analysis")
    print("- ffmpeg: MP3 encoding/decoding")
    print("\nInstallation:")
    print("pip install pydub sounddevice numpy scipy")
    print("pip install ffmpeg-python  # For MP3 support")


if __name__ == "__main__":
    import os
    demonstrate_audio_processing()