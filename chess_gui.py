import pygame
import chess
from typing import Optional, List

BOARD_SIZE = 600
SQUARE_SIZE = BOARD_SIZE // 8
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)
HIGHLIGHT_COLOR = (186, 202, 68)
MOVE_COLOR = (246, 246, 105)

PIECE_UNICODE = {
    chess.PAWN:   ('♙', '♟'),
    chess.KNIGHT: ('♘', '♞'),
    chess.BISHOP: ('♗', '♝'),
    chess.ROOK:   ('♖', '♜'),
    chess.QUEEN:  ('♕', '♛'),
    chess.KING:   ('♔', '♚'),
}

class ChessGUI:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Chess GUI")
        self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('DejaVu Sans', SQUARE_SIZE)
        self.board = chess.Board()
        self.selected_square: Optional[chess.Square] = None
        self.legal_moves: List[chess.Move] = []
        self.running = True

    def square_to_xy(self, square: chess.Square) -> tuple[int, int]:
        file = chess.square_file(square)
        rank = 7 - chess.square_rank(square)
        return file * SQUARE_SIZE, rank * SQUARE_SIZE

    def xy_to_square(self, x: int, y: int) -> chess.Square:
        file = x // SQUARE_SIZE
        rank = 7 - (y // SQUARE_SIZE)
        return chess.square(file, rank)

    def draw_board(self) -> None:
        for rank in range(8):
            for file in range(8):
                square = chess.square(file, 7 - rank)
                color = LIGHT_COLOR if (file + rank) % 2 == 0 else DARK_COLOR
                rect = pygame.Rect(file * SQUARE_SIZE, rank * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                if self.selected_square == square:
                    pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, rect)
                if any(m.to_square == square for m in self.legal_moves):
                    pygame.draw.rect(self.screen, MOVE_COLOR, rect)
                piece = self.board.piece_at(square)
                if piece:
                    text = PIECE_UNICODE[piece.piece_type][int(not piece.color)]
                    text_surf = self.font.render(text, True, (0, 0, 0))
                    text_rect = text_surf.get_rect(center=rect.center)
                    self.screen.blit(text_surf, text_rect)

    def handle_click(self, x: int, y: int) -> None:
        square = self.xy_to_square(x, y)
        piece = self.board.piece_at(square)
        if self.selected_square is None:
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.legal_moves = [m for m in self.board.legal_moves if m.from_square == square]
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
            self.selected_square = None
            self.legal_moves = []

    def draw_game_over(self) -> None:
        if self.board.is_game_over():
            overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            result = self.board.result()
            if self.board.is_checkmate():
                if result == '1-0':
                    text = 'White wins by checkmate'
                else:
                    text = 'Black wins by checkmate'
            elif self.board.is_stalemate():
                text = 'Draw by stalemate'
            elif self.board.is_insufficient_material():
                text = 'Draw by insufficient material'
            else:
                text = 'Draw'
            msg = self.font.render(text, True, (255, 255, 255))
            rect = msg.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2))
            self.screen.blit(msg, rect)

    def new_game(self) -> None:
        self.board.reset()
        self.selected_square = None
        self.legal_moves = []

    def undo(self) -> None:
        if self.board.move_stack:
            self.board.pop()
            self.selected_square = None
            self.legal_moves = []

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    self.handle_click(x, y)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.new_game()
                    elif event.key == pygame.K_u:
                        self.undo()

            self.draw_board()
            self.draw_game_over()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == '__main__':
    gui = ChessGUI()
    gui.run()
