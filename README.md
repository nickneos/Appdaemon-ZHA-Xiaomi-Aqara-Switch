# ZHA Controlled Xiaomi Aqara Wireless Switch
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs) [![homeassistant_community](https://img.shields.io/badge/HA%20community-forum-brightgreen)](https://community.home-assistant.io/) 

<a href="https://www.buymeacoffee.com/so3n" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

Fully customize the button events on a ZHA controlled Xiaomi Aqara Wireless Switch.
  
## Installing
Install via [HACS](https://hacs.xyz/). Alternatively, place the apps folder and its contents in your appdaemon folder.

## Configuration

### Main Config options

| Variable | Type   | Required                                   | Description                                                                                                                                                                                                                                                    |
| -------- | ------ | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| module   | string | True                                       | Set to `zha_xiaomi_aqara_switch`                                                                                                                                                                                                                               |
| class    | string | True                                       | Set to `aqara_switch`                                                                                                                                                                                                                                          |
| switch   | string | True                                       | `IEEE` of the Aqara Switch. This can be found by going to the integrations page on HA, and under Zigbee Home Automation click on [configure] > [devices] and then click on the device belonging to the Aqara Switch. `IEEE` will be listed under `Zigbee Info` |
| entity   | string | True (unless using advanced configuration) | `entity_id` of the device to control                                                                                                                                                                                                                           |
| advanced | list   | False                                      | Optional. Customize the actions for each button. See below                                                                                                                                                                                                     |


### **Advanced** Config options

| Variable       | Type   | Required | Description                                                                                                                                                       |
| -------------- | ------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `button event` | string | True     | Set the name of the variable to one of the button events you want to customize: `single`, `double`, `triple`, `quadruple`                                         |
| action_type    | string | True     | Service call to execute. Valid options: `turn_on`, `turn_off`, `toggle` or `cycle`                                                                                |
| entity         | string | True     | `entity_id` of the device to control. Can be a list of devices.                                                                                                                              |
| parameters     | dict   | False    | Optional. Specify the parameters to use for the service call (eg. `brightness`, `rgb_color`, `flash`, etc). Can include a list of parameters for the cycle option |



### Basic Example

```yaml
dimmer_bedroom:
  module: zha_xiaomi_aqara_switch
  class: aqara_switch
  switch: '00:00:00:00:00:00:00:00'
  light: light.bedroom
```

This sets up `light.bedroom` to be controlled by the Aqara Switch. Each `single` click toggles the light on and off:


### Advanced Example

```yaml
dimmer_main:
  module: zha_xiaomi_aqara_switch
  class: aqara_switch
  switch: '00:00:00:00:00:00:00:00'
  advanced:
    sinlge: 
      action_type: cycle
      entity: light.bedroom
      parameters:
        - brightness_pct: 33
          kelvin: 3000
        - brightness_pct: 67
          kelvin: 3000
        - brightness_pct: 100
          kelvin: 3000
        - brightness_pct: 0
    double:
      action_type: turn_off
      entity:
        - group.all_lights
        - switch.bedroom_tv

    
```
This advanced config customizes the button events on the Hue Dimmer Switch as follows::

* `single` click turns on or off the bedroom light by cycling through the following settings with each button press: 1) 33% brightness 3000 kelvin; 2) 67% brightness 3000 kelvin; 3) 100% brightness 3000 kelvin; and 4) off.
* `double` click turns of all lights, and the bedroom tv.


<hr/>

<a href="https://www.buymeacoffee.com/so3n" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
