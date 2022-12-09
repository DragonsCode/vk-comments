import requests
from bs4 import BeautifulSoup


def get_comment(fullname, url):
    headers = {'Accept-Language': 'ru'}
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        comments = soup.findAll('div', {'class': 'Replies'})[0].findAll('div', {'class': 'ReplyItem__content'})
    except Exception as e:
        print(e)
        return False, 'comment not found'

    for i in comments:
        date = i.find('div', {'class': 'ReplyItem__date'}).find('a', {'class': 'item_date'}).text
        name = i.find('a', {'class': 'ReplyItem__name'}).text
        msg = i.find('div', {'class': 'ReplyItem__body'}).text
        if name == fullname:
            if not date.split(' ')[0].isdigit():
                return True, msg.strip()
            return False, 'old comment'
    return False, 'comment not found'


def get_post(url):
    try:
        wall = url.split('wall')
        if wall[0][-1] == '=':
            url = 'https://vk.com/wall'+wall[1]
        id = url[-1]
        int(id)
    except Exception as e:
        return False, 'Invalid post'
    headers = {'Accept-Language': 'ru'}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            return False, 'invalid status'
    except Exception as e:
        return False, 'Missing schema, example of correct url: https://vk.com/wall{owner_id}_{post_id}'

    soup = BeautifulSoup(r.text, 'html.parser')
    post_head = soup.findAll('div', {'class': 'wi_head'})
    author = post_head[0].findAll('a', {'class': 'pi_author'})
    post_date = post_head[0].findAll('span', {'class': 'wi_date'})[0].text
    type = author[0]['data-post-owner-type']
    if post_date[0].isdigit():
        return False, 'Old post'
    return True, type

# url = 'https://vk.com/wall748706491_55'
# print(get_post('https://vk.com/wall748706491_55'))
# print(url.split('/wall')[1].split('_')[0])
