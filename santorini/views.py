import math

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from santorini.santorini_models.board import Board
from santorini.santorini_models.minimax import minimax, alpha_beta_project, alpha_beta_custom

from .serializers import serialize_ai_move, serialize_valid_moves, deserialize_moves_request


def home_view(request):
    return render(request, 'santorini/index.html', {})


def huai_view(request):
    return render(request, 'santorini/hu_vs_ai.html', {})

@csrf_exempt
def available_moves(request):
    start_position, board, _, _ = deserialize_moves_request(request.body)
    all_avail_moves = board.get_all_available_moves()
    valid_moving_moves = [move for move in Board.get_valid_moving_moves(start_position, board, all_avail_moves)]
    list_of_valid_moves = {"moves": valid_moving_moves}
    return HttpResponse(serialize_valid_moves(list_of_valid_moves))

@csrf_exempt
def available_builds(request):
    start_position, board, _, _ = deserialize_moves_request(request.body)
    all_avail_moves = board.get_all_available_moves()
    valid_building_moves = [build for build in Board.get_valid_builds(start_position, all_avail_moves)]
    list_of_valid_builds = {"moves": valid_building_moves}
    return HttpResponse(serialize_valid_moves(list_of_valid_builds))

@csrf_exempt
def minimax_result(request):
    start_position, board, depth, maximizer = deserialize_moves_request(request.body)
    print(maximizer)
    builder_number, move, build, _ = minimax(board, maximizer, depth, None, None, None)
    return HttpResponse(serialize_ai_move(builder_number, move, build))

@csrf_exempt
def minimax_alpha_beta_result(request):
    start_position, board, depth, maximizer = deserialize_moves_request(request.body)
    builder_number, move, build, _ = alpha_beta_project(board, maximizer, depth, None, None, None, -math.inf, math.inf)
    return HttpResponse(serialize_ai_move(builder_number, move, build))

@csrf_exempt
def minimax_alpha_beta_custom_result(request):
    start_position, board, depth, maximizer = deserialize_moves_request(request.body)
    builder_number, move, build, heur = alpha_beta_custom(board, maximizer, depth, None, None, None, -math.inf, math.inf)
    return HttpResponse(serialize_ai_move(builder_number, move, build))
