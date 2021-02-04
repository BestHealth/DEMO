import json
from httprunner import HttpRunner, logger

from testing_runner.utils.loader import parse_summary

logger.setup_logger('INFO')


def mock_judgment(mock_type, runner_data, front_data):
    if runner_data:
        for data_key, data_value in runner_data.items():
            if mock_type == 'headers':
                if data_key == 'Content-Type':
                    value = front_data.get(str(data_key).replace('-', '_').upper(), None)
                else:
                    value = front_data.get('HTTP_' + str(data_key), None)
            else:
                if front_data:
                    value = front_data.get(str(data_key), None)
                else:
                    return False
            if value:
                if data_value != value:
                    return False
            else:
                return False


def run_mock(mock_obj, base_url):
    mock = mock_obj.request_body.replace("'", '"')
    mock = json.loads(mock.replace('False', 'false'))

    runner_url = mock.get('request').get('url')
    runner_url = runner_url.split('?')
    mock_url = base_url + '/api/runner/mock/' + str(mock_obj.project_id) + str(runner_url[0])

    params = {}
    if len(runner_url) > 1:
        params = dict(url_params.split('=') for url_params in runner_url[1].split('&'))
        runner_params = mock.get('request').get('params', None)
        if runner_params:
            params = dict(params, **runner_params)

    kwargs = {
        'failfast': False
    }

    data = [{
        'config': {
            'name': mock.get('name', None),
        },
        'teststeps': [{
            'name': mock.get('name', None),
            'description': mock.get('description', None),
            'times': 1,
            'request': {
                'url': mock_url,
                'params': params,
                'headers': mock.get('request').get('headers', None),
                'method': mock.get('request').get('method'),
                'json': mock.get('request').get('json', None),
                'data': mock.get('request').get('data', None)
            }
        }]
    }]

    runner = HttpRunner(**kwargs)
    runner.run(data)
    summary = parse_summary(runner.summary)

    return summary
