# SpaceLaunch skill

This skill interacts with https://launchlibrary.net/ api to return the latest space launch.

## How to install

Unzip or clone `SpaceLaunch` into `mycroft-core/mycroft/skills` directory.

`pip install arrow` into mycroft's virtual environment.

Restart mycroft instance and test with the following sentences: "when is the next space launch" or "what is the exact time of the next space launch".

Thanks praxeo for inspiration https://github.com/praxeo/mycroft_spaceflightnow_skill, his skill scrapes the webpage, while mine interacts with an api.
