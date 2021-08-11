from src.implement import *
import json

class Impl:
    @staticmethod
    def get_json(username: str):
        result = shopee.get_shop_detail(username, data)
        result = shopee.get_browser_open(result['shop_id'], result)

        return result
