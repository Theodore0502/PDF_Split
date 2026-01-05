import os
import argparse
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pypdf import PdfReader, PdfWriter

INPUT_DIR = r"E:\Spliter\TachFile\2013\Tháng 11\A231"
OUTPUT_DIR = r"E:\Spliter\TachFile\2013\Tháng 11\A231"


def split_pdf(input_path: str, out_dir: str = None):
    if out_dir is None:
        out_dir = OUTPUT_DIR
    
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    
    base_name = os.path.splitext(os.path.basename(input_path))[0].strip()
    
    # Tạo folder con có tên giống tên file PDF
    pdf_folder = os.path.join(out_dir, base_name)
    os.makedirs(pdf_folder, exist_ok=True)
    
    if total_pages == 1:
        writer = PdfWriter()
        writer.add_page(reader.pages[0])
        out_path = os.path.join(pdf_folder, f"{base_name}_Part1.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
    
    else:
        writer1 = PdfWriter()
        writer1.add_page(reader.pages[0])
        out_path1 = os.path.join(pdf_folder, f"{base_name}_Part1.pdf")
        with open(out_path1, "wb") as f:
            writer1.write(f)
        
        writer2 = PdfWriter()
        for i in range(1, total_pages):
            writer2.add_page(reader.pages[i])
        out_path2 = os.path.join(pdf_folder, f"{base_name}_Part2.pdf")
        with open(out_path2, "wb") as f:
            writer2.write(f)


def batch_split_all(input_dir: str, out_dir: str = None, max_workers: int = None):
    start_time = time.time()
    
    if out_dir is None:
        out_dir = OUTPUT_DIR
    
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"Không tìm thấy file PDF trong: {input_dir}")
        return
    
    # Sử dụng số CPU cores, mặc định là số cores của máy
    if max_workers is None:
        max_workers = os.cpu_count() or 4
    
    print(f"Tìm thấy {len(pdf_files)} file PDF. Đang xử lý song song với {max_workers} tiến trình...\n")
    
    # Xử lý song song
    success_count = 0
    error_count = 0
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Tạo các tasks
        future_to_file = {
            executor.submit(split_pdf, os.path.join(input_dir, pdf_file), out_dir): pdf_file 
            for pdf_file in pdf_files
        }
        
        # Xử lý kết quả khi hoàn thành
        for future in as_completed(future_to_file):
            pdf_file = future_to_file[future]
            try:
                future.result()
                success_count += 1
                print(f"✓ Hoàn thành: {pdf_file}")
            except Exception as e:
                error_count += 1
                print(f"✗ LỖI ({pdf_file}): {e}")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\n{'='*60}")
    print(f"Xử lý batch hoàn tất! Kết quả lưu tại: {out_dir}")
    print(f"📊 Thống kê: {success_count} thành công, {error_count} lỗi")
    print(f"⏱️  Tổng thời gian: {elapsed_time:.2f} giây ({elapsed_time/60:.2f} phút)")
    print(f"🚀 Tốc độ: {len(pdf_files)/elapsed_time:.2f} file/giây")


def main():
    parser = argparse.ArgumentParser(description="Tách PDF thành Part1 và Part2")
    parser.add_argument("input", nargs='?', default=INPUT_DIR, help=f"Đường dẫn file PDF HOẶC thư mục chứa các file PDF (mặc định: {INPUT_DIR})")
    parser.add_argument("-o", "--outdir", default=OUTPUT_DIR, help=f"Thư mục lưu kết quả (mặc định: {OUTPUT_DIR})")
    parser.add_argument("-b", "--batch", action="store_true", help="Chế độ batch: xử lý tất cả PDF trong thư mục")
    parser.add_argument("-w", "--workers", type=int, default=None, help=f"Số tiến trình song song (mặc định: {os.cpu_count()} cores)")
    
    args = parser.parse_args()
    
    if args.batch:
        batch_split_all(args.input, args.outdir, args.workers)
    else:
        split_pdf(args.input, args.outdir)


if __name__ == "__main__":
    main()
