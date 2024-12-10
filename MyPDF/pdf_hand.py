# 拆分pdf
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
from PyPDF2 import PdfReader
from pdf2docx import Converter
import os
from OtherFunctions.logdefine import MyLogging
from docx import Document
mlogger = MyLogging(file=f"./log.log")

class MyPDF:
    def __init__(self, inputPDF, save_dirpath):
        self.input = inputPDF
        self.save_dirpath = save_dirpath

    def split_pdf(self, step=5):
        """
        拆分PDF为多个小的PDF文件
        @param step: 每step间隔的页面生成一个文件，例如step=5，表示0-4页、5-9页...为一个文件
        @return:
        """
        for i in self.input:
            pdf_reader = PdfReader(i)
            # 读取每一页的数据
            pages = len(pdf_reader.pages)
            for page in range(0, pages, step):
                pdf_writer = PdfWriter()
                # 拆分pdf，每 step 页的拆分为一个文件
                for index in range(page, page + step):
                    if index < pages:
                        pdf_writer.add_page(pdf_reader.pages[index])
                        # 保存拆分后的小文件
                filename = os.path.basename(i).rsplit('.', 1)[0]
                save_path = os.path.join(self.save_dirpath, filename + str(int(page / step) + 1) + '.pdf')
                with open(save_path, "wb") as out:
                    pdf_writer.write(out)
                mlogger.info(f"文件已成功拆分，保存路径为：{save_path}")

    def concat_pdf(self):
        """
        合并多个PDF文件
        @return:
        """
        pdf_writer = PdfWriter()
        # 对文件名进行排序
        self.input.sort(key=lambda x: os.path.basename(x))
        for filename in self.input:
            mlogger.info(f'{filename}')
            # 读取文件并获取文件的页数
            pdf_reader = PdfReader(filename)
            pages = len(pdf_reader.pages)
            # 逐页添加
            for page in range(pages):
                pdf_writer.add_page(pdf_reader.pages[page])
        # 保存合并后的文件
        save_filepath = os.path.join(self.save_dirpath, '合并后.pdf')
        with open(save_filepath, "wb") as out:
            pdf_writer.write(out)
        mlogger.info(f"文件已成功合并，保存路径为：{save_filepath}")

    def pdf2doc(self, start: int = 0, end: int = None, pages: list = None):

        for pdf_file in self.input:
            save_filepath = os.path.join(self.save_dirpath, os.path.basename(pdf_file).rsplit('.', 1)[0] + '.docx')
            cv = Converter(pdf_file)
            cv.convert(save_filepath, start, end, pages)  # 默认参数start=0, end=None
            cv.close()
            mlogger.info(f"PDF转WORD完成，保存路径为：{save_filepath}")

    # PDF转可编辑word
    def pdf2word(self):
        for pdf_file in self.input:
            # 打开PDF文件pdf
            pdf = open(pdf_file, 'rb')
            # 创建一个PDF读取器对象
            pdf_reader = PdfReader(pdf)
            # print(pdf_reader._get_num_pages())
            # 创建一个word文档对象
            doc = Document()
            # 读取PDF文件中的每一页，并将其转换为Word文档中的段落
            for page_num in range(pdf_reader._get_num_pages()):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                doc.add_paragraph(text)
            # 保存word文档
            save_filepath = os.path.join(self.save_dirpath, os.path.basename(pdf_file).rsplit('.', 1)[0] + '.docx')
            doc.save(save_filepath)
            # 关闭PDF文件
            pdf.close()
        return '转换成可编辑word完成'

    def pdf2low(self):
        for pdf_file in self.input:
            save_filepath = os.path.join(self.save_dirpath, os.path.basename(pdf_file).rsplit('.', 1)[0] + '.pdf')
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)
            with open(save_filepath, 'wb') as f:
                writer.write(f)
        return 'PDF文件压缩完成'


app = MyPDF([r'E:\Desktop\全国通信专业技术人员职业水平考试-王心悦.pdf'], r'E:\Desktop\pdf')
app.pdf2word()
