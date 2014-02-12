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
                    # init the method manager
                    manager = MethodManager()
                    for line in lines:
                        # init the data provider generator
                        dp = DataProviderGenerator(line, manager, StringChainer(), OptionsManager())
                        # init the outputs
                        out = ''
                        # what comes before the actual test method
                        pre = ''
                        # '$arg1, $arg2, $arg3'
                        variables = []
                        # 'testMethodWillDoForSomething'
                        testMethodName = ''
                        # the method body and its signature
                        testMethodBody = ''
                        post = ''
                        # check for the data provider token
                        if dp.containsToken() and dp.shouldGenerate():
                            pre += dp.getPre()
                            variables = dp.getVariables()
                        tg = TestMethodGenerator(line, variables, StringChainer(), OptionsManager())
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


class MethodManager:
    generatedMethods = []

    def add(self, methodName):
        if methodName in self.generatedMethods:
            return
        self.generatedMethods.append(methodName)

    def contains(self, methodName):
        if methodName in self.generatedMethods:
            return True
        return False


class StringChainer():

    def uchain(self, strings, pre='', sep='', post=''):
        out = ''
        buf = []
        for string in strings:
            buf.append(pre + string.title() + post)
        out = sep.join(buf)
        return out

    def chain(self, strings, pre='', sep='', post=''):
        out = ''
        buf = []
        for string in strings:
            buf.append(pre + string + post)
        out = sep.join(buf)
        return out

    def lchain(self, strings, pre='', sep='', post=''):
        out = ''
        buf = []
        for string in strings:
            buf.append(pre + string[0].lower() + string[1:] + post)
        out = sep.join(buf)
        return out


class OptionsManager:

    def getNonTextSeparators(self):
        return (',', ', ', ' ,')

    def getDataProviderSeparators(self):
        return ('for', 'with')

    def getDataProviderSubSeparators(self):
        return (' and ', ', ')

    def getDataProviderMethodGenerationNegationChars(self):
        return ('-')

class TestMethodGenerator:
    variables = []
    stringChainer = None
    optionsManager = None

    def __init__(self, text, variables, stringChainer, optionsManager):
        self.variables = variables
        self.optionsManager = optionsManager
        charsToStrip = self.optionsManager.getNonTextSeparators()
        pattern = '|'.join(charsToStrip)
        self.text = re.sub(pattern, '', text)
        # strip any leading or trailing data provider method generation
        # negation char
        for char in self.optionsManager.getDataProviderMethodGenerationNegationChars():
            self.text = self.text.strip(char)
        # remove and put in dep in
        self.stringChainer = stringChainer

    def getTestMethodName(self):
        cc = CamelCase(self.text)
        out = cc.uFirst()
        out = 'public function test' + out
        varsString = self.stringChainer.chain(self.variables, '$', ', ')
        out += '(' + varsString + ')\n'
        return out

    def getTestMethodBody(self):
        out = ''
        out += '{'
        out += "\n\t$this->markTestIncomplete('This test has not been implemented yet.');"
        out += '\n}\n'
        return out


class DataProviderGenerator:
    generatedDataProviderMethodNames = []
    text = ''
    variablesText = ''
    variables = []
    methodManager = None
    optionsManager = None

    def __init__(self, text, methodManager, stringChainer, optionsManager):
        self.text = text
        self.methodManager = methodManager
        self.stringChainer = stringChainer
        self.optionsManager = optionsManager

    def getVariables(self):
        return self.variables

    def containsToken(self):
        for token in self.optionsManager.getDataProviderSeparators():
            if token in self.text:
                return True
        return False

    def chopStringUsing(self, string, tokens):
        out = ''
        pattern = '|'.join(tokens)
        out = re.split(pattern, string)
        return out

    def setVariables(self):
        # get the part of the line after the token
        separators = '|'.join(self.optionsManager.getDataProviderSeparators())
        variables = re.sub("(.*)\\s+(" + separators + ")\\s+(.*)\\s*", "\\3", self.text)
        self.variablesText = variables
        # split the line using the sub-tokens
        self.variables = self.chopStringUsing(variables, self.optionsManager.getDataProviderSubSeparators())
        buf = []
        for variableString in self.variables:
            cc = CamelCase(variableString)
            buf.append(cc.lFirst())
        self.variables = buf

    def getVariablesString(self):
        out = ''
        out = self.stringChainer.chain(self.variables, '$', ', ')
        return out

    def getCommentBlock(self, dataProviderMethodName):
        out = ''
        out += '\n\t/**'
        out += '\n\t * @dataProvider ' + dataProviderMethodName
        out += '\n\t */'
        out += '\n'
        return out

    def getMethodName(self):
        out = ''
        escapedVariablesText = re.sub("[^\\w\\s_]", "", self.variablesText)
        cc = CamelCase(escapedVariablesText)
        out = cc.uFirst()
        out += 'Provider'
        return out

    def getPre(self):
        out = ''
        self.setVariables()
        variablesString = self.getVariablesString()
        dataProviderMethodName = self.getMethodName()
        methodNameWithParenthesis = dataProviderMethodName + '()'
        # if same data provider method has been generated before skip
        if not self.methodManager.contains(dataProviderMethodName):
            self.methodManager.add(dataProviderMethodName)
            out += '\npublic function ' + methodNameWithParenthesis
            out += '\n{'
            out += '\n\treturn array('
            out += '\n\t\t// ' + variablesString
            out += '\n\t);'
            out += '\n}\n'
        # generate the comment block
        out += self.getCommentBlock(dataProviderMethodName)
        return out

    def shouldGenerate(self):
        for negationChar in self.optionsManager.getDataProviderMethodGenerationNegationChars():
            # look for the negation char at the end of the line
            pattern = '^.*' + negationChar + '$'
            if re.search(pattern, self.text):
                return False
        return True


class CamelCase:
    text = ''

    def __init__(self, text):
        self.text = text

    def uFirst(self):
        out = ''
        if len(out) is 1:
            return out.upper()
        out = self.text.strip().title()
        out = re.sub('\\s', '', out)
        return out

    def lFirst(self):
        out = ''
        out = self.uFirst()
        out = out[0].lower() + out[1:]
        return out
