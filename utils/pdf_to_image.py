import fitz
import os


def pdf_to_images(pdf_path, output_folder, zoom=2.0):
    """
    将 PDF 文件的前六页转换为图片（PNG 格式）

    :param pdf_path: PDF 文件路径
    :param output_folder: 输出图片的文件夹路径
    :param zoom: 分辨率缩放因子，值越大越清晰（1.0 = 72dpi, 2.0 = 144dpi）
    """
    # 打开 PDF
    pdf_document = fitz.open(pdf_path)

    # 创建输出目录
    os.makedirs(output_folder, exist_ok=True)

    # 设置矩阵以控制分辨率
    matrix = fitz.Matrix(zoom, zoom)

    # 遍历前六页（或更少）
    for page_num in range(min(6, pdf_document.page_count)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(matrix=matrix)  # 渲染为像素图
        image_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        pix.save(image_path)
        print(f"已保存: {image_path}")

    pdf_document.close()
    print("转换完成！")