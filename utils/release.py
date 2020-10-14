"""
发布说明：
一. 开发
为了防止共同开发引起代码错乱风险（暂于测试服务器内开发、无git做版本控制），统一在test_predictor内开发；

二. 自测
代码文件需要编译和执行自测脚本，运行成功则证明代码修改无逻辑错误，但是是否符合要求仍需要开发同事去查看日志文件进行比对；

三. 发布（这个脚本对新增的代码文件不会自动拷贝，需要仔细提前拷贝好）
1. 执行该python脚本将自动准备好待发布的文件
2. python3 release.py release.txt dl /opt/dinglei
   python3  执行脚本   配置脚本  版本号   输出目录
3. 配置文件格式
data:
***,***,***
conf:
***,***,***
code:
***,***,***
"""

import os
import sys
import time
import shutil

form_code2path_map = dict()
test_code2path_map = dict()
test_root_path = "/opt/predict/predictor/test_predictor"
formal_root_path = "/opt/predict/predictor/dsp_predictor"
history_dir = "/opt/predict/predictor/history"
build_dir = "/opt/predict/predictor/dsp_predictor/build"
so_name = "libmtai.so"
so_touch_name = "libmtai.so.touch"

# 替换操作
replace_cmd = 'sed -i "s/\/opt\/predict\/predictor\/test_predictor/\/opt\/predict\/predictor\/{t1}/g" {t2}'


def main(release_config, version="tj", save_path="."):
    suffix = version+"_"+time.strftime('%m%d_%H%M', time.localtime(time.time()))
    save_path = os.path.join(
        save_path, suffix
    )
    if os.path.exists(save_path):
        print("warning! already exists this dir 【{}】, please check!".format(save_path))
        return
    os.mkdir(save_path)

    # 读取待发布的配置文件
    release_files = {
        "data": [],
        "conf": [],
        "code": []
    }
    curr_key = ""
    with open(release_config, "r") as fin:
        for line in fin:
            line = line.strip().strip(":")
            if line == "" or line[0] == "#" or line[0] == "//":
                continue
            elif line in ["data", "conf", "code"]:
                curr_key = line
            elif curr_key != "":
                release_files[curr_key] = [x.strip() for x in line.split(",")]
    # print(release_files)
    for k, v in release_files.items():
        if v:
            if k == "code":
                k = "lib"
            os.mkdir(os.path.join(save_path, k))

    # 拷贝配置文件到正式目录和指定待发布目录
    for key in ["data", "conf"]:
        from_data_dir = os.path.join(test_root_path, key)
        for ele in release_files[key]:
            if ele == "log4cpp.conf":
                continue
            to_file1 = os.path.join(save_path, key, ele)
            to_file2 = os.path.join(formal_root_path, key, ele)
            shutil.copy(
                os.path.join(from_data_dir, ele), to_file1
            )
            if os.path.exists(to_file2):
                shutil.copy(to_file2, os.path.join(history_dir, key, ele+"_"+suffix))
            shutil.copy(
                os.path.join(from_data_dir, ele), to_file2
            )
            os.system(replace_cmd.format(t1="", t2=to_file1))
            os.system(replace_cmd.format(t1="dsp_predictor", t2=to_file2))

    # 拷贝代码到正式目录进行编译
    form_file_path_map(os.path.join(formal_root_path, "src"))
    test_file_path_map(os.path.join(test_root_path, "src"))
    for cf in release_files["code"]:
        if cf in test_code2path_map:
            modify_file = test_code2path_map[cf]
            if cf in form_code2path_map:
                ori_file = form_code2path_map[cf]
                shutil.copy(ori_file, os.path.join(history_dir, "code", cf+"_"+suffix))
                shutil.copy(modify_file, ori_file)
            else:
                print("【{}】 is a new file, you need to cp it manually for first time".format(cf))
        else:
            print("cannot find 【{}】 in test_predictor dir, please check".format(cf))

    # 开始编译
    if len(release_files["code"]) > 0:
        os.chdir(build_dir)
        sub_files = os.listdir(".")
        if "CMakeCache.txt" not in sub_files or "Makefile" not in sub_files:
            os.system("cmake ../src")
        outcome = os.system("make clean && make -j4")
        if outcome == 0:
            so_version = -1 
            if os.path.exists(so_touch_name):
                with open(so_touch_name, "r") as t_fin:
                    for line in t_fin:
                        so_version = int(line.strip())
                        break
            so_version += 1
            os.system("echo {so_ver} > {so_touch}".format(so_ver=so_version, so_touch=so_touch_name))
            release_so_name = so_name+"."+str(so_version)
            shutil.copy(so_name, release_so_name)
            shutil.copy(so_touch_name, os.path.join(save_path, "lib"))
            shutil.copy(release_so_name, os.path.join(save_path, "lib"))
        else:
            print("compile c++ code failed, please check!")


def form_file_path_map(root_dir):
    global form_code2path_map
    children = os.listdir(root_dir)
    for child in children:
        tmp_path = os.path.join(root_dir, child)
        if os.path.isfile(tmp_path):
            form_code2path_map[child] = tmp_path
        elif os.path.isdir(tmp_path):
            form_file_path_map(tmp_path)


def test_file_path_map(root_dir):
    global test_code2path_map
    children = os.listdir(root_dir)
    for child in children:
        tmp_path = root_dir + "/" + child
        if os.path.isfile(tmp_path):
            test_code2path_map[child] = tmp_path
        elif os.path.isdir(tmp_path):
            test_file_path_map(tmp_path)


if __name__ == "__main__":
    args1 = sys.argv
    assert len(args1) >= 4
    release_config1, version1, save_path1 = args1[1:4]
    main(release_config1, version1, save_path1)


