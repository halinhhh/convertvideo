import subprocess
import os
import json

def get_video_info(input_video_path):
    """Lấy thông số của video sử dụng ffmpeg"""
    command = [
        '/opt/homebrew/bin/ffmpeg',
        '-i', input_video_path,
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        '-hide_banner',
        '-f', 'null', '-'
    ]
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if stderr:
        try:
            # Tìm kiếm thông tin JSON trong output
            start_idx = stderr.find(b'{')
            if start_idx != -1:
                info_json = stderr[start_idx:]
                return json.loads(info_json)
        except:
            pass

def video_to_binary(input_video_path, output_binary_path):
    """Chuyển đổi video thành dữ liệu nhị phân và lưu vào file"""
    print(f"Đang đọc video từ: {input_video_path}")
    
    # Lấy thông số video
    video_info = get_video_info(input_video_path)
    
    # Đọc video trực tiếp dưới dạng binary
    with open(input_video_path, 'rb') as video_file:
        binary_data = video_file.read()
    
    # Chuyển dữ liệu binary thành chuỗi '0' và '1'
    binary_string = ''.join(format(byte, '08b') for byte in binary_data)
    
    # Lưu chuỗi binary vào file text
    with open(output_binary_path, 'w') as output_file:
        output_file.write(binary_string)
    
    print(f"Đã chuyển đổi video thành chuỗi bit và lưu vào: {output_binary_path}")
    print(f"Kích thước video gốc: {len(binary_data)} bytes")
    print(f"Kích thước chuỗi bit: {len(binary_string)} ký tự")
    
    # Lưu thông tin video để sử dụng cho quá trình giải mã
    if video_info:
        with open(output_binary_path + '.info', 'w') as info_file:
            info_file.write(f"original_size={len(binary_data)}\n")
            info_file.write(f"input_video={input_video_path}\n")
            
            # Lưu các thông số quan trọng từ ffmpeg
            try:
                if 'streams' in video_info and len(video_info['streams']) > 0:
                    video_stream = next((s for s in video_info['streams'] if s['codec_type'] == 'video'), video_info['streams'][0])
                    
                    info_file.write(f"width={video_stream.get('width', 0)}\n")
                    info_file.write(f"height={video_stream.get('height', 0)}\n")
                    info_file.write(f"codec={video_stream.get('codec_name', '')}\n")
                    info_file.write(f"duration={video_stream.get('duration', video_info.get('format', {}).get('duration', 0))}\n")
                    info_file.write(f"bitrate={video_info.get('format', {}).get('bit_rate', 0)}\n")
                    
                    print(f"Đã lưu thông số video: {video_stream.get('width', 0)}x{video_stream.get('height', 0)}, codec: {video_stream.get('codec_name', '')}")
            except Exception as e:
                print(f"Không thể lưu đầy đủ thông số video: {e}")
    
    return binary_string

def main():
    # Sử dụng đường dẫn cố định 
    input_video_path = '/Users/linhha/Downloads/output_video.mp4'
    output_binary_path = '/Users/linhha/Downloads/video_binary.txt'
    
    print(f"Bắt đầu chuyển đổi video từ: {input_video_path}")
    print(f"Lưu kết quả vào: {output_binary_path}")
    
    if not os.path.exists(input_video_path):
        print(f"Lỗi: Không tìm thấy file {input_video_path}")
        return
    
    try:
        video_to_binary(input_video_path, output_binary_path)
        print("Chuyển đổi thành công!")
    except Exception as e:
        print(f"Lỗi khi chuyển đổi video: {e}")

if __name__ == "__main__":
    main()
