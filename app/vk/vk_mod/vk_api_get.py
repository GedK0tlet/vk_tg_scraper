import requests
base_url='https://api.vk.com/method/'

def wall_get(domain, count_posts):
    url=base_url+'wall.get'
    comments = []
    posts = []
    payload={'access_token': serv_key,'owner_id': -1,'domain':f'{domain}', 'offset':0, 'count':count_posts, 'v': "5.236"}
    resp =  requests.post(url,data=payload)
    if resp.status_code==200:
        try:
            q = resp.json()['response']['items']
            for item in q:
                posts.append([item['text'], item['id']])
                tr = wall_getComment(post_id=item['id'], count_comments=20, owner_id=int(item['owner_id']))
                comments.append(tr)
            return posts, comments
        except:
            return [], []

    else:
        print('Somthing strange')

def wall_getComment(post_id, count_comments, owner_id):
    url=base_url+'wall.getComments'
    threads_msgs = []
    payload={'access_token': serv_key,'owner_id': owner_id,'post_id':f'{post_id}', 'offset':0, 'thread_items_count': 10,  'count':count_comments, 'v': "5.236"}
    resp =  requests.post(url,data=payload)
    if resp.status_code==200:
        
        try:
            q = resp.json()["response"]["items"]
            # print(q)
            for item in q:
                threads_msgs.append([item['text'], item['from_id'], item['post_id']])
                thred = item["thread"]['items']
                for m in thred:
                    s =  m['text']
                    if s != ',' or s != ' ' or not s:
                        threads_msgs.append([s, m['from_id'], m['post_id']])
                    else: pass
            # print(threads_msgs)
            return threads_msgs
        except:
            return []
    else:
        print('Somthing strange')

serv_key = '1f90a7391f90a7391f90a739a91c8826d311f901f90a73979ccfa3ea3e8d4d644c1809f'
