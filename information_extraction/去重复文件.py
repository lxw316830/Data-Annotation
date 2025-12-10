import os
import hashlib
import shutil
from typing import List


def remove_duplicate_images_and_limit(
        file_list: List[str],
        source_folder: str,
        target_folder: str,
        max_files: int = 300
) -> None:
    """
    去除重复图片，并将最多 max_files 个不重复的图片复制到目标文件夹。

    :param file_list: 图片文件名列表（如 ['a.jpg', 'b.png']）
    :param source_folder: 源文件夹路径
    :param target_folder: 目标文件夹路径
    :param max_files: 最多保留多少个文件
    """
    seen_hashes = set()
    unique_files = []

    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)

    for file_name in file_list:
        if len(unique_files) >= max_files:
            break

        file_path = os.path.join(source_folder, file_name)

        # 跳过非文件（如子目录）
        if not os.path.isfile(file_path):
            continue

        try:
            # 计算 MD5 哈希
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            file_hash = hash_md5.hexdigest()

            if file_hash not in seen_hashes:
                seen_hashes.add(file_hash)
                unique_files.append(file_name)  # 保留文件名

                # 复制到目标文件夹
                dest_path = os.path.join(target_folder, file_name)
                shutil.copy2(file_path, dest_path)  # copy2 保留元数据
                print(f"已复制: {file_name}")

        except Exception as e:
            print(f"跳过文件 {file_name}: {e}")
            continue

    print(f"\n✅ 去重完成！共保留 {len(unique_files)} 个不重复图片。")
    print(f"📁 目标文件夹: {target_folder}")


# ================== 配置路径 ==================
source_dir = r"C:\Users\33908\Documents\文档\date\yolo-seg-唐文龙\img\yyzz"
target_dir = r"C:\Users\33908\Documents\pycharm\保定25.9.09智慧网办\information_extraction\uie_date\yyzz"  # 修改这里

# 获取源文件夹中所有文件
file_names = os.listdir(source_dir)

# 执行去重并复制
remove_duplicate_images_and_limit(
    file_list=file_names,
    source_folder=source_dir,
    target_folder=target_dir,
    max_files=300
)