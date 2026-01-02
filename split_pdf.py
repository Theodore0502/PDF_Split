import os
import argparse
from pypdf import PdfReader, PdfWriter


OUTPUT_DIR = r"E:\Spliter\output"


def split_pdf(input_path: str, out_dir: str = None):
    if out_dir is None:
        out_dir = OUTPUT_DIR
    
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    
    os.makedirs(out_dir, exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    
    if total_pages == 1:
        writer = PdfWriter()
        writer.add_page(reader.pages[0])
        out_path = os.path.join(out_dir, f"{base_name}_Part1.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
        print(f"PDF has 1 page -> Created: {out_path}")
    
    else:
        writer1 = PdfWriter()
        writer1.add_page(reader.pages[0])
        out_path1 = os.path.join(out_dir, f"{base_name}_Part1.pdf")
        with open(out_path1, "wb") as f:
            writer1.write(f)
        
        writer2 = PdfWriter()
        for i in range(1, total_pages):
            writer2.add_page(reader.pages[i])
        out_path2 = os.path.join(out_dir, f"{base_name}_Part2.pdf")
        with open(out_path2, "wb") as f:
            writer2.write(f)
        
        print(f"PDF has {total_pages} pages -> Created:")
        print(f"  - {out_path1} (page 1)")
        print(f"  - {out_path2} (pages 2-{total_pages})")


def batch_split_all(input_dir: str, out_dir: str = None):
    if out_dir is None:
        out_dir = OUTPUT_DIR
    
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in: {input_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s). Processing...\n")
    
    for pdf_file in pdf_files:
        input_path = os.path.join(input_dir, pdf_file)
        print(f"Processing: {pdf_file}")
        try:
            split_pdf(input_path, out_dir)
        except Exception as e:
            print(f"  ERROR: {e}")
        print()
    
    print(f"Batch processing complete! Output saved to: {out_dir}")


def main():
    parser = argparse.ArgumentParser(description="Split PDF into Part1 and Part2")
    parser.add_argument("input", help="Input PDF file path OR directory containing PDFs")
    parser.add_argument("-o", "--outdir", default=OUTPUT_DIR, help=f"Output folder (default: {OUTPUT_DIR})")
    parser.add_argument("-b", "--batch", action="store_true", help="Batch mode: process all PDFs in the input directory")
    
    args = parser.parse_args()
    
    if args.batch:
        batch_split_all(args.input, args.outdir)
    else:
        split_pdf(args.input, args.outdir)


if __name__ == "__main__":
    main()
