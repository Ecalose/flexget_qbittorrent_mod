from ..base.request import NetworkState
from ..base.request import check_network_state
from ..base.sign_in import check_final_state, SignState, Work

from ..schema.gazelle import Gazelle
from ..utils import net_utils
from ..utils.net_utils import get_module_name


class MainClass(Gazelle):
    URL = 'https://jpopsuki.eu/'
    USER_CLASSES = {
        'uploaded': [26843545600],
        'share_ratio': [1.05],
        'days': [14]
    }

    @classmethod
    def sign_in_build_schema(cls):
        return {
            get_module_name(cls): {
                'type': 'object',
                'properties': {
                    'cookie': {'type': 'string'},
                    'login': {
                        'type': 'object',
                        'properties': {
                            'username': {'type': 'string'},
                            'password': {'type': 'string'}
                        },
                        'additionalProperties': False
                    }
                },
                'additionalProperties': False
            }
        }

    def sign_in_build_login_workflow(self, entry, config):
        return [
            Work(
                url='/login.php',
                method=self.sign_in_by_login,
                assert_state=(check_network_state, NetworkState.SUCCEED),
                response_urls=['/index.php'],
            ),
        ]

    def sign_in_build_login_data(self, login, last_content):
        return {
            'username': login['username'],
            'password': login['password'],
            'keeplogged': 1,
            'login': 'Log In!',
        }

    def sign_in_build_workflow(self, entry, config):
        return [
            Work(
                url='/',
                method=self.sign_in_by_get,
                succeed_regex=['JPopsuki 2.0'],
                assert_state=(check_final_state, SignState.SUCCEED),
                is_base_content=True
            )
        ]

    @property
    def details_selector(self) -> dict:
        selector = super().details_selector
        net_utils.dict_merge(selector, {
            'user_id': 'user.php\\?id=(\\d+)',
            'detail_sources': {
                'default': {
                    'link': '/user.php?id={}',
                    'elements': {
                        'table': '#content > div > div.sidebar > div:nth-last-child(4) > ul',
                        'Community': '#content > div > div.sidebar > div:last-child > ul'

                    }
                }
            }
        })
        return selector
