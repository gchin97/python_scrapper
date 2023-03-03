from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jobs(keyword):
  base_url = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term=python"
  response = get(f"{base_url}+{keyword}")

  if response.status_code != 200:
    print("cant request")
  else:
    results = []
    # 선정 웹페이지에서 모든 html을 다 긁어옴
    soup = BeautifulSoup(response.text, "html.parser")
    # 모든 html에서 job html Text의 section만 가져오는 분류 작업 시작
    jobs = soup.find_all("section", class_="jobs")
    # 위에서 섹션만 정리한 리스트 안에서 이제 상세한 추려내기 시작
    for job_section in jobs:
      # 추려낸 섹션 html에서 li 만 뽑아내기
      job_post = job_section.find_all("li")
      # 뽑아낸 리스트에서 마지막꺼는 필요없으니까 빼버리기
      job_post.pop(-1)
      # 뽑아낸 li 리스트에서 이제 앵커 뽑아내기
      for post in job_post:
        anchors = post.find_all("a")
        anchor = anchors[1]
        link = anchor["href"]
        company, position, location = anchor.find_all("span", class_="company")
        # 각 명칭을 정해주고 그 태그만 가져옴
        title = anchor.find("span", class_="title")
        # make a dictionary based on what we have created
        # `find_all` returns a list, lists don't have .string.
        job_data = {
          "company": company.string.replace(",", " "),
          # "position": position.string.replace(",", " "),
          "position": title.string.replace(",", " "),
          "location": location.string.replace(",", " "),
          "link": f"https://weworkremotely.com+{link}"
        }
        results.append(job_data)

  for a in results:
    print(results)
    return results
