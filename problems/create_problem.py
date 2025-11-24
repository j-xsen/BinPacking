import random

def create_bin_file(filename, capacity, num_items, min_size=1, max_size=10):
    """
    Create a file with bin capacity on line 1
    and item sizes on line 2.
    """
    # Generate random item sizes
    items = [random.randint(min_size, max_size) for _ in range(num_items)]

    with open(filename, "w") as f:
        # Line 1: bin capacity
        f.write(f"{capacity}\n")
        # Line 2: item sizes separated by spaces
        f.write(" ".join(map(str, items)))

# Example usage
create_bin_file("problem100.txt", capacity=100, num_items=100, min_size=1, max_size=30)
