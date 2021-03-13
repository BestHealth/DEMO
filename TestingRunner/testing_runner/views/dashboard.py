from rest_framework.decorators import api_view
from rest_framework.response import Response

from testing_runner.utils import prepare
from testing_runner.utils.decorator import request_log


@api_view(['GET'])
@request_log(level='INFO')
def possess(request):
    """
    得到相关统计信息
    """
    possess_info = prepare.get_possess_detail()
    print(possess_info)
    return Response(possess_info)
