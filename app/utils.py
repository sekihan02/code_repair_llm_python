import os
import zipfile
import shutil
import logging
from flask import Flask, send_from_directory, current_app
from .generate_file import technical_decision_maker, programmer_and_designer_work, tester_work

from contextlib import contextmanager
from time import time

class Timer:
    """処理時間を表示するクラス
    with Timer(prefix=f'pred cv={i}'):
        y_pred_i = predict(model, loader=test_loader)
    
    with Timer(prefix='fit fold={} '.format(i)):
        clf.fit(x_train, y_train, 
                eval_set=[(x_valid, y_valid)],  
                early_stopping_rounds=100,
                verbose=verbose)

    with Timer(prefix='fit fold={} '.format(i), verbose=500):
        clf.fit(x_train, y_train, 
                eval_set=[(x_valid, y_valid)],  
                early_stopping_rounds=100,
                verbose=verbose)
    """
    def __init__(self, logger=None, format_str='{:.3f}[s]', prefix=None, suffix=None, sep=' ', verbose=0):

        if prefix: format_str = str(prefix) + sep + format_str
        if suffix: format_str = format_str + sep + str(suffix)
        self.format_str = format_str
        self.logger = logger
        self.start = None
        self.end = None
        self.verbose = verbose

    @property
    def duration(self):
        if self.end is None:
            return 0
        return self.end - self.start

    def __enter__(self):
        self.start = time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time()
        out_str = self.format_str.format(self.duration)
        if self.logger:
            self.logger.info(out_str)
        else:
            current_app.logger.info(out_str)
            

def process_zip_file(uploaded_file_path, uploaded_request):
    # アップロードされたZIPファイルの解凍とファイル構成の表示
    files_in_directory, extract_path = extract_and_display_file_structure(uploaded_file_path)

    # プログラムファイルの拡張子を定義
    program_file_extensions = ['.py', '.js', '.css', '.html']

    # プログラムファイルのみを含むリストを生成
    program_files = [file for file in files_in_directory if any(file.endswith(ext) for ext in program_file_extensions)]

    for file_path in program_files:
        with Timer(prefix=f'{file_path}: Chief Technical Officer work'):
            file_doc_test = technical_decision_maker(uploaded_request, program_files, file_path)
            current_app.logger.info(file_doc_test)
            # ファイルに書き込み
            with open(file_path, 'w') as file:
                file.write(file_doc_test)
                
        with Timer(prefix=f'{file_path}: programmer and designer work'):
            file_doc_test = programmer_and_designer_work(uploaded_request, program_files, file_path)
            current_app.logger.info(file_doc_test)
            # ファイルに書き込み
            with open(file_path, 'w') as file:
                file.write(file_doc_test)
                
        with Timer(prefix=f'{file_path}: tester work'):
            file_doc_test = tester_work(uploaded_request, program_files, file_path)
            current_app.logger.info(file_doc_test)
            # ファイルに書き込み
            with open(file_path, 'w') as file:
                file.write(file_doc_test)
    # 再圧縮するZIPファイルの名前
    output_zip_path = os.path.join(current_app.root_path, 'output.zip')

    # 再圧縮
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_in_directory:
            zipf.write(file_path, os.path.relpath(file_path, extract_path))

    # 一時ディレクトリを削除
    shutil.rmtree(extract_path)

    return output_zip_path

def extract_and_display_file_structure(zip_file_path):
    # ZIPファイルの解凍とファイル構成の表示
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        extract_path = os.path.splitext(zip_file_path)[0]
        zip_ref.extractall(extract_path)
    
    current_app.logger.info(f"{zip_file_path}を解凍しました。")
    
    files_in_directory = list_files_recursively(extract_path)
    current_app.logger.info(files_in_directory)  # ファイルリストをデバッグログに出力
    return files_in_directory, extract_path

def list_files_recursively(directory):
    """
    指定されたディレクトリおよびサブディレクトリ内のすべてのファイルをリストアップする関数
    """
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files
