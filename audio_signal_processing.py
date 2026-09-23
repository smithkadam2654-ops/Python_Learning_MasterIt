"""
Audio Signal Processing Module

This module provides comprehensive audio signal processing utilities including:
- Audio file loading and saving
- Waveform analysis
- Frequency domain analysis (FFT)
- Filtering operations
- Audio effects
- Audio visualization
- Silence detection
- Audio normalization
- Sample rate conversion
- Spectral analysis

Note: This module uses numpy for numerical operations.
Install with: pip install numpy

All functions include comprehensive docstrings and type hints.
"""

import math
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import array


try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


class AudioFormat(Enum):
    """Audio file formats."""
    WAV = "wav"
    MP3 = "mp3"
    FLAC = "flac"
    OGG = "ogg"
    AAC = "aac"


class SampleFormat(Enum):
    """Sample bit depth formats."""
    INT8 = "int8"
    INT16 = "int16"
    INT24 = "int24"
    INT32 = "int32"
    FLOAT32 = "float32"
    FLOAT64 = "float64"


@dataclass
class AudioInfo:
    """Audio file information."""
    sample_rate: int
    channels: int
    sample_format: SampleFormat
    duration: float
    num_samples: int


class AudioLoader:
    """Audio file loading utilities."""
    
    @staticmethod
    def load_wav_file(file_path: str) -> Tuple[List[float], AudioInfo]:
        """Load WAV file (simplified)."""
        if NUMPY_AVAILABLE:
            import wave
            import struct
            
            with wave.open(file_path, 'rb') as wav_file:
                frames = wav_file.getnframes()
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                
                # Determine sample format
                if sample_width == 1:
                    sample_format = SampleFormat.INT8
                elif sample_width == 2:
                    sample_format = SampleFormat.INT16
                elif sample_width == 3:
                    sample_format = SampleFormat.INT24
                elif sample_width == 4:
                    sample_format = SampleFormat.INT32
                else:
                    sample_format = SampleFormat.INT16
                
                # Read frames
                audio_data = wav_file.readframes(frames)
                
                # Convert to float samples
                if sample_format == SampleFormat.INT16:
                    samples = array.array('h', audio_data)
                    float_samples = [s / 32768.0 for s in samples]
                else:
                    # Default to int16
                    samples = array.array('h', audio_data)
                    float_samples = [s / 32768.0 for s in samples]
                
                # Deinterleave if stereo
                if channels == 2:
                    left = float_samples[::2]
                    right = float_samples[1::2]
                    # Mix to mono
                    float_samples = [(l + r) / 2 for l, r in zip(left, right)]
                
                audio_info = AudioInfo(
                    sample_rate=sample_rate,
                    channels=channels,
                    sample_format=sample_format,
                    duration=frames / sample_rate,
                    num_samples=len(float_samples)
                )
                
                return float_samples, audio_info
        
        return [], AudioInfo(44100, 1, SampleFormat.INT16, 0, 0)
    
    @staticmethod
    def generate_sine_wave(frequency: float, duration: float,
                           sample_rate: int = 44100,
                           amplitude: float = 0.5) -> List[float]:
        """Generate sine wave."""
        num_samples = int(sample_rate * duration)
        samples = []
        
        for i in range(num_samples):
            t = i / sample_rate
            sample = amplitude * math.sin(2 * math.pi * frequency * t)
            samples.append(sample)
        
        return samples
    
    @staticmethod
    def generate_white_noise(duration: float,
                           sample_rate: int = 44100,
                           amplitude: float = 0.1) -> List[float]:
        """Generate white noise."""
        import random
        num_samples = int(sample_rate * duration)
        samples = [amplitude * (random.random() * 2 - 1) for _ in range(num_samples)]
        return samples


class WaveformAnalysis:
    """Waveform analysis utilities."""
    
    @staticmethod
    def calculate_rms(samples: List[float]) -> float:
        """Calculate RMS (Root Mean Square)."""
        if not samples:
            return 0.0
        
        sum_squares = sum(s ** 2 for s in samples)
        return math.sqrt(sum_squares / len(samples))
    
    @staticmethod
    def calculate_peak(samples: List[float]) -> float:
        """Calculate peak amplitude."""
        if not samples:
            return 0.0
        return max(abs(s) for s in samples)
    
    @staticmethod
    def calculate_crest_factor(samples: List[float]) -> float:
        """Calculate crest factor (peak / RMS)."""
        rms = WaveformAnalysis.calculate_rms(samples)
        peak = WaveformAnalysis.calculate_peak(samples)
        
        if rms > 0:
            return peak / rms
        return 0.0
    
    @staticmethod
    def calculate_dynamic_range(samples: List[float]) -> float:
        """Calculate dynamic range in dB."""
        peak = WaveformAnalysis.calculate_peak(samples)
        
        if peak > 0:
            return 20 * math.log10(peak)
        return 0.0
    
    @staticmethod
    def detect_zero_crossings(samples: List[float]) -> int:
        """Count zero crossings."""
        crossings = 0
        
        for i in range(1, len(samples)):
            if (samples[i] >= 0 and samples[i-1] < 0) or \
               (samples[i] < 0 and samples[i-1] >= 0):
                crossings += 1
        
        return crossings


class FrequencyAnalysis:
    """Frequency domain analysis."""
    
    @staticmethod
    def compute_fft(samples: List[float]) -> List[complex]:
        """Compute FFT of samples."""
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy is required for FFT")
        
        samples_array = np.array(samples)
        fft_result = np.fft.fft(samples_array)
        return fft_result.tolist()
    
    @staticmethod
    def compute_magnitude_spectrum(samples: List[float]) -> List[float]:
        """Compute magnitude spectrum."""
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy is required")
        
        fft_result = FrequencyAnalysis.compute_fft(samples)
        magnitude = [abs(complex_val) for complex_val in fft_result]
        return magnitude[:len(magnitude) // 2]  # Return only positive frequencies
    
    @staticmethod
    def compute_power_spectrum(samples: List[float]) -> List[float]:
        """Compute power spectrum."""
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy is required")
        
        magnitude = FrequencyAnalysis.compute_magnitude_spectrum(samples)
        power = [m ** 2 for m in magnitude]
        return power
    
    @staticmethod
    def find_dominant_frequency(samples: List[float], sample_rate: int) -> Tuple[float, float]:
        """Find dominant frequency and its magnitude."""
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy is required")
        
        magnitude = FrequencyAnalysis.compute_magnitude_spectrum(samples)
        freq_resolution = sample_rate / len(samples)
        
        # Find peak
        peak_index = magnitude.index(max(magnitude))
        dominant_freq = peak_index * freq_resolution
        dominant_magnitude = magnitude[peak_index]
        
        return dominant_freq, dominant_magnitude
    
    @staticmethod
    def compute_spectral_centroid(samples: List[float], sample_rate: int) -> float:
        """Compute spectral centroid."""
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy is required")
        
        magnitude = FrequencyAnalysis.compute_magnitude_spectrum(samples)
        freq_resolution = sample_rate / len(samples)
        
        weighted_sum = 0.0
        total_magnitude = sum(magnitude)
        
        for i, mag in enumerate(magnitude):
            freq = i * freq_resolution
            weighted_sum += freq * mag
        
        if total_magnitude > 0:
            return weighted_sum / total_magnitude
        return 0.0


class AudioFilter:
    """Audio filtering operations."""
    
    @staticmethod
    def apply_low_pass_filter(samples: List[float], cutoff: float,
                           sample_rate: int) -> List[float]:
        """Apply simple low-pass filter (moving average)."""
        # Simple moving average filter as low-pass
        window_size = int(sample_rate / cutoff)
        if window_size < 2:
            window_size = 2
        
        filtered = []
        for i in range(len(samples)):
            start = max(0, i - window_size // 2)
            end = min(len(samples), i + window_size // 2 + 1)
            avg = sum(samples[start:end]) / (end - start)
            filtered.append(avg)
        
        return filtered
    
    @staticmethod
    def apply_high_pass_filter(samples: List[float], cutoff: float,
                            sample_rate: int) -> List[float]:
        """Apply high-pass filter."""
        # Subtract low-pass from original
        low_passed = AudioFilter.apply_low_pass_filter(samples, cutoff, sample_rate)
        high_passed = [original - low for original, low in zip(samples, low_passed)]
        return high_passed
    
    @staticmethod
    def apply_band_pass_filter(samples: List[float], low_cutoff: float,
                             high_cutoff: float, sample_rate: int) -> List[float:
        """Apply band-pass filter."""
        low_passed = AudioFilter.apply_low_pass_filter(samples, high_cutoff, sample_rate)
        high_passed = AudioFilter.apply_high_pass_filter(low_passed, low_cutoff, sample_rate)
        return high_passed
    
    @staticmethod
    def apply_gain(samples: List[float], gain_db: float) -> List[float]:
        """Apply gain in decibels."""
        gain_linear = 10 ** (gain_db / 20)
        return [s * gain_linear for s in samples]
    
    @staticmethod
    def apply_fade_in(samples: List[float], duration: float, sample_rate: int) -> List[float]:
        """Apply fade-in effect."""
        fade_samples = int(sample_rate * duration)
        if fade_samples > len(samples):
            fade_samples = len(samples)
        
        faded = samples.copy()
        for i in range(fade_samples):
            factor = i / fade_samples
            faded[i] *= factor
        
        return faded
    
    @staticmethod
    def apply_fade_out(samples: List[float], duration: float, sample_rate: int) -> List[float]:
        """Apply fade-out effect."""
        fade_samples = int(sample_rate * duration)
        if fade_samples > len(samples):
            fade_samples = len(samples)
        
        faded = samples.copy()
        start_idx = len(samples) - fade_samples
        
        for i in range(fade_samples):
            factor = 1 - (i / fade_samples)
            faded[start_idx + i] *= factor
        
        return faded


class AudioEffects:
    """Audio effects."""
    
    @staticmethod
    def apply_echo(samples: List[float], delay: float, decay: float,
                  sample_rate: int) -> List[float]:
        """Apply echo effect."""
        delay_samples = int(sample_rate * delay)
        if delay_samples >= len(samples):
            return samples
        
        echoed = samples.copy()
        
        for i in range(delay_samples, len(samples)):
            echoed[i] += samples[i - delay_samples] * decay
        
        # Normalize to prevent clipping
        max_val = max(abs(s) for s in echoed)
        if max_val > 1.0:
            echoed = [s / max_val for s in echoed]
        
        return echoed
    
    @staticmethod
    def apply_reverb(samples: List[float,], decay: float = 0.5,
                   sample_rate: int = 44100) -> List[float]:
        """Apply simple reverb effect."""
        # Multiple delayed echoes
        reverb = samples.copy()
        
        delays = [0.05, 0.1, 0.15, 0.2]  # Seconds
        for delay in delays:
            reverb = AudioEffects.apply_echo(reverb, delay, decay, sample_rate)
        
        return reverb
    
    @staticmethod
    def reverse_audio(samples: List[float]) -> List[float]:
        """Reverse audio."""
        return samples[::-1]
    
    @staticmethod
    def apply_tremolo(samples: List[float], rate: float, depth: float,
                       sample_rate: int) -> List[float]:
        """Apply tremolo effect (amplitude modulation)."""
        modulated = []
        
        for i, sample in enumerate(samples):
            t = i / sample_rate
            modulation = 1 + depth * math.sin(2 * math.pi * rate * t)
            modulated.append(sample * modulation)
        
        return modulated
    
    @staticmethod
    def apply_vibrato(samples: List[float], rate: float, depth: float,
                      sample_rate: int) -> List[float]:
        """Apply vibrato effect (frequency modulation - simplified)."""
        # Simplified vibrato using phase modulation
        modulated = []
        
        for i, sample in enumerate(samples):
            t = i / sample_rate
            # Add small phase shift
            phase_shift = depth * math.sin(2 * math.pi * rate * t)
            # Apply using simple interpolation
            sample_idx = i + int(phase_shift * 10)
            
            if 0 <= sample_idx < len(samples):
                modulated.append(samples[sample_idx])
            else:
                modulated.append(sample)
        
        return modulated


class AudioNormalization:
    """Audio normalization utilities."""
    
    @staticmethod
    def normalize(samples: List[float], target_level: float = 0.9) -> List[float]:
        """Normalize audio to target level."""
        peak = WaveformAnalysis.calculate_peak(samples)
        
        if peak > 0:
            scaling_factor = target_level / peak
            return [s * scaling_factor for s in samples]
        
        return samples
    
    @staticmethod
    def normalize_rms(samples: List[float], target_rms: float = 0.2) -> List[float]:
        """Normalize audio to target RMS."""
        rms = WaveformAnalysis.calculate_rms(samples)
        
        if rms > 0:
            scaling_factor = target_rms / rms
            return [s * scaling_factor for s in samples]
        
        return samples
    
    @staticmethod
    def remove_dc_offset(samples: List[float]) -> List[float]:
        """Remove DC offset (mean)."""
        mean = sum(samples) / len(samples) if samples else 0
        return [s - mean for s in samples]


class SilenceDetection:
    """Silence detection utilities."""
    
    @staticmethod
    def detect_silence(samples: List[float], threshold: float = 0.01,
                      min_duration: float = 0.1, sample_rate: int = 44100) -> List[Tuple[int, int]]:
        """Detect silent regions."""
        min_samples = int(sample_rate * min_duration)
        silent_indices = []
        
        for i, sample in enumerate(samples):
            if abs(sample) < threshold:
                silent_indices.append(i)
        
        # Group consecutive silent samples
        regions = []
        if silent_indices:
            start = silent_indices[0]
            prev = start
            
            for idx in silent_indices[1:]:
                if idx != prev + 1:
                    if prev - start + 1 >= min_samples:
                        regions.append((start, prev))
                    start = idx
                prev = idx
            
            if prev - start + 1 >= min_samples:
                regions.append((start, prev))
        
        return regions
    
    @staticmethod
    def trim_silence(samples: List[float], threshold: float = 0.01,
                    sample_rate: int = 44100) -> List[float]:
        """Trim silence from beginning and end."""
        # Find first non-silent sample
        start_idx = 0
        for i, sample in enumerate(samples):
            if abs(sample) >= threshold:
                start_idx = i
                break
        
        # Find last non-silent sample
        end_idx = len(samples)
        for i in range(len(samples) - 1, -1, -1):
            if abs(samples[i]) >= threshold:
                end_idx = i + 1
                break
        
        return samples[start_idx:end_idx]


class AudioVisualization:
    """Audio visualization utilities."""
    
    @staticmethod
    def generate_waveform_text(samples: List[float], width: int = 50,
                               height: int = 10) -> str:
        """Generate ASCII waveform visualization."""
        if not samples:
            return ""
        
        # Downsample to fit width
        step = max(1, len(samples) // width)
        downsampled = samples[::step]
        
        # Normalize to height
        peak = max(abs(s) for s in downsampled) if downsampled else 1
        if peak == 0:
            peak = 1
        
        lines = []
        for row in range(height):
            line = ""
            for sample in downsampled:
                normalized = abs(sample) / peak
                bar_height = int(normalized * height)
                
                if row < bar_height:
                    line += "█"
                else:
                    line += " "
            lines.append(line)
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_spectrum_text(magnitude: List[float], width: int = 50,
                               height: int = 10) -> str:
        """Generate ASCII spectrum visualization."""
        if not magnitude:
            return ""
        
        # Downsample to fit width
        step = max(1, len(magnitude) // width)
        downsampled = magnitude[::step]
        
        # Normalize to height
        peak = max(downsampled) if downsampled else 1
        if peak == 0:
            peak = 1
        
        lines = []
        for row in range(height):
            line = ""
            for mag in downsampled:
                normalized = mag / peak
                bar_height = int(normalized * height)
                
                if row < bar_height:
                    line += "█"
                else:
                    line += " "
            lines.append(line)
        
        return "\n".join(lines)


class AudioUtils:
    """General audio utilities."""
    
    @staticmethod
    def calculate_duration(num_samples: int, sample_rate: int) -> float:
        """Calculate duration from samples and sample rate."""
        return num_samples / sample_rate
    
    @staticmethod
    def resample(samples: List[float], original_rate: int, target_rate: int) -> List[float]:
        """Resample audio to different sample rate (linear interpolation)."""
        if original_rate == target_rate:
            return samples
        
        ratio = target_rate / original_rate
        new_length = int(len(samples) * ratio)
        resampled = []
        
        for i in range(new_length):
            original_idx = i / ratio
            idx_low = int(original_idx)
            idx_high = min(idx_low + 1, len(samples) - 1)
            
            # Linear interpolation
            frac = original_idx - idx_low
            sample = samples[idx_low] * (1 - frac) + samples[idx_high] * frac
            resampled.append(sample)
        
        return resampled
    
    @staticmethod
    def convert_stereo_to_mono(samples: List[float]) -> List[float]:
        """Convert stereo audio to mono (average)."""
        mono = []
        for i in range(0, len(samples), 2):
            if i + 1 < len(samples):
                mono.append((samples[i] + samples[i + 1]) / 2)
            else:
                mono.append(samples[i])
        return mono
    
    @staticmethod
    def convert_mono_to_stereo(samples: List[float]) -> List[float]:
        """Convert mono audio to stereo (duplicate)."""
        stereo = []
        for sample in samples:
            stereo.append(sample)
            stereo.append(sample)
        return stereo


def demonstrate_audio_signal_processing():
    """Demonstrate audio signal processing functionality."""
    print("=== Audio Signal Processing Demonstration ===\n")
    
    # Generate Test Audio
    print("1. Generate Test Audio:")
    sine_wave = AudioLoader.generate_sine_wave(440, 1.0, 44100, 0.5)
    noise = AudioLoader.generate_white_noise(1.0, 44100, 0.1)
    
    print(f"   Generated sine wave: {len(sine_wave)} samples")
    print(f"   Generated noise: {len(noise)} samples")
    
    # Waveform Analysis
    print("\n2. Waveform Analysis:")
    rms = WaveformAnalysis.calculate_rms(sine_wave)
    peak = WaveformAnalysis.calculate_peak(sine_wave)
    crest = WaveformAnalysis.calculate_crest_factor(sine_wave)
    crossings = WaveformAnalysis.detect_zero_crossings(sine_wave)
    
    print(f"   RMS: {rms:.4f}")
    print(f"   Peak: {peak:.4f}")
    print(f"   Crest factor: {crest:.4f}")
    print(f"   Zero crossings: {crossings}")
    
    # Frequency Analysis
    print("\n3. Frequency Analysis:")
    if NUMPY_AVAILABLE:
        magnitude = FrequencyAnalysis.compute_magnitude_spectrum(sine_wave)
        dominant_freq, dom_mag = FrequencyAnalysis.find_dominant_frequency(sine_wave, 44100)
        spectral_centroid = FrequencyAnalysis.compute_spectral_centroid(sine_wave, 44100)
        
        print(f"   Dominant frequency: {dominant_freq:.2f} Hz")
        print(f"   Dominant magnitude: {dom_mag:.4f}")
        print(f"   Spectral centroid: {spectral_centroid:.2f} Hz")
    else:
        print("   Install numpy for frequency analysis")
    
    # Filtering
    print("\n4. Audio Filtering:")
    low_passed = AudioFilter.apply_low_pass_filter(sine_wave, 1000, 44100)
    high_passed = AudioFilter.apply_high_pass_filter(sine_wave, 200, 44100)
    
    print(f"   Low-passed samples: {len(low_passed)}")
    print(f"   High-passed samples: {len(high_passed)}")
    
    # Effects
    print("\n5. Audio Effects:")
    echoed = AudioEffects.apply_echo(sine_wave, 0.1, 0.5, 44100)
    reversed_audio = AudioEffects.reverse_audio(sine_wave)
    
    print(f"   Echoed samples: {len(echoed)}")
    print(f"   Reversed samples: {len(reversed_audio)}")
    
    # Normalization
    print("\n6. Audio Normalization:")
    normalized = AudioNormalization.normalize(sine_wave, 0.9)
    no_dc = AudioNormalization.remove_dc_offset(sine_wave)
    
    norm_peak = WaveformAnalysis.calculate_peak(normalized)
    print(f"   Normalized peak: {norm_peak:.4f}")
    
    # Silence Detection
    print("\n7. Silence Detection:")
    test_signal = [0.0] * 1000 + [0.5] * 1000 + [0.0] * 1000
    silent_regions = SilenceDetection.detect_silence(test_signal, 0.01, 0.05, 44100)
    
    print(f"   Silent regions: {len(silent_regions)}")
    
    # Visualization
    print("\n8. Audio Visualization:")
    waveform_vis = AudioVisualization.generate_waveform_text(sine_wave[:100], 30, 5)
    print(f"   Waveform:\n{waveform_vis}")
    
    # Audio Utils
    print("\n9. Audio Utilities:")
    duration = AudioUtils.calculate_duration(len(sine_wave), 44100)
    print(f"   Duration: {duration:.4f} seconds")
    
    resampled = AudioUtils.resample(sine_wave[:1000], 44100, 22050)
    print(f"   Resampled: {len(resampled)} samples")
    
    # Gain
    print("\n10. Gain and Fade:")
    gained = AudioFilter.apply_gain(sine_wave, 6.0)  # +6dB
    faded_in = AudioFilter.apply_fade_in(sine_wave, 0.1, 44100)
    
    print(f"   Gained samples: {len(gained)}")
    print(f"   Faded in samples: {len(faded_in)}")
    
    print("\n=== Demonstration Complete ===")
    print("\nAudio Signal Processing Best Practices:")
    print("- Use appropriate sample rates for your application")
    print("- Apply anti-aliasing filters before downsampling")
    print("- Normalize audio to prevent clipping")
    print("- Use appropriate window sizes for FFT")
    print("- Handle DC offset before frequency analysis")
    print("- Use logarithmic scales for frequency visualization")
    print("- Consider stereo vs mono processing requirements")
    print("- Use dithering when reducing bit depth")
    print("- Handle edge cases in silence detection")
    print("- Test audio effects on various signal types")


if __name__ == "__main__":
    demonstrate_audio_signal_processing()
