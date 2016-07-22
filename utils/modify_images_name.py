import convert_image_grey
import os
"""
用于按序号依次递增转换文件夹下所有图片名
"""


def modify_name_by_sequence(path, type='.jpg'):
    """用于按序号依次递增转换文件夹下所有图片名

    :param path: 文件夹路径
    :param type: 要修改的文件类型
    """
    # 得到目录下所有jpg文件路径
    filelist = convert_image_grey.get_all_image_path(path, [], type)
    index = 1
    for oldfiles in filelist:
        # 获取文件路径
        dirpath = os.path.dirname(oldfiles)
        # 生成新文件名
        newfilename = str(index) + type
        # 连接目录与文件名
        newfiles = os.path.join(dirpath, newfilename)
        # 重命名文件
        os.rename(oldfiles, newfiles)
        print(oldfiles + '-->' + newfiles)
        index += 1
    print('Completed! modify ' + str(index) + ' images')

if __name__ == '__main__':
    # 默认在images文件夹下
    modify_name_by_sequence('./images')
    # modify_name_by_sequence('C:/Users/35492/Desktop/手势数据集/数据集4/Set1')
