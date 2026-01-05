# 📚 Hướng dẫn sử dụng PDF Tools

Bộ công cụ xử lý file PDF hàng loạt với 3 chức năng chính.

---

## 🔧 Các công cụ

### 1. **split_pdf.py** - Tách file PDF

Tách PDF thành 2 phần: trang 1 và phần còn lại

**Cấu hình:**

```python
INPUT_DIR = r"E:\Spliter\TachFile\2013\Tháng 11\A231"
OUTPUT_DIR = r"E:\Spliter\TachFile\2013\Tháng 11\A231"
```

**Chạy:**

```bash
python split_pdf.py --batch
```

**Tùy chọn:**

- `--batch` : Xử lý tất cả file trong thư mục (song song, nhanh)
- `--workers 4` : Giới hạn số CPU cores (mặc định: dùng hết)
- `python split_pdf.py "file.pdf"` : Xử lý 1 file

---

### 2. **pdf_name.py** - Thêm đuôi .pdf vào tên file

Sao chép file từ INPUT sang OUTPUT và thêm `.pdf` vào tên file chưa có đuôi

**Cấu hình:**

```python
INPUT_FOLDER = r"E:\Spliter\TachFile\2013\Tháng 12\A232"
OUTPUT_FOLDER = r"E:\Spliter\OUTPUT"
```

**Chạy:**

```bash
python pdf_name.py
```

Sau đó nhấn Enter 2 lần để dùng thư mục mặc định, hoặc nhập đường dẫn tùy chỉnh.

---

### 3. **pdf_number.py** - Đánh số thứ tự file

Đánh số 01. 02. 03... vào đầu tên file dựa theo thời gian modified (cũ → mới)

**Cấu hình:**

```python
INPUT_FOLDER = r"E:\Spliter\TachFile\2013\Tháng 12\A232"
OUTPUT_FOLDER = r"E:\Spliter\OUTPUT_NUMBERED"
```

**Chạy:**

```bash
python pdf_number.py
```

Sau đó nhấn Enter 2 lần để dùng thư mục mặc định, hoặc nhập đường dẫn tùy chỉnh.

**Kết quả:**

```
01.Xa Đức Sinh.pdf
02.Nguyễn Hữu Thọ.pdf
03.Vũ Đình Toản.pdf
...
```

---

## 💡 Tips

- Mở terminal: `Ctrl + ~`
- Tất cả file đều giữ nguyên file gốc (sao chép, không xóa)
- Thay đổi đường dẫn mặc định ở đầu mỗi file .py

---

## ⚡ Hiệu năng

- **split_pdf.py**: ~7-17 file/giây (xử lý song song)
- **pdf_name.py**: Tức thì với file nhỏ
- **pdf_number.py**: Tức thì với file nhỏ
