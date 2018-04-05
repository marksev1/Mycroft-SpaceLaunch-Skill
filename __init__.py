from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler

import requests
import arrow

__author__ = 'msev', 'jarbas'


class SpaceLaunchSkill(MycroftSkill):
    def __init__(self):
        super(SpaceLaunchSkill, self).__init__(name="SpaceLaunchSkill")

    @intent_handler(IntentBuilder("SpaceLaunchIntent").\
            require("SpaceLaunchKeyword").optionally(
            'ExactLaunchKeyword').optionally("next"))
    def handle_space_launch_intent(self, message):
        try:
            r = requests.get("https://launchlibrary.net/1.2/launch/next/1")
            date = str(r.json()['launches'][0]['windowstart'])
            description = str(r.json()['launches'][0]["missions"][0]
                                   ["description"])
            self.set_context("launch_description", description)
            day_len = len(date.split(",")[0].split(" ")[1])

            if day_len == 1 and 'ExactLaunchKeyword' in message.data:
                date_time = 'at ' + arrow.get(date, 'MMMM D, YYYY HH:mm:SS')\
                    .to('local').format('HH:mm, on MMMM DD, YYYY')
            elif day_len == 1:
                date_time = arrow.get(date, 'MMMM D, YYYY HH:mm:SS')\
                    .to('local').humanize()
            elif 'ExactLaunchKeyword' in message.data:
                date_time = 'at ' + arrow.get(date, 'MMMM DD, YYYY HH:mm:SS')\
                    .to('local').format('HH:mm, on MMMM DD, YYYY')
            else:
                date_time = arrow.get(date, 'MMMM DD, YYYY HH:mm:SS').to(
                        'local').humanize()

            rocket = str(r.json()['launches'][0]['rocket']['name'])
            location = str(r.json()['launches'][0]['location']['pads'][0]
                           ['name'])
            self.speak_dialog("space.launch",
                              data={'rocket': rocket,
                                    'time': date_time,
                                    'location': location})
        except Exception as e:
            self.log.error(e)
            self.speak_dialog("not.found")

    @intent_handler(IntentBuilder("SpaceLaunchIntent")
                    .require("launch_description")
                    .require('MoreKeyword'))
    def handle_space_launch_intent(self, message):
        description = message.data["launch_description"]
        self.speak(description)


def create_skill():
    return SpaceLaunchSkill()
