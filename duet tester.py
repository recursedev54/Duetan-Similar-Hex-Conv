def invert_hex(hex_code):
    # Remove the '#' character if present
    if hex_code.startswith('#'):
        hex_code = hex_code[1:]

    # Convert hexadecimal to RGB
    red = int(hex_code[0:2], 16)
    green = int(hex_code[2:4], 16)
    blue = int(hex_code[4:6], 16)

    # Invert RGB values
    inverted_red = 255 - red
    inverted_green = 255 - green
    inverted_blue = 255 - blue

    # Convert inverted RGB back to hexadecimal
    inverted_hex = "#{:02X}{:02X}{:02X}".format(inverted_red, inverted_green, inverted_blue)
    
    return inverted_hex

# Example usage
hex_code = "#FFFF00"  # Yellow color
inverted_hex = invert_hex(hex_code)
print("Inverted hex color:", inverted_hex)



def split_color(hex_code):
    # Split the original color into itself and its inverse
    inverse_hex = invert_hex(hex_code)
    return hex_code, inverse_hex

# Example usage
original_hex = "#FFFF00"  # Yellow color
color1, color2 = split_color(original_hex)
print("Original color:", original_hex)
print("Color 1 (original):", color1)
print("Color 2 (inverse):", color2)

def rgb_to_xyz(rgb):
    r, g, b = [c / 255.0 for c in rgb]
    r = ((r + 0.055) / 1.055) ** 2.4 if r > 0.04045 else r / 12.92
    g = ((g + 0.055) / 1.055) ** 2.4 if g > 0.04045 else g / 12.92
    b = ((b + 0.055) / 1.055) ** 2.4 if b > 0.04045 else b / 12.92
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
    return x, y, z

def xyz_to_lms(xyz):
    conversion_matrix = [
        [0.4002, 0.7076, -0.0808],
        [-0.2263, 1.1653, 0.0457],
        [0, 0, 0.9182]
    ]
    l = conversion_matrix[0][0] * xyz[0] + conversion_matrix[0][1] * xyz[1] + conversion_matrix[0][2] * xyz[2]
    m = conversion_matrix[1][0] * xyz[0] + conversion_matrix[1][1] * xyz[1] + conversion_matrix[1][2] * xyz[2]
    s = conversion_matrix[2][0] * xyz[0] + conversion_matrix[2][1] * xyz[1] + conversion_matrix[2][2] * xyz[2]
    return l, m, s

def simulate_deuteranopia(rgb):
    lms = xyz_to_lms(rgb_to_xyz(rgb))
    l_prime = lms[0]
    m_prime = lms[1]  # Keep the original M component
    s_prime = lms[2]
    
    # Perform deuteranopia transformation
    l_prime_original, m_prime_original, s_prime_original = deuteranopia_transform((l_prime, m_prime, s_prime))
    l_prime_inverted, m_prime_inverted, s_prime_inverted = deuteranopia_transform((l_prime, -m_prime, s_prime))  # Invert the M component
    
    # Convert back to RGB
    rgb_original = lms_to_rgb((l_prime_original, m_prime_original, s_prime_original))
    rgb_inverted = lms_to_rgb((l_prime_inverted, m_prime_inverted, s_prime_inverted))
    
    return rgb_original + rgb_inverted  # Concatenate RGB tuples




def deuteranopia_transform(lms):
    l_prime = lms[0]
    m_prime = 0
    s_prime = lms[2]
    return l_prime, m_prime, s_prime

def lms_to_rgb(lms):
    # Convert lms to tuple if it's not already
    lms = tuple(lms)
    
    conversion_matrix = [
        [4.4679, -3.5873, 0.1193],
        [-1.2186, 2.3809, -0.1624],
        [0.0497, -0.2439, 1.2045]
    ]
    r = conversion_matrix[0][0] * lms[0] + conversion_matrix[0][1] * lms[1] + conversion_matrix[0][2] * lms[2]
    g = conversion_matrix[1][0] * lms[0] + conversion_matrix[1][1] * lms[1] + conversion_matrix[1][2] * lms[2]
    b = conversion_matrix[2][0] * lms[0] + conversion_matrix[2][1] * lms[1] + conversion_matrix[2][2] * lms[2]
    r = max(0, min(r, 1))
    g = max(0, min(g, 1))
    b = max(0, min(b, 1))
    r = round(r * 255)
    r = r + 40
    g = round(g * 255)
    b = round(b * 255)
    print("Debug - LMS to RGB conversion:")
    print("LMS:", lms)
    print("RGB:", (r, g, b))
    return r, g, b

rgb_color = (0,0,255)  # Cyan color in RGB format
simulated_lms = simulate_deuteranopia(rgb_color)
#print("Simulated Deuteranopia LMS color:", simulated_lms)
simulated_rgb = lms_to_rgb(simulated_lms)
print("Simulated Deuteranopia RGB color:", simulated_rgb)


def hex_to_rgb(hex_code):
    # Remove the '#' character if present
    if hex_code.startswith('#'):
        hex_code = hex_code[1:]

    # Convert hexadecimal to RGB
    red = int(hex_code[0:2], 16)
    green = int(hex_code[2:4], 16)
    blue = int(hex_code[4:6], 16)

    return red, green, blue


def rgb_to_hex(rgb):
    # Convert RGB tuple to hexadecimal color code
    hex_code = "#{:02X}{:02X}{:02X}".format(*map(round, rgb))
    return hex_code


def combine_colors(hex_code):
    # Split the original color into itself and its inverse
    original_color, inverted_color = split_color(hex_code)
    print("Original color:", original_color)
    print("Inverted color:", inverted_color)
    
    # Simulate deuteranopia for the original color and its inverse
    simulated_original_rgb = simulate_deuteranopia(hex_to_rgb(inverted_color))  # Simulate deuteranopia for the inverted color
    simulated_inverted_rgb = simulate_deuteranopia(hex_to_rgb(original_color))  # Simulate deuteranopia for the original color
    
    # Convert simulated original and inverted RGB values to hexadecimal
    simulated_original_hex = rgb_to_hex(simulated_original_rgb)
    simulated_inverted_hex = rgb_to_hex(simulated_inverted_rgb)
    print("Simulated original hex:", simulated_original_hex)
    print("Simulated inverted hex:", simulated_inverted_hex)
    
    # Adjust the RGB values to avoid clipping by dividing each value by two
    simulated_original_rgb = tuple(int(c / 2) for c in simulated_original_rgb)
    simulated_inverted_rgb = tuple(int(c / 2) for c in simulated_inverted_rgb)
    
    # Add the adjusted RGB tuples together
    combined_rgb = tuple(a + b for a, b in zip(simulated_original_rgb, simulated_inverted_rgb))
    
    # Convert the combined RGB tuple to a hex color representation
    combined_hex = rgb_to_hex(combined_rgb)
    
    return combined_hex

# Example usage
hex_code = "#00FFFF"  # Yellow color
combined_hex = combine_colors(hex_code)
print("Combined hex color:", combined_hex)  # Expected: #A77F7F






