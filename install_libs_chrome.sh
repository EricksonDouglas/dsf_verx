# shellcheck disable=SC2164
curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/109.0.5414.74/chromedriver_linux64.zip" && \
curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1070081%2Fchrome-linux.zip?alt=media" && \
unzip /tmp/chromedriver.zip -d layers/ && \
unzip /tmp/chrome-linux.zip -d layers/