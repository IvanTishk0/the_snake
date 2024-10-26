import pygame
from random import randint

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш пользователем"""
    """и изменяет направление змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self):
        """Инициализация объекта."""
        self.position = (GRID_WIDTH // 2 * GRID_SIZE,
                         GRID_HEIGHT // 2 * GRID_SIZE)
        self.body_color = None

    def draw(self):
        """Рисует объект на экране."""
        pass


class PoisonApple(GameObject):
    """Класс для отравленного яблока."""

    def __init__(self):
        """Инициализация отравленного яблока."""
        super().__init__()
        self.body_color = (0, 0, 255)
        self.position = self.randomize_position(
            [(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)]
        )

    def randomize_position(self, snake_positions):
        """Случайным образом выбирает позицию для яблока,"""
        """избегая занятых позиций."""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x, y)
            if self.position not in snake_positions:
                return self.position

    def draw(self):
        """Рисует отравленное яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для обычного яблока."""

    def __init__(self):
        """Инициализация обычного яблока."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position(
            [(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)]
        )

    def randomize_position(self, snake_positions):
        """Случайным образом выбирает позицию для яблока,"""
        """избегая занятых позиций."""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x, y)
            if self.position not in snake_positions:
                return self.position

    def draw(self):
        """Рисует яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(GameObject):
    """Класс для камней."""

    def __init__(self):
        """Инициализация камня."""
        super().__init__()
        self.body_color = (255, 255, 255)
        self.position = self.randomize_position(
            [(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)]
        )

    def randomize_position(self, snake_positions):
        """Случайным образом выбирает позицию для камня,"""
        """избегая занятых позиций."""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x, y)
            if self.position not in snake_positions:
                return self.position

    def draw(self):
        """Рисует камень на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__()
        self.positions = [
            (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)
        ]
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def draw(self):
        """Рисует змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def update_direction(self):
        """Обновляет направление змейки на основе следующего направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[-1]

    def move(self):
        """Двигает змейку в текущем направлении."""
        head_x, head_y = self.get_head_position()

        if self.direction == RIGHT:
            head_x += GRID_SIZE
        elif self.direction == LEFT:
            head_x -= GRID_SIZE
        elif self.direction == UP:
            head_y -= GRID_SIZE
        elif self.direction == DOWN:
            head_y += GRID_SIZE

        # Handle wrapping at the edges
        head_x %= SCREEN_WIDTH
        head_y %= SCREEN_HEIGHT

        new_head = (head_x, head_y)
        self.positions.append(new_head)

        while len(self.positions) > self.length:
            self.positions.pop(0)

    def reset(self):
        """Сбрасывает состояние змейки."""
        self.__init__()


def main():
    """Основная функция игры."""
    pygame.init()

    snake = Snake()
    apple = Apple()
    poison_apple = PoisonApple()
    stones = [Stone() for _ in range(3)]  # Список камней

    running = True
    while running:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на съедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            ap = [poison_apple.position]
            apple.position = apple.randomize_position(
                snake.positions + ap + [st.position for st in stones]
            )

        # Проверка на съедание яда
        if snake.get_head_position() == poison_apple.position:
            if snake.length > 1:
                snake.length -= 1
            else:
                snake.reset()
            ap = [apple.position]
            poison_apple.position = poison_apple.randomize_position(
                snake.positions + ap + [stone.position for stone in stones]
            )

        # Проверка на столкновение с камнем
        for stone in stones:
            if snake.get_head_position() == stone.position:
                snake.reset()
                for st in stones:
                    ap = [apple.position]
                    st.position = st.randomize_position(
                        snake.positions + ap + [poison_apple.position]
                    )
                break

        # Проверка на столкновение с собственным телом
        if snake.get_head_position() in snake.positions[:-1]:
            snake.reset()

        # Очистка экрана
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовка объектов
        apple.draw()
        poison_apple.draw()
        snake.draw()
        for stone in stones:
            stone.draw()

        # Обновление экрана
        pygame.display.update()

        # Задержка между кадрами
        clock.tick(SPEED)

    pygame.quit()


if __name__ == '__main__':
    main()
