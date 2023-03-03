from requests import get
from bs4 import BeautifulSoup

# from extractors.wwr import extract_wwr_jobs
# 타 폴더에서 불러옴
# from extractors.jobkr import extract_jobkr_jobs


# need to request the first page
def get_page_count(keyword):

  # request the first page of the search
  base_url = "https://www.jobkorea.co.kr/Search/?stext="
  response = get(f"{base_url}+{keyword}")
  if response.status_code != 200:
    print("cant request")
    # create the soup of the first page
  else:
    soup = BeautifulSoup(response.text, "html.parser")
    # 직업 대신에 페이지 번호를 soup에서 생성함
    # 1개만 찾을 때 find, 그 모든 recursive 한거 찾을 때는 find_all
    pagination_div = soup.find("div", class_="tplPagination")
    pagination = pagination_div.find("ul")
    if pagination == None:
      return 1
    pages = pagination.find_all("li")
    count = len(pages)
    #페이지가 10개보다 많다면, 10개만 return 해줘!
    if count >= 10:
      return 10
    else:
      return count


def extract_jobkr_jobs(keyword):
  #scrap 할 페이지 갯수를 찾기 위해서 아래와 같이 작성
  # range creates sequence of number from
  pages = get_page_count(keyword)
  print("found", pages, "pages")
  # for 밖으로 빼줘야 됨
  results = []

  for page in range(pages):
    # 처음 seach 할 시 첫번째 페이지에서 search를 수행해야 함
    # 그 다음엔 각각의 페이지에 아래 함수를 계속 요청할 것임
    base_url = "https://www.jobkorea.co.kr/Search/?stext="
    final_url = f"{base_url}+{keyword}&tabType=recruit&Page_No={page+1}"
    print(final_url)
    response = get(final_url)

    if response.status_code != 200:
      print("cant request")
    else:
      soup = BeautifulSoup(response.text, "html.parser")
      job_list = soup.find("div", class_="list-default")
      jobs = job_list.find("ul", class_="clear")
      # recursive tag를 찾을 때에는 find_all을 하면 된다.
      job = jobs.find_all("li", class_="list-post")
      for job_section in job:
        post = job_section.find_all("div", class_="post")

        for job_section in post:
          post_list = job_section.find("div", class_="post-list-corp")

          # company name
          company_name = post_list.find("a")
          company = company_name["title"]
          # link
          link = company_name["href"]
          # company position
          post_list_info = job_section.find("div", class_="post-list-info")
          title_name = post_list_info.find("a")
          title = title_name["title"]
          # location
          location_name = post_list_info.find("p", class_="option")
          location = location_name.find("span", class_="loc long")
          # position
          # position = location_name.find("span", class_="exp")
          job_data = {
            "company": company.replace(",", " "),
            "position": title.replace(",", " "),
            "location": location.string.replace(",", " "),
            "link": f"https://www.jobkorea.co.kr/Search/?stext=+{link}",
            # "title": title.string
          }

          results.append(job_data)
          # getting value out of the function
  # should always return the results
  return results
