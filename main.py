# from extractors.jobkr import extract_jobkr_jobs
# from extractors.wwr import extract_wwr_jobs
# from file import save_to_file
from flask import Flask, render_template, request
from extractors.jobkr import extract_jobkr_jobs
from extractors.wwr import extract_wwr_jobs

# keyword = input("what job are you searching for? ")

# # because these are list, because it returns a list, I can combine both of them
# jobkr = extract_jobkr_jobs(keyword)
# wwr = extract_wwr_jobs(keyword)
# jobs = jobkr + wwr
# save_to_file(keyword, jobs)

# app이라는 변수를 만들고 네이밍
# run this application
# 아래는 페이지에 방문했을 때 그 함수를 호출함(둘은 항상 앞뒤로 같이 있어야 됨)
app = Flask("JobScrapper")


@app.route("/")
def home():
  # 위에서 import render_template
  # sending variable name to html
  return render_template("home.html")


# run the application by app.run
# flask looks for a folder "templates" and it has to be a FOLDER and create html and css file

# grab the keyword and use the extractor


@app.route("/search")
def search():
  # 위에서 import render_template
  # sending variable name to html
  keyword = request.args.get("keyword")
  wwr = extract_wwr_jobs(keyword)
  jobkr = extract_jobkr_jobs(keyword)
  # you need to render the jobs
  # jobs is a LIST
  jobs = wwr + jobkr
  return render_template("search.html", keyword=keyword, jobs=jobs)


app.run("0.0.0.0")
