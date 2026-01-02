# 🎬 Video to ASCII Converter

Convert any video into ASCII art and play it right in your terminal! This tool transforms video files into real-time ASCII animations with support for color and adaptive terminal sizing.

## ✨ Features

- **Real-time ASCII Video Playback** - Watch videos as ASCII art in your terminal
- **24-bit True Color Support** - Enable colorized output for a more vivid experience
- **Adaptive Terminal Sizing** - Automatically adjusts to your terminal dimensions
- **Aspect Ratio Calibration** - Interactive calibration for perfect square rendering
- **Smooth Playback** - Maintains original video FPS for fluid animations
- **Wide ASCII Character Set** - Uses 70+ characters for detailed gradients

## 🔧 Requirements

- Python 3.6+
- OpenCV (`cv2`)
- NumPy
- Colorama

## 📦 Installation

1. Clone this repository into vs code or any code editor:
```bash
git clone https://github.com/yourusername/video-to-ascii.git
cd video-to-ascii
```

2. Install required dependencies:
```bash
pip install opencv-python numpy colorama
```

## 🚀 Usage

Run the script:
```bash
python video_to_ascii.py
```

You'll be prompted to:
1. Enter the path to your video file
2. Choose whether to display in color
3. Select automatic terminal width or specify a custom width
4. Optionally calibrate the character aspect ratio for your terminal

### Example Session

```
🎬 Enter video file path: myvideo.mp4
🎨 Show in color? (y/n): y
🖥️ Use terminal width? (y/n, default y): y
Would you like to calibrate character aspect for your terminal? (y/N): n
Playing 'myvideo.mp4' as ASCII — width=100, color=True
(Press Ctrl+C to stop)
```

## 🎨 Color Mode

Enable color mode for a more immersive experience! The script uses 24-bit ANSI color codes to preserve the original video's colors in ASCII form.

## ⚙️ Configuration

### Character Aspect Ratio

The default character aspect ratio is `1.8`, which works well for most monospace terminal fonts. You can calibrate this interactively when running the script to ensure squares appear correctly on your specific terminal/font combination.

### ASCII Character Ramp

The script uses a gradient of 70+ ASCII characters from darkest to lightest:
```
$@B%8&WM#*oahkbdpqwmZ0OQLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,"^`'. 
```

### Width Settings

- **Auto mode**: Automatically detects terminal width (with a 2-column margin)
- **Manual mode**: Specify custom width (minimum 20 characters)
- **Max width**: Capped at 160 characters by default

## 🎯 How It Works

1. **Frame Extraction**: Reads video frames using OpenCV
2. **Resizing**: Scales frames to fit terminal width while maintaining aspect ratio
3. **Grayscale Conversion**: Converts to grayscale and normalizes contrast
4. **Character Mapping**: Maps pixel brightness to ASCII characters
5. **Colorization** (optional): Applies 24-bit RGB color codes to each character
6. **Display**: Clears screen and prints the ASCII frame at the original FPS

## 🐛 Troubleshooting

### Video won't play
- Ensure the video file path is correct and the file is accessible
- Check that OpenCV supports the video codec (try converting to MP4)

### Aspect ratio looks wrong
- Run the interactive calibration when prompted
- Adjust the `DEFAULT_CHAR_ASPECT` value (1.6-2.0 works for most terminals)

### Performance issues
- Reduce the ASCII width for faster rendering
- Disable color mode for better performance
- Use videos with lower resolution or frame rates

### Colors not displaying
- Ensure your terminal supports 24-bit true color
- Try modern terminal emulators like Windows Terminal, iTerm2, or Alacritty

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 🌟 Acknowledgments

- Built with OpenCV for video processing
- Uses Colorama for cross-platform color support

---

**Tip**: For the best experience, use a terminal with true color support and a monospace font like Consolas, Monaco, or JetBrains Mono!

