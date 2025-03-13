import os
import cv2
import numpy as np
import argparse

def stitch_images_horizontal(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    if not image_files:
        print("No images found in the directory.")
        return
    
    images = [cv2.imdecode(np.fromfile(os.path.join(folder_path, f), dtype=np.uint8), cv2.IMREAD_COLOR) for f in image_files]
    
    # 过滤掉加载失败的图像
    images = [img for img in images if img is not None]
    if not images:
        print("No valid images loaded.")
        return
    
    # 获取所有图片中的最大高度
    max_height = max(img.shape[0] for img in images)
    
    # 计算等比例缩放后的宽度
    resized_images = []
    for img in images:
        h, w = img.shape[:2]
        scale = max_height / h
        new_width = int(w * scale)
        resized_img = cv2.resize(img, (new_width, max_height), interpolation=cv2.INTER_LINEAR)
        resized_images.append(resized_img)
    
    # 水平拼接所有图片
    stitched_image = np.hstack(resized_images)
    
    # 计算缩放倍数（输出宽度 / 图片数量）
    num_images = len(resized_images)
    output_width = stitched_image.shape[1] // num_images
    output_height = stitched_image.shape[0] // num_images
    stitched_image_resized = cv2.resize(stitched_image, (output_width, output_height), interpolation=cv2.INTER_AREA)
    
    # 创建 output 文件夹
    output_folder = os.path.join(folder_path, "output")
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "stitched_image.jpg")
    
    # 保存拼接后的图片（支持中文路径）
    cv2.imencode(".jpg", stitched_image_resized)[1].tofile(output_path)
    print(f"Stitched image saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stitch images horizontally.")
    parser.add_argument("folder_path", type=str, nargs="?", help="Path to the folder containing images.")
    args = parser.parse_args()
    
    if not args.folder_path:
        print("Error: No folder path provided. Please specify a directory containing images.")
        print("Usage: python script.py /path/to/images")
    else:
        stitch_images_horizontal(args.folder_path)