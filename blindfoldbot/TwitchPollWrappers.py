import dateutil



###RFC 3339 timestamp
###There's probably an elegant way to do this without bothering to make a class wrapper.  
###Replace this code if such a way is found :)
class datetime_rfc3339:
    
    def __init__(self, datestring):
        self.datetimee = dateutil.parser.parse(datestring)

    def __str__(self):
        return self.datetimee.isoformat()

class hundredlist:
    def __init__(self, liststring):
        self.listee = list(liststring)
        if len(self.listee) > 100:
            raise ValueError('The list is too long, maximum of 100 entries')

    def __str__(self):
        return self.listee.__str__()

class twitchmanifestid:
    def __init__(self, manifeststring):
        self.manifeststring = manifeststring
        if len(self.manifeststring) < 1 or len(self.manifeststring) > 64:
            raise ValueError('Length of Twitch manifest id must be between 1 and 64 characters')

    def __str__(self):
        return self.manifeststring

#I'm using this class because using a regular int with choices=range(1,101) ends up generating ugly help (it lists ALL numbers and not just a concise 1-100)
class hundredint:
    def __init__(self, intstring):
        self.intee = int(intstring)
        if self.intee < 1 or self.intee > 100:
            raise ValueError('number needs to be between 1 and 100')

    def __str__(self):
        return str(self.intee)

