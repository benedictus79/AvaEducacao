from download import download_video
from tqdm import tqdm
from login import sesskey, avaeducacaosession, selected_course, BeautifulSoup
from utils import concat_path, re, clear_folder_name, create_folder, headers_api, shorten_folder_name

def list_sections(course_link):
  sectionid = 0  # Inicializa o sectionid com 0
  data_modules = {}

  while True:
    params = {
      'sesskey': sesskey,
      'info': 'format_tiles_get_single_section_page_html',
    }
    json_data = [
      {
        'index': 0,
        'methodname': 'format_tiles_get_single_section_page_html',
        'args': {
          'courseid': course_link,
          'sectionid': sectionid,
          'setjsusedsession': True,
        },
      },
    ]
    response = avaeducacaosession.post(
      'https://saladeaula.avaeducacao.com.br/lib/ajax/service.php',
      params=params,
      headers=headers_api,
      json=json_data,
    ).json()
    response = response[0]['data']['html']
    soup = BeautifulSoup(response, 'html.parser')
    elements = soup.find_all('li', attrs={"data-cmid": True})
    if not elements:
      break
    for element in elements:
      data_cmid = element.get('data-cmid')
      data_title = element.get('data-title')
      data_modules[data_title] = data_cmid
    sectionid += 1
  return data_modules


def process_sections(data_modules):
  params = {
    'sesskey': sesskey,
    'info': 'format_tiles_get_mod_page_html',
  }
  data_download = {}
  for title, cmid in data_modules.items():
    json_data = [
      {
        'index': 0,
        'methodname': 'format_tiles_get_mod_page_html',
        'args': {
          'courseid': course_link,
          'cmid': cmid,
        },
      },
    ]
    response = avaeducacaosession.post(
      'https://saladeaula.avaeducacao.com.br/lib/ajax/service.php',
      params=params,
      json=json_data,
    ).json()
    for item in response:
      if not item.get('error', True) and 'data' in item:
        html_content = item['data']['html']
        data_download[title] = get_vimeo(html_content)
  return data_download


def get_download(main_course_folder, data_download):
  for index, (name, url) in enumerate(tqdm(data_download.items(), desc="Downloading Videos"), start=1):
    folder_name = shorten_folder_name(concat_path(main_course_folder, f'{index:03d} - {clear_folder_name(name)}'))
    referer = {'Referer': 'https://saladeaula.avaeducacao.com.br/'}
    if 'vimeo' in url:
      download_video(url, folder_name, referer)
    else:
      with open(f"{folder_name}.html", "w", encoding='utf-8') as file:
        file.write(str(url))


def get_vimeo(html_content):
  soup = BeautifulSoup(html_content, 'html.parser')
  
  iframe = soup.find('iframe')
  if iframe and 'src' in iframe.attrs:
    src = iframe['src']
    if not src.startswith('https:'):
      src = 'https:' + src
    return src
  else:
    return soup


if __name__ == '__main__':
  course_name, course_link = selected_course
  main_course_folder = create_folder(clear_folder_name(course_name))
  data_modules = list_sections(course_link)
  data_download = process_sections(data_modules)
  get_download(main_course_folder, data_download)