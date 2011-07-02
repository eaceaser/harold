from ConfigParser import RawConfigParser

HAROLD_PREFIX = "harold"
IRC_SECTION_NAME = HAROLD_PREFIX + ":" + "irc"
HTTP_SECTION_NAME = HAROLD_PREFIX + ":" + "http"
REPOSITORY_PREFIX = HAROLD_PREFIX + ":" + "repository" + ":"

class _ConfigStub(object):
    pass

class HaroldConfiguration(object):
    def __init__(self, filenames):
        parser = RawConfigParser()
        parser.read(filenames)

        # read the basic IRC configuration
        self.irc = _ConfigStub()
        self.irc.host = parser.get(IRC_SECTION_NAME, "host")
        self.irc.port = parser.getint(IRC_SECTION_NAME, "port")
        self.irc.use_ssl = parser.getboolean(IRC_SECTION_NAME, "use_ssl")
        self.irc.nick = parser.get(IRC_SECTION_NAME, "nick")
        self.irc.password = parser.get(IRC_SECTION_NAME, "password")

        # read the basic HTTP configuration
        self.http = _ConfigStub()
        self.http.port = parser.getint(HTTP_SECTION_NAME, "port")
        self.http.secret = parser.get(HTTP_SECTION_NAME, "secret")

        # read the repositories
        self.repositories = []
        self.repositories_by_name = {}
        self.channels = set()
        for section in parser.sections():
            if not section.startswith(REPOSITORY_PREFIX):
                continue

            repository = _ConfigStub()
            repository.name = section[len(REPOSITORY_PREFIX):]
            repository.channel = parser.get(section, "channel")
            repository.format = parser.get(section, "format")

            self.repositories.append(repository)
            self.repositories_by_name[repository.name] = repository
            self.channels.add(repository.channel)