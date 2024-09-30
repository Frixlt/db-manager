# DB Manager

[Читать русскую версию](README.ru.md)

The "DB Manager" project was initially designed as a simple database management tool. However, during development, many security vulnerabilities were discovered, along with a significant amount of new knowledge that had to be learned to implement it fully.

Unfortunately, many of the planned features were not completed, and the need for this project has since disappeared.

Additionally, the project lacks a `requirements.txt` file, which complicates installation and execution. The project currently only works on Windows due to incorrect path handling (I did not use `os.path`).

## Usage

1. Modify the `app/data_base_functions.py` file to fit your database.
2. Run `app/config_controll.py` to configure the settings.
3. Open and adjust the configuration file `app/config/config.ini` as needed.
4. Launch the application through `main.py`.

## Additional Information

This project is deprecated and no longer maintained.

Refer to the [Russian version of README](readme.ru.md).
