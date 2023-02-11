from flask import Flask, request, jsonify
import chess
import chess.pgn
import chess.engine
app = Flask(__name__)
engine = chess.engine.SimpleEngine.popen_uci("./sfish/sfish")
@app.route('/next-move', methods=['POST'])
def next_move():
    fen = request.headers.get('fen')
    board = chess.Board(fen)
    result = engine.play(board, chess.engine.Limit(time=0.2))
    next_move = result.move.uci()
    san_next_move = board.san(result.move)
    turn = None
    if board.turn == chess.WHITE:
        turn = 'white'
    else:
        turn = 'black'
    ip = request.remote_addr
    print("Sent next move: " + next_move + " To: " + ip)
    return jsonify({'turn': turn, 'next_move': next_move, 'san_next_move': san_next_move})


if __name__ == '__main__':
    app.run()
