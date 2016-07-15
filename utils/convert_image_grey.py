import os
from PIL import Image
"""
用于批量将图片转换成灰度图，根据需求分为
    1. 仅转换当前目录下的图片，不包括子目录：convert_currentdir_images
    2. 仅转换当前目录的单层子目录中的图片（对应数据集的格式）：convert_formatdir_images
    3. 转换该目录下所有的图片：convert_all_images
"""


def convert_currentdir_images(path, type='.jpg', resulttype='.jpg'):
    """仅转换当前目录下的图片，不包括子目录

    :param path: 文件路径
    :param type: 要转换的文件路径
    :param resulttype: 转换后的格式（可用于转换格式）
    """
    convert_grey_by_filelist(get_currentdir_image_path(path, type), resulttype)


def convert_formatdir_images(path, type='.jpg', resulttype='.jpg'):
    """仅转换当前目录的单层子目录中的图片（对应数据集的格式）

    :param path: 文件路径
    :param type: 要转换的文件路径
    :param resulttype: 转换后的格式（可用于转换格式）
    """
    convert_grey_by_filelist(get_format_image_path(path, type), resulttype)


def convert_all_images(path, type='.jpg', resulttype='.jpg'):
    """转换该目录下所有的图片

    :param path: 文件路径
    :param type: 要转换的文件路径
    :param resulttype: 转换后的格式（可用于转换格式）
    """
    convert_grey_by_filelist(get_all_image_path(path, [], type), resulttype)


def get_currentdir_image_path(path, type):
    """返回目录中所有JPG图像的文件名列表

    :param path: 文件夹路径
    :param type: 寻找的的图片类型
    :return: 所有获取到的图片路径
    """
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(type)]


def get_format_image_path(path, type):
    """按格式返回目录中的文件路径(对应训练数据集的格式，该文件夹下含有若干个子文件夹，获取这些子文件夹中的图片)

    :param path: 文件夹路径
    :param type: 寻找的的图片类型
    :return: 所有获取到的图片路径
    """
    filelist = []  # 存储每个图片的路径
    for dirname in os.listdir(path):
        path1 = os.path.join(path, dirname)  # 文件路径
        # 遍历每个文件夹的所有图片
        for filename in os.listdir(path1):
            if filename.endswith(type):
                filelist.append(os.path.join(path, dirname, filename))

    return filelist


def get_all_image_path(dir, fileList, type):
    """返回目录中的所有文件路径（包括各种格式）

    :param dir: 文件夹路径
    :param fileList: 空列表即可
    :param type: 找的的图片类型
    :return: 所有获取到的图片路径
    """
    newDir = dir
    # 如果当前是文件，则保存到列表
    if os.path.isfile(dir) and os.path.splitext(dir)[1] == type:
        fileList.append(dir)
    elif os.path.isdir(dir):  # 如果是文件夹，则继续递归寻找
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            # if s == "xxx":
                # continue
            newDir = os.path.join(dir, s)
            get_all_image_path(newDir, fileList, type)
    return fileList


def convert_grey_by_filelist(path_images, resulttype):
    """将图片转换成灰度图并保存

    :param path_images: 图片路径列表
    """
    for filename in path_images:
        # 转为灰度图
        img = Image.open(filename).convert('L')
        # 输出路径：取去了后缀的图片路径，并加上需要的后缀
        outfile = os.path.splitext(filename)[0] + resulttype
        # 保存图片
        img.save(outfile)
        print(filename + '---grey--->' + outfile)
    print('completely!')


if __name__ == '__main__':
    path = './images'  # 默认在同一目录的images文件夹下
    # convert_currentdir_images(path)
    convert_formatdir_images(path)
    # convert_all_images(path, '.jpg', '.png')