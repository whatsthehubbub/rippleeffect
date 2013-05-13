def colorify(str, s, v):
    m = hashlib.md5()
    m.update(str)

    # get a hue value by chopping the first two digits off a hex digest
    hue = int(m.hexdigest()[:4], 16) # yields an 8-bit integer; 0-255
    #print "raw hue", str, hue

    hue = hue / (255*255*1.0) # map 0-255 to 0-1 for colorsys
    #print "normalized hue", str, hue

    # compute rgb values based on our new h value, and preset s and v values
    rgb = colorsys.hsv_to_rgb(hue, s, v)

    # scale the rgb 0-1 range back to 0-255
    rgb = tuple([int(math.floor(255.0*x)) for x in rgb])

    # convert the rgb values to hex
    return '#%02x%02x%02x' % rgb
