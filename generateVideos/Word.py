class Word:
    wordCount = 0
    def __init__(self, dict):
        '''
        Parameters:
          dict (dict) dictionary from JSON, containing:
            conf (float): degree of confidence, from 0 to 1
            end (float): end time of the pronouncing the word, in seconds
            start (float): start time of the pronouncing the word, in seconds
            word (str): recognized word
        '''
        
        self.conf = dict["conf"]
        self.end = dict["end"]
        self.start = dict["start"]
        self.word = dict["word"]
        Word.wordCount+=1
        self.idx = Word.wordCount

    def to_string(self):
        return "{:20} from {:.2f} sec to {:.2f} sec, confidence is {:.2f}%, idx: {}".format(
            self.word, self.start, self.end, self.conf*100, self.idx)
