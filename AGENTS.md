## Правила проекта

- Перед написанием или правкой любого текста года читать `СТИЛЬ.md`.
- Структура — в `README.md`. Тексты годов — только `years/*.md`; HTML в `site/` пересобирается `python3 tools/generate_html.py`, руками не правится.
- Не создавать в корне варианты файлов (`_v2`, `_Claude`, `_temp`). Временное — в `_tmp/`, в конце работы удалить.
- Сырые сканы — в `../namedni_источники/`, в папку проекта и в git их не копировать. Для поиска по книгам — `ref/ocr/`.
- Фото для вёрстки — в `img/<год>/`, имена по `img/NAMING.md`.
- Отправка на GitHub: с Mac напрямую нет пароля. Делать так: `git bundle create _tmp/push.bundle main` → забрать файл в облачную сессию → `git clone` из бандла → `git push --force https://github.com/yurivolosnikov-cell/namedni main` (доступ через подключённый GitHub) → на Mac `git fetch origin`, удалить `_tmp/push.bundle`.
