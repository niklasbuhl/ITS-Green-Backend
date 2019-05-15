# Recompile javascript
browserify javascript.js -o static/js/bundle.js
# browserify javascript/color.js -o static/js/color.js
# browserify javascript/global.js -o static/js/global.js

# Run the webserver
python3 main.py
