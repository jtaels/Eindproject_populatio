class FormErrorException(Exception):
    def __init__(self, messages=None):
        # Als geen berichten worden meegegeven, wordt een lege lijst gebruikt.
        if messages is None:
            messages = []
        self.messages = messages
        super().__init__(self.messages)

    def add_message(self, message):

        self.messages.append(message)

    def merge_messages(self, messages_to_add):

        self.messages + messages_to_add

    def __str__(self):

        return f"FormErrorException: {', '.join(self.messages)}"
