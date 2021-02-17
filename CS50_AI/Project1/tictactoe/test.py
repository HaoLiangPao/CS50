from tictactoe import initial_state, player, terminal, utility

# a = initial_state()
# a = [["X", "X", "X"], [None, None, None], [None, None, None]]
a = [["X", "X", "O"], [None, None, "O"], [None, None, "O"]]
player(a)
# winner(a)
terminal(a)
utility(a)