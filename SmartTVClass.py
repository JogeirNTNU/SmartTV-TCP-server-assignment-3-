class SmartTV:
  def __init__(self):
    self.tv_is_on = False
    self.currentChannel = 1  # TV remembers last channel
    self.availableChannels = 5

  def handle_command(self, command: str):
    """
    Support turn on and off TV, is TV on, switch channel, get available channels,
    get current channel and program version
    """
    parts = command.strip().split(" ", 1)
    if not parts:
      return "Error: No command received"
    cmd = parts[0].lower()
    
    if len(parts) > 1:
      args = parts[1]
    else:
      args = ""
    
    match cmd:
      case "version":
        return "SmartTV v1.0"
      case "turn":
        return self.handle_turn(args)  # handles both turn on and turn off
      case "switch":
        return self.handle_switch(args)  # handles both switch up and switch down
      case "set":
        return self.handle_set(args)  # handles setting current channel
      case "currentchannel":
        return self.handle_currentChannel()
      case "channels":
        return self.handle_channels()
      case "help":
        return (
          "Supported commands:\n" \
          "-turn on\n" \
          "-turn off\n" \
          "-switch up\n" \
          "-switch down\n" \
          "-set (channel)\n" \
          "-currentChannel\n" \
          "-channels\n" \
          "-help\n"
        )
      case _:
        return "Error: Unknown command"

  def handle_turn(self, args):  # Handles turning on or off
    try:
      if args.lower() == "on" and not self.isOn():  # if args is on as well as tv is off
        self.tv_is_on = True
        return "TV is turned on"
      elif args.lower() == "off" and self.isOn():
        self.tv_is_on = False
        return "TV is turned off"
      else:
        if self.isOn():
          return "TV is already on"
        else:
          return "TV is already off"
    except:
      return "Error: Invalid arguments"

  def handle_switch(self, args):  # Switches channel
    try:
      if not self.isOn():
        return "Cannot switch channel because tv is off"
      
      if args.lower() == "up":
        if self.currentChannel < self.availableChannels:
          self.currentChannel += 1
          return f"Channel switched to {self.currentChannel}"
        else:
          return f"Already on highest channel ({self.availableChannels})"
      elif args.lower() == "down":
        if self.currentChannel > 1:
          self.currentChannel -= 1
          return f"Channel switched to {self.currentChannel}"
        else:
          return f"Already on lowest channel (1)"
      else:
        return "Error: Invalid argument. Use 'up' or 'down'"
    except:
      return "Error: Invalid argument"

  def handle_set(self, args):  # changes currentChannel to any number from 1 to availableChannels
    try:
      if not self.isOn():
        return "Cannot switch channel because tv is off"
      
      channel = int(args)
      if channel < 1:
        return "Cannot change to a channel lower than 1"
      elif channel > self.availableChannels:
        return f"Cannot change to a channel higher than {self.availableChannels}"
      else:
        self.currentChannel = channel
        return f"Switched to channel {self.currentChannel}"
    except ValueError:
      return "Error: Channel must be a number"
    except:
      return "Error: Invalid argument"

  def handle_currentChannel(self):  # returns the current channel
    return f"Current channel is {self.currentChannel}"

  def handle_channels(self):
    result = "Current available channels are:"
    for channel in range(1, self.availableChannels + 1):
      result += f"\n{channel}"
    return result

  def isOn(self):  # returns bool value for the TV's status
    return self.tv_is_on