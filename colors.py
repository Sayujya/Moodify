from colorthief import ColorThief

# halogen color
DEFAULT_COLOR = (255, 241, 224)
DEFAULT_NUM_COLORS = 2

def get_mood_colors(image):
  colors = get_colors(image, DEFAULT_NUM_COLORS)

  primary = colors[0]
  accent = colors[1]

  return primary, accent

def get_colors(image, num_colors):
  if image is None:
    return None

  color_thief = ColorThief(image)
  colors = color_thief.get_palette(color_count=num_colors, quality=1)

  return [get_hex_code(color) for color in colors]

def get_default_color():
  return get_hex_code(DEFAULT_COLOR)

def get_hex_code(color_tuple):
  return "#%02x%02x%02x" % color_tuple