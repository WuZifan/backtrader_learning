import os
import re


def modify_doc_title_dir(abspath_rstfiles_dir):
    """
    rst文件中：有‘========’和‘----------’行的表示其行上一行的文字是标题，
    ‘=’和‘-’要大于等于标题的长度。
    使用sphinx-apidoc -o ./source/rst_files /home/myubuntu/pro/mypro命令将
    生成rst文件放在./source/rst_files目录下。 或在source目录下新建
    rst_files目录然后将rst文件剪切到这个目录下，修改后再剪切出来
    生成rst文件后将rst_files/modules.rst文件中的标题去掉，并修改maxdepth字段。
    删除和修改使用sphinx-apidoc -o 命令的生成的rst文件中的标题
    :param abspath_rstfiles_dir: rst文件所在的文件夹的绝对路径
    :return:
    """
    rst_files = os.listdir(abspath_rstfiles_dir)
    # 要删除的节点(标题目录的节点)
    del_nodes = ['Submodules', 'Module contents', 'Subpackages']
    # 要删除的标题中的字符串
    del_str = [' module', ' package']
    for rst_file in rst_files:
        f = open(os.path.join(abspath_rstfiles_dir, rst_file), 'r')
        file_lines = f.readlines()
        f.close()
        write_con = []
        flag = 0
        for file_line in file_lines:
            if file_line.strip() in del_nodes:
                flag = 1
                continue
            if flag:
                flag = 0
                continue
            if re.search(del_str[0], file_line):
                modify_line = file_line.split('.')[-1].replace(del_str[0], '.py')
                write_con.append(modify_line)
                continue
            if re.search(del_str[1], file_line):
                modify_line = file_line.split('.')[-1].replace(del_str[1], '')
                write_con.append(modify_line)
                continue
            write_con.append(file_line)
        f = open(os.path.join(abspath_rstfiles_dir, rst_file), 'w')
        f.writelines(write_con)
        f.close()


if __name__ == '__main__':

    rst_files_abs_path = os.path.abspath('./source/rst_files')
    modify_doc_title_dir(rst_files_abs_path)