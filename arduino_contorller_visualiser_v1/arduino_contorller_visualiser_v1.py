# Python code transmits a byte to Arduino /Microcontroller
from cmath import pi
from pickle import FALSE
from turtle import Screen
import serial.tools.list_ports
import pygame
import math
import time

# _____________ Initial Variables _____________________________________
# These variables determines the initial screen size.
INITAL_SCREEN_WIDTH = 1000
INITAL_SCREEN_HEIGHT = 500

# _____________ Objects and initializes _______________________________
# This command creates a clock object used for the tick time.
clock = pygame.time.Clock()

pygame.font.init()

pygame.display.set_caption('Arduino Contorller Visualiser v1')

Icon = pygame.image.load('controller_image.png')

pygame.display.set_icon(Icon)

# This command creates a display object of the size defined by the
# INITAL_SCREEN_WIDTH and INITAL_SCREEN_HEIGHT variables.
screen = pygame.display.set_mode((INITAL_SCREEN_WIDTH, INITAL_SCREEN_HEIGHT))

not_quit_game = True


HUD_GREY = (25, 25, 25)

OUTLINE_LIGHT_GREY  = (56,56,56)

WHITE_BACKROUND = (255,255,255)

TEXT_WHITE = (255, 255, 255)


CONTROLLER_GREEN = (35,217,155)


TEXT_PURPLE = (217,35,97)

ACCENT_BLUE = (35,188,217)

value_names = ["pot left","pot middle","pot right","left toggle","right toggle","left up switch","left down switch","right up switch","right down switch","left joy x","left joy y","left joy switch","right joy x","right joy y","right joy switch"]

not_quit = True

# _____________ Functions _____________________________________________
def message(text, text_color, x_pos, y_pos, text_size):
    """Draw text, returns none.

    Keyword arguments:
    text -- The text to be drawn.
    text_color -- The color of the text to be drawn.
    x_pos -- The x position of the center of the text.
    Y_pos -- The y position of the center of the text.
    text_size -- The size of the text to be drawn.
    """
    # This statement attempts to load FreeSansBold.ttf font.
    try:
        # This statement creates a pygame.font object using the
        # FreeSansBold font and the font size given.
        font = pygame.font.Font("FreeSansBold.ttf", text_size)
    # This statement catches the exception if the font file could not
    # be loaded.
    except FileNotFoundError:
        #print("FreeSansBold.ttf Font file could not be loaded")
        return None
    # This statement renders text using the font object created and the
    # text color given.
    text_render = font.render(text, False, text_color)
    # This statement creates a text box centered on the x and y
    # positions.
    text_box = text_render.get_rect(left=x_pos, top= y_pos)
    # This statement draws the rendered text onto the text box
    screen.blit(text_render, text_box)
    return None

def port_selector():

    port_num_str = ""
    non_valid_comport = True
    while non_valid_comport:
        port_num_str = ""
        name_attempt = True
        while name_attempt:
            for event in pygame.event.get():
                # This statement breaks the while loop if the quit
                # button is pressed.
                if event.type == pygame.QUIT:
                    return "1",False
                # This statement checks if an event is a key being
                # pressed down.
                if event.type == pygame.KEYDOWN:
                    # This statement removes the last character
                    # from the entered name if the back space key
                    # is pressed.
                    if event.key == pygame.K_BACKSPACE:
                        port_num_str = port_num_str[:-1]
                    # This statement checks if the enter or return
                    # key has been pressed and breaks the loop if
                    # so.
                    elif event.key == pygame.K_RETURN:
                        name_attempt = False
                    # This statement adds the Unicode character
                    # corresponding to the key pressed to the

                    else:
                        port_num_str += event.unicode
            
            port_selected = ""
            message("Please enter the comport number", TEXT_WHITE,30, 13, 30)
            pygame.draw.line(screen,TEXT_PURPLE,(30,45),(530,45),width=4)

            ports = serial.tools.list_ports.comports()
            num_of_ports = len(ports)
            for onePort in ports:
                pygame.draw.line(screen,TEXT_PURPLE,(50,20*num_of_ports + 50),(60,20*num_of_ports + 50),width=2)
                message(str(onePort), TEXT_WHITE,70, 20*num_of_ports + 40, 15)
                num_of_ports += 1

            pygame.draw.rect(screen, OUTLINE_LIGHT_GREY, [30, 270, 500, 50])
            message("COM:{}".format(port_num_str), CONTROLLER_GREEN,50, 275, 30)

            pygame.display.update()

        if(port_num_str.isdigit() and int(port_num_str) != 0):
            non_valid_comport = False

            return port_num_str,True
         

def read_data():
    #Reads a line from the buffer
    packet = serialInst.readline()
    #Decodes it from utf8 and removes newline charicters
    values = packet.decode('utf').rstrip('\n')

    if len(values) != 51:
        raise UnicodeDecodeError 

    str_list_values = []
    temp_str = ""
    #Splits the string into a list of strings
    for charicter in values:
        if charicter != ',':
            temp_str += charicter
        if charicter == ',':
            str_list_values.append(temp_str)
            temp_str = ""
    str_list_values.append(temp_str)

    #converts the list of strings into a list of intergers
    int_list_values = []
    for numbers in str_list_values:
        int_list_values.append(int(numbers))

    for number in range(0,len(int_list_values),1):
        
        if int_list_values[number] > 900:
            int_list_values[number] -=1000

    return int_list_values

def draw_display(int_list_values_local):
    #----------MISC----------------------------------------------------
    screen.fill(OUTLINE_LIGHT_GREY)
    #Draws the purple accent and grey backround for the left of the screen
    pygame.draw.rect(screen, HUD_GREY, [0, 0, 300, 500])
    pygame.draw.line(screen,TEXT_PURPLE,(50,30),(50,470),width=5)
    #Draws the raw values from the controller
    for num in range(0,len(int_list_values_local),1):
        message("{}:{}".format(value_names[num],int_list_values_local[num]), TEXT_WHITE,57, 30*num+30, 15)
    #Draws the green rounded rectangle for the controller
    pygame.draw.rect(screen, CONTROLLER_GREEN, [400, 100, 500, 214],border_radius =30)
    #Draws hint to slect another device by pressing escape
    message("Press esc to select another device",CONTROLLER_GREEN,350,450,20)

    #----------POTS----------------------------------------------------
    #Draws the circles for the pots
    pygame.draw.circle(screen,HUD_GREY,[584,168],17)
    pygame.draw.circle(screen,HUD_GREY,[650,168],17)
    pygame.draw.circle(screen,HUD_GREY,[716,168],17)
    #Draws the wipers for the pots (Left, middle then right)
    pygame.draw.line(screen,TEXT_PURPLE,[584,168],[584+(17*-math.cos((int_list_values_local[0]*4.71239/1023)-0.785398))-2.5, 168+(17*-math.sin((int_list_values_local[0]*4.71239/1023)-0.785398))-2.5],width=5)
    pygame.draw.line(screen,TEXT_PURPLE,[650,168],[650+(17*-math.cos((int_list_values_local[1]*4.71239/1023)-0.785398))-2.5, 168+(17*-math.sin((int_list_values_local[1]*4.71239/1023)-0.785398))-2.5],width=5)
    pygame.draw.line(screen,TEXT_PURPLE,[716,168],[716+(17*-math.cos((int_list_values_local[2]*4.71239/1023)-0.785398))-2.5, 168+(17*-math.sin((int_list_values_local[2]*4.71239/1023)-0.785398))-2.5],width=5)

    #----------JOYSTICKS-----------------------------------------------
    #Draws the squares for the joy sticks
    pygame.draw.rect(screen, HUD_GREY, [430, 130, 60, 60])
    pygame.draw.rect(screen, HUD_GREY, [810, 130, 60, 60])
    #Draws the indicator for the left joy stick
    if int_list_values_local[11] == 0:
        left_joy_size = 12
    else:
        left_joy_size = 6
    pygame.draw.rect(screen, TEXT_PURPLE, [((int_list_values_local[9])*(60-left_joy_size)/1023)+430, (1023-(int_list_values_local[10]))*(60-left_joy_size)/1023+130, left_joy_size, left_joy_size])
    #Draws the indicator for the right joy stick
    if int_list_values_local[14] == 0:
        right_joy_size = 12
    else:
        right_joy_size = 6
    pygame.draw.rect(screen, TEXT_PURPLE, [((int_list_values_local[12])*(60-right_joy_size)/1023)+810, (1023-(int_list_values_local[13]))*(60-right_joy_size)/1023+130, right_joy_size, right_joy_size])

    #----------TOGGLE SWITCHES-----------------------------------------
    #Draws the rectangles for the toggle switches
    pygame.draw.rect(screen, HUD_GREY, [520, 125, 33, 47])
    pygame.draw.rect(screen, HUD_GREY, [747, 125, 33, 47])
    #Draws the indicator for the left toggle switche
    if int_list_values_local[3] == 1:
        pygame.draw.rect(screen, TEXT_PURPLE, [531, 127, 10, 25])
    else:
        pygame.draw.rect(screen, TEXT_PURPLE, [531, 145, 10, 25])
    #Draws the indicator for the right toggle switche
    if int_list_values_local[4] == 1:
        pygame.draw.rect(screen, TEXT_PURPLE, [758, 127, 10, 25])
    else:
        pygame.draw.rect(screen, TEXT_PURPLE, [758, 145, 10, 25])

    #----------MOMENTARY SWITCHES--------------------------------------
    #Draws the rectangles for the momentary switches
    pygame.draw.rect(screen, HUD_GREY, [520, 200, 33, 48])
    pygame.draw.rect(screen, HUD_GREY, [747, 200, 33, 48])
    #Draws the indicator for the left momentary switch
    pygame.draw.rect(screen, TEXT_PURPLE, [531, 220, 10, 10])
    if int_list_values_local[5] == 0:
        pygame.draw.rect(screen, TEXT_PURPLE, [531, 204, 10, 16])
    elif int_list_values_local[6] == 0:
        pygame.draw.rect(screen, TEXT_PURPLE, [531, 230, 10, 16])
    #Draws the indicator for the right momentary switch
    pygame.draw.rect(screen, TEXT_PURPLE, [758, 220, 10, 10])
    if int_list_values_local[7] == 0:
        pygame.draw.rect(screen, TEXT_PURPLE, [758, 204, 10, 16])
    elif int_list_values_local[8] == 0:
        pygame.draw.rect(screen, TEXT_PURPLE, [758, 230, 10, 16])

    pygame.display.update()

def quit_check():
    for event in pygame.event.get():
        # This statement breaks the while loop if the quit
        # button is pressed.
        if event.type == pygame.QUIT:
            return False,True
        # This statement checks if an event is a key being
        # pressed down.
        if event.type == pygame.KEYDOWN:
            # This statement removes the last character
            # from the entered name if the back space key
            # is pressed.
            if event.key == pygame.K_ESCAPE:
                return True,False


    return True,True
  

# _____________ Main loop _____________________________________________
while not_quit:
    escape_not_pressed = True
    device_connected = True
    num_of_connectons_failed = 0;

    screen.fill(HUD_GREY)
    port_num,not_quit = port_selector()
    screen.fill(HUD_GREY)
    
    while num_of_connectons_failed < 5 and device_connected and escape_not_pressed and not_quit:
        
        not_quit,escape_not_pressed = quit_check()
                    
        try:
            message("Attempting connection...",TEXT_PURPLE,50,50*num_of_connectons_failed+50,30)
            pygame.display.update()

            serialInst = serial.Serial()

            serialInst.baudrate = 9600

            serialInst.port = "COM"+port_num

            serialInst.open()

            while device_connected and escape_not_pressed and not_quit:
                try:
                    not_quit,escape_not_pressed = quit_check()
                    
                    if serialInst.in_waiting:

                        draw_display(read_data())

                except serial.SerialException:
                    
                    device_connected = False
        
        except serial.SerialException:
            device_connected = False

        except UnicodeDecodeError:
            
            num_of_connectons_failed +=1
            
            time.sleep(1)
            


