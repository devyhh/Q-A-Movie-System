import json
import requests

def get_data():
    url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=330&page_start=0'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    }
    json_data = requests.get(url,headers = headers)
    #print(json_data.text)
    data = json_data.text
    json_data = json.loads(data)
    subjects = json_data['subjects']
    result = []
    i=1
    for movie in subjects:
        print(i,movie['title'])
        i=i+1
        # row = {
        #     'movie_rate': movie['rate'],
        #     'movie_name': movie['title'],
        #     'movie_url' : movie['url']
        # }
        # result.append(row)
    return result

if __name__ == '__main__':
    get_data()
