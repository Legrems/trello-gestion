# trello-gestion

## Install
It's a package pip, simply install it via `pip install .` when inside the root folder of the project.

You must export an os environ variable to the location of the settings file.
`export TRELLO_GESTION_SETTINGS_FILE="~/Documents/trello-gestion/settings.py"`

## Commands

### `-n`, `--names`
List of board name to perform the action. If this argument is not passed, all board defined in `settings.py` will be used.

#### Example:
`trello-gestion -n "my board name"`

### `-c`, `--cards`
List of cards names, only the one with matching string (case insensitive) will have the action performed.

#### Example:
`trello-gestion -c "my card name" "my other card name" ...`

### `--duedate`

### `--labels`

### `--restore`

### `--confirm`
