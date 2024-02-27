import requests
from bs4 import BeautifulSoup
from utils import re, benedictus_ascii_art, clear_screen


avaeducacaosession = requests.Session()

headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
  'Accept-Language': 'pt-BR,pt;q=0.8',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Pragma': 'no-cache',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'none',
  'Sec-Fetch-User': '?1',
  'Sec-GPC': '1',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
  'dnt': '1',
  'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
}


def get_authenticity_token():
  response = avaeducacaosession.get('https://saladeaula.avaeducacao.com.br/', headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  token_element = soup.find('input', {'name': 'logintoken'})
  if token_element:
    token_login = token_element['value']

    return token_login


def login(token_login):
  benedictus_ascii_art()
  username = input('email: ')
  password = input('senha: ')
  clear_screen()
  data = {
    'username': username,
    'password': password,
    'submit': 'Acessar',
    'logintoken': token_login,
  }
  response = avaeducacaosession.post('https://saladeaula.avaeducacao.com.br/login/index.php', data=data)
  soup = BeautifulSoup(response.text, 'html.parser')
  script_tags = soup.find_all('script')
  sesskey_regex = re.compile(r'"sesskey":"(.*?)"')
  for script in script_tags:
    if 'sesskey' in script.text:
      match = sesskey_regex.search(script.text)
      if match:
        sesskey_value = match.group(1)
        break
  return sesskey_value


def list_course(sesskey_value):
  params = {
    'sesskey': sesskey_value,
    'info': 'core_course_get_enrolled_courses_by_timeline_classification',
  }
  json_data = [
    {
      'index': 0,
      'methodname': 'core_course_get_enrolled_courses_by_timeline_classification',
      'args': {
        'offset': 0,
        'limit': 0,
        'classification': 'allincludinghidden',
        'sort': 'fullname',
        'customfieldname': '',
        'customfieldvalue': '',
      },
    },
  ]
  response = avaeducacaosession.post(
    'https://saladeaula.avaeducacao.com.br/lib/ajax/service.php',
    params=params,
    json=json_data,
  ).json()
  courses = {}
  for course_data in response:
    courses_list = course_data['data']['courses']
    for course in courses_list:
      fullname = course['fullname']
      viewurl = course['viewurl']
      course_id = course['id']
      courses[fullname] = course_id
  
  return courses


def choose_course(courses):
  print('Cursos disponíveis:')
  if courses is None:return None, None
  for i, (course_title, course_info) in enumerate(courses.items(), start=1):
    print(f'{i}. {course_title}')
    
  choice = input('Escolha um curso pelo número: ')
  if not choice.isdigit():return None, None
  selected_course_title = list(courses.keys())[int(choice) - 1]
  selected_course_id = courses[selected_course_title]
  
  return selected_course_title, selected_course_id


token = get_authenticity_token()
sesskey = login(token)
courses = list_course(sesskey)
selected_course = choose_course(courses)