#http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter


from tkinter import *
import tkinter as tk
from tkinter import ttk
action = ""

action = "print_font"
#action = "print_color"
#action = "print_relief"

if action == "print_font":
    font_type_list = [
    'System', 
    'Terminal',
    'Fixedsys',
    'Modern',
    'Roman',
    'Script',
    'Courier',
    'MS Serif',
    'MS Sans Serif',
    'Small Fonts',
    'Marlett',
    'Arial',
    'Arabic Transparent',
    'Arial Baltic',
    'Arial CE',
    'Arial CYR',
    'Arial Greek',
    'Arial TUR',
    'Arial Black',
    'Bahnschrift Light',
    'Bahnschrift SemiLight',
    'Bahnschrift',
    'Bahnschrift SemiBold',
    'Bahnschrift Light SemiCondensed',
    'Bahnschrift SemiLight SemiConde',
    'Bahnschrift SemiCondensed',
    'Bahnschrift SemiBold SemiConden',
    'Bahnschrift Light Condensed',
    'Bahnschrift SemiLight Condensed',
    'Bahnschrift Condensed',
    'Bahnschrift SemiBold Condensed',
    'Calibri',
    'Calibri Light',
    'Cambria',
    'Cambria Math',
    'Candara',
    'Candara Light',
    'Comic Sans MS',
    'Consolas',
    'Constantia',
    'Corbel',
    'Corbel Light',
    'Courier New',
    'Courier New Baltic',
    'Courier New CE',
    'Courier New CYR',
    'Courier New Greek',
    'Courier New TUR',
    'Ebrima',
    'Franklin Gothic Medium',
    'Gabriola',
    'Gadugi',
    'Georgia',
    'Impact',
    'Ink Free',
    'Javanese Text',
    'Leelawadee UI',
    'Leelawadee UI Semilight',
    'Lucida Console',
    'Lucida Sans Unicode',
    'Malgun Gothic',
    '@Malgun Gothic',
    'Malgun Gothic Semilight',
    '@Malgun Gothic Semilight',
    'Microsoft Himalaya',
    'Microsoft JhengHei',
    '@Microsoft JhengHei',
    'Microsoft JhengHei UI',
    '@Microsoft JhengHei UI',
    'Microsoft JhengHei Light',
    '@Microsoft JhengHei Light',
    'Microsoft JhengHei UI Light',
    '@Microsoft JhengHei UI Light',
    'Microsoft New Tai Lue',
    'Microsoft PhagsPa',
    'Microsoft Sans Serif',
    'Microsoft Tai Le',
    'Microsoft YaHei',
    '@Microsoft YaHei',
    'Microsoft YaHei UI',
    '@Microsoft YaHei UI',
    'Microsoft YaHei Light',
    '@Microsoft YaHei Light',
    'Microsoft YaHei UI Light',
    '@Microsoft YaHei UI Light',
    'Microsoft Yi Baiti',
    'MingLiU-ExtB',
    '@MingLiU-ExtB',
    'PMingLiU-ExtB',
    '@PMingLiU-ExtB',
    'MingLiU_HKSCS-ExtB',
    '@MingLiU_HKSCS-ExtB',
    'Mongolian Baiti',
    'MS Gothic',
    '@MS Gothic',
    'MS UI Gothic',
    '@MS UI Gothic',
    'MS PGothic',
    '@MS PGothic',
    'MV Boli',
    'Myanmar Text',
    'Nirmala UI',
    'Nirmala UI Semilight',
    'Palatino Linotype',
    'Segoe MDL2 Assets',
    'Segoe Print',
    'Segoe Script',
    'Segoe UI',
    'Segoe UI Black',
    'Segoe UI Emoji',
    'Segoe UI Historic',
    'Segoe UI Light',
    'Segoe UI Semibold',
    'Segoe UI Semilight',
    'Segoe UI Symbol',
    'SimSun',
    '@SimSun',
    'NSimSun',
    '@NSimSun',
    'SimSun-ExtB',
    '@SimSun-ExtB',
    'Sitka Small',
    'Sitka Text',
    'Sitka Subheading',
    'Sitka Heading',
    'Sitka Display',
    'Sitka Banner',
    'Sylfaen',
    'Symbol',
    'Tahoma',
    'Times New Roman',
    'Times New Roman Baltic',
    'Times New Roman CE',
    'Times New Roman CYR',
    'Times New Roman Greek',
    'Times New Roman TUR',
    'Trebuchet MS',
    'Verdana',
    'Webdings',
    'Wingdings',
    'Yu Gothic',
    '@Yu Gothic',
    'Yu Gothic UI',
    '@Yu Gothic UI',
    'Yu Gothic UI Semibold',
    '@Yu Gothic UI Semibold',
    'Yu Gothic Light',
    '@Yu Gothic Light',
    'Yu Gothic UI Light',
    '@Yu Gothic UI Light',
    'Yu Gothic Medium',
    '@Yu Gothic Medium',
    'Yu Gothic UI Semilight',
    '@Yu Gothic UI Semilight',
    'HoloLens MDL2 Assets',
    'BIZ UDGothic',
    '@BIZ UDGothic',
    'BIZ UDPGothic',
    '@BIZ UDPGothic',
    'BIZ UDMincho Medium',
    '@BIZ UDMincho Medium',
    'BIZ UDPMincho Medium',
    '@BIZ UDPMincho Medium',
    'Meiryo',
    '@Meiryo',
    'Meiryo UI',
    '@Meiryo UI',
    'MS Mincho',
    '@MS Mincho',
    'MS PMincho',
    '@MS PMincho',
    'UD Digi Kyokasho N-B',
    '@UD Digi Kyokasho N-B',
    'UD Digi Kyokasho NP-B',
    '@UD Digi Kyokasho NP-B',
    'UD Digi Kyokasho NK-B',
    '@UD Digi Kyokasho NK-B',
    'UD Digi Kyokasho N-R',
    '@UD Digi Kyokasho N-R',
    'UD Digi Kyokasho NP-R',
    '@UD Digi Kyokasho NP-R',
    'UD Digi Kyokasho NK-R',
    '@UD Digi Kyokasho NK-R',
    'Yu Mincho',
    '@Yu Mincho',
    'Yu Mincho Demibold',
    '@Yu Mincho Demibold',
    'Yu Mincho Light',
    '@Yu Mincho Light',
    'DengXian',
    '@DengXian',
    'DengXian Light',
    '@DengXian Light',
    'FangSong',
    '@FangSong',
    'KaiTi',
    '@KaiTi',
    'SimHei',
    '@SimHei',
    'Ubuntu',
    'Raleway',
    'Ubuntu Condensed',
    'Ubuntu Light'
    ]


    root = Tk()
    root.title("print all the font type")
    root.geometry("1920x1080")
    r = 0
    c = 0
    Num = 30
    for font_type in font_type_list:
        label = tk.Label(root, text=str(r+1)+'. '+font_type, font=(font_type, 12))
        label.grid(row=(r%Num), column=(c%Num))
        r += 1
        if not r == 1 and r%Num == 0:
            c += 1






elif action == "print_color":
    MAX_ROWS = 36
    FONT_SIZE = 10 # (pixels)

    COLORS = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
        'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
        'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
        'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
        'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
        'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
        'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
        'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
        'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
        'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
        'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
        'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
        'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
        'indian red', 'saddle brown', 'sandy brown',
        'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
        'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
        'pale violet red', 'maroon', 'medium violet red', 'violet red',
        'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
        'thistle', 'snow2', 'snow3',
        'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
        'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
        'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
        'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
        'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
        'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
        'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
        'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
        'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
        'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
        'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
        'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
        'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
        'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
        'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
        'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
        'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
        'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
        'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
        'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
        'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
        'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
        'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
        'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
        'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
        'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
        'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
        'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
        'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
        'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
        'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
        'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
        'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
        'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
        'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
        'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
        'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
        'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
        'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
        'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
        'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
        'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
        'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
        'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
        'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
        'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
        'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
        'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
        'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
        'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
        'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
        'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
        'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
        'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
        'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
        'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
        'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']

    root = Tk()
    root.title("Named colour chart")
    row = 0
    col = 0
    for color in COLORS:
        e = Button(root, text=color, background=color, 
                font=(None, -FONT_SIZE))
        e.grid(row=row, column=col, sticky=E+W)
        row += 1
        if (row > 36):
            row = 0
            col += 1



elif action == "print_relief":
    root = Tk()

    B1 = tk.Entry(root, text ="FLAT", relief=FLAT, foreground = "blue")
    B2 = tk.Entry(root, text ="RAISED", relief=RAISED,insertbackground = "red")
    B3 = tk.Entry(root, text ="SUNKEN", relief=SUNKEN ,  selectbackground = "green")
    B4 = tk.Entry(root, text ="GROOVE", relief=GROOVE )
    B5 = tk.Entry(root, text ="RIDGE", relief=RIDGE )

    B1.pack(pady = 10)
    B2.pack(pady = 10)
    B3.pack(pady = 10)
    B4.pack(pady = 10)
    B5.pack(pady=10)

else:

    root = Tk()
    nameentryframe = Frame(root, background = 'BLACK', borderwidth = 1, relief = SUNKEN)
    nameentry = Entry(nameentryframe,relief=FLAT)
    nameentryframe.pack(pady = 10)
    nameentry.pack()
    nameentryframe1 = Frame(root, background = 'BLACK', borderwidth = 1, relief = SUNKEN)
    nameentry1 = Entry(nameentryframe1,relief=FLAT)
    nameentryframe1.pack(pady = 10)
    nameentry1.pack()    
          

root.mainloop()





