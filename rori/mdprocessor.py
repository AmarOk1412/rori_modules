from rori import Interaction

class MDProcessor:
    def __init__(self, interaction):
        self.metadatas = interaction.metadatas

    def process(self):
        '''Craft metadatas to answer to a message'''
        return {}


class DirectReplyMDProcessor(MDProcessor):
    def __init__(self, interaction):
        super().__init__(interaction)

    def process(self):
        metadatas = {}
        if 'th' in self.metadatas:
            metadatas.update(rt=self.metadatas['th'])
        if 'ch' in self.metadatas:
            metadatas.update(ch=self.metadatas['ch'])
        return metadatas
