# app/routes.py
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
import subprocess
from flask import Blueprint, render_template, request, send_file
from flask import current_app, jsonify
from markupsafe import Markup

from .utils import process_zip_file
from .generate_file import code_error_corrected_with_openai

load_dotenv()
main = Blueprint('main', __name__)

@main.route('/')
def welcome():
    return render_template('welcome.html')


@main.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        uploaded_request = request.form['request']  # テキスト入力のデータを取得
        if uploaded_file.filename != '':
            uploaded_file_path = os.path.join(current_app.root_path, 'uploads', uploaded_file.filename)
            os.makedirs(os.path.dirname(uploaded_file_path), exist_ok=True)
            uploaded_file.save(uploaded_file_path)

            output_zip = process_zip_file(uploaded_file_path, uploaded_request)
            return send_file(output_zip, as_attachment=True)

    return render_template('index.html')

@main.route('/code-correction')
def code_correction():
    return render_template('code_correction.html')

@main.route('/process-correction', methods=['POST'])
def process_correction():
    # フォームデータの取得
    request_text = request.form['request']
    language = request.form['language']
    error_log = request.form['error-log']
    before_error_log = request.form['before-error-code']
    uploaded_file = request.files['file']

    # ここでファイル処理とログ出力
    # ...
    # request_text = request.form['request'].replace('\n', '<br>')

    lang_text = f"print('{language}')"
    formatted_text = Markup(f"{lang_text}\n\n{request_text}\n\n{error_log}\n\n{before_error_log}\n\n{uploaded_file.filename}")

    corrected_proposal = code_error_corrected_with_openai(request_text, error_log, language, before_error_log)


    # JSON形式でレスポンスを返す
    # return jsonify({"text": str(formatted_text)})
    return jsonify({"text": str(corrected_proposal)})
    
@main.route('/execute-python', methods=['POST'])
def execute_python():
    code = request.form['code']

    try:
        output = subprocess.check_output(['python3', '-c', code], text=True, stderr=subprocess.STDOUT)
        if output.strip() == "":
            # 標準出力が空の場合は「正常に実行されました」というメッセージを返す
            output = "コードが正常に実行されました。"
    except subprocess.CalledProcessError as e:
        output = e.output  # エラー出力をキャプチャ

    return jsonify({"result": output})
