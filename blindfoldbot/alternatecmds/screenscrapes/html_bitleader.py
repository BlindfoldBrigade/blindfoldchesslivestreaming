from html.parser import HTMLParser
from enum import Enum

class BitInformationType(Enum):
    USERNAME = 1
    SCORE = 2

class BitLeaderHTMLParser(HTMLParser):
    bit_information = []

    currently_parsing = None
    current_info = {}

    bit_information_type_from_element_name = {
        'bits-leaderboard-header-first-entry__username' : BitInformationType.USERNAME,
        'bits-leaderboard-header-first-entry__score' : BitInformationType.SCORE,
        'bits-leaderboard-header-runner-up-entry__username' : BitInformationType.USERNAME,
        'bits-leaderboard-header-runner-up-entry__score': BitInformationType.SCORE 
    }
    
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'class':
                    classeslist = attr[1].split()
                    for classs in classeslist:
                        if classs in self.bit_information_type_from_element_name.keys():
                            self.currently_parsing = self.bit_information_type_from_element_name[classs]
                            break

    def handle_endtag(self, tag):
        if tag == 'div':
            self.currently_parsing = None
            if BitInformationType.USERNAME in self.current_info.keys() and BitInformationType.SCORE in self.current_info.keys():
                self.bit_information.append([self.current_info[BitInformationType.USERNAME], self.current_info[BitInformationType.SCORE]])
                self.current_info = {}

    def handle_data(self, data):
        if not self.currently_parsing == None:
            self.current_info[self.currently_parsing] = data

def perform_parse(html_text_to_parse):
    parser = BitLeaderHTMLParser()
    parser.feed(html_text_to_parse)
    
    return parser.bit_information


if __name__ == "__main__":
    hauntfile = open('hauntcontent.html', 'r')
    hauntcontent = hauntfile.read()
    hauntfile.close()

    print(perform_parse(hauntcontent))
