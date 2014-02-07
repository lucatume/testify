import sublime
import sublime_plugin
import re


class HumanTestNamesCommand(sublime_plugin.TextCommand):
    variableName = ''
    blockText = ''

    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                    # get the selected text
                    s = self.view.substr(region)
                    # split the text in lines
                    lines = s.splitlines()
                    newLines = ''
                    for line in lines:
                        out = ''
                        pre = ''
                        testMethodName = ''
                        testMethodBody = ''
                        post = ''
                        # get new generator instances
                        dp = DataProviderGenerator(line)
                        variableName = ''
                        # check for the data provider token
                        if dp.containsDataProviderToken():
                            pre += dp.getDataProviderMethodTextAndCommentBlock()
                            variableName = dp.getVariableName()
                        tg = TestMethodGenerator(line, variableName)
                        testMethodName = tg.getTestMethodName()
                        testMethodBody = tg.getTestMethodBody()
                        out += pre
                        out += testMethodName
                        out += testMethodBody
                        out += post
                        # append modified line
                        newLines = newLines + out
                    # replace in text
                    self.view.replace(edit, region, newLines)
                    # reindent output
                    self.view.run_command('reindent')


class TestMethodGenerator:

    def __init__(self, text, variableName=''):
        self.variableName = variableName
        if variableName != '':
            self.variableName = '$'+variableName
        self.text = self.removeGeneratorTokensFrom(text)

    def removeGeneratorTokensFrom(self, text):
        return re.sub("#", "", text)

    def getTestMethodName(self):
        # make a title
        out = self.text.title().strip()
        # remove spaces
        out = re.sub("\\s+", "", out)
        out = 'public function test' + out
        out += '(' + self.variableName + ')\n'
        return out

    def getTestMethodBody(self):
        out = ''
        out += '{'
        out += "\n\t$this->markTestIncomplete('This test has not been implemented yet.');"
        out += '\n}\n'
        return out

class DataProviderGenerator:

    def __init__(self, text):
        self.text = text

    def containsDataProviderToken(self):
        # search for the opening token
        return re.search("\\s+#", self.text)

    def getVariableName(self):
        out = re.sub("(.*)\\s+#([^#]*)\\s*(.*)", "\\2", self.text)
        out = out.strip().title()
        out = out[0].lower() + out[1:]
        out = re.sub('\\s', '', out)
        return out

    def getDataProviderMethodTextAndCommentBlock(self):
        dataProviderMethodName = self.getVariableName() + 'Provider()'
        out = ''
        out += '\npublic function ' + dataProviderMethodName
        out += '\n{'
        out += '\n\treturn array('
        out += '\n\t\t// ' + self.getVariableName()
        out += '\n\t);'
        out += '\n}'
        out += '\n\t/**'
        out += '\n\t * @dataProvider ' + dataProviderMethodName
        out += '\n\t */'
        out += '\n'
        return out