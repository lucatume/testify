import sublime, sublime_plugin ,re

class HumanTestNamesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                    # get the selected text
                    s = self.view.substr(region)
                    # split the text in lines
                    lines = s.splitlines()
                    newLines = ''
                    for line in lines:
                        # transform to uppercase
                        s = line.title()
                        # remove spaces
                        s = re.sub("\\s+", "", s)
                        # prepend text
                        s = 'public function test' + s
                        # append text
                        plcHolder = "$this->markTestIncomplete('This test has not been implemented yet.');"
                        s = s + "()\n{\n" + plcHolder + "\n}\n\n"
                        # append modified line
                        newLines = newLines + s
                    # replace in text
                    self.view.replace(edit, region, newLines)
