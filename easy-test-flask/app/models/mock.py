import time

from app.libs.error_code import AddMockException, EditMockException
from app.libs.init import mongo


class Mock:
    def __init__(self, method=None, url=None, request_header=None, request_body=None, response_header=None,
                 response_body=None, status_code=None, msg=None):
        self.mid = int(round(time.time() * 1000))
        self.method = method
        self.url = url
        self.request_header = request_header
        self.request_body = request_body
        self.response_header = response_header
        self.response_body = response_body
        self.status_code = status_code
        self.msg = msg
        self.delete_time = None

    def new_mock(self):
        search_by_url = mongo.db.mock.find(
            {
                'url': '/mock' + self.url,
                'method': self.method,
                'delete_time': None
            },
            {"_id": 0}).sort([('_id', -1)]).limit(1)
        count = search_by_url.count()
        # 存在url相同的数据，不允许新增
        if count >= 1:
            raise AddMockException(msg='已存在同名的url')

        mock = {
            'mid': self.mid,
            'method': self.method,
            'url': '/mock' + self.url,
            'request_header': self.request_header,
            'request_body': self.request_body,
            'response_header': self.response_header,
            'response_body': self.response_body,
            'status_code': self.status_code,
            'msg': self.msg,
            'delete_time': self.delete_time,
        }

        mongo.db.mock.insert(mock)

    def edit_mock(self):
        old_mock = self.search_mock(self.mid, None)
        if not old_mock:
            raise EditMockException(msg='mock接口不存在')

        if not (old_mock[0]['url'] == self.url and old_mock[0]['method'] == self.method):
            search_by_url = mongo.db.mock.find(
                {
                    'url': self.url,
                    'method': self.method,
                    'delete_time': None
                },
                {"_id": 0}).sort([('_id', -1)]).limit(1)
            count = search_by_url.count()
            # 存在url相同的数据，不允许修改
            if count >= 1:
                raise EditMockException(msg='已存在同名的url')

        mocks = mongo.db.mock.update_one(
            {'mid': int(self.mid)},
            {
                '$set': {
                    'method': self.method,
                    'url': self.url,
                    'request_header': self.request_header,
                    'request_body': self.request_body,
                    'response_header': self.response_header,
                    'response_body': self.response_body,
                    'status_code': self.status_code,
                    'msg': self.msg,
                }
            }
        )
        return mocks.modified_count

    def delete_mock(self):
        old_mock = self.search_mock(self.mid, None)
        if not old_mock:
            raise EditMockException(msg='mock接口不存在')
        mocks = mongo.db.mock.update_one(
            {'mid': int(self.mid)},
            {'$set': {'delete_time': int(round(time.time() * 1000))}}
        )
        return mocks.modified_count

    @classmethod
    def search_mock(cls, mid, url):
        mocks = mongo.db.mock.find(
            {
                'mid': int(mid) if mid is not None else {'$type': 18},
                'url': {'$regex': url} if url is not None else {'$regex': ''},
                'delete_time': None
            },
            {"_id": 0}).sort([('_id', -1)])

        mocks = list(mocks)

        return mocks

    @classmethod
    def total(cls):
        return mongo.db.mock.find(
            {
                'delete_time': None
            },
            {"_id": 0}).sort([('_id', -1)]).count()
