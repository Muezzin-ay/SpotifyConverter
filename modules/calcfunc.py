

def convert_duration(duration_text) -> int:
    units = duration_text.split(":")
    seconds = int(units[0]) * 60 + int(units[1])
    return seconds