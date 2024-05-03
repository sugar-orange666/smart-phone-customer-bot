# app.py
from flask import Flask, request, render_template, jsonify
import demo01  # 假设你的 a.py 在同一目录下，并且定义了一个 a 函数

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # 渲染前端页面

@app.route('/process', methods=['POST'])
def process_content():
    content = request.form.get('content')  # 从前端表单获取内容
    result = demo01.a(content)  # 调用 a.py 中的 a 函数
    return jsonify({'result': result})  # 返回 JSON 响应给前端

if __name__ == '__main__':
    app.run(debug=True)  # 运行 Flask 应用，开启调试模式