"""Generate simple app icons as PNG files."""
import struct
import zlib

def create_png(width, height, color_rgb):
    """Create a minimal PNG with a solid color and centered wrench text."""
    r, g, b = color_rgb

    # Create raw pixel data (RGBA)
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'  # filter byte
        for x in range(width):
            # Create a gradient circle effect
            cx, cy = width // 2, height // 2
            dx, dy = x - cx, y - cy
            dist = (dx*dx + dy*dy) ** 0.5
            max_dist = min(width, height) * 0.45

            if dist < max_dist:
                # Inside circle - gradient from accent to accent2
                t = dist / max_dist
                pr = int(r * (1 - t * 0.3))
                pg = int(g * (1 - t * 0.2))
                pb = int(b * (1 + t * 0.2))
                pb = min(255, pb)
                raw_data += bytes([pr, pg, pb, 255])
            else:
                # Outside circle - transparent
                raw_data += bytes([0, 0, 0, 0])

    # PNG signature
    signature = b'\x89PNG\r\n\x1a\n'

    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)  # 8bit RGBA
    ihdr = make_chunk(b'IHDR', ihdr_data)

    # IDAT chunk
    compressed = zlib.compress(raw_data)
    idat = make_chunk(b'IDAT', compressed)

    # IEND chunk
    iend = make_chunk(b'IEND', b'')

    return signature + ihdr + idat + iend

def make_chunk(chunk_type, data):
    chunk = chunk_type + data
    return struct.pack('>I', len(data)) + chunk + struct.pack('>I', zlib.crc32(chunk) & 0xffffffff)

# Generate icons
for size in [192, 512]:
    png_data = create_png(size, size, (102, 126, 234))  # #667eea
    with open(f'icons/icon-{size}.png', 'wb') as f:
        f.write(png_data)
    print(f'Generated icon-{size}.png')

print('Done!')
