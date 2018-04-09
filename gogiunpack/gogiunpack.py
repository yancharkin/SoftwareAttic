#!/usr/bin/env python

import os
import sys
import shutil
import time
import subprocess
import zlib

def unpack_gog_installer(installer, unpack_to):

    files_dict = {}
    chunks_dict = {}
    files_chunks_dict = {}

    if not os.path.exists(unpack_to):
        os.makedirs(unpack_to)

    if sys.platform.startswith('linux'):

        if unpack_to[-1] != '/':
            unpack_to += '/'

        files_list = []

        if not os.path.exists('./innoextract'):
            innoextract = 'innoextract'
        else:
            innoextract = './innoextract'

        proc = subprocess.Popen(
                [innoextract, installer, '-d', unpack_to],
                bufsize=1, universal_newlines=True, stdout=subprocess.PIPE
        )

        for line in iter(proc.stdout.readline, ''):
            line = line.strip('\n')
            print(line)
            files_list.append(line)

        if os.path.exists(unpack_to + 'commonappdata'):
            shutil.rmtree(unpack_to + 'commonappdata')
        if os.path.exists(unpack_to + 'app'):
            shutil.rmtree(unpack_to + 'app')

        files_dict, \
        chunks_dict, \
        files_chunks_dict = get_files_info_innoextract(files_list)

    elif sys.platform.startswith('win'):

        if unpack_to[-1] != '\\':
            unpack_to += '\\'

        os.system('innounp.exe -x "' + installer + '" -d"' + unpack_to + '"')

        if os.path.exists(unpack_to + '{commonappdata}'):
            shutil.rmtree(unpack_to + '{commonappdata}')
        if os.path.exists(unpack_to + '{app}'):
            shutil.rmtree(unpack_to + '{app}')

        files_dict, \
        chunks_dict, \
        files_chunks_dict = get_files_info_innounp(unpack_to)

    else:
        print("Platform not supported (yet).")
        return

    decompress_files(files_dict, unpack_to)
    decompress_files(chunks_dict, unpack_to)
    append_chuncks(files_chunks_dict, unpack_to)

    if os.path.exists(unpack_to + 'tmp'):
        shutil.rmtree(unpack_to + 'tmp')
    elif os.path.exists(unpack_to + '{tmp}'):
        shutil.rmtree(unpack_to + '{tmp}')
        if os.path.exists(unpack_to + 'install_script.iss'):
            os.remove(unpack_to + 'install_script.iss')

    print("Done.")

def get_files_info_innoextract(files_list):

    files_dict = {}
    chunks_dict = {}
    files_chunks_dict = {}

    for i in range(len(files_list)):

        if 'before_install' in files_list[i]:

            line = files_list[i].replace('-', '').replace("'", '').replace('"', '').strip(' ')

            if '[before_install_dependency(' in line:
                temp_list = line.split(' [before_install_dependency(')
            else:
                temp_list = line.split(' [before_install(')

            file_src = temp_list[0].replace('"', '')
            file_dest = temp_list[1].split(', ')[1].replace("'", '')
            files_dict[file_dest] = file_src
            chunks_n = int(temp_list[1].split(', ')[2].strip(')'))

            if chunks_n != 1:

                chunks_list = []

                for j in range(1, chunks_n):

                    line = files_list[i+j].replace('-', '').replace("'", '').replace('"', '').strip(' ')

                    if '[after_install_dependency(' in line:
                        temp_list = line.split(' [after_install_dependency(')
                    else:
                        temp_list = line.split(' [after_install(')

                    chunk_src = temp_list[0]
                    chunk_dest = temp_list[1].split(', ')[0]
                    chunks_dict[chunk_dest] = chunk_src
                    chunks_list.append(chunk_dest)

                files_chunks_dict[file_dest] = chunks_list

    return files_dict, chunks_dict, files_chunks_dict

def get_files_info_innounp(dest_dir):

    if sys.version_info[0] == 3:
        install_script = open(dest_dir + 'install_script.iss', 'r', encoding='utf-8')
    else:
        install_script = open(dest_dir + 'install_script.iss', 'r')

    raw_data = install_script.read().splitlines()
    install_script.close()

    files_dict = {}
    chunks_dict = {}
    files_chunks_dict = {}

    for i in range(len(raw_data)):

        if ('Source: ' in raw_data[i]) and ('BeforeInstall: ' in raw_data[i]):

            temp_list = raw_data[i].split('; ')
            file_src = temp_list[0].split(': ')[1].replace('"', '')
            file_dest = temp_list[3].split(': ')[1].replace('"', '').split(', ')[1].replace("'", '')
            files_dict[file_dest] = file_src

            chunks_n = int(temp_list[3].split(': ')[1].replace('"', '').split(', ')[2].strip(')'))

            if chunks_n != 1:

                chunks_list = []

                for j in range(1, chunks_n):
                    temp_list = raw_data[i+j].split('; ')
                    chunk_src = temp_list[0].split(': ')[1].replace('"', '')
                    chunk_dest = temp_list[3].split(': ')[1].split(', ')[0].replace('"after_install(', '').replace('"after_install_dependency(', '').replace("'", '')
                    chunks_dict[chunk_dest] = chunk_src
                    chunks_list.append(chunk_dest)

                files_chunks_dict[file_dest] = chunks_list

    return files_dict, chunks_dict, files_chunks_dict

def decompress_files(files_dict, dest_dir):

    for path_dest in files_dict:

        path_dest_full = dest_dir + path_dest
        path_dest_dir = os.path.dirname(path_dest_full)
        file_name = os.path.basename(path_dest_full)
        path_src = dest_dir + files_dict[path_dest]

        print("Decompressing: " + file_name)

        if not os.path.exists(path_dest_dir):
            os.makedirs(path_dest_dir)

        with open(path_src, 'rb') as comp_file, \
                open(path_dest_full, 'wb') as decomp_file:

            comp_data = comp_file.read()
            decomp_data = zlib.decompress(comp_data)
            decomp_file.write(decomp_data)

def append_chuncks(files_chunks_dict, dest_dir):

    for file_path in files_chunks_dict:

        for chunk in files_chunks_dict[file_path]:

            print("Appending chunk to: " + os.path.basename(file_path))

            full_file_path = dest_dir + file_path
            full_chunk_path = dest_dir + chunk

            with open(full_chunk_path, 'rb') as chunk_file, \
                    open(full_file_path, 'ab') as cur_file:

                chunk = chunk_file.read()
                cur_file.write(chunk)

            os.remove(full_chunk_path)

if __name__ == '__main__':

    if len(sys.argv) == 1:
        files_in_dir = os.listdir('.')
        n_installers = 0
        for file_name in files_in_dir:
            if ('setup' in file_name) and '.exe' in file_name:
                n_installers += 1
                installer = file_name
                unpack_to = file_name.replace('setup_', '').replace('.exe', '')
                unpack_gog_installer(installer, unpack_to)
        if n_installers == 0:
            print("Nothing to do.")
    elif len(sys.argv) == 3:
        unpack_gog_installer(sys.argv[1], sys.argv[2])
    else:
        print("Wrong number of arguments.")
        time.sleep(3)
