from extractors.jobkr import extract_jobkr_jobs
from extractors.wwr import extract_wwr_jobs

keyword = input("what job are you searching for? ")

# because these are list, because it returns a list, I can combine both of them
jobkr = extract_jobkr_jobs(keyword)
wwr = extract_wwr_jobs(keyword)
jobs = jobkr + wwr

# csv 파일 열기 시작
file = open(f"{keyword}.csv", "w", encoding="utf-8")
# comma separated value 이기 때문에, 그리고 마지막에 \n 적어줘야 함
file.write("Company, Position, location, link\n")

# because we are combining two lists (jobkr+wwr- 이거 두개 다 리스트임), we need to do a for loop
# remember that both of your extractors are using same keyname(job_data) DICTIONARY to save the extracted content
for job in jobs:
  # job(job_data)는 dictionary 이기 때문에 아래에서도 {Job}를 적어줘야 함
  # 딕셔너리에 저장되어있는 값을
       file.write(
        f"{job['company']},{job['position']},{job['location']},{job['link']}\n")


    
file.close()
