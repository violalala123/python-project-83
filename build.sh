#!/usr/bin/env bash
# скачиваем uv и запускаем команду установки зависимостей
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
make install

npm install
npx @tailwindcss/cli -i page_analyzer/src_styles.css -o page_analyzer/static/styles.css --minify