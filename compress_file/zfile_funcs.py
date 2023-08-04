import os
import zipfile
import py7zr
import pyzipper

# 加密zip文件的密码
password = b"password"

# 打开加密的zip文件
file_name = os.sep.join(['compress_file', 'testing', "uz4.zip"])
zip_file = zipfile.ZipFile(file_name)

# 获取zip文件中的加密文件名
encrypted_file = zip_file.namelist()[0]
print(f'{zip_file.filename=} {zip_file.infolist()[0].flag_bits} {zip_file.infolist()[0].compress_type=}')

# 设置密码
zip_file.setpassword(password)

# 解压所有文件到指定目录
zip_file.extractall("unzip_dir")
zip_file.extract(member=encrypted_file)

##
# 打开加密的zip文件
zip_file = py7zr.SevenZipFile(file_name, mode="r", password="password")

# 解压所有文件到指定目录
zip_file.extractall("unzip_dir")


# 关闭zip文件
zip_file.close()


##
with pyzipper.AESZipFile(file_name) as myzip:
    myzip.pwd = b'password'  # 设置密码
    myzip.extract(member='')
    myzip.extractall()
