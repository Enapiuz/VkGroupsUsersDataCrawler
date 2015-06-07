import requests


def recieve_users(group_name):
    pattern = "https://api.vk.com/method/groups.getMembers?group_id={0}&count={1}&offset={2}"
    offset = 0
    count = 1000
    max_users = count + 1
    myset = set()

    while offset < max_users:
        r = requests.get(pattern.format(group_name, count, offset))
        req = r.json()
        offset += count
        if 'response' in req:
            # print('Current {0}, total {1}'.format(offset, req['response']['count']))

            if 'count' in req['response']:
                max_users = req['response']['count']

            if 'users' in req['response']:
                myset |= set(req['response']['users'])

    return myset