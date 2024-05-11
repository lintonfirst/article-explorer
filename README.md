# 拉取项目代码
git clone https://github.com/lintonfirst/article-explorer.git
# 安装python依赖
pip install -r requirements.txt
# 使用pyinstaller打包生成可执行文件（可执行文件将生成在dist目录下）
pyinstaller app.spec

