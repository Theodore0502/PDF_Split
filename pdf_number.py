import os
import sys
import shutil
from pathlib import Path

# ============================================================
# CẤU HÌNH: Thay đổi đường dẫn folder ở đây
# ============================================================
INPUT_FOLDER = r"E:\Spliter\TachFile\2013\Tháng 12\A232"   # Thư mục chứa file gốc
OUTPUT_FOLDER = r"E:\Spliter\OUTPUT_NUMBERED"               # Thư mục lưu file đã đánh số
# ============================================================


def get_files_with_time(input_dir):
    """Lấy danh sách file và thời gian modified"""
    files_info = []
    
    try:
        for item in os.listdir(input_dir):
            item_path = os.path.join(input_dir, item)
            
            # Chỉ xử lý file, bỏ qua thư mục
            if os.path.isfile(item_path):
                # Lấy thời gian modified
                modified_time = os.path.getmtime(item_path)
                files_info.append((item_path, item, modified_time))
    
    except Exception as e:
        print(f"Lỗi khi đọc thư mục: {e}")
        return []
    
    # Sắp xếp theo thời gian modified (cũ nhất lên đầu)
    files_info.sort(key=lambda x: x[2])
    
    return files_info


def create_numbered_files(files_info, output_dir):
    """Tạo danh sách file với số thứ tự"""
    numbered_files = []
    
    for index, (input_path, original_name, modified_time) in enumerate(files_info, start=1):
        # Tạo tên mới với số thứ tự
        new_name = f"{index:02d}.{original_name}"
        output_path = os.path.join(output_dir, new_name)
        
        numbered_files.append((input_path, output_path, original_name, new_name, modified_time))
    
    return numbered_files


def preview_changes(numbered_files):
    """Hiển thị preview các thay đổi sẽ được thực hiện"""
    if not numbered_files:
        print("Không có file nào cần xử lý!")
        return False
    
    print(f"\nSẽ đánh số thứ tự cho {len(numbered_files)} file(s):")
    print("=" * 80)
    
    from datetime import datetime
    
    for input_path, output_path, old_name, new_name, modified_time in numbered_files:
        # Chuyển timestamp thành datetime để hiển thị
        dt = datetime.fromtimestamp(modified_time)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        print(f"  {new_name:<40} | {time_str}")
    
    print("=" * 80)
    return True


def process_files(numbered_files, output_dir, auto_confirm=False):
    """Sao chép và đánh số thứ tự cho các file"""
    if not preview_changes(numbered_files):
        return
    
    # Xác nhận từ người dùng
    if not auto_confirm:
        response = input("\nBạn có muốn tiếp tục? (y/n): ").strip().lower()
        if response != 'y':
            print("Đã hủy thao tác.")
            return
    
    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)
    
    # Thực hiện sao chép với tên mới
    success_count = 0
    error_count = 0
    
    print("\nĐang xử lý file...")
    for input_path, output_path, old_name, new_name, modified_time in numbered_files:
        try:
            shutil.copy2(input_path, output_path)
            success_count += 1
            print(f"✓ {new_name}")
        except Exception as e:
            error_count += 1
            print(f"✗ Lỗi khi xử lý {old_name}: {e}")
    
    # Tổng kết
    print("\n" + "=" * 80)
    print(f"Hoàn thành! Thành công: {success_count}, Lỗi: {error_count}")
    print(f"Kết quả lưu tại: {os.path.abspath(output_dir)}")
    print("=" * 80)


def main():
    """Hàm chính"""
    print("=" * 80)
    print("CHƯƠNG TRÌNH ĐÁNH SỐ THỨ TỰ FILE THEO THỜI GIAN")
    print("=" * 80)
    
    # Lấy thư mục input
    if len(sys.argv) > 2:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        print(f"\n📁 INPUT mặc định: {INPUT_FOLDER}")
        print(f"📁 OUTPUT mặc định: {OUTPUT_FOLDER}")
        print()
        
        input_dir = input("Nhập đường dẫn INPUT (Enter để dùng mặc định): ").strip()
        if not input_dir:
            input_dir = INPUT_FOLDER
        
        output_dir = input("Nhập đường dẫn OUTPUT (Enter để dùng mặc định): ").strip()
        if not output_dir:
            output_dir = OUTPUT_FOLDER
    
    # Kiểm tra thư mục input có tồn tại không
    if not os.path.isdir(input_dir):
        print(f"Lỗi: Thư mục INPUT '{input_dir}' không tồn tại!")
        return
    
    print(f"\n📂 INPUT:  {os.path.abspath(input_dir)}")
    print(f"📂 OUTPUT: {os.path.abspath(output_dir)}")
    
    # Lấy danh sách file với thời gian
    files_info = get_files_with_time(input_dir)
    
    # Tạo danh sách file đã đánh số
    numbered_files = create_numbered_files(files_info, output_dir)
    
    # Xử lý file
    process_files(numbered_files, output_dir)


if __name__ == "__main__":
    main()
