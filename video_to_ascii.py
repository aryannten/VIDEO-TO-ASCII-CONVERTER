# video_to_ascii_enhanced_fixed.py
import cv2
import numpy as np
import os
import time
import shutil
from colorama import Style, init

init(autoreset=False)  # we'll manually reset per line

# More detailed ASCII ramp (dark -> light)
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZ0OQLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# Typical character height/width ratio (height divided by width).
# Common monospace fonts have char height ≈ 1.6–2.0 × width on many terminals.
DEFAULT_CHAR_ASPECT = 1.8

def get_terminal_width(default=100, margin=2):
    try:
        cols, _ = shutil.get_terminal_size()
        # leave a small margin so it doesn't wrap
        return max(20, cols - margin)
    except Exception:
        return default

def resize_frame(frame, new_width, char_aspect=DEFAULT_CHAR_ASPECT):
    """Resize frame maintaining aspect ratio tuned for terminal text.

    new_height is computed from: new_height_chars = (frame_h/frame_w) * new_width_chars / char_aspect
    where char_aspect = character_height / character_width.
    """
    h, w = frame.shape[:2]
    aspect_ratio = h / w
    new_height = max(1, int(aspect_ratio * new_width / float(char_aspect)))
    return cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)


def calibrate_char_aspect(initial=DEFAULT_CHAR_ASPECT):
    """Interactively calibrate character aspect ratio.

    The function shows a rendered ASCII square and asks for feedback so the
    user can tune char_aspect until a printed square looks visually square
    in their terminal/font.
    """
    try:
        ans = input("Would you like to calibrate character aspect for your terminal? (y/N): ").strip().lower()
    except Exception:
        return initial

    if ans != 'y':
        return initial

    char_aspect = float(initial)
    print("Calibration: you'll be shown a square. Reply 't' if it looks too tall, 's' if too short, 'g' if good.")
    for _ in range(4):
        # create a simple square image (white square on black)
        side = 80
        img = np.zeros((side, side, 3), dtype=np.uint8)
        # draw a centered smaller white square
        pad = int(side * 0.15)
        cv2.rectangle(img, (pad, pad), (side - pad - 1, side - pad - 1), (255, 255, 255), -1)

        # render centered at a reasonable width
        test_width = min(60, get_terminal_width())
        small = resize_frame(img, test_width, char_aspect=char_aspect)
        print("\n--- Calibration Preview ---")
        print(frame_to_ascii(small, colored=False))
        print("--- End Preview ---\n")

        resp = input("Does the square look (t)oo tall, (s)hort, or (g)ood? [g]: ").strip().lower() or 'g'
        if resp == 'g':
            break
        # Adjust char_aspect: if it's too tall, increase char_aspect to reduce rows; if too short, decrease.
        if resp == 't':
            char_aspect *= 1.15
        elif resp == 's':
            char_aspect /= 1.15
        # clamp
        char_aspect = max(0.5, min(3.0, char_aspect))
        print(f"Adjusted char_aspect -> {char_aspect:.2f}\n")

    print(f"Using character aspect ratio: {char_aspect:.2f}")
    return char_aspect

def frame_to_ascii(frame, colored=False):
    """Convert a BGR OpenCV frame to ASCII string. If colored=True, include 24-bit color escapes."""
    # Convert to grayscale and normalize contrast across the frame for better clarity
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    rows, cols = normalized.shape
    chars_len = len(ASCII_CHARS)
    out_lines = []

    for i in range(rows):
        row_chars = []
        if colored:
            # build a colored line then append a reset once at the end
            for j in range(cols):
                pixel = int(normalized[i, j])
                # safe index: ensure it never equals chars_len
                idx = min(chars_len - 1, (pixel * chars_len) // 256)
                ch = ASCII_CHARS[idx]
                b, g, r = frame[i, j]
                row_chars.append(f"\033[38;2;{int(r)};{int(g)};{int(b)}m{ch}")
            row_str = "".join(row_chars) + Style.RESET_ALL
        else:
            for j in range(cols):
                pixel = int(normalized[i, j])
                idx = min(chars_len - 1, (pixel * chars_len) // 256)
                row_chars.append(ASCII_CHARS[idx])
            row_str = "".join(row_chars)
        out_lines.append(row_str)

    return "\n".join(out_lines)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def play_video_as_ascii(video_path, width=None, colored=False, max_width=160, char_aspect=DEFAULT_CHAR_ASPECT):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video:", video_path)
        return

    # get video fps, fallback if unavailable
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    frame_delay = 1.0 / fps

    # auto width detection
    if width is None:
        term_width = get_terminal_width()
        width = min(term_width, max_width)
    width = max(20, int(width))

    # get terminal rows so we can avoid producing more lines than the terminal height
    try:
        term_cols, term_rows = shutil.get_terminal_size()
    except Exception:
        term_cols, term_rows = (width, 40)

    print(f"Playing '{video_path}' as ASCII — width={width}, color={colored}")
    print("(Press Ctrl+C to stop)\n")

    try:
        prev_time = time.perf_counter()
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            start = time.perf_counter()
            # compute a width that will not exceed terminal rows when rendered
            h, w = frame.shape[:2]
            # predicted height for currently-chosen width
            predicted_h = int((h / w) * width / float(char_aspect))
            max_allowed_h = max(4, term_rows - 4)
            use_width = width
            if predicted_h > max_allowed_h:
                # recompute width so predicted_h == max_allowed_h
                use_width = max(20, int(max_allowed_h * char_aspect * (w / h)))
            small = resize_frame(frame, use_width, char_aspect=char_aspect)
            ascii_frame = frame_to_ascii(small, colored=colored)
            clear_screen()
            print(ascii_frame)

            # timing: aim for original fps but subtract processing time
            elapsed = time.perf_counter() - start
            sleep_for = frame_delay - elapsed
            if sleep_for > 0:
                time.sleep(sleep_for)

    except KeyboardInterrupt:
        print("\nPlayback interrupted by user.")
    finally:
        cap.release()
        print("Done ✅")

if __name__ == "__main__":
    path = input("🎬 Enter video file path: ").strip()
    if not path:
        print("No path provided. Exiting.")
        raise SystemExit(1)

    color_choice = input("🎨 Show in color? (y/n): ").strip().lower() == "y"
    auto_width = input("🖥️ Use terminal width? (y/n, default y): ").strip().lower() != "n"
    if auto_width:
        chosen_width = None
    else:
        w = input("Enter desired ASCII width (e.g. 80): ").strip()
        try:
            chosen_width = int(w) if w else None
        except ValueError:
            chosen_width = None

    # optional calibration step to tune character aspect ratio for this terminal/font
    char_aspect = calibrate_char_aspect(DEFAULT_CHAR_ASPECT)

    play_video_as_ascii(path, width=chosen_width, colored=color_choice, char_aspect=char_aspect)
