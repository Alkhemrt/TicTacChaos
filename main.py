import tkinter as tk
import random
import copy

PLAYER_X = "😺"
PLAYER_O = "🤖"
BOARD_SIZE = 3
EVENT_CHANCE = 0.34
EVENT_DELAY = 1500
AI_MOVE_DELAY = 1000

class TicTacChaos:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Chaos")
        self.root.geometry("900x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#fffcf2")

        self.current_player = PLAYER_X
        self.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.skip_next = None
        self.after_event_action = None
        self.game_over = False

        self.status_label = tk.Label(root, text="Your turn", font=('Comic Sans MS', 18, 'bold'), bg="#fffcf2")
        self.status_label.pack(pady=10)

        self.create_board()

        restart_btn = tk.Button(root, text="🔁 Restart", font=('Comic Sans MS', 14, 'bold'),
                                bg="#ffd966", fg="#333", command=self.restart_game)
        restart_btn.pack(pady=10)

    def create_board(self):
        frame = tk.Frame(self.root, bg="#fffcf2")
        frame.pack()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                btn = tk.Button(frame, text="", font=('Comic Sans MS', 32), width=4, height=2,
                                bg="#ffffff", fg="#333", relief="ridge", bd=6,
                                command=lambda row=r, col=c: self.human_move(row, col))
                btn.grid(row=r, column=c, padx=6, pady=6)
                self.buttons[r][c] = btn

    def human_move(self, row, col):
        if self.current_player != PLAYER_X or self.game_over:
            return
        self.animate_click(self.buttons[row][col])
        self.make_move(row, col)

    def make_move(self, row, col):
        if self.board[row][col] or self.check_winner():
            return

        if self.skip_next == self.current_player:
            self.status_label.config(text=f"{self.get_player_label(self.current_player)}'s turn was skipped!")
            self.skip_next = None
            self.end_turn()
            return

        self.board[row][col] = self.current_player
        self.update_cell_visual(row, col)

        winner = self.check_winner()
        if winner:
            winner_label = "You win!" if winner == PLAYER_X else "Computer wins!"
            self.status_label.config(text=f"🎉 {winner_label}", fg="#4caf50")
            self.animate_victory(row, col)
            self.game_over = True
        elif self.is_draw():
            self.status_label.config(text="🤝 It's a draw!", fg="#9e9e9e")
            self.animate_draw()
            self.game_over = True
        else:
            self.trigger_random_event()

    def update_cell_visual(self, r, c):
        symbol = self.board[r][c]
        self.buttons[r][c].config(
            text=symbol,
            fg="#2196f3" if symbol == PLAYER_X else "#e91e63"
        )

    def switch_player(self):
        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X

    def is_draw(self):
        return all(self.board[r][c] for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))

    def check_winner(self):
        lines = []
        for i in range(BOARD_SIZE):
            lines.append(self.board[i])
            lines.append([self.board[j][i] for j in range(BOARD_SIZE)])
        lines.append([self.board[i][i] for i in range(BOARD_SIZE)])
        lines.append([self.board[i][BOARD_SIZE - i - 1] for i in range(BOARD_SIZE)])

        for line in lines:
            if line.count(line[0]) == BOARD_SIZE and line[0] != "":
                return line[0]
        return None

    def restart_game(self):
        self.current_player = PLAYER_X
        self.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                btn = self.buttons[r][c]
                btn.config(text="", bg="#ffffff", fg="#333")
        self.status_label.config(text="Your turn", fg="#000")
        self.skip_next = None
        self.game_over = False

    def trigger_random_event(self):
        if random.random() > EVENT_CHANCE:
            self.end_turn()
            return

        events = [
            ("🔁 Turns swapped!", self.event_swap_players),
            ("❌ Random cell cleared!", self.event_clear_random_cell),
            ("🔄 Extra turn!", self.event_extra_turn),
            ("⛔ Skip a turn!", self.event_skip_opponent_turn),
            ("🌀 Board shuffled!", self.event_shuffle_board)
        ]

        message, effect = random.choice(events)
        self.show_chaos_message(message)
        self.root.after(EVENT_DELAY, lambda: self.apply_event(effect))

    def apply_event(self, effect):
        effect()
        if self.after_event_action:
            self.after_event_action()
            self.after_event_action = None
        self.clear_chaos_message()
        self.end_turn()

    def end_turn(self):
        if not self.skip_next == self.current_player:
            self.switch_player()
        if not self.game_over:
            if self.current_player == PLAYER_O:
                self.status_label.config(text="🤖 Computer's thinking...", fg="#e91e63")
                self.root.after(AI_MOVE_DELAY, self.ai_move)
            else:
                self.status_label.config(text="Your turn", fg="#2196f3")

    def ai_move(self):
        if self.skip_next == PLAYER_O:
            self.status_label.config(text="Computer's turn was skipped!", fg="#e91e63")
            self.skip_next = None
            self.switch_player()
            self.status_label.config(text="Your turn", fg="#2196f3")
            return

        _, move = self.minimax(copy.deepcopy(self.board), PLAYER_O)
        if move:
            row, col = move
            self.animate_click(self.buttons[row][col])
            self.make_move(row, col)

    def minimax(self, board, player, depth=0):
        winner = self.check_winner_static(board)
        if winner == PLAYER_O:
            return 10 - depth, None
        elif winner == PLAYER_X:
            return depth - 10, None
        elif all(board[r][c] for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
            return 0, None  # Draw

        opponent = PLAYER_X if player == PLAYER_O else PLAYER_O
        best = (-float('inf'), None) if player == PLAYER_O else (float('inf'), None)

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if not board[r][c]:
                    board[r][c] = player
                    score, _ = self.minimax(board, opponent, depth + 1)
                    board[r][c] = ""
                    if player == PLAYER_O:
                        if score > best[0]:
                            best = (score, (r, c))
                    else:
                        if score < best[0]:
                            best = (score, (r, c))

        return best

    def check_winner_static(self, board):
        lines = []
        for i in range(BOARD_SIZE):
            lines.append(board[i])
            lines.append([board[j][i] for j in range(BOARD_SIZE)])
        lines.append([board[i][i] for i in range(BOARD_SIZE)])
        lines.append([board[i][BOARD_SIZE - i - 1] for i in range(BOARD_SIZE)])
        for line in lines:
            if line.count(line[0]) == BOARD_SIZE and line[0] != "":
                return line[0]
        return None

    # === Chaos Events ===
    def event_swap_players(self):
        self.switch_player()
        self.status_label.config(text="🔁 Turns swapped!", fg="#ff9800")

    def event_clear_random_cell(self):
        filled = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.board[r][c]]
        if filled:
            r, c = random.choice(filled)
            self.board[r][c] = ""
            self.buttons[r][c].config(text="")
            self.pulse_button(self.buttons[r][c])

    def event_extra_turn(self):
        self.status_label.config(text="🔄 Extra turn!", fg="#00bcd4")
        self.after_event_action = lambda: self.switch_player()

    def event_skip_opponent_turn(self):
        self.skip_next = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
        label = self.get_player_label(self.skip_next)
        self.status_label.config(text=f"⛔ {label} skips next turn!", fg="#9c27b0")

    def event_shuffle_board(self):
        cells = [self.board[r][c] for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)]
        random.shuffle(cells)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.board[r][c] = cells[r * BOARD_SIZE + c]
                self.update_cell_visual(r, c)
                self.pulse_button(self.buttons[r][c])

    def get_player_label(self, symbol):
        return "You" if symbol == PLAYER_X else "Computer"

    # === Animations ===
    def animate_click(self, btn, step=0):
        colors = ["#fff", "#fdd", "#faa", "#fdd", "#fff"]
        if step < len(colors):
            btn.config(bg=colors[step])
            self.root.after(50, lambda: self.animate_click(btn, step + 1))

    def pulse_button(self, btn, step=0):
        colors = ["#ffe0b2", "#ffcc80", "#ffb74d", "#ffa726", "#ff9800", "#ffffff"]
        if step < len(colors):
            btn.config(bg=colors[step])
            self.root.after(80, lambda: self.pulse_button(btn, step + 1))

    def show_chaos_message(self, msg):
        self.status_label.config(text=f"⚠️ CHAOS: {msg}", fg="#f44336", font=('Comic Sans MS', 18, 'bold'))

    def clear_chaos_message(self):
        self.root.after(1000, self.update_status_after_chaos)

    def update_status_after_chaos(self):
        if not self.game_over:
            if self.current_player == PLAYER_X:
                self.status_label.config(text="Your turn", fg="#2196f3")
            else:
                self.status_label.config(text="🤖 Computer's thinking...", fg="#e91e63")

    def animate_victory(self, row, col, step=0):
        blink_colors = ["#4caf50", "#ffffff"] * 5
        if step < len(blink_colors):
            self.status_label.config(fg=blink_colors[step])
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    if self.board[r][c] == self.current_player:
                        self.buttons[r][c].config(bg=blink_colors[step])
            self.root.after(150, lambda: self.animate_victory(row, col, step + 1))

    def animate_draw(self, step=0):
        colors = ["#d7ccc8", "#cfd8dc", "#eceff1", "#f5f5f5", "#ffffff", "#f5f5f5", "#eceff1", "#cfd8dc", "#d7ccc8"]
        if step < len(colors):
            self.status_label.config(fg=colors[step])
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    self.buttons[r][c].config(bg=colors[step])
            self.root.after(120, lambda: self.animate_draw(step + 1))

# === Launch Game ===
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacChaos(root)
    root.mainloop()