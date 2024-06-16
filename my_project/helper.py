def chart_color(r, g, b, color_count):
# Create color for expence pie chart

    base_color = [r, g, b]
    rgb_colors = []

    factor = 0.2

    for i in range(color_count):
        color = []
        for j in base_color:
            j = int(j * (1 - factor))
            color.append(j)
        formated_rgb = f"rgb{color[0], color[1], color[2]}"
        base_color = color
        rgb_colors.append(formated_rgb)

    return(rgb_colors)

chart_color(100, 173, 255, 5)