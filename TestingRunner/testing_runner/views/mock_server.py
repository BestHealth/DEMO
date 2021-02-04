import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from testing_runner import models
from testing_runner.utils.decorator import request_log
from testing_runner.utils import response
from testing_runner.utils.mock import mock_judgment


class MOCKServerTemplateView(GenericViewSet):

    authentication_classes = []
    permission_classes = []

    @method_decorator(request_log(level='INFO'))
    def mockServer(self, request, **kwargs):
        """
        Mock 模拟
        """
        method = request.method
        pk = kwargs['pk']
        ret_url = request.get_full_path().split('/')
        del ret_url[0:5]
        ret_url = '/' + ('/'.join(ret_url))
        url = ret_url.split('?')

        mock_obj = models.Mock.objects.filter(project=pk, url__contains=url[0], status=True).first()
        if mock_obj and mock_obj.status and mock_obj.method == method:
            runner_request_body = mock_obj.request_body.replace("'", '"')
            runner_request = json.loads(runner_request_body.replace('False', 'false')).get('request', None)

            runner_params = runner_request.get('params', None)
            runner_url = runner_request.get('url', None)
            url_params = runner_url.split('?')
            if runner_params:
                if len(url) == 1:
                    return Response(response.MOCK_PARAMS_EXISTS)
                front_params_dict = dict(url_params.split('=') for url_params in url[1].split('&'))
                runner_params_dict = dict(url_params.split('=') for url_params in url_params[1].split('&'))
                params = dict(runner_params, **runner_params_dict)
                if mock_judgment('params', params, front_params_dict) is False:
                    return Response(response.MOCK_PARAMS_EXISTS)

            headers = runner_request.get('headers', None)
            meta = request.META
            if mock_judgment('headers', headers, meta) is False:
                return Response(response.MOCK_HEADER_EXISTS)

            request_json = runner_request.get('json', None)
            runner_data = runner_request.get('data', None)
            request_body = request.data
            if runner_data:
                if mock_judgment('request', runner_data, request_body) is False:
                    return Response(response.MOCK_BODY_EXISTS)
            else:
                if mock_judgment('request', request_json, request_body) is False:
                    return Response(response.MOCK_BODY_EXISTS)

            response_body = json.loads(mock_obj.response_body.replace("'", '"'))

            content_json = response_body['response'].get('json', None)
            content_text = response_body['response'].get('text', None)
            if content_json:
                resp = HttpResponse(str(content_json), content_type='application/json,charset=utf-8')
            elif content_text:
                resp = HttpResponse(str(content_text), content_type='charset=utf-8')
            else:
                resp = HttpResponse('')
            header = response_body['response'].get('header')
            if header:
                for header_key, header_value in header.items():
                    resp[header_key] = header_value
            return resp
        return Response(response.MOCK_VISIT_EXISTS)
