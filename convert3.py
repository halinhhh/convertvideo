import subprocess

def binary_string_to_binary(binary_string):
    # Convert a string of binary digits to binary data
    binary_data = bytes(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8))
    return binary_data

def binary_to_video(binary_data, output_video_path, width, height, duration, audio_channels, bitrate):
    # Use ffmpeg to write binary data to a video file
    command = [
        '/opt/homebrew/bin/ffmpeg',    # Adjust this path to the location of your ffmpeg executable
        '-f', 'h264',  
        '-i', '-',  
        '-vf', f'scale={width}:{height}',  
        '-b:v', bitrate,  # Adjust bitrate
        '-t', duration,   # Adjust the format to HH:MM:SS
        '-ac', audio_channels,  
        output_video_path
    ]

    process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate(input=binary_data)

    if process.returncode != 0:
        raise Exception("FFmpeg error")

def main():
    input_file_path = '/Users/linhha/C++/video_binary.txt'
    output_video_path = 'reconstructed_video2.mp4'
    bitrate = '500k'  

    try:
        with open(input_file_path, 'r') as file:
            binary_string = file.read()

        binary_data = binary_string_to_binary(binary_string)
        
        # Use the original video parameters
        width, height = 320, 240
        duration = '00:00:07'
        audio_channels = '2'

        binary_to_video(binary_data, output_video_path, width, height, duration, audio_channels, bitrate)
        print(f"Video reconstructed and saved to {output_video_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
