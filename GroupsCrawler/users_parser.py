from grab.selector import XpathSelector
from grab.spider import Spider, Task
import xlsxwriter


class VkSpider(Spider):
    __slots__ = ['ids', 'wb', 'ws', 'cur_col', 'parsed']

    def __init__(self, ids, output_filename):
        super().__init__()
        self.ids = ids
        self.wb = xlsxwriter.Workbook(output_filename + '.xlsx')
        self.ws = self.wb.add_worksheet()
        self.cur_col = -1
        self.parsed = 0

    def create_grab_instance(self, **kwargs):
        g = super(VkSpider, self).create_grab_instance(**kwargs)
        g.setup(headers={
            'accept-language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
        })
        return g

    def task_generator(self):
        vk_url = 'https://vk.com/id{0}'
        for user_id in self.ids:
            yield Task('parse_page', url=vk_url.format(user_id), user_id=user_id)

        # print('Parsed pages: {0}'.format(self.parsed))
        self.wb.close()

    def task_parse_page(self, grab, task):
        try:
            if len(grab.doc.select('//*[@id="profile_info"]/h4/div[contains(@class, "profile_deleted")]').text()) > 0:
                # print("-- Hidden user's page")
                return
        except Exception:
            pass

        try:
            user_id = task.user_id
            username = grab.doc.select('//*[@id="profile_info"]/h4/div[contains(@class, "page_name")]').text()
            city = grab.doc.select(
                "//*[@id='profile_full_info']//div[contains(@class, 'clear_fix') and div[@class='label fl_l'] = 'Город:']/div[@class='labeled fl_l']/a")\
                .one(default=XpathSelector('')).text()
            languages = grab.doc.select(
                "//*[@id='profile_info']//div[contains(@class, 'clear_fix') and div[@class='label fl_l'] = 'Языки:']/div[@class='labeled fl_l']/a")\
                .one(default=XpathSelector('')).text()
            # print((user_id, username, city, languages))
            self.cur_col += 1
            self.ws.write(self.cur_col, 0, user_id)
            self.ws.write(self.cur_col, 1, username)
            self.ws.write(self.cur_col, 2, city)
            self.ws.write(self.cur_col, 3, languages)

            self.parsed += 1
        except Exception:
            pass


def parse(users, output_filename):
    if len(users) > 0:
        s = VkSpider(users, output_filename)
        s.run()
