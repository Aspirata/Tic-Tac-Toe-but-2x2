import locale
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QMessageBox, QLabel, QVBoxLayout
import random
import json
import os

class TicTacToe(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.translate("Tic Tac Toe but 2x2", "Крестики-нолики но 2x2"))
        self.current_player = "X"
        self.board = [[" " for _ in range(2)] for _ in range(2)]

        self.load_results()

        self.layout = QVBoxLayout()

        self.rules_window = QMessageBox()
        self.rules_window.setWindowTitle(self.translate("Rules and Information", "Правила и Информация"))
        self.rules_window.setText(self.translate("Welcome to Tic Tac Toe but 2x2 ! The game is played on a 2x2 grid. The first who gets two of their symbols in a row (up, down, across, or diagonally) is the winner. \
                                                 \n \
                                                 \nIf all of the squares are filled and no player has won, then the game is a draw. \
                                                 \nNote: AI always goes first.", 

                                                 "Добро пожаловать в Крестики-нолики но 2x2 ! \
                                                 \n \
                                                 \nИгра происходит на сетке 2x2. Первый, кто поставит два своих символа в ряд (вверх, вниз, горизонтально или диагонально), является победителем. Если все квадраты заполнены и никто не выиграл, то игра заканчивается вничью. \
                                                 \n \
                                                 \nПримечание: ИИ всегда ходит первым."))
        self.rules_window.exec()

        self.score_label = QLabel(self.translate(f"Player wins: {self.player_wins} | Games played: {self.games_played} | AI wins: {self.ai_wins}", f"Победы игрока: {self.player_wins} | Сыграно игр: {self.games_played} | Победы ИИ: {self.ai_wins}"))
        self.layout.addWidget(self.score_label)

        self.grid_layout = QGridLayout()
        self.buttons = [[QPushButton(" ") for _ in range(2)] for _ in range(2)]

        for row in range(2):
            for col in range(2):
                button = self.buttons[row][col]
                button.setFixedSize(100, 100)
                button.clicked.connect(lambda _, r=row, c=col: self.player_move(r, c))
                self.grid_layout.addWidget(button, row, col)

        self.layout.addLayout(self.grid_layout)
        self.setLayout(self.layout)

        self.ai_move()

    def player_move(self, row, col):
        if self.board[row][col] != " ":
            QMessageBox.warning(self, self.translate("Invalid move", "Неверный ход"), self.translate("This cell is already occupied", "Эта клетка уже занята."))
            return

        self.board[row][col] = "X"
        self.buttons[row][col].setText("X")

        winner = self.check_winner()
        if winner == "O":
            self.update_score(winner)
            QMessageBox.information(self, self.translate("Loss", "Поражение !"), self.translate("AI won", "ИИ победил."))
            self.reset_game()
            return
        
        elif winner == "X":
            self.update_score(winner)
            QMessageBox.information(self, self.translate("HOLY MOLY !", "ДА НУ НАФИГ !"), self.translate("HOW DID YOU WIN, MAGICIAN ???", "ТЫ КАК ПОБЕДИЛ, ФОКУСНИК ЧЁРТОВ ???."))
            self.reset_game()
            return

        if self.is_draw():
            self.games_played += 1
            self.update_scoreboard()
            QMessageBox.information(self, self.translate("Draw", "Ничья"), self.translate("The game ended in a draw", "Игра окончилась вничью."))
            self.reset_game()

        self.ai_move()

    def ai_move(self):
        empty_cells = [(r, c) for r in range(2) for c in range(2) if self.board[r][c] == " "]
        if not empty_cells:
            return

        row, col = random.choice(empty_cells)
        self.board[row][col] = "O"
        self.buttons[row][col].setText("O")

        winner = self.check_winner()
        if winner == "O":
            self.update_score(winner)
            QMessageBox.information(self, self.translate("Loss", "Поражение !"), self.translate("AI won", "ИИ победил."))
            self.reset_game()
            return
        
        elif winner == "X":
            self.update_score(winner)
            QMessageBox.information(self, self.translate("HOLY MOLY !", "ДА НУ НАФИГ !"), self.translate("HOW DID YOU WIN, MAGICIAN ???", "ТЫ КАК ПОБЕДИЛ, ФОКУСНИК ЧЁРТОВ ???."))
            self.reset_game()
            return

        if self.is_draw():
            self.games_played += 1
            self.update_scoreboard()
            QMessageBox.information(self, self.translate("Draw", "Ничья"), self.translate("The game ended in a draw", "Игра окончилась вничью."))
            self.reset_game()

    def check_winner(self):
        for i in range(2):
            if self.board[i][0] == self.board[i][1] and self.board[i][0] != " ":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] and self.board[0][i] != " ":
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] and self.board[0][0] != " ":
            return self.board[0][0]
        if self.board[0][1] == self.board[1][0] and self.board[0][1] != " ":
            return self.board[0][1]

        return None

    def is_draw(self):
        for row in self.board:
            if " " in row:
                return False
        return True

    def reset_game(self):
        self.board = [[" " for _ in range(2)] for _ in range(2)]
        for row in range(2):
            for col in range(2):
                self.buttons[row][col].setText(" ")
        self.ai_move()

    def update_score(self, winner):
        self.games_played += 1
        if winner == "X":
            self.player_wins += 1
        elif winner == "O":
            self.ai_wins += 1
        self.update_scoreboard()
        self.save_results()

    def update_scoreboard(self):
        self.score_label.setText(self.translate(f"Player wins: {self.player_wins} | Games played: {self.games_played} | AI wins: {self.ai_wins}", f"Победы игрока: {self.player_wins} | Сыграно игр: {self.games_played} | Победы ИИ: {self.ai_wins}"))

    def translate(self, eng_text, ru_text):
        user_language = locale.getlocale()[0]
        return ru_text if 'Ru' in user_language else eng_text

    def load_results(self):
        json_path = os.path.join(os.path.dirname(__file__), "game_results.json")
        if os.path.exists(json_path):
            with open(json_path, "r") as file:
                data = json.load(file)
                self.games_played = data["games_played"]
                self.player_wins = data["player_wins"]
                self.ai_wins = data["ai_wins"]
        else:
            self.games_played = 0
            self.player_wins = 0
            self.ai_wins = 0
    
    def save_results(self):
        results = {
            "games_played": self.games_played,
            "player_wins": self.player_wins,
            "ai_wins": self.ai_wins
        }
        json_path = os.path.join(os.path.dirname(__file__), "game_results.json")
        if os.path.exists(json_path):
            with open(json_path, "w") as file:
                json.dump(results, file)

if __name__ == "__main__":
    app = QApplication([])
    window = TicTacToe()
    window.show()
    app.exec()
