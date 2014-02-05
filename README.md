testify
=======

A Sublime Text plugin aimed at making writing PHPUnit tests less painful.

## Installation
1. Download the file
2. Unarchive the file in Sublime Text [packages folder](http://sublimetext.info/docs/en/extensibility/packages.html)

The new menus and command palette options should appear in yout Sublime Text installation

## Usage

### Natural language test names
The plugin will take test method names written in natural language

    should throw for this
    should not call that when called with this
    constructor properly sets some value
    constructor will not do something

and will transform those in proper [PHPUnit](http://phpunit.de/) test methods like

    public function testShouldThrowForThis()
    {
        $this->markTestIncomplete('This test has not been implemented yet.');
    }

    public function testShouldNotCallThatWhenCalledWithThis()
    {
        $this->markTestIncomplete('This test has not been implemented yet.');
    }

    public function testConstructorProperlySetsSomeValue()
    {
        $this->markTestIncomplete('This test has not been implemented yet.');
    }

    public function testConstructorWillNotDoSomething()
    {
        $this->markTestIncomplete('This test has not been implemented yet.');
    }

using camelCase notation.