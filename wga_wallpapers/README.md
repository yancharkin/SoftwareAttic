# WGA Wallpapers

Python script that download random image from [Web Gallery of Art](https://www.wga.hu), scale it to the given size and (optionally) add some info.

## Dependencies

**Debian/Ubuntu**

    sudo apt install python-bs4 python-lxml python-pil

**Archlinux**

    sudo pacman -S python-beautifulsoup4 python-lxml python-pillow python-requests
    
**Fedora**

    sudo dnf install python-beautifulsoup4 python-pillow python-requests
    
**Pip**

    pip install beautifulsoup4 lxml Pillow

## Usage

#### Unix

    python wga_wallpapers.py PATH WIDTH HEIGHT FONT_SIZE INFO KEYWORDS
    
#### Window

    python.exe wga_wallpapers.py PATH WIDTH HEIGHT FONT_SIZE INFO KEYWORDS
    
 - **PATH**- full path to file
 - **WIDTH** - image width in pixels
 - **HEIGHT** - image height in pixels
 - **FONT_SIZE** - font size
 - **INFO** - how much info print on the image
   * **0** - no info
   * **1** - add only author and title
   * **2** - add full info
 - **KEYWORDS** - filter images by this keywords

### Example:

#### Unix

    python wga_wallpapers.py "/home/$USER/Pictures/wallpaper.jpg" 1366 768 18 2 "van gogh, monet"

#### Window

    pythonw.exe wga_wallpapers.py "C:\Users\user\Desktop\wallpaper.jpg" 1366 768 18 2 "van gogh, monet"
    
If there is image named 'background.jpg' in configuration directory ('$HOME/.config/wga_wallpapers' or 'C:\Users\USER_NAME\wga_wallpapers' by default) it will be used as background, else backgound will be black.

### Advanced usage examples

#### Change wallpapers in Awesome WM with shortcut

- Put 'wga_wallpapers.py' to $PATH (or create simlink)
- Create file 'wga_wallpapers_set' in $PATH (and make it executable):

      #!/bin/bash
        
      # Adjust accordingly to your system
      # Example for two monitors.
        
      wga_wallpapers.py \
      '/home/$USER/.config/awesome/wallpapers/wallpaper_1.jpg' 1600 900 18 2 "van gogh"

      wga_wallpapers.py \
      '/home/$USER/.config/awesome/wallpapers/wallpaper_2.jpg' 1280 1024 18 2 "monet, repin"

      echo -e 'local gears = require("gears") ; 
      gears.wallpaper.maximized("/home/$USER/.config/awesome/wallpapers/wallpaper_1.jpg", screen[1], true) ; 
      gears.wallpaper.maximized("/home/$USER/.config/awesome/wallpapers/wallpaper_2.jpg", screen[2], true)' \
      | awesome-client

    

- In 'rc.lua' add to 'Key bindings':

      awful.key( { modkey, }, "w", function () awful.util.spawn_with_shell("wga_wallpapers_set") end ),
        
- Restart awesome wm, now wallpapers can be changed by pressing **'Supper + w'**
