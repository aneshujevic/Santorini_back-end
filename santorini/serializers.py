import json
from .santorini_models.board import Board


# move that AI has done returned by appropriate algorithm
def serialize_move(move):
    """
    :param move: move returned by the AI algorithm [builder_number, move, build]
    :return: JSON object with names {"BuilderId": builder_number , "moveCoords": move, "buildCoords": build}
    """
    names = ["BuilderId", "moveCoords", "buildCoords"]
    dict_to_serialize = dict(zip(names, move))
    return json.dumps(dict_to_serialize)


# valid moves or builds
def serialize_valid_moves(moves):
    """
    :param moves: dictionary of moves (be it a builds or moving moves)
    :return: JSON object which contains all available moves with appropriate number in sequence
    """
    return json.dumps(moves)


# serializing move that AI should do
def serialize_ai_move(builder_number, move, build):
    """
    :param builder_number: id of builder that should be moved
    :param move: coordinates where to move the builder
    :param build: coordinates where to build a block
    :return: JSON object which contains information about the move that AI should do
    """
    builder_number = -builder_number
    dict_to_serialize = {"id": builder_number, "move": move, "build": build}
    return json.dumps(dict_to_serialize)

# deserializing incoming JSON request carrying information about ongoing game
def deserialize_moves_request(data_json):
    """
    :param data_json: JSON data that contains information about the game coming from client
    :return: list containing starting position and board object needed for AI calculations
    """
    decoded_info = json.loads(data_json)[0]
    board_array = decoded_info["cells"]
    board_matrix = [[board_array[i + j * 5] for i in range(5)] for j in range(5)]
    board = Board(board_matrix)
    
    maximizer = True

    if "minNext" in decoded_info:
        maximizer = not decoded_info["minNext"]

    builders_coordinates = [
        [decoded_info["firstHE"] // 5, decoded_info["firstHE"] % 5],
        [decoded_info["secondHE"] // 5, decoded_info["secondHE"] % 5],
        [decoded_info["firstJU"] // 5, decoded_info["firstJU"] % 5],
        [decoded_info["secondJU"] // 5, decoded_info["secondJU"] % 5]
    ]

    # first two builders are AI
    # second two builders are HU
    for i in range(4):
        if i < 2:
            affiliation = "AI"
        else:
            affiliation = "HU"
        builder_x = builders_coordinates[i][0]
        builder_y = builders_coordinates[i][1]
        previous_value_of_cell = board.board_state[builder_x][builder_y]
        new_builder = board.add_builder(affiliation, builders_coordinates[i], - (i + 1))
        new_builder.previous_value_of_cell = previous_value_of_cell
        board.board_state[builder_x][builder_y] = new_builder.id

    starting_position = decoded_info["startPosition"]
    depth = decoded_info["depth"]
    return starting_position, board, depth, maximizer
