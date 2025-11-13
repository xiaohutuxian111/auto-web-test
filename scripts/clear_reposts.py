import os
import shutil


def delete_test_result_dirs(root_dir: str):
    """
    删除指定目录下所有名称为 test_result 的文件夹
    :param root_dir: 根目录路径
    """
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        for dirname in dirnames:
            if dirname == "test-results" or dirname == "allure-results" or dirname == "logs":
                folder_path = os.path.join(dirpath, dirname)
                try:
                    shutil.rmtree(folder_path)
                    print(f"已删除: {folder_path}")
                except Exception as e:
                    print(f"删除失败 {folder_path}: {e}")


if __name__ == "__main__":
    root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    delete_test_result_dirs(root)
