from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from santorini.santorini_models.board import Board

from .serializers import serialize_move, serialize_valid_moves, deserialize_valid_moves_request


# do the csrf thingy :)
@csrf_exempt
def available_moves(request):
    start_position, board = deserialize_valid_moves_request(request.body)
    all_avail_moves = board.get_all_available_moves()
    list_of_valid_moves = {"moves": Board.get_valid_moving_moves(start_position, board, all_avail_moves)}
    return HttpResponse(serialize_valid_moves(list_of_valid_moves))

@csrf_exempt
def available_builds(request):
    start_position, board = deserialize_valid_moves_request(request.body)
    all_avail_moves = board.get_all_available_moves()
    list_of_valid_builds = {"moves": Board.get_valid_builds(start_position, all_avail_moves)}
    print(start_position)
    print(board)
    print(list_of_valid_builds)
    return HttpResponse(serialize_valid_moves(list_of_valid_builds))


def minimax(request):
    return None


def minimax_alpha_beta(request):
    return None


def minimax_alpha_beta_custom(request):
    return None