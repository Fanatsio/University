def read_ppm(filename):
    with open(filename, 'rb') as f:
        header = f.readline().strip()
        if header != b'P6':
            raise ValueError(f'{filename} is not a valid PPM file.')

        while True:
            line = f.readline().strip()
            if line.startswith(b'#'):
                continue
            else:
                break

        dimensions = line
        max_color = f.readline().strip()
        
        width, height = map(int, dimensions.split())
        max_color_value = int(max_color)

        pixel_data = f.read(width * height * 3)
        
    return (width, height, max_color_value, pixel_data)

def compare_ppm(file1, file2):
    width1, height1, max_color1, pixel_data1 = read_ppm(file1)
    width2, height2, max_color2, pixel_data2 = read_ppm(file2)

    if width1 != width2 or height1 != height2 or max_color1 != max_color2:
        return False

    return pixel_data1 == pixel_data2

file1 = 'data.ppm'
file2 = 'decompressData.ppm'

if compare_ppm(file1, file2):
    print("The PPM files are identical.")
else:
    print("The PPM files are not identical.")
