以下所有命令需在GoogleScholarPapersBibTex文件夹下运行。

```
cd GoogleScholarPapersBibTex
```

## 1、前端

```
python -m http.server
```

或

```
npm install -g http-server
http-server
```

## 2、后端

### 安装环境依赖

```
pip install -r backend\requirements_pip.txt
```

或

```
conda create --name env --file backend\requirements_conda.txt
```

### 运行

```
python backend\app.py
```

#### 接口1：爬虫

```
http://127.0.0.1:5000/spider
```

**Method**: POST

**Headers**: Content-Type=application/x-www-form-urlencoded

**Body**: papers="""Attention is all you need

Yan, E., Zhang, T., Yu, J., Hao, T., Chen, Q., 2024. A preliminary study on few-shot knowledge reasoning mechanism based on three-way partial order structure. Information Sciences 665, 120366. https://doi.org/10.1016/j.ins.2024.120366"""

#### 接口2：压缩

```
http://127.0.0.1:5000/compress
```

**Method**: GET

## 3、文件

```
D:.
│  output.zip                  # 输出文件夹压缩包
│  README.md                   # 文档
│  
├─backend                      # 后端
│      app.py                  # Flask后端运行文件，含爬虫压缩接口
│      requirements_conda.txt  # conda环境依赖
│      requirements_pip.txt    # pip环境依赖
│      spider.py               # 爬虫文件
│      
├─frontend                     # 前端
│      index.html              # html页面
│      script.js               # script脚本，负责用户与页面的交互
│      style.css               # css文件，渲染页面
│      
└─output                       # 输出文件夹
        error_papers.log       # 检索错误日志
        papers.txt             # 所有待检索论文
        references.bib         # 检索成功的BibTex
```

