class eventlistener:

    messageRegistered = []
    specialRegistered = []

    def registerMessage(self, module):
        self.messageRegistered.append(module)

    def registerSpecial(self, module):
        self.specialRegistered.append(module)

    def handleMessage(self, text):
        for module in self.messageRegistered:
            user = "?"
            msg = "?"

            module.handleMessage(text, user, msg)

    def handleSpecial(self, text):
        for module in self.specialRegistered:
            module.handleSpecial(text)
