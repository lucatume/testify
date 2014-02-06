import sublime, sublime_plugin , re

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
                        # set block text if any
                        if self.containsDataProviderToken(line):
                            self. setDataProviderMethodTextAndCommentBlockUsing(self.getDataProviderTokenTextFrom(line))
                        # transform to uppercase
                        s = line.title()
                        # remove spaces
                        s = re.sub("\\s+", "", s)
                        # prepend text
                        s = self.blockText + 'public function test' + s
                        # append text
                        plcHolder ="\t$this->markTestIncomplete('This test has not been implemented yet.');"
                        s = s + "(%s)\n{\n" % (self.variableName)
                        s = s + plcHolder + "\n}\n"
                        # append modified line
                        newLines = newLines + s
                    # replace in text
                    self.view.replace(edit, region, newLines)
                    # reindent output
                    self.view.run_command('reindent')
    def containsDataProviderToken(self, searchText):
        if re.search("@dp\\s+", searchText):
            return True
        return False
    def getDataProviderTokenTextFrom(self, searchText):
        result = re.sub("^.*@dp\\s([\\w\\s]*)@*.*", "\\1", searchText)
        return result
    def setDataProviderMethodTextAndCommentBlockUsing(self, text):
        # remove leading and trailing spaces
        text = text.strip()
        # create the dataProviderMethodName
        methodName = text.title()
        methodName = re.sub("\\s+", "", methodName)
        self.variableName = '$' + methodName[0].lower() + methodName[1:]
        methodName =  methodName + 'Provider'
        methodName = methodName[0].lower() + methodName[1:]
        # create data provider method placeholder text like
        commentText = text
        # replace the strings in the template
        self.blockText = "public function %s(){\nreturn array(\n\t\t\t//%s\n);\n}\n\t/**\n\t * @dataProvider %s\n\t */\n" % (methodName, commentText, methodName)
