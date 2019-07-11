# coding: utf-8
"""
清洗图片数据，将指定文件夹内的图书数据统一为RGB模式
测试在 python3
"""
import glob
from PIL import Image
import os
import shutil
import argparse
import warnings


def main():
    parser = argparse.ArgumentParser(description='script params')
    parser.add_argument('-target_dir', type=str, help='Directory to clean')
    parser.add_argument('--trash_dir', type=str, default=None, help='Directory to save original picture')
    parser.add_argument('--change_ext', type=bool, default=False, help='If changing file extension name to .jpg')
    opt = parser.parse_args()

    target_dir = opt.target_dir
    trash_dir = opt.trash_dir
    change_ext = opt.change_ext

    if trash_dir:
        print('Target directory is {}, trash directory is {}.'.format(target_dir, trash_dir))
    else:
        print('Target directory is {}, trash directory is None. Original picture will be deleted.'.format(target_dir))

    files = glob.glob(os.path.join(target_dir, '*'))
    for f in files:
        remove_exif_info = False
        with warnings.catch_warnings():
            try:
                img = Image.open(f)
                img.load()
            except UserWarning as w:
                print(f, w)
                remove_exif_info = True
            except Exception as e:
                print(f, e)
                if trash_dir:
                    shutil.move(f, os.path.join(trash_dir, f.split('/')[-1]))
                else:
                    os.remove(f)
                continue
        if img.mode == 'RGBA':
            new_img = Image.new('RGB', img.size, (255, 255, 255))
            new_img.paste(img, mask=img.split()[3])
            if trash_dir:
                shutil.move(f, os.path.join(trash_dir, f.split('/')[-1]))
            save_file = f if not change_ext else f[:f.rindex('.')] + '.jpg'
            new_img.save(save_file, 'JPEG', quality=80)
        elif img.mode == 'P':
            if trash_dir:
                shutil.move(f, os.path.join(trash_dir, f.split('/')[-1]))
            save_file = f if not change_ext else f[:f.rindex('.')] + '.jpg'
            img.convert('RGB').save(save_file, 'JPEG', quality=80)
        elif remove_exif_info and 'exif' in img.info:
            new_img = Image.new(img.mode, img.size)
            new_img.putdata(list(img.getdata()))
            if trash_dir:
                shutil.move(f, os.path.join(trash_dir, f.split('/')[-1]))
            save_file = f if not change_ext else f[:f.rindex('.')] + '.jpg'
            new_img.save(save_file, 'JPEG', quality=80)


if __name__ == '__main__':
    main()
