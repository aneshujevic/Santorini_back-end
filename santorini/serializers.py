import json
from .santorini_models.board import Board


# move that AI has done returned by appropriate algorithm
def serialize_move(move):
	"""
	:param move: move returned by the AI algorithm [builder_number, move, build]
	:return: JSON string with names {"BuilderId": builder_number , "moveCoords": move, "buildCoords": build}
	"""
	names = ["BuilderId", "moveCoords", "buildCoords"]
	dict_to_serialize = dict(zip(names, move))
	return json.dumps(dict_to_serialize)


# valid moves or builds
def serialize_valid_moves(moves):
	"""
	:param moves: list of moves (be it a builds or moving moves)
	:return: JSON string which contains all available moves with appropriate number in sequence
	"""
	length = len(moves)
	dict_to_serialize = {i: moves[i] for i in range(length)}
	return json.dumps(dict_to_serialize)


# deserializing incoming JSON request carrying information about ongoing game
def deserialize_valid_moves_request(data_json):
	"""
	:param data_json: JSON data that contains information about the game coming from client
	:return: list containing starting position and board object needed for AI calculations
	"""
	decoded_info = json.loads(data_json)[0]
	board_array = decoded_info["cells"]
	board_matrix = [[board_array[i + j] for i in range(5)] for j in range(5)]
	board = Board(board_matrix)
	builders_coordinates = [
		decoded_info["firstHE"], decoded_info["secondHE"],
		decoded_info["firstJU"], decoded_info["secondJU"]
	]
	# TODO: proveriti ID-eve od buildera zbog minimaxa
	# first two builders are AI
	# second two builders are HU
	for i in range(1):
		if i < 2:
			affiliation = "AI"
		else:
			affiliation = "HU"
		new_builder = board.add_builder(affiliation, builders_coordinates[i], -(i + 1))
		builder_x = builders_coordinates[i][0]
		builder_y = builders_coordinates[i][1]
		previous_value_of_cell = (board.board_state[builder_x][builder_y] + 1) % 5
		new_builder.previous_value_of_cell = previous_value_of_cell
		board.board_state[builder_x][builder_y] = new_builder.id

	starting_position = decoded_info["startPosition"]

	return starting_position, board
