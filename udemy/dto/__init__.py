
class Course(object):
    def __init__(self, api, item=None):
        self.predictive_score = item['predictive_score']
        self.relevancy_score = item['relevancy_score']
        self.published_title = item['published_title']
        self.input_features = item['input_features']
        self.title = item['input_features']
        self.url = item['url']
        self.is_paid = item['is_paid']
        instructors = []
        for each in item['visible_instructors']:
            instructors.each(Instructor(item=each))
        self.visible_instructors = instructors
        self.is_practice_test_course = item['is_practice_test_course']
        self.id = item['id']
        self.price_detail = PriceDetail(item=item['price_detail'])
        self.lecture_search_result = item['lecture_search_result']
        self.image_240x315 = item['image_240x315']
        self.image_480x270 = item['image_480x270']
        self._class = item['_class']
        self.price = item['price']
        self.image_125_H = item['image_125_H']


class Instructor(object):
    def __init__(self, item=None):
        self.image_100x100 = item['image_100x100']
        self.display_name = item['display_name']
        self.name = item['name']
        self.title = item['title']
        self.url = item['url']
        self.initials = item['initials']
        self.image_50x50 = item['image_50x50']
        self._class = item['user']
        self.job_title = item['job_title']


class PriceDetail(object):
    def __init__(self, item):
        self.price_string = None
        self.amount = None
        self.currency_symbol = None
        self.currency = None