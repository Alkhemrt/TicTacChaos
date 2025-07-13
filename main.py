#main
import tkinter as tk
import tkinter.font as tkfont
import random
import copy

PLAYER_X = "😺"
PLAYER_O = "🤖"
BOARD_SIZE = 3
EVENT_CHANCE = 0.10
EVENT_DELAY = 1500
AI_MOVE_DELAY = 1000

class TicTacChaos:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Chaos")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#fffcf2")

        self.chaos_levels = {
            "Calm (0%)": 0.0,
            "Classic (10%)": 0.10,
            "Chaotic (30%)": 0.30,
            "Anarchy (60%)": 0.60,
            "Madness (90%)": 0.90,
            "Pure Mayhem (100%)": 1.0
        }

        self.current_player = PLAYER_X
        self.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.skip_next = None
        self.after_event_action = None
        self.game_over = False
        self.scores = {
            PLAYER_X: 0,
            PLAYER_O: 0,
            "draw": 0
        }
        self.score_labels = {}

        # Frame Layout
        self.left_panel = tk.Frame(self.root, bg="#ffe57f", width=250, bd=8, relief="groove")
        self.left_panel.pack(side="left", fill="y", padx=10, pady=20)

        self.right_panel = tk.Frame(self.root, bg="#fff59d", bd=10, relief="ridge")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=20)

        self.create_chaos_selector()
        self.create_mode_selector()
        self.create_score_display()
        self.create_board()
        self.status_label = tk.Label(self.right_panel, text="Your turn", font=('Cascadia Code', 18, 'bold'),
                                     bg="#fff59d", fg="#0d47a1", pady=10)
        self.status_label.pack(pady=10)

        restart_btn = tk.Button(self.left_panel, text="🔁 Restart", font=('Cascadia Code', 14, 'bold'),
                                bg="#80deea", fg="#004d40", activebackground="#4dd0e1", activeforeground="#000",
                                relief="raised", bd=6, command=self.restart_game)
        restart_btn.pack(pady=30)

    def create_chaos_selector(self):
        label = tk.Label(self.left_panel, text="Chaos Intensity", font=("Cascadia Code", 16, "bold"),
                         bg="#ffe57f", fg="#d500f9")
        label.pack(pady=10)

        self.chaos_var = tk.StringVar(value="Classic (10%)")
        dropdown = tk.OptionMenu(self.left_panel, self.chaos_var, *self.chaos_levels.keys(),
                                 command=self.update_chaos_level)
        dropdown.config(font=("Cascadia Code", 14), bg="#f8bbd0", fg="#4a148c", width=15, activebackground="#ce93d8")
        dropdown["menu"].config(font=("Cascadia Code", 12), bg="#f3e5f5")
        dropdown.pack(pady=10)

        self.update_chaos_level(self.chaos_var.get())

    def create_score_display(self):
        label = tk.Label(self.left_panel, text="Scoreboard", font=("Cascadia Code", 16, "bold"),
                         bg="#ffe57f", fg="#4a148c")
        label.pack(pady=(10, 5))

        self.score_labels[PLAYER_X] = tk.Label(self.left_panel, font=("Cascadia Code", 14),
                                               bg="#ffe57f", fg="#1a237e")
        self.score_labels[PLAYER_X].pack(pady=2)

        self.score_labels[PLAYER_O] = tk.Label(self.left_panel, font=("Cascadia Code", 14),
                                               bg="#ffe57f", fg="#b71c1c")
        self.score_labels[PLAYER_O].pack(pady=2)

        self.score_labels["draw"] = tk.Label(self.left_panel, text="🤝 Draws: 0", font=("Cascadia Code", 14),
                                             bg="#ffe57f", fg="#616161")
        self.score_labels["draw"].pack(pady=2)

        self.update_score_display()

    def update_score_display(self):
        mode = self.mode_var.get()
        if mode == "PvP":
            self.score_labels[PLAYER_X].config(text=f"😺 Player 1: {self.scores[PLAYER_X]}")
            self.score_labels[PLAYER_O].config(text=f"🐶 Player 2: {self.scores[PLAYER_O]}")
        else:
            self.score_labels[PLAYER_X].config(text=f"😺 You: {self.scores[PLAYER_X]}")
            self.score_labels[PLAYER_O].config(text=f"🤖 Computer: {self.scores[PLAYER_O]}")

        self.score_labels["draw"].config(text=f"🤝 Draws: {self.scores['draw']}")

    def update_chaos_level(self, selected):
        self.event_chance = self.chaos_levels[selected]

    def create_mode_selector(self):
        label = tk.Label(self.left_panel, text="Game Mode", font=("Cascadia Code", 16, "bold"),
                         bg="#ffe57f", fg="#00796b")
        label.pack(pady=(10, 5))

        self.mode_var = tk.StringVar(value="PvC")
        modes = [("Player vs Computer", "PvC"), ("Player vs Player", "PvP")]
        for text, mode in modes:
            rb = tk.Radiobutton(self.left_panel, text=text, variable=self.mode_var, value=mode,
                                font=("Cascadia Code", 13), bg="#ffe57f", fg="#004d40",
                                selectcolor="#b2dfdb", activebackground="#b2dfdb", command=self.restart_game)
            rb.pack(anchor="w", padx=20)

    def create_board(self):
        frame = tk.Frame(self.right_panel, bg="#fff59d")
        frame.pack(pady=20)
        funky_fonts = ["Cascadia Code", "Chalkboard", "Courier New", "Segoe Script"]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                font_name = random.choice(funky_fonts)
                btn = tk.Button(frame, text="", font=(font_name, 32, 'bold'), width=4, height=1,
                                bg="#ffffff", fg="#333", relief="groove", bd=8,
                                activebackground="#f06292", activeforeground="#000000",
                                command=lambda row=r, col=c: self.human_move(row, col))
                btn.grid(row=r, column=c, padx=6, pady=6)
                self.buttons[r][c] = btn

    def random_color(self):
        return f"#{random.randint(0x888888, 0xFFFFFF):06x}"

    def human_move(self, row, col):
        if self.game_over or self.board[row][col]:
            return
        mode = self.mode_var.get()
        if mode == "PvC" and self.current_player != PLAYER_X:
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
            self.scores[winner] += 1
            self.update_score_display()

            mode = self.mode_var.get()
            if mode == "PvP":
                winner_label = "Player 1 wins!" if winner == PLAYER_X else "Player 2 wins!"
            else:
                winner_label = "You win!" if winner == PLAYER_X else "Computer wins!"

            self.status_label.config(text=f"🎉 {winner_label}", fg="#4caf50")
            self.animate_victory(row, col)
            self.game_over = True

        elif self.is_draw():
            self.scores["draw"] += 1
            self.update_score_display()
            self.status_label.config(text="🤝 It's a draw!", fg="#9e9e9e")
            self.animate_draw()
            self.game_over = True
        else:
            self.trigger_random_event()

    def update_cell_visual(self, r, c):
        symbol = self.get_display_symbol(self.board[r][c])
        color = "#81d4fa" if symbol == PLAYER_X else "#f48fb1"
        self.buttons[r][c].config(
            text=symbol,
            fg=color,
            bg="#ffffff"
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
        self.skip_next = None
        self.game_over = False
        self.update_score_display()

        mode = self.mode_var.get()
        if mode == "PvP":
            self.status_label.config(text="Player 1's turn", fg="#2196f3", bg="#fff59d")
        else:
            self.status_label.config(text="Your turn", fg="#2196f3", bg="#fff59d")

    def trigger_random_event(self):
        if random.random() > self.event_chance:
            self.end_turn()
            return

        events = [
            ("🔁 Turns swapped!", self.event_swap_players),
            ("❌ Random cell cleared!", self.event_clear_random_cell),
            ("🔄 Extra turn!", self.event_extra_turn),
            ("🌀 Board shuffled!", self.event_shuffle_board),
            ("🎭 Roles reversed!", self.event_swap_symbols),
            ("🧹 Clean sweep!", self.event_clear_row_or_col),
            ("🔀 Symbol swap!", self.event_swap_two_cells),
            ("🪞 Mirror board!", self.event_mirror_board),
            ("💥 Bomb dropped!", self.event_explode_area),
            ("⏪ Rewind Move!", self.event_rewind_move),
            ("🔒 Cell Lockdown!", self.event_lock_random_cell),
            ("🎲 Random Move!", self.event_random_forced_move),
            ("🌪️ Diagonal Swap!", self.event_diagonal_swap),
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
            mode = self.mode_var.get()
            if mode == "PvP":
                label = "Player 1" if self.current_player == PLAYER_X else "Player 2"
                fg_color = "#2196f3" if self.current_player == PLAYER_X else "#e91e63"
                self.status_label.config(text=f"{label}'s turn", fg=fg_color)
            elif mode == "PvC":
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
            return 0, None

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

    def event_shuffle_board(self):
        cells = [self.board[r][c] for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)]
        random.shuffle(cells)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.board[r][c] = cells[r * BOARD_SIZE + c]
                self.update_cell_visual(r, c)
                self.pulse_button(self.buttons[r][c])

    def event_swap_symbols(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == PLAYER_X:
                    self.board[r][c] = PLAYER_O
                elif self.board[r][c] == PLAYER_O:
                    self.board[r][c] = PLAYER_X
                self.update_cell_visual(r, c)

        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
        self.status_label.config(text="🎭 Roles reversed!", fg="#ff5722")

    def event_clear_row_or_col(self):
        is_row = random.choice([True, False])
        idx = random.randint(0, BOARD_SIZE - 1)
        for i in range(BOARD_SIZE):
            r, c = (idx, i) if is_row else (i, idx)
            self.board[r][c] = ""
            self.buttons[r][c].config(text="")
            self.pulse_button(self.buttons[r][c])
        label = f"row {idx+1}" if is_row else f"column {idx+1}"
        self.status_label.config(text=f"🧹 Cleared {label}!", fg="#795548")

    def event_swap_two_cells(self):
        filled = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.board[r][c]]
        if len(filled) >= 2:
            (r1, c1), (r2, c2) = random.sample(filled, 2)
            self.board[r1][c1], self.board[r2][c2] = self.board[r2][c2], self.board[r1][c1]
            self.update_cell_visual(r1, c1)
            self.update_cell_visual(r2, c2)
            self.pulse_button(self.buttons[r1][c1])
            self.pulse_button(self.buttons[r2][c2])

    def event_mirror_board(self):
        for r in range(BOARD_SIZE):
            self.board[r] = list(reversed(self.board[r]))
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.update_cell_visual(r, c)
                self.pulse_button(self.buttons[r][c])
        self.status_label.config(text="🪞 Board mirrored!", fg="#3f51b5")

    def event_explode_area(self):
        center_r = random.randint(0, BOARD_SIZE - 1)
        center_c = random.randint(0, BOARD_SIZE - 1)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                r, c = center_r + dr, center_c + dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    self.board[r][c] = ""
                    self.buttons[r][c].config(text="")
                    self.pulse_button(self.buttons[r][c])
        self.status_label.config(text="💥 Bomb dropped!", fg="#d32f2f")

    def event_rewind_move(self):
        for r in reversed(range(BOARD_SIZE)):
            for c in reversed(range(BOARD_SIZE)):
                if self.board[r][c]:
                    self.board[r][c] = ""
                    self.buttons[r][c].config(text="")
                    self.pulse_button(self.buttons[r][c])
                    self.status_label.config(text="⏪ Last move undone!", fg="#607d8b")
                    return

    def event_lock_random_cell(self):
        empty = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if not self.board[r][c]]
        if empty:
            r, c = random.choice(empty)
            self.board[r][c] = "🔒"
            self.buttons[r][c].config(text="🔒", fg="#000000")
            self.status_label.config(text="🔒 A cell is now locked!", fg="#455a64")

    def event_random_forced_move(self):
        empty = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if not self.board[r][c]]
        if empty:
            r, c = random.choice(empty)
            self.board[r][c] = self.current_player
            self.update_cell_visual(r, c)
            self.pulse_button(self.buttons[r][c])
            self.status_label.config(text="🎲 Forced random move!", fg="#8e24aa")

    def event_diagonal_swap(self):
        primary = [self.board[i][i] for i in range(BOARD_SIZE)]
        secondary = [self.board[i][BOARD_SIZE - i - 1] for i in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            self.board[i][i], self.board[i][BOARD_SIZE - i - 1] = secondary[i], primary[i]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.update_cell_visual(r, c)
                self.pulse_button(self.buttons[r][c])
        self.status_label.config(text="🌪️ Diagonals swapped!", fg="#009688")

    def get_player_label(self, symbol):
        if self.mode_var.get() == "PvP":
            return "Player 1" if symbol == PLAYER_X else "Player 2"
        return "You" if symbol == PLAYER_X else "Computer"

    def get_display_symbol(self, symbol):
        mode = self.mode_var.get()
        if symbol == PLAYER_X:
            return "😺"
        if symbol == PLAYER_O:
            return "🐶" if mode == "PvP" else "🤖"
        return symbol

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
        bg_color = random.choice(["#f8bbd0", "#e1bee7", "#d1c4e9", "#b2dfdb", "#ffccbc"])
        self.status_label.config(text=f"⚠️ CHAOS: {msg}",
                                 fg=random.choice(["#d500f9", "#f44336", "#1e88e5", "#e91e63"]),
                                 bg=bg_color,
                                 font=('Cascadia Code', 20, 'bold'))

    def clear_chaos_message(self):
        self.root.after(1000, self.update_status_after_chaos)

    def update_status_after_chaos(self):
        if not self.game_over:
            mode = self.mode_var.get()
            if mode == "PvP":
                label = "Player 1" if self.current_player == PLAYER_X else "Player 2"
                fg_color = "#2196f3" if self.current_player == PLAYER_X else "#e91e63"
                self.status_label.config(text=f"{label}'s turn", fg=fg_color, bg="#fff59d")
            else:  # PvC
                if self.current_player == PLAYER_X:
                    self.status_label.config(text="Your turn", fg="#2196f3", bg="#fff59d")
                else:
                    self.status_label.config(text="🤖 Computer's thinking...", fg="#e91e63", bg="#fff59d")

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
