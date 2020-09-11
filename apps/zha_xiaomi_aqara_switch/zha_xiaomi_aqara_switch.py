"""
Customise the buttons on a Xiaomi Wireless Button integrated with ZHA
https://github.com/nickneos/Appdaemon-ZHA-Xiaomi-Aqara-Switch
"""
from appdaemon.plugins.hass.hassapi import Hass

# default values
DEFAULT_DIM_STEP_VALUE = 3
BUTTON_MAP = {
    1: "single",
    2: "double",
    3: "triple",
    4: "quadruple"
}
ALL_LIGHTS_NAME = [
    "lights",
    "all_lights",
    "group.all_lights"
]


class aqara_switch(Hass):
    """Define a Xiaomi Wireless Button base feature"""

    def initialize(self) -> None:
        """Configure"""
        # configure entities
        self.light = self.args.get("light", None)
        self.switch = self.args.get("switch")

        self.time_fired = None
        self.cycle_idx = -1
        
        # get the advanced button config if specified
        self.button_config = self.args.get("advanced", None)

        # get default button config if advanced config not specified
        if not self.button_config:
            if not self.light:
                self.log("Light entity not specified")
                return
            
            self.button_config = {
                "single": {
                    "action_type": "toggle",
                    "entity": self.light,
                    "parameters": {"transition": 0}
                }
            }

        # listener for button press
        self.listen_event(self.button_pressed_cb, "zha_event", device_ieee=self.switch)


    def button_pressed_cb(self, event_name: str, data: dict, kwargs: dict) -> None:
        """Take action when button is pressed"""
        
        try:
            click_value = data['args']['value']
        except KeyError:
            return

        click_type = BUTTON_MAP.get(click_value)
        self.log(click_type)

        # do action if defined in button config
        if click_type in self.button_config:
            self.action(self.button_config[click_type])


    def action(self, button_config: dict) -> None:
        """Call the respective service based on the passed button config."""

        action_type = button_config["action_type"]
        entities = button_config["entity"]
        parameters = button_config.get("parameters", {})

        # convert entities to list if not already
        if type(entities) is not list:
            entities = [entities]

        for entity in entities:

            # handle cycle action
            if action_type == "cycle":
                parameters = [parameters] if type(parameters) is not list else parameters
                self.cycle_action(entity, parameters)
                return
            
            # reset cycle index back to -1 on turn_off
            if action_type == "turn_off":
                self.cycle_idx = -1

            # handle entity for all lights
            if entity in ALL_LIGHTS_NAME:
                self.call_service(
                    f"light/{action_type}", 
                    entity_id="all", 
                    **parameters
                )
                return

            # lets do this
            self.call_service(
                f"{entity.split('.')[0]}/{action_type}", 
                entity_id=entity, 
                **parameters
            )
            

    def cycle_action(self, light, param_list):
        """Cycle through the parameter list with each button press"""

        if self.cycle_idx == -1:
            # when index -1, turn on light with previous settings
            parameters = {}
        else:
            # otherwise get paramaters from list using index 
            try:
                parameters = param_list[self.cycle_idx]
            except IndexError:
                self.cycle_idx = 0
                parameters = param_list[self.cycle_idx]
        
        # lets do this
        self.call_service(
            f"{light.split('.')[0]}/turn_on", 
            entity_id=light, 
            **parameters
        )
        
        # increment index for next button press
        self.cycle_idx += 1              


