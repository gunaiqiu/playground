from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

def search_ips(filename, ip):
    results = []
    if len(ip) > 4:  # 只当输入长度超过4个字符时才进行搜索
        with open(filename, mode='r', encoding='utf-8') as file:
            for line in file:
                if ip in line:  # 进行模糊匹配
                    results.append(line.strip())  # 移除行尾的换行符并添加到结果中
    return results

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>IP查询</title>
    </head>
    <body>
        <h1>IP查询</h1>
        <input type="text" id="ip-input" placeholder="输入IP地址" onkeyup="searchIP(this.value)">
        <ul id="result"></ul>

 <script>
    let currentIp = ''; // 用于跟踪当前的IP输入

    function searchIP(ip) {
        if (ip.length > 4 && ip !== currentIp) {  // 只当输入长度超过4个字符且输入发生变化时才发送请求
            currentIp = ip; // 更新当前IP
            document.getElementById('result').innerHTML = ''; // 清空之前的结果

            fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ip: ip})
            })
            .then(response => response.json())
            .then(data => {
                var resultElement = document.getElementById('result');
                if (data.rows && data.rows.length > 0) {
                    data.rows.forEach(row => {
                        var li = document.createElement('li');
                        li.textContent = row;
                        resultElement.appendChild(li);
                    });
                } else {
                    var li = document.createElement('li');
                    li.textContent = '没有找到包含该IP的行';
                    resultElement.appendChild(li);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                document.getElementById('result').innerHTML = '<li>查询出错</li>';
            });
        }
    }

    // 将 onkeyup 事件处理程序更改为调用 searchIP 并传递当前输入值
    document.getElementById('ip-input').addEventListener('keyup', function() {
        searchIP(this.value);
    });
</script>
    </body>
    </html>
    '''

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    ip = data.get('ip')
    
    # 检查是否有有效的 IP 输入
    if not ip:
        # 如果没有 IP 输入，返回空的结果
        return jsonify({'rows': []})  # 或者返回一个带有错误信息的响应
    
    rows = search_ips('ips.csv', ip)  # 注意文件名应该是 'ips.csv'，而不是 'ips.txt'
    return jsonify({'rows': rows})


if __name__ == '__main__':
    app.run(debug=True)