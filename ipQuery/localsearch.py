from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>文件搜索</title>
    </head>
    <body>
        <h1>文件搜索</h1>
        <input type="file" id="file-input" accept=".csv">
        <input type="text" id="search-input" placeholder="输入搜索关键字" onkeyup="searchInFile()">
        <ul id="result"></ul>

        <script>
            let fileContent = null; // 用于存储文件内容

            // 当文件被选中时读取文件
            document.getElementById('file-input').addEventListener('change', function(event) {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        fileContent = e.target.result.split('\n'); // 假设文件是文本文件，按行分割
                    };
                    reader.readAsText(file);
                }
            });

            function searchInFile(keyword) {
                if (!fileContent) {
                    alert('请先选择一个文件！');
                    return;
                }
                
                const keywordLower = keyword.toLowerCase();
                const resultElement = document.getElementById('result');
                resultElement.innerHTML = ''; // 清空之前的结果
                
                let found = false;
                fileContent.forEach(line => {
                    if (line.toLowerCase().includes(keywordLower)) {
                        found = true;
                        const li = document.createElement('li');
                        li.textContent = line;
                        resultElement.appendChild(li);
                    }
                });
                
                if (!found) {
                    const li = document.createElement('li');
                    li.textContent = '没有找到包含该关键字的行';
                    resultElement.appendChild(li);
                }
            }

            // 将 onkeyup 事件处理程序更改为调用 searchInFile 并传递当前输入值
            document.getElementById('search-input').addEventListener('keyup', function() {
                searchInFile(this.value);
            });
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)