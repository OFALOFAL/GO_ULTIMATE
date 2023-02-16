import pygame

class Window:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.DEF_FONT = pygame.font.SysFont('Corbel', 35)
        self.WIDTH = 1800
        self.HEIGHT = 950
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GOLD = (212, 175, 55)
        self.CON_TEXT = self.DEF_FONT.render('connect', True, self.BLACK)
        self.CON_BTN = pygame.Rect((self.WIDTH/2 - 100, self.HEIGHT/2 - 37.5), (200, 75))

    def draw(self, server_status, ):
        self.WIN.fill(self.WHITE)
        if server_status == 'CLOSED':
            pygame.draw.rect(self.WIN, self.RED, self.CON_BTN)
        else:
            pygame.draw.rect(self.WIN, self.GOLD, self.CON_BTN)
        self.WIN.blit(self.CON_TEXT, (self.WIDTH/2 - self.CON_TEXT.get_width()/2, self.HEIGHT/2 - self.CON_TEXT.get_height()/2))
        pygame.display.update()

    def run(self, run, server_status):
        self.draw(server_status)

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                run = False

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if self.CON_BTN.contains(pygame.Rect(pygame.mouse.get_pos(), (1, 1))):
                    return 'connect', ''

        return 'run', run
