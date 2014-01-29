# -*- coding: utf-8 -*-

import urllib2
# Import Salt Testing libs
from salttesting import skipIf, TestCase
from salttesting.helpers import ensure_in_syspath
from salttesting.mock import NO_MOCK, NO_MOCK_REASON, MagicMock, Mock, patch

from salt.modules import uwsgi

ensure_in_syspath('../../')

uwsgi.__salt__ = {}

class MockUrllibStatus(object):
    """Mock of urllib2 call for Nginx status"""
    def read(self):
        return MOCK_STATUS_OUTPUT
    
    def close(self):
        pass

@skipIf(NO_MOCK, NO_MOCK_REASON)
@patch('salt.utils.which', Mock(return_value='/usr/bin/uwsgi'))
class UwsgiTestCase(TestCase):

    def test_uwsgi_stats(self):
        socket = "127.0.0.1:5050"
        mock = MagicMock(return_value='{"a": 1, "b": 2}')
        with patch.dict(uwsgi.__salt__, {'cmd.run': mock}):
            result = uwsgi.stats(socket)
            mock.assertCalledWith(socket)
            self.assertEqual(result, {'a': 1, 'b': 2})
        

if __name__ == '__main__':
    from integration import run_tests
    run_tests(UwsgiTestCase, needs_daemon=False)