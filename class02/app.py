# app.py
import json

from flask import Flask, request, render_template, jsonify
import demo01  # 假设你的 a.py 在同一目录下，并且定义了一个 a 函数
import lang_chain_demo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # 渲染前端页面

@app.route('/process', methods=['POST'])
def process_content():
    content = request.json['content']  # 从前端表单获取内容
    print(content)

    result = lang_chain_demo.multIChat(content)
    # result = demo01.chatPromot(content)
    return jsonify({'result': result})  # 返回 JSON 响应给前端

if __name__ == '__main__':
    app.run(debug=True)  # 运行 Flask 应用，开启调试模式