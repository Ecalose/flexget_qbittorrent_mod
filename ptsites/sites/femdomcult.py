from ..schema.luminance import Luminance
from ..schema.site_base import Work, SignState


class MainClass(Luminance):
    URL = 'https://femdomcult.org/'
    USER_CLASSES = {
        'downloaded': [5497558138880],
        'share_ratio': [1.05],
        'days': [56]
    }

    def build_login_workflow(self, entry, config):
        return [
            Work(
                url='/login.php',
                method='password',
                succeed_regex='Logout',
                check_state=('final', SignState.SUCCEED),
                is_base_content=True,
                response_urls=['/index.php']
            )
        ]

    def sign_in_by_password(self, entry, config, work, last_content):
        if not (login := entry['site_config'].get('login')):
            entry.fail_with_prefix('Login data not found!')
            return
        data = {
            'username': login['username'],
            'password': login['password'],
            'keeplogged': 1,
            'login': 'Login'
        }
        return self._request(entry, 'post', work.url, data=data)