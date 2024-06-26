import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

# Tesseract 경로 설정
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # Tesseract 설치 경로를 설정

# PDF 파일 열기
pdf_document = "./python/건축물대장.pdf"  # PDF 파일 경로 설정
doc = fitz.open(pdf_document)

# 출력 디렉토리 설정
output_dir = "output_images"
os.makedirs(output_dir, exist_ok=True)

# 페이지 순회
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    
    # 페이지에서 이미지 추출
    image_list = page.get_images(full=True)
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]  # 이미지 확장자

        # 이미지 열기
        image = Image.open(io.BytesIO(image_bytes))

        # 추출된 이미지 저장
        image_path = os.path.join(output_dir, f"page_{page_num+1}_image_{img_index+1}.{image_ext}")
        image.save(image_path)
        print(f"Extracted image saved to {image_path}")

        # OCR 수행
        text = pytesseract.image_to_string(image, lang="kor")  # 한국어 OCR
        print(f"Page {page_num+1} - Image {img_index+1} OCR Result:\n{text}\n")

        # OCR 결과를 파일로 저장 (옵션)
        with open(f"page_{page_num+1}_image_{img_index+1}.txt", "w", encoding="utf-8") as f:
            f.write(text)
