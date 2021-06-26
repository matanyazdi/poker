import pygame
import sys
import time
import socket

IP = "127.0.0.1"
PORT = 42069

black = 0, 0, 0
red = 255, 0, 0
darkred = 140, 0, 0
darkerred = 100, 0, 0
green = 0, 255, 0
darkgreen = 0, 90, 0
pygame.init()
gamesize = 1375, 907
loginsize = 1280, 720
loginscreen = pygame.display.set_mode(loginsize)
font = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()
players = [0, 0, 0, 0]
yourturn = True
bet_on_table = 0
time_limit = 20
timer_counter = time_limit


class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text, pos, font, color, size):
        self.x, self.y = pos
        self.color = color
        self.text = text
        self.width, self.height = size
        self.draw(font)

    def draw(self, font):
        """Create the button"""
        pygame.draw.rect(loginscreen, self.color, (self.x, self.y, self.width, self.height), 0)
        self.change_text(font)

    def change_text(self, font):
        """Change the text whe you click"""
        self.font = pygame.font.SysFont("Arial", font)
        text = self.font.render(self.text, True, pygame.Color("White"))
        loginscreen.blit(text, (
        self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def click(self):
        if self.text == "Start":
            return True
        elif self.text == "amount":
            return True
        else:
            return False

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


def main():
    connect = False
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((IP, PORT))
    except:
        if not connect:
            connect = False
            print("not connected yet")
            time.sleep(5)
            main()
    connect = True
    if connect:
        print("connected")
        startpage(server)


def gamepage(server):
    gamescreen = pygame.display.set_mode(gamesize)
    gamescreen.fill(pygame.Color('black'))
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    background = pygame.image.load("backround.png")  # create background
    background = pygame.transform.smoothscale(background, (1375, 907))  # ^^
    gamescreen.blit(background, background.get_rect())  # create background
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    game_image = pygame.image.load("Poker_board.png")  # create table
    game_image_rect = game_image.get_rect()  # ^^
    gamescreen.blit(game_image, game_image_rect)  # create table
    continue1 = True
    betbutton = Button("bet", (450, 840), 50, red, size=(180, 60))  # bet button
    amountbutton = Button("amount", (790, 840), 50, green, size=(180, 60))  # amount bet button
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    base_font = pygame.font.SysFont("Arial", 25)  # create bet amount
    bet_on_table = 0
    bet_on_table_place = pygame.Rect(600, 280, 160, 57)
    amount_text = "enter amount"
    bet_text = "Bet on table"
    input_bet_amount = pygame.Rect(600, 480, 161, 57)
    color_active = (0, 255, 255)
    color_passive = (0, 213, 255)
    amount_active = False
    betactive = True  # end create bet amount
    yourturn = False
    cards_list = []
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    timer_place = pygame.Rect(0, 0, 160, 57)  # create timer place
    input = server.recv(1024).decode('UTF-8')
    print(input)
    if input == "startgame":
        players = server.recv(1024).decode('UTF-8')
        print(players)
        players = int(players)
        while True:

            input = server.recv(1024).decode('UTF-8')
            print(input)
            if input == "first round":
                card1 = server.recv(1024).decode('UTF-8')
                print(card1)
                card2 = server.recv(1024).decode('UTF-8')
                print(card2)
                location = server.recv(1024).decode('UTF-8')
                location = int(location)
                drawcards(gamescreen, card1, card2, location)
                draw_middle_cards(gamescreen, "back", "back", "back", "back", "back")
                for i in range(players):
                    if location != i:
                        drawcards(gamescreen, "back", "back", i)
            elif input == "2nd round":
                card1 = server.recv(1024).decode('UTF-8')
                card2 = server.recv(1024).decode('UTF-8')
                card3 = server.recv(1024).decode('UTF-8')
                draw_middle_cards(gamescreen, card1, card2, card3, "back", "back")
            elif input == "3rd round":
                card1 = server.recv(1024).decode('UTF-8')
                card2 = server.recv(1024).decode('UTF-8')
                card3 = server.recv(1024).decode('UTF-8')
                card4 = server.recv(1024).decode('UTF-8')
                draw_middle_cards(gamescreen, card1, card2, card3, card4, "back")
            elif input == "4th round":
                card1 = server.recv(1024).decode('UTF-8')
                card2 = server.recv(1024).decode('UTF-8')
                card3 = server.recv(1024).decode('UTF-8')
                card4 = server.recv(1024).decode('UTF-8')
                card5 = server.recv(1024).decode('UTF-8')
                draw_middle_cards(gamescreen, card1, card2, card3, card4, card5)
            elif input == "5th round":
                pass
            elif input == "6th round":
                location = 0
                for i in range(players):
                    cards_list.append(server.recv(1024).decode('UTF-8'))
                    cards_list.append(server.recv(1024).decode('UTF-8'))
                for card in cards_list:
                    drawcards(gamescreen, card[0], card[1], location)
                    location += 1

            for i in range(players):
                yourturn = True
                pygame.display.update()
                if yourturn:  # create timer
                    start_timer = time.time()
                    elapsed_time = time.time() - start_timer
                    if elapsed_time > time_limit:
                        if amount_text == "enter amount":
                            bet_on_table += 500
                        else:
                            bet_on_table += int(amount_text)
                    timer = time_limit - int(elapsed_time)
                    text_timer = base_font.render(str(timer), True, (0, 0, 0))
                    pygame.draw.rect(gamescreen, (0, 255, 255), timer_place)
                    gamescreen.blit(text_timer, (0, 30))
                    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
                    create_bet_text = base_font.render(bet_text, True, (0, 0, 0))
                    gamescreen.blit(create_bet_text, (612, 282))
                    pygame.draw.rect(gamescreen, (0, 255, 255), bet_on_table_place)
                    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
                    create_bet_on_table = base_font.render(str(bet_on_table), True, (0, 0, 0))
                    gamescreen.blit(create_bet_on_table, (600, 310))
                    if betactive == True:
                        color = color_active
                    else:
                        color = color_passive
                    text_surface = base_font.render(amount_text, True, (0, 0, 0))
                    if amount_active:  # check if amount active(have pressed)
                        for i in range(len(amount_text)):
                            if amount_text == "enter amount":
                                pass
                            elif not amount_text[i:i + 1].isnumeric():
                                amount_text = amount_text[:i] + amount_text[i + 1:]
                        pygame.draw.rect(gamescreen, pygame.Color(color), input_bet_amount)
                        gamescreen.blit(text_surface, (605, 492))

                    for event in pygame.event.get():  # events
                        pos = pygame.mouse.get_pos()
                        # if event.type == pygame.QUIT:#quit
                        #     quit()
                        if event.type == pygame.MOUSEMOTION:  # quit if over the button
                            if betbutton.isOver(pos):
                                betbutton = Button("bet", (450, 840), 50, darkred, size=(180, 60))
                            else:
                                betbutton = Button("bet", (450, 840), 50, red, size=(180, 60))
                            if amountbutton.isOver(pos):
                                amountbutton = Button("amount", (790, 840), 50, darkgreen, size=(180, 60))
                            else:
                                amountbutton = Button("amount", (790, 840), 50, green, size=(180, 60))

                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if amountbutton.isOver(pos) and amountbutton.click():
                                amount_active = True
                                pygame.draw.rect(gamescreen, pygame.Color(color), input_bet_amount)
                                gamescreen.blit(text_surface, (605, 492))
                            if input_bet_amount.collidepoint(pos):
                                betactive = True
                            else:
                                betactive = False

                        if event.type == pygame.KEYDOWN:
                            if betactive:
                                if amount_text == "enter amount":
                                    amount_text = ""
                                if event.key == pygame.K_BACKSPACE:
                                    amount_text = amount_text[:-1]
                                elif event.key == pygame.K_RETURN:
                                    if amount_active and betactive:
                                        bet_on_table += int(amount_text)
                                        create_bet_on_table = base_font.render(str(bet_on_table), True, (0, 0, 0))
                                        gamescreen.blit(background, background.get_rect())
                                        betbutton = Button("bet", (450, 840), 50, red, size=(180, 60))
                                        amountbutton = Button("amount", (790, 840), 50, green, size=(180, 60))
                                        amount_active = False
                                        betactive = False

                                        gamescreen.blit(game_image, game_image_rect)

                                else:
                                    if amount_text.isalpha():
                                        amount_text = amount_text[:-1]
                                    else:
                                        amount_text += event.unicode
                server.send((str(bet_on_table)).encode('UTF-8'))
            else:
                bet = server.recv(1024).decode('UTF-8')
                print(bet)
                bet_on_table += int(bet)
                create_bet_on_table = base_font.render(str(bet_on_table), True, (0, 0, 0))
                gamescreen.blit(create_bet_on_table, (600, 310))
            clock.tick(60)
    else:
        gamescreen = pygame.display.set_mode(gamesize)
        gamescreen.fill(pygame.Color('black'))
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
        background = pygame.image.load("backround.png")  # create background
        background = pygame.transform.smoothscale(background, (1375, 907))  # ^^
        gamescreen.blit(background, background.get_rect())  # create background
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
        game_image = pygame.image.load("Poker_board.png")  # create table
        game_image_rect = game_image.get_rect()  # ^^
        gamescreen.blit(game_image, game_image_rect)  # create table
        time.sleep(5)


def drawcards(screen1, card1, card2, location):
    CardSpot = {
        4: [(600, 150), (700, 150)],
        1: [(296, 338), (243, 338)],
        2: [(69, 203), (114, 203)],
        3: [(243, 69), (288, 69)],
        0: [(600, 570), (700, 570)],
        5: [(765, 203), (809, 203)]
    }
    # card 1
    card1 = pygame.image.load(f"cards/{card1}.png")
    card1 = pygame.transform.smoothscale(card1, (57, 88))  # size dived by 12 of the table picture size
    screen1.blit(card1, CardSpot[location][0])

    # card 2
    card2 = pygame.image.load(f"cards/{card2}.png")
    card2 = pygame.transform.smoothscale(card2, (57, 88))  # size dived by 12 of the table picture size
    screen1.blit(card2, CardSpot[location][1])

def draw_middle_cards(screen1, card1, card2, card3, card4, card5):
    Middle_Spots = {
        0: [(510, 360), (580, 360), (650, 360), (720, 360), (790, 360)]
    }
    # middle card 1
    mcard1 = pygame.image.load(f"cards/{card1}.png")
    mcard1 = pygame.transform.smoothscale(mcard1, (57, 88))  # size dived by 12 of the table picture size
    screen1.blit(mcard1, Middle_Spots[0][0])

    # middle card 2
    mcard2 = pygame.image.load(f"cards/{card2}.png")
    mcard2 = pygame.transform.smoothscale(mcard2, (57, 88))  # size dived by 12 of the table picture size
    screen1.blit(mcard2, Middle_Spots[0][1])

    # middle card 3
    mcard3 = pygame.image.load(f"cards/{card3}.png")
    mcard3 = pygame.transform.smoothscale(mcard3, (57, 88))  # size dived by 12 of the table picture size
    screen1.blit(mcard3, Middle_Spots[0][2])

    # middle card 4
    mcard4 = pygame.image.load(f"cards/{card4}.png")
    mcard4 = pygame.transform.smoothscale(mcard4, (57, 88))  # size dived by 12 of the table picture size
    screen1.blit(mcard4, Middle_Spots[0][3])

    # middle card 5
    mcard5 = pygame.image.load(f"cards/{card5}.png")
    mcard5 = pygame.transform.smoothscale(mcard5, (57, 88))  # size dived by 12 of the table picture size
    screen1.blit(mcard5, Middle_Spots[0][4])


def startpage(server):
    loginscreen.fill(black)
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    start_game_image = pygame.image.load("login.png")
    start_game_imagerect = start_game_image.get_rect()
    loginscreen.blit(start_game_image, start_game_imagerect)
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    game_register = pygame.image.load("register.png")  # register image
    game_register = pygame.transform.smoothscale(game_register, (1216, 608))  # register image
    loginscreen.blit(game_register, (400, 30))
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    startbutton = Button("Start", (515, 550), font=70, color=black, size=(250, 100))  # create start button
    registerbutton = Button("Register", (930, 500), font=40, color=black, size=(162, 75))  # create register button
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    continue1 = True
    base_font = pygame.font.SysFont("Cabin-Bold", 50)
    register_font = pygame.font.SysFont("Cabin-Bold", 30)
    error_font = pygame.font.SysFont("Cabin-Bold", 25)
    color_active = pygame.Color(darkred)
    color_passive = pygame.Color(darkerred)
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    input_name = pygame.Rect(505, 285, 161, 50)  # create username text
    user_text = ""
    ucolor = color_passive
    useractive = False
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    input_password = pygame.Rect(505, 345, 161, 50)  # create password text
    pass_text = ""
    pcolor = color_passive
    passactive = False
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    input_user_reg = pygame.Rect(860, 235, 170, 20)
    user_reg_text = "USERNAME"
    user_reg_active = False
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    input_email_reg = pygame.Rect(860, 290, 170, 20)
    email_reg_text = "EMAIL"
    email_reg_active = False
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    input_reemail_reg = pygame.Rect(860, 345, 170, 20)
    reemail_reg_text = "RE EMAIL"
    reemail_reg_active = False
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    input_pass_reg = pygame.Rect(860, 398, 170, 20)
    pass_reg_text = "PASSWORD"
    pass_reg_active = False
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    input_repass_reg = pygame.Rect(860, 446, 170, 20)
    repass_reg_text = "RE PASSWORD"
    repass_reg_active = False
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    while continue1:
        usernametext = base_font.render(user_text, True, (255, 255, 255))  # create user text
        input_name.w = max(160, usernametext.get_width() + 10)
        pygame.draw.rect(loginscreen, ucolor, input_name)
        loginscreen.blit(usernametext, (input_name.x + 5, input_name.y + 9))
        if useractive:
            ucolor = color_active
        else:
            ucolor = color_passive  # end user
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
        passwordtext = base_font.render(pass_text, True, (255, 255, 255))  # create password text
        input_password.w = max(160, passwordtext.get_width() + 10)
        pygame.draw.rect(loginscreen, pcolor, input_password)
        loginscreen.blit(passwordtext, (input_password.x + 5, input_password.y + 9))
        if passactive:
            pcolor = color_active
        else:
            pcolor = color_passive  # end password
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
        user_register_text = register_font.render(user_reg_text, True, (255, 255, 255))  # create username register text
        pygame.draw.rect(loginscreen, black, input_user_reg)
        loginscreen.blit(user_register_text, (input_user_reg.x, input_user_reg.y))
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
        email_regist_text = register_font.render(email_reg_text, True, (255, 255, 255))  # create email register text
        pygame.draw.rect(loginscreen, black, input_email_reg)
        loginscreen.blit(email_regist_text, (input_email_reg.x, input_email_reg.y))
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
        reemail_regist_text = register_font.render(reemail_reg_text, True,
                                                   (255, 255, 255))  # create re email register text
        pygame.draw.rect(loginscreen, black, input_reemail_reg)
        loginscreen.blit(reemail_regist_text, (input_reemail_reg.x, input_reemail_reg.y))
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
        pass_regist_text = register_font.render(pass_reg_text, True, (255, 255, 255))  # create password register text
        pygame.draw.rect(loginscreen, black, input_pass_reg)
        loginscreen.blit(pass_regist_text, (input_pass_reg.x, input_pass_reg.y))
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
        repass_regist_text = register_font.render(repass_reg_text, True,
                                                  (255, 255, 255))  # create password register text
        pygame.draw.rect(loginscreen, black, input_repass_reg)
        loginscreen.blit(repass_regist_text, (input_repass_reg.x, input_repass_reg.y))
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
        #   if email_reg_text != reemail_reg_text and email_reg_text != "EMAIL" and reemail_reg_text != "RE EMAIL":
        # print("not same")
        if pass_reg_text != repass_reg_text and pass_reg_text != "PASSWORD" and repass_reg_text != "RE PASSWORD":
            errorpassword = error_font.render("Password you entered not the same", True, (0, 0, 0))
            # pygame.draw.rect(loginscreen, black, input_user_reg)
            loginscreen.blit(errorpassword, (880, 480))
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
        for event in pygame.event.get():  # check events
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEMOTION:  # mouse is moving
                if startbutton.isOver(pos):
                    startbutton = Button("Start", (515, 550), font=70, color=darkred, size=(250, 100))
                else:
                    startbutton = Button("Start", (515, 550), font=70, color=black, size=(250, 100))
                if registerbutton.isOver(pos):
                    registerbutton = Button("Register", (930, 500), font=40, color=(30, 30, 30), size=(162, 75))
                else:
                    registerbutton = Button("Register", (930, 500), font=40, color=black, size=(162, 75))
            elif event.type == pygame.KEYDOWN:  # if key clicked
                if useractive:  # username text
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[0:-1]
                        loginscreen.blit(start_game_image, start_game_imagerect)
                        loginscreen.blit(game_register, (400, 30))
                        startbutton = Button("Start", (515, 550), font=70, color=black, size=(250, 100))
                        registerbutton = Button("Register", (930, 500), font=40, color=black, size=(162, 75))
                    else:
                        user_text += event.unicode
                elif passactive:  # pasword text
                    if event.key == pygame.K_BACKSPACE:
                        pass_text = pass_text[0:-1]
                        loginscreen.blit(start_game_image, start_game_imagerect)
                        loginscreen.blit(game_register, (400, 30))
                        startbutton = Button("Start", (515, 550), font=70, color=black, size=(250, 100))
                        registerbutton = Button("Register", (930, 500), font=40, color=black, size=(162, 75))
                    else:
                        pass_text += event.unicode
                elif user_reg_active:  # register username text
                    if user_reg_text == "USERNAME":
                        user_reg_text = ""
                    if event.key == pygame.K_BACKSPACE:
                        user_reg_text = user_reg_text[:-1]
                        loginscreen.blit(start_game_image, start_game_imagerect)
                        loginscreen.blit(game_register, (400, 30))
                        startbutton = Button("Start", (515, 550), font=70, color=black, size=(250, 100))
                        registerbutton = Button("Register", (930, 500), font=40, color=black, size=(162, 75))
                    else:
                        user_reg_text += event.unicode
                elif email_reg_active:  # register email text
                    if email_reg_text == "EMAIL":
                        email_reg_text = ""
                    if event.key == pygame.K_BACKSPACE:
                        email_reg_text = email_reg_text[:-1]
                        loginscreen.blit(start_game_image, start_game_imagerect)
                        loginscreen.blit(game_register, (400, 30))
                        startbutton = Button("Start", (515, 550), font=70, color=black, size=(250, 100))
                        registerbutton = Button("Register", (930, 500), font=40, color=black, size=(162, 75))
                    else:
                        email_reg_text += event.unicode
                elif reemail_reg_active:  # register re email text
                    if reemail_reg_text == "RE EMAIL":
                        reemail_reg_text = ""
                    if event.key == pygame.K_BACKSPACE:
                        reemail_reg_text = reemail_reg_text[:-1]
                        loginscreen.blit(start_game_image, start_game_imagerect)
                        loginscreen.blit(game_register, (400, 30))
                        startbutton = Button("Start", (515, 550), font=70, color=black, size=(250, 100))
                        registerbutton = Button("Register", (930, 500), font=40, color=black, size=(162, 75))
                    else:
                        reemail_reg_text += event.unicode
                elif pass_reg_active:  # register password text
                    if pass_reg_text == "PASSWORD":
                        pass_reg_text = ""
                    if event.key == pygame.K_BACKSPACE:
                        pass_reg_text = pass_reg_text[:-1]
                        loginscreen.blit(start_game_image, start_game_imagerect)
                        loginscreen.blit(game_register, (400, 30))
                        startbutton = Button("Start", (515, 550), font=70, color=black, size=(250, 100))
                        registerbutton = Button("Register", (930, 500), font=40, color=black, size=(162, 75))
                    else:
                        pass_reg_text += event.unicode
                elif repass_reg_active:  # register re password text
                    if repass_reg_text == "RE PASSWORD":
                        repass_reg_text = ""
                    if event.key == pygame.K_BACKSPACE:
                        repass_reg_text = repass_reg_text[:-1]
                        loginscreen.blit(start_game_image, start_game_imagerect)
                        loginscreen.blit(game_register, (400, 30))
                        startbutton = Button("Start", (515, 550), font=70, color=black, size=(250, 100))
                        registerbutton = Button("Register", (930, 500), font=40, color=black, size=(162, 75))
                    else:
                        repass_reg_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:  # check for clicks
                if registerbutton.isOver(pos):
                    if registerbutton.click():
                        print("register button has clicked")
                    if user_reg_text != "USERNAME" and pass_reg_text != "PASSWORD" and repass_reg_text != "RE PASSWORD" and reemail_reg_text != "EMAIL" and email_reg_text != "RE EMAIL":
                        print("hello")
                        register(user_reg_text, pass_reg_text, email_reg_text, server)
                        loginscreen.blit(start_game_image, start_game_imagerect)
                        loginscreen.blit(game_register, (400, 30))
                        startbutton = Button("Start", (515, 550), font=70, color=black, size=(250, 100))
                        registerbutton = Button("Register", (930, 500), font=40, color=black, size=(162, 75))
                        user_reg_text = "USERNAME"
                        pass_reg_text = "PASSWORD"
                        repass_reg_text = "RE PASSWORD"
                        email_reg_text = "EMAIL"
                        reemail_reg_text = "RE EMAIL"

                if startbutton.isOver(pos) and startbutton.click():  # check if start button has clicked
                    if pass_text != "" and user_text != "":
                        if login(user_text, pass_text, server):
                            gamepage(server)
                        else:
                            errortext = base_font.render("Username or password", True, (255, 255, 255))
                            errortext2 = base_font.render("are not exist", True, (255, 255, 255))
                            loginscreen.blit(errortext, (380, 450))
                            loginscreen.blit(errortext2, (470, 485))
                    else:
                        errortext = base_font.render("Enter password and username", True, (255, 255, 255))
                        loginscreen.blit(errortext, (380, 450))

                if input_name.collidepoint(pos):  # check if username text selected
                    useractive = True
                else:
                    useractive = False
                if input_password.collidepoint(pos):  # check if pass text selected
                    passactive = True
                else:
                    passactive = False
                if input_user_reg.collidepoint(pos):
                    user_reg_active = True
                else:
                    user_reg_active = False
                if input_email_reg.collidepoint(pos):
                    email_reg_active = True
                else:
                    email_reg_active = False
                if input_reemail_reg.collidepoint(pos):
                    reemail_reg_active = True
                else:
                    reemail_reg_active = False
                if input_pass_reg.collidepoint(pos):
                    pass_reg_active = True
                else:
                    pass_reg_active = False
                if input_repass_reg.collidepoint(pos):
                    repass_reg_active = True
                else:
                    repass_reg_active = False
        pygame.display.flip()
        clock.tick(60)


def register(username, password, email, server):
    server.send("register".encode('UTF-8'))
    server.send(username.encode('UTF-8'))
    time.sleep(1)
    server.send(password.encode('UTF-8'))
    time.sleep(1)
    server.send(email.encode('UTF-8'))
    input = server.recv(1024)
    if input.decode('UTF-8') == True:
        pass


def login(username, password, server):
    server.send("login".encode('UTF-8'))
    server.send(username.encode('UTF-8'))
    time.sleep(1)
    server.send(password.encode('UTF-8'))
    input = server.recv(1024)
    if input.decode('UTF-8') == "True":
        return True
    else:
        return False


def main2():
    str = "123f12"
    for i in range(len(str)):
        print(str[i:i + 1])
        if str[i:i + 1].isalpha():
            str = str[:i] + str[i + 1:]
        print(str)


if __name__ == '__main__':
    main()
