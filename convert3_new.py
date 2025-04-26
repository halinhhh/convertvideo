import os
import subprocess

def binary_string_to_binary(binary_string):
    """Chuyển đổi chuỗi bit thành dữ liệu nhị phân"""
    print(f"Đang chuyển đổi chuỗi bit dài {len(binary_string)} ký tự...")
    binary_data = bytes(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8))
    print(f"Đã chuyển đổi thành {len(binary_data)} bytes dữ liệu nhị phân")
    return binary_data

def main():
    input_binary_path = input("Nhập đường dẫn đến file chuỗi bit: ") or "video_binary.txt"
    output_video_path = input("Nhập đường dẫn lưu video đầu ra: ") or "reconstructed_video.mp4"
    
    if not os.path.exists(input_binary_path):
        print(f"Lỗi: Không tìm thấy file {input_binary_path}")
        return
    
    # Đọc thông số video từ file info
    info_file_path = input_binary_path + '.info'
    video_info = {}
    
    if os.path.exists(info_file_path):
        print(f"Đang đọc thông tin video từ {info_file_path}")
        with open(info_file_path, 'r') as info_file:
            for line in info_file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    video_info[key] = value
        
        print(f"Đã đọc thông số video: {video_info}")
    
    try:
        print(f"Đang đọc chuỗi bit từ: {input_binary_path}")
        with open(input_binary_path, 'r') as input_file:
            binary_string = input_file.read()
        
        print(f"Đã đọc {len(binary_string)} ký tự")
        
        # Chuyển chuỗi bit thành dữ liệu nhị phân
        binary_data = binary_string_to_binary(binary_string)
        
        # Kiểm tra kích thước nếu có thông tin
        if 'original_size' in video_info and int(video_info['original_size']) != len(binary_data):
            print(f"Cảnh báo: Kích thước dữ liệu khôi phục ({len(binary_data)} bytes) khác với kích thước gốc ({video_info['original_size']} bytes)")
        
        # Lưu dữ liệu nhị phân vào file tạm
        temp_file = 'temp_binary.mp4'
        with open(temp_file, 'wb') as temp:
            temp.write(binary_data)
        
        # Sử dụng ffmpeg để xử lý file nếu có thông số
        if 'width' in video_info and 'height' in video_info:
            # Tạo lệnh ffmpeg với thông số từ file gốc
            command = [
                '/opt/homebrew/bin/ffmpeg',
                '-i', temp_file,
                '-c:v', video_info.get('codec', 'libx264'),
            ]
            
            if 'bitrate' in video_info:
                command.extend(['-b:v', video_info['bitrate']])
            
            if 'duration' in video_info:
                command.extend(['-t', video_info['duration']])
            
            command.append(output_video_path)
            
            print(f"Đang xử lý video với ffmpeg: {' '.join(command)}")
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"Lỗi khi xử lý video với ffmpeg: {stderr.decode()}")
                print("Thực hiện phục hồi trực tiếp không qua ffmpeg...")
                os.rename(temp_file, output_video_path)
            else:
                os.remove(temp_file)
                print(f"Đã xử lý video thành công với ffmpeg!")
        else:
            # Nếu không có thông số, lưu trực tiếp
            os.rename(temp_file, output_video_path)
        
        print(f"Tạo video thành công: {output_video_path}")
        print(f"Kích thước file video: {os.path.getsize(output_video_path)} bytes")
        
    except Exception as e:
        print(f"Lỗi khi khôi phục video: {e}")

if __name__ == "__main__":
    main()
