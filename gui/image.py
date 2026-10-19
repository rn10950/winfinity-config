'''
Windows Classic Theme Preview Generator
=======================================

Generates the image found in the theme preview dialog in Windows 95-2000 from
supplied theme color data.

def genImg(DICT):
	Input:
	======
	A dict with the MS Theme color names (all lowercase) as keys
	and hex colors as values.
	
	Example (Windows Standard theme):
	=================================
	{   'activeborder': '#c0c0c0',
		'activetitle': '#000080',
		'appworkspace': '#7f7f7f',
		'background': '#3a6ea5',
		'buttonalternateface': '#b5b5b5',
		'buttondkshadow': '#404040',
		'buttonface': '#c0c0c0',
		'buttonhilight': '#e0e0e0',
		'buttonlight': '#c0c0c0',
		'buttonshadow': '#7f7f7f',
		'buttontext': '#000000',
		'gradientactivetitle': '#1084d0',
		'gradientinactivetitle': '#b5b5b5',
		'graytext': '#7f7f7f',
		'hilight': '#000080',
		'hilighttext': '#ffffff',
		'hottrackingcolor': '#000080',
		'inactiveborder': '#c0c0c0',
		'inactivetitle': '#808080',
		'inactivetitletext': '#c0c0c0',
		'infotext': '#000000',
		'infowindow': '#ffffe1',
		'menu': '#c0c0c0',
		'menubar': '#d4d0c8',
		'menuhilight': '#0a246a',
		'menutext': '#000000',
		'scrollbar': '#e0e0e0',
		'titletext': '#ffffff',
		'window': '#ffffff',
		'windowframe': '#000000',
		'windowtext': '#000000'}

	  
	Output:
	=======
	a PIL Image object.


'''
import math 
from PIL import Image, ImageDraw, ImageFont
import base64
import io

# ====================
#  Gradient Functions
# ====================
def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]


def RGB_to_hex(RGB):
    ''' [255,255,255] -> "#FFFFFF" '''
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
                        "{0:x}".format(v) for v in RGB])

def color_dict(gradient):
    ''' Takes in a list of RGB sub-lists and returns dictionary of
      colors in RGB and hex form for use in a graphing function
      defined later on '''
    return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
            "r":[RGB[0] for RGB in gradient],
            "g":[RGB[1] for RGB in gradient],
            "b":[RGB[2] for RGB in gradient]}

def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    ''' returns a gradient list of (n) colors between
      two hex colors. start_hex and finish_hex
      should be the full six-digit color string,
      inlcuding the number sign ("#FFFFFF") '''
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
            int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
            for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)

    return color_dict(RGB_list)


# ================================
#  Main Image Generation Function
# ================================
def genImg(c):
	w, h = 350, 190
	
	# maximize and close buttons
	maxb64 = r'iVBORw0KGgoAAAANSUhEUgAAAAkAAAAJCAYAAADgkQYQAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEUBQQLnTMXjgAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAAALElEQVQY02NkYGD4z0AAMDEQAVgYGBgYDhw4wIhLgYODw3+iTBqMihiJCScAOOAGER8Zq2MAAAAASUVORK5CYII='
	closeb64 = r'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAHCAYAAAA1WQxeAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEUBQQbgIQH6gAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAAAPElEQVQI14WPQRIAMAQDl5d5en6mF512OMiJkAgDEkCS8SEikhpQSylp9FbEUxSuo3ei1z5udrc1w/bFASq9Mj7TrccrAAAAAElFTkSuQmCC'
	up64 = 'iVBORw0KGgoAAAANSUhEUgAAAAcAAAAECAYAAABCxiV9AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEUBxobV0HsWwAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAAAKklEQVQI11WJsQ0AMAzCoJdxuj9rp0TUCzI2oCHJBTx+OvRu7KPdkr7QPDlkDkIHctQQAAAAAElFTkSuQmCC'
	down64 = 'iVBORw0KGgoAAAANSUhEUgAAAAcAAAAECAYAAABCxiV9AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEUBxomDymgSgAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAAAKUlEQVQI12NkYGD4z4ADMB04cIARm8SBAwcYmWAMdAkGBgYGJnQBZIUAxO4Ojb7C3QMAAAAASUVORK5CYII='
	maxF = base64.b64decode(str(maxb64))
	closeF = base64.b64decode(str(closeb64))
	upF = base64.b64decode(str(up64))
	downF = base64.b64decode(str(down64))
	maxI = Image.open(io.BytesIO(maxF))
	closeI = Image.open(io.BytesIO(closeF))
	upI = Image.open(io.BytesIO(upF))
	downI = Image.open(io.BytesIO(downF))
	  
	# creating new Image object 
	img = Image.new("RGB", (w, h)) 
	  
	font = ImageFont.truetype("WinfinityTitle.ttf", 10)
	smFont = ImageFont.truetype("micross.ttf", 10)
	
	#pprint.pprint(c)
	
	oB = c['windowframe']
	iB = c['buttondkshadow']
	tB = c['buttonhilight']
	wbg = c['buttonface']
	btnbg = wbg
	iTxt = c['inactivetitletext']
	aTxt = c['titletext']
	mTxt = c['menutext']
	wTxt = c['windowtext']
	dbg = c['background']
	iT = c['inactivetitle']
	iTG = c['gradientinactivetitle']
	aT = c['activetitle']
	aTG = c['gradientactivetitle']
	winBg = c['window']
	gTxt = c['graytext']
	
	# create rectangle image 
	img1 = ImageDraw.Draw(img)
	img1.fontmode = "1"

	#desktop bg
	img1.rectangle([(0, 0), (w, h)], fill =dbg)

	#inactive window
	img1.rectangle([(18, 10), (321, 145)], fill =wbg)
	#img1.rectangle([(21, 13), (318, 31)], fill ="#000080")
	gW = 298
	i = 0
	g = linear_gradient(iT, iTG, gW)
	for c in g['hex']:
		x = 21 + i
		img1.line([(x, 13), (x, 31)], fill =c)
		i = i + 1
	img1.fontmode = "1"
	img1.text((24, 17), "Inactive Window", fill=iTxt, font=font)

	img1.rectangle([(267, 15), (280, 27)], fill =btnbg)
	img1.rectangle([(283, 15), (296, 27)], fill =btnbg)
	img1.rectangle([(301, 15), (314, 27)], fill =btnbg)

	img1.line([(266, 15), (297, 15)], fill =tB)
	img1.line([(267, 27), (297, 27)], fill =iB)
	img1.line([(266, 28), (297, 28)], fill =oB)

	img1.line([(280, 16), (280, 27)], fill =iB)
	img1.line([(296, 16), (296, 27)], fill =iB)

	img1.line([(266, 15), (266, 27)], fill =tB)
	img1.line([(282, 16), (282, 27)], fill =tB)

	img1.line([(281, 15), (281, 28)], fill =oB)
	img1.line([(297, 15), (297, 28)], fill =oB)

	img1.line([(301, 27), (314, 27)], fill =iB)
	img1.line([(314, 16), (314, 27)], fill =iB)
	img1.line([(300, 15), (300, 27)], fill =tB)
	img1.line([(300, 15), (314, 15)], fill =tB)
	img1.line([(300, 28), (315, 28)], fill =oB)
	img1.line([(315, 15), (315, 28)], fill =oB)

	img1.line([(17, 9), (320, 9)], fill =wbg)
	img1.line([(17, 9), (17, 146)], fill =wbg)
	img1.line([(18, 10), (319, 10)], fill =tB)
	img1.line([(18, 10), (18, 145)], fill =tB)
	img1.line([(18, 146), (50, 146)], fill =iB)
	img1.line([(320, 10), (320, 50)], fill =iB)
	img1.line([(17, 147), (50, 147)], fill =oB)
	img1.line([(321, 9), (321, 50)], fill =oB)

	img1.rectangle([(270, 24), (275, 25)], fill ="#000000")
	img.paste(maxI, (285, 17), mask=maxI)
	img.paste(closeI, (304, 18), mask=closeI)


	#active window
	img1.rectangle([(21, 32), (343, 152)], fill =wbg)
	#img1.rectangle([(25, 36), (339, 53)], fill ="#ff0000")

	gW = 315
	i = 0
	g = linear_gradient(aT, aTG, gW)
	for c in g['hex']:
		x = 25 + i
		img1.line([(x, 36), (x, 53)], fill =c)
		i = i + 1

	img1.text((27, 40), "Active Window", fill=aTxt, font=font)

	img1.rectangle([(289, 39), (302, 50)], fill =btnbg)
	img1.rectangle([(305, 39), (318, 50)], fill =btnbg)
	img1.rectangle([(323, 39), (336, 50)], fill =btnbg)

	img1.text((32, 58), "Normal", fill=mTxt, font=smFont)
	img1.text((77, 58), "Disabled", fill=gTxt, font=smFont)
	img1.text((130, 58), "Selected", fill=mTxt, font=smFont)

	img1.rectangle([(27, 75), (338, 147)], fill =winBg) #text area
	img1.text((29, 79), "Window Text", fill=wTxt, font=font)

	#win controls
	img1.line([(288, 38), (319, 38)], fill =tB)
	img1.line([(289, 50), (319, 50)], fill =iB)
	img1.line([(288, 38), (288, 51)], fill =tB)
	img1.line([(304, 38), (304, 51)], fill =tB)
	img1.line([(302, 39), (302, 50)], fill =iB)
	img1.line([(318, 39), (318, 50)], fill =iB)
	img1.line([(303, 38), (303, 51)], fill =oB)
	img1.line([(319, 38), (319, 51)], fill =oB)
	img1.line([(288, 51), (319, 51)], fill =oB)

	img1.line([(322, 38), (337, 38)], fill =tB)
	img1.line([(322, 38), (322, 50)], fill =tB)
	img1.line([(323, 50), (336, 50)], fill =iB)
	img1.line([(336, 39), (336, 50)], fill =iB)
	img1.line([(322, 51), (337, 51)], fill =oB)
	img1.line([(337, 38), (337, 51)], fill =oB)

	#win border
	img1.line([(21, 32), (342, 32)], fill =wbg)
	img1.line([(21, 32), (21, 151)], fill =wbg)
	img1.line([(22, 33), (341, 33)], fill =tB)
	img1.line([(22, 33), (22, 150)], fill =tB)
	img1.line([(22, 151), (342, 151)], fill =iB)
	img1.line([(342, 33), (342, 151)], fill =iB)
	img1.line([(21, 152), (343, 152)], fill =oB)
	img1.line([(343, 32), (343, 152)], fill =oB)

	#textarea border
	img1.line([(25, 73), (338, 73)], fill =iB)
	img1.line([(25, 73), (25, 147)], fill =iB)
	img1.line([(26, 74), (337, 74)], fill =oB)
	img1.line([(26, 74), (26, 146)], fill =oB)
	img1.line([(26, 147), (338, 147)], fill =wbg)
	img1.line([(338, 74), (338, 147)], fill =wbg)
	img1.line([(25, 148), (339, 148)], fill =tB)
	img1.line([(339, 73), (339, 148)], fill =tB)

	#scroll
	img1.rectangle([(322, 75), (337, 145)], fill =wbg)
	img1.line([(323, 76), (335, 76)], fill =tB)
	img1.line([(323, 76), (323, 88)], fill =tB)
	img1.line([(323, 89), (336, 89)], fill =iB)
	img1.line([(336, 76), (336, 89)], fill =iB)
	img1.line([(322, 90), (337, 90)], fill =oB)
	img1.line([(337, 75), (337, 90)], fill =oB)
	img1.line([(323, 132), (335, 132)], fill =tB)
	img1.line([(323, 132), (323, 144)], fill =tB)
	img1.line([(323, 145), (336, 145)], fill =iB)
	img1.line([(336, 132), (336, 145)], fill =iB)
	img1.line([(322, 146), (337, 146)], fill =oB)
	img1.line([(337, 131), (337, 146)], fill =oB)
	img.paste(upI, (326, 81), mask=upI)
	img.paste(downI, (326, 137), mask=downI)

	img1.rectangle([(292, 47),(297,48)], fill="#000000")
	img.paste(maxI, (307, 40), mask=maxI)
	img.paste(closeI, (326, 41), mask=closeI)

	#message box
	img1.rectangle([(29, 111), (235, 173)], fill =wbg)
	#img1.rectangle([(32, 114), (233, 132)], fill ="#ff0000")

	gW = 201
	i = 0
	g = linear_gradient(aT, aTG, gW)
	for c in g['hex']:
		x = 32 + i
		img1.line([(x, 114), (x, 131)], fill =c)
		i = i + 1

	img1.text((35, 117), "Message Box", fill=aTxt, font=font)
	img1.rectangle([(216, 117), (229, 128)], fill =wbg)
	img1.text((36, 137), "Message Text", fill=mTxt, font=smFont)
	img1.rectangle([(97, 145), (166, 166)], fill =wbg)
	img1.text((125, 151), "O", fill=mTxt, font=smFont)
	img1.text((133, 150), "K", fill=mTxt, font=smFont)
	img1.line([(215, 116), (229, 116)], fill =tB)
	img1.line([(215, 116), (215, 128)], fill =tB)
	img1.line([(216, 128), (229, 128)], fill =iB)
	img1.line([(229, 117), (229, 128)], fill =iB)
	img1.line([(215, 129), (230, 129)], fill =oB)
	img1.line([(230, 116), (230, 129)], fill =oB)

	img1.line([(29, 111), (234, 111)], fill =wbg)
	img1.line([(29, 111), (29, 172)], fill =wbg)
	img1.line([(30, 112), (233, 112)], fill =tB)
	img1.line([(30, 112), (30, 171)], fill =tB)
	img1.line([(30, 172), (234, 172)], fill =iB)
	img1.line([(234, 112), (234, 172)], fill =iB)
	img1.line([(235, 111), (235, 173)], fill =oB)
	img1.line([(29, 173), (235, 173)], fill =oB)

	img1.line([(96, 144), (166, 144)], fill =tB)
	img1.line([(96, 144), (96, 166)], fill =tB)
	img1.line([(97, 166), (166, 166)], fill =iB)
	img1.line([(166, 145), (166, 166)], fill =iB)
	img1.line([(96, 167), (167, 167)], fill =oB)
	img1.line([(167, 144), (167, 167)], fill =oB)
	img.paste(closeI, (219, 119), mask=closeI)

	return img
