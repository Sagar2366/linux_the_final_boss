# Define a function to calculate area
def calculate_area(length, width):
    """Calculates the area of a rectangle."""
    area = length * width
    return area

# Call the function with some values
room_length = 5
room_width = 8

total_area = calculate_area(room_length, room_width)

print(f"The room is {room_length}m long and {room_width}m wide.")
print(f"The total area is {total_area} square meters.")
