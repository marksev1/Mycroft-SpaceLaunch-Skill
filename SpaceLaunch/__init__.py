from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

import requests
import arrow

__author__ = 'msev'

LOGGER = getLogger(__name__)

class SpaceLaunchSkill(MycroftSkill):
    def __init__(self):
        super(SpaceLaunchSkill, self).__init__(name="SpaceLaunchSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))
        space_launch_intent = IntentBuilder("SpaceLaunchIntent").\
            require("SpaceLaunchKeyword").optionally('ExactLaunchKeyword').build()
        self.register_intent(space_launch_intent, self.handle_space_launch_intent)

    def handle_space_launch_intent(self, message):
        r = requests.get("https://launchlibrary.net/1.2/launch/next/1")
        t = str(r.json()['launches'][0]['windowstart'])
        try:
            if 'ExactLaunchKeyword' in message.data:
                self.speak_dialog("space.launch", data={'rocket': str(r.json()['launches'][0]['rocket']['name']),
                                                    'time': 'at ' + arrow.get(t,'MMMM DD, YYYY HH:mm:SS').to('local').format('HH:mm, on MMMM DD, YYYY'),
                                                    'location': str(r.json()['launches'][0]['location']['pads'][0]['name'])})
            else:
                self.speak_dialog("space.launch", data={'rocket': str(r.json()['launches'][0]['rocket']['name']),
                                                    'time': arrow.get(t,'MMMM DD, YYYY HH:mm:SS').to('local').humanize(),
                                                    'location': str(r.json()['launches'][0]['location']['pads'][0]['name'])})

                                                    
        except:
            self.speak_dialog("not.found")
        
    def stop(self):
        pass


def create_skill():
    return SpaceLaunchSkill()
