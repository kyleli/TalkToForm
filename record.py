import pyaudio
import wave
import keyboard
import time
from pydub import AudioSegment

def record_audio(filename, chunk=1024, channels=1, rate=44100, format=pyaudio.paInt16):
    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []
    recording = False
    key_pressed = False

    print("Press 'r' to start/pause recording, and press 'esc' to stop recording and save the file.")

    while True:
        if keyboard.is_pressed('esc'):
            break

        if keyboard.is_pressed('r') and not key_pressed:
            recording = not recording
            key_pressed = True
            print("Recording..." if recording else "Recording paused.")
            time.sleep(0.5)
        elif not keyboard.is_pressed('r'):
            key_pressed = False

        if recording:
            data = stream.read(chunk)
            frames.append(data)

    print("Recording stopped and saving...")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert frames to AudioSegment
    audio_segment = AudioSegment(
        b''.join(frames),
        frame_rate=rate,
        sample_width=p.get_sample_size(format),
        channels=channels
    )

    # Export audio segment as MP3 file
    audio_segment.export(filename, format="mp3")

    print(f"File saved as {filename}")

if __name__ == '__main__':
    record_audio('output.mp3')