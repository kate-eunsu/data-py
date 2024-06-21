# %%
from PIL import Image
import os


def resize_and_convert_to_webp(source_folder, target_folder, width=1000):
    # 대상 폴더가 없으면 생성
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 소스 폴더 내의 모든 파일을 순회
    for filename in os.listdir(source_folder):

        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            continue  # 이미지 파일이 아니면 건너뛰기

        # 이미지 파일 경로 생성
        img_path = os.path.join(source_folder, filename)
        # 이미지 로드
        with Image.open(img_path) as img:
            print(img_path)
            # 가로 사이즈가 600보다 크면 조정
            if img.width > width:
                # 높이는 가로 사이즈 비율에 맞춰 조정
                height = int((width / img.width) * img.height)
                img = img.resize((width, height))

            # 파일명에서 확장자 제거
            base_filename = os.path.splitext(filename)[0]
            # 대상 폴더에 webp 포맷으로 저장
            img.save(os.path.join(target_folder,f"{base_filename}.webp"), "WEBP")


# 사용 예
source_folder = 'images'
target_folder = 'output'
resize_and_convert_to_webp(source_folder, target_folder)
# %%