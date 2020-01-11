from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .serializers import serialize_move, serialize_valid_moves, deserialize_valid_moves_request


# do the csrf thingy :)
@csrf_exempt
def available_moves(request):
    start_position, board = deserialize_valid_moves_request(request.body)
    print(start_position)
    print(board)
    return HttpResponse("")


def available_builds(request):
    return None


def minimax(request):
    return None


def minimax_alpha_beta(request):
    return None


def minimax_alpha_beta_custom(request):
    return None