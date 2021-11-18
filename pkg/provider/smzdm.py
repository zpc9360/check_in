
import requests
from datetime import datetime, timezone, timedelta


class Smzdm(object):
    def __init__(self, cookies):
        print('smzdm')
        self.session = requests.Session()
        self.set_headers()
        self.session.headers['Cookie'] = cookies.encode('utf-8')    
        self.url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'

    def set_headers(self):
        self.session.headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'zhiyou.smzdm.com',
        'Referer': 'https://www.smzdm.com/',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        }

    def __json_check(self, msg):
        try:
            res = msg.json()
            # print(res)
            return res['data']
        except Exception as e:
            print(f'Error: {e}')            
            return str(e)

    def check_in(self):
        # print(self.session.headers)
        msg = self.session.get(self.url)
        
        tz = timezone(timedelta(hours=+8))

        fmt = '%Y-%m-%d %H:%M:%S'

        dateTime = datetime.today().astimezone(tz)

        status = '失败'

        resp = self.__json_check(msg)

        # 签到天数
        checkin_num = resp['checkin_num']

        # 连续签到天数
        continue_checkin_days =  resp['continue_checkin_days']

        #金币
        gold = resp['gold']


        #获得经验
        exp = resp['exp']

        if resp != '':
            status = '成功'
        else:
            status += f', {resp}'


        return f'「什么值得买每日签到经验」：{exp} \n'\
               f'「签到状态」：{status} \n' \
               f'「签到天数」：{checkin_num} \n' \
               f'「连续签到天数」：{continue_checkin_days} \n' \
               f'「金币」：{gold} \n' \
               f'「签到时间」：{dateTime.strftime(fmt)} \n'


