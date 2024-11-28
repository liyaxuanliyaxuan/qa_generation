import os
import PyPDF2

def split_pdf(input_dir, output_dir, pages_per_file=5):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            pdf = PyPDF2.PdfReader(pdf_path)
            num_pages = len(pdf.pages)

            # 创建PDF名的子文件夹
            output_subdir = os.path.join(output_dir, os.path.splitext(filename)[0])
            if not os.path.exists(output_subdir):
                os.makedirs(output_subdir)

            # 分割PDF文件
            for start_page in range(0, num_pages, pages_per_file):
                end_page = min(start_page + pages_per_file, num_pages)
                output_pdf_path = os.path.join(output_subdir, f"{filename[:-4]}_{start_page}-{end_page}.pdf")

                # 创建PDF写入对象
                output_pdf = PyPDF2.PdfWriter()

                # 添加指定页码的页面
                for page_num in range(start_page, end_page):
                    page = pdf.pages[page_num]
                    output_pdf.add_page(page)

                # 写入PDF文件
                with open(output_pdf_path, "wb") as f:
                    output_pdf.write(f)

            print(f"Splitted {filename} into {output_subdir}")

# 设置输入目录和输出目录
input_directory = "./pdf"
output_directory = "./split"

# 调用函数
split_pdf(input_directory, output_directory)