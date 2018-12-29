# Glyph table
GLYPH_TABLE = [[[[0, 1, 0, 1, 0, 0, 0, 1, 1], [0, 0, 1, 1, 0, 1, 0, 1, 0], [1, 1, 0, 0, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 1, 0, 0]], "devil"], [
                   [[1, 0, 0, 0, 1, 0, 1, 0, 1], [0, 0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 0, 0, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0, 0]], "devil_red"]]


# Match glyph pattern to database record
def match_glyph_pattern(glyph_pattern):
    glyph_found = False
    glyph_rotation = None
    glyph_substitute = None

    for glyph_record in GLYPH_TABLE:
        for idx, val in enumerate(glyph_record[0]):
            if glyph_pattern == val:
                glyph_found = True
                glyph_rotation = idx
                glyph_substitute = glyph_record[1]
                break
        if glyph_found: break

    return (glyph_found, glyph_rotation, glyph_substitute)