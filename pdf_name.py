import os
import sys
from pathlib import Path

# ============================================================
# CẤU HÌNH: Thay đổi đường dẫn folder ở đây
# ============================================================
INPUT_FOLDER = r"E:\Spliter\TachFile\2013\Tháng 11\A231"
OUTPUT_FOLDER = r"E:\Spliter\output"
# ============================================================


def get_files_to_rename(input_dir, output_dir):
    """Lấy danh sách các file cần đổi tên (chưa có đuôi .pdf)"""
    files_to_rename = []
    
    try:
        for item in os.listdir(input_dir):
            input_path = os.path.join(input_dir, item)
            
            # Chỉ xử lý file, bỏ qua thư mục
            if os.path.isfile(input_path):
                # Kiểm tra xem file đã có đuôi .pdf chưa
                if not item.lower().endswith('.pdf'):
                    output_path = os.path.join(output_dir, item + '.pdf')
                    files_to_rename.append((input_path, output_path, item, item + '.pdf'))
                else:
                    # File đã có .pdf, copy nguyên vẹn
                    output_path = os.path.join(output_dir, item)
                    files_to_rename.append((input_path, output_path, item, item))
    
    except Exception as e:
        print(f"Lỗi khi đọc thư mục: {e}")
        return []
    
    return files_to_rename


def preview_changes(files_to_rename):
    """Hiển thị preview các thay đổi sẽ được thực hiện"""
    if not files_to_rename:
        print("Không có file nào cần xử lý!")
        return False
    
    print(f"\nSẽ xử lý {len(files_to_rename)} file(s):")
    print("-" * 80)
    
    for input_path, output_path, old_name, new_name in files_to_rename:
        if old_name != new_name:
            print(f"  ✎ {old_name} -> {new_name}")
        else:
            print(f"  ✓ {old_name}")
    
    print("-" * 80)
    return True


def process_files(files_to_rename, output_dir, auto_confirm=False):
    """Sao chép và đổi tên các file"""
    if not preview_changes(files_to_rename):
        return
    
    # Xác nhận từ người dùng
    if not auto_confirm:
        response = input("\nBạn có muốn tiếp tục? (y/n): ").strip().lower()
        if response != 'y':
            print("Đã hủy thao tác.")
            return
    
    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)
    
    # Thực hiện sao chép và đổi tên
    success_count = 0
    error_count = 0
    
    print("\nĐang xử lý file...")
    for input_path, output_path, old_name, new_name in files_to_rename:
        try:
            import shutil
            shutil.copy2(input_path, output_path)
            success_count += 1
            if old_name != new_name:
                print(f"✓ Đã đổi tên: {old_name} -> {new_name}")
            else:
                print(f"✓ Đã sao chép: {old_name}")
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
    print("CHƯƠNG TRÌNH ĐỔI TÊN FILE HÀNG LOẠT - THÊM ĐUÔI .PDF")
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
    
    # Lấy danh sách file cần đổi tên
    files_to_rename = get_files_to_rename(input_dir, output_dir)
    
    # Xử lý file
    process_files(files_to_rename, output_dir)


if __name__ == "__main__":
    main()
