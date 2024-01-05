from flask import current_app
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
load_dotenv()

            
def technical_decision_maker(request, file_structure, file_path):
    """
    最高技術責任者
    要求とファイル構造、ファイル構造内の出力するファイルを入力として受け取り
    
    """
    file = file_path.split("/")[-1]
    file_extension = file.split(".")[-1]  # 拡張子の取得
    # 拡張子に基づいてプログラム言語をセット
    if file_extension == "py":
        language = "Python"
    elif file_extension == "js":
        language = "JavaScript"
    elif file_extension == "java":
        language = "Java"
    elif file_extension == "html":
        language = "html"
    elif file_extension == "cpp":
        language = "C++"
    # その他の拡張子に基づく言語設定を追加
    else:
        language = str(file_extension)

    
    client = OpenAI()

    res_sum = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        # model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are the Chief Technical Officer. You receive as input the requirements, the file structure, and the names of the files to be executed within the file structure. The output is to declare the functions needed to realize the requirement and generate a dockstring-like comment describing the function's role within that function."},
            {"role": "system", "content": "Output must be in a format that allows the code received as input to be used as is, and comments must absolutely be written in Japanese."},
            {"role": "user", "content": f"request: {request}"},
            {"role": "user", "content": f"file structure: {file_structure}"},
            {"role": "user", "content": f"the filename to be executed within the file structure: {language}"},
            {"role": "user", "content": f"Programming language of the output program: {file}"},
            {"role": "user", "content": f"the filename to be executed: {file}. 絶対に以下の説明を守ってください。このファイル{file}対して関数と対応する処理の dockstring 風に説明コメントをプログラミング言語で{language}生成してください。"},
        ],
        temperature=0.2
    )
    file_doc = res_sum.choices[0].message.content
    current_app.logger.info(file_doc)
    # バックティックと言語指定を除外する
    # 言語指定は '```' の後の任意の文字列である可能性があるため、正規表現を使用する
    modified_file_content = re.sub(r'```[a-zA-Z]*\n', '', file_doc)
    modified_file_content = modified_file_content.replace('```', '')
    
    return modified_file_content


def programmer_and_designer_work(request, file_structure, file_path):
    """
    プログラマーとデザイナーによるコードの生成と再編集を行う
    要求とファイル構造、ファイル構造内の出力するファイルを入力として受け取り
    
    """
    with open(file_path, 'r') as file:
        file_content = file.read()
        
    file = file_path.split("/")[-1]
    file_extension = file.split(".")[-1]  # 拡張子の取得
    # 拡張子に基づいてプログラム言語をセット
    if file_extension == "py":
        language = "Python"
    elif file_extension == "js":
        language = "JavaScript"
    elif file_extension == "java":
        language = "Java"
    elif file_extension == "html":
        language = "html"
    elif file_extension == "cpp":
        language = "C++"
    # その他の拡張子に基づく言語設定を追加
    else:
        language = str(file_extension)

    client = OpenAI()

    res_sum = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        # model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a programmer and designer. You receive as input a file with a filename and comments with the requirements, the file structure, and a dockstring-like comment describing the role of the function to be executed in the file structure. The output is to generate code that can execute the comments against the file."},
            {"role": "system", "content": "Output must be in a format that allows the code received as input to be used as is, and comments must absolutely be written in Japanese."},
            {"role": "user", "content": f"request: {request}"},
            {"role": "user", "content": f"file structure: {file_structure}"},
            {"role": "user", "content": f"the filename to be executed within the file structure: {file}"},
            {"role": "user", "content": f"the filename to be executed within the file structure: {language}"},
            {"role": "user", "content": f"Code with a description of the code you want to execute to process the output code generation: {file_content}"},
            {"role": "user", "content": f"Code with a description of the cod: {file_content}. 絶対に以下の説明を守ってください。このコード {file_content}に対して、実行できるコードをプログラミング言語{language}で生成してください。"},
        ],
        temperature=0.2
    )
    file_doc = res_sum.choices[0].message.content
    current_app.logger.info(file_doc)
    # バックティックと言語指定を除外する
    # 言語指定は '```' の後の任意の文字列である可能性があるため、正規表現を使用する
    modified_file_content = re.sub(r'```[a-zA-Z]*\n', '', file_doc)
    modified_file_content = modified_file_content.replace('```', '')
    
    return modified_file_content


def tester_work(request, file_structure, file_path):
    """
    テスターによるコードの修正を行う
    要求とファイル構造、ファイル構造内の出力するファイルを入力として受け取り
    
    """
    with open(file_path, 'r') as file:
        file_content = file.read()
        
    file = file_path.split("/")[-1]
    file_extension = file.split(".")[-1]  # 拡張子の取得
    # 拡張子に基づいてプログラム言語をセット
    if file_extension == "py":
        language = "Python"
    elif file_extension == "js":
        language = "JavaScript"
    elif file_extension == "java":
        language = "Java"
    elif file_extension == "html":
        language = "Html"
    elif file_extension == "cpp":
        language = "C++"
    # その他の拡張子に基づく言語設定を追加
    else:
        language = str(file_extension)

    client = OpenAI()

    res_sum = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        # model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a tester. You receive as input the name of the file, the requirements, the file structure and the code to be executed in the file structure. The output is to modify the code in a way that it is error-free."},
            {"role": "system", "content": "Output must be in a format that allows the code received as input to be used as is, and comments must absolutely be written in Japanese."},
            {"role": "user", "content": f"request: {request}"},
            {"role": "user", "content": f"file structure: {file_structure}"},
            {"role": "user", "content": f"the filename to be executed within the file structure: {file}"},           
            {"role": "user", "content": f"the filename to be executed within the file structure: {language}"},
            {"role": "user", "content": f"Code with a description of the code you want to execute to process the output code generation: {file_content}"}, 
            {"role": "user", "content": f"Code with a description of the cod: {file_content}. 絶対に以下の説明を守ってください。このコード {file_content}に対して、エラーの出ない実行できるコードをプログラミング言語{language}で生成してください。"},
        ],
        temperature=0.2
    )
    file_doc = res_sum.choices[0].message.content
    current_app.logger.info(file_doc)
    # バックティックと言語指定を除外する
    # 言語指定は '```' の後の任意の文字列である可能性があるため、正規表現を使用する
    modified_file_content = re.sub(r'```[a-zA-Z]*\n', '', file_doc)
    modified_file_content = modified_file_content.replace('```', '')
    
    return modified_file_content

def code_error_corrected_with_openai(buggy_code, error_log, language, before_error_log):
    if not before_error_log:
        before_error_log = "前回のエラーログはありません。"
    if not error_log:
        error_log = "エラーログはありません。"
    
    client = OpenAI()  # OpenAIクライアントの初期化
    response = client.chat.completions.create(
        # model="gpt-4-1106-preview",  # モデルの指定
        model="gpt-3.5-turbo-1106",  # モデルの指定
        messages=[
            {"role": "system", "content": "Fix the following buggy code snippet. In your response, output the fixed code only."},
            {"role": "system", "content": "Fix the following buggy code snippet according to the suggestion in the '<Comment> ' line. In your response, output the fixed code only"},
            {"role": "user", "content": f"次のバグのあるコードを修正してください。レスポンスには修正されたコードのみを出力してください。{error_log}"},
            {"role": "user", "content": f"前回エラーが発生したときのコードは以下になります。{before_error_log}"},
            {"role": "user", "content": f"the filename to be executed within the file structure: {language}"},
            {"role": "user", "content": f"Code and description of the error to be corrected: 絶対に以下の説明を守ってください。このコード {buggy_code}に対して、実行できるコードをプログラミング言語{language}で生成してください。"},
            {"role": "user", "content": f"以下のコードにはエラーがあります：\n{buggy_code}\nエラーログ：\n{error_log}\nこのエラーを修正するためのコードを提案してください。\n"}
        ],
        temperature=0.2
    )
    file_doc = response.choices[0].message.content
    current_app.logger.info(file_doc)
    
    # バックティックと言語指定を除外する
    # 言語指定は '```' の後の任意の文字列である可能性があるため、正規表現を使用する
    modified_code_content = re.sub(r'```[a-zA-Z]*\n', '', file_doc)
    modified_code_content = modified_code_content.replace('```', '')
    
    return modified_code_content

