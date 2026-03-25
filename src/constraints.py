def build_constraints(channel_cols):
    bounds = {}

    for ch in channel_cols:
        bounds[ch] = (0.05, 0.6)

    return bounds