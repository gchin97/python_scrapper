# from extractors.jobkr import extract_jobkr_jobs
# from extractors.wwr import extract_wwr_jobs
# from file import save_to_file
from flask import Flask, render_template, request, redirect, send_file
from extractors.jobkr import extract_jobkr_jobs
from extractors.wwr import extract_wwr_jobs
from file import save_to_file

# created variable outside of the below function because the function is called everytime the user visits:  data being collected everytime the keyword is being called
db = {
  # 'python':[...]
}

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

# when the user clicks export, the user will be directed to the page with the keyword


@app.route("/search")
def search():
  # 위에서 import render_template
  # sending variable name to html
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword in db:
    jobs = db[keyword]
  else:
    wwr = extract_wwr_jobs(keyword)
    jobkr = extract_jobkr_jobs(keyword)
    # you need to render the jobs
    # jobs is a LIST
    jobs = wwr + jobkr
    db[keyword] = jobs
  return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
  keyword = request.args.get("keyword")
  if keyword == None:
    # <!--       export page will grab the keyword from the url -->
    return redirect("/")
  if keyword not in db:
    return redirect(f"/search?keyword={keyword}")
    # jobs are going to be saved in the db[keyword]
  # name and list of jobs will be from searchpage's keyword and db[keyword]
  save_to_file(keyword, db[keyword])
  return send_file(f"{keyword}.csv", as_attachment = True)

app.run("0.0.0.0")
