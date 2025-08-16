import os
import shutil
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/spider", methods=["POST"])
def spider():
    papers = request.form.get("papers", None)
    if not papers:
        return jsonify({"status": "error", "message": "No papers provided."}), 400
    papers = papers.split("\n")
    papers = [paper for paper in papers if paper != ""]

    with open("output\papers.txt", "w", encoding="utf-8") as file:
        file.writelines("\n".join(papers))
    with open(r"output\references.bib", "w", encoding="utf-8") as file:
        pass
    with open("output\error_papers.log", "w", encoding="utf-8") as file:
        pass

    try:
        # 调用爬虫逻辑（运行另一个 Python 脚本）
        # 爬虫逻辑保存在 spider.py
        subprocess.Popen(
            ["python", "backend/spider.py"],
        ).wait()

        papers_total_num = len(papers)
        with open(r"output\references.bib", "r", encoding="utf-8") as file:
            papers_success_num = file.read().count("@")
        if not papers_success_num:
            raise Exception("All papers retrieval failed!")
        with open("output\error_papers.log", "r", encoding="utf-8") as file:
            papers_error_num = len(file.readlines())
        assert papers_success_num + papers_error_num == papers_total_num
        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"Received {papers_success_num} papers!",
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/compress", methods=["GET"])
def compress():
    try:
        if not os.path.isdir("output"):
            raise Exception("The folder does not exist!")
        shutil.make_archive("output", "zip", "output")
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "The folder has been successfully compressed!",
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
