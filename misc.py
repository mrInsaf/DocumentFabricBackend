import os
import qrcode
from docx.shared import Inches
from docx import Document as DocxDocument

def add_qr_to_docx(docx_path, qr_data, output_path):
    # Создаем QR-код
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Генерируем изображение QR-кода
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img_path = "qr_code.png"
    qr_img.save(qr_img_path)

    # Загружаем документ
    doc = DocxDocument(docx_path)

    # Вставляем пустой параграф в начало документа
    first_paragraph = doc.paragraphs[0]  # Получаем первый параграф
    new_paragraph = doc.add_paragraph()  # Создаем новый параграф

    # Вставляем QR-код в новый параграф
    new_paragraph.add_run().add_picture(qr_img_path, width=Inches(2))  # Указываем ширину в дюймах

    # Перемещаем новый параграф перед первым абзацем
    doc._element.body.insert(0, new_paragraph._element)  # Вставляем элемент нового параграфа в начало

    # Сохраняем новый документ
    doc.save(output_path)

    # Удаляем временный QR-код
    os.remove(qr_img_path)

# Пример использования
# add_qr_to_docx('input.docx', 'https://example.com', 'output.docx')
