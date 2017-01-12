from rori import RORIModule, RORIData

class Module(RORIModule):
    def process(self, data):
        question = self.rori.is_awaiting(data.author)
        if question is not None:
            self.rori.remove_awaiting(data.author)
            string_to_say = self.rori.get_localized_sentence("np", self.sentences)
            self.rori.send_for_best_client("text", data.author, string_to_say, data.client)
        self.stop_processing = True
