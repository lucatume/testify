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

    should throw for something
    should not call that when called with this
    constructor properly sets some value
    constructor will not do something
    some method should fail with foo, baz and bar

and will transform those in proper [PHPUnit](http://phpunit.de/) test methods like

    public function SomethingProvider()
    {
        // $something
        return array(
            array(null)
        );
    }

    /**
     * @dataProvider SomethingProvider
     */
    public function testShouldThrowForThis($something)
    {
        $this->markTestIncomplete('This test has not been implemented yet.');
    }

    /**
     * @dataProvider ThisProvider
     */
    public function testShouldNotCallThatWhenCalledWithThis($this)
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

    public function FooBazBarProvider()
    {
        // $foo, $baz, $bar
        return array(
            array(null, null, null)
        );
    }

    /**
     * @dataProvider FooBazBarProvider
     */
    public function testSomeMethodShouldFailWithFooBazAndBar($foo, $baz, $bar)
    {
        $this->markTestIncomplete('This test has not been implemented yet.');
    }

using camelCase notation.

### Data Providers
The plugin will presume that lines containing the words <code>with</code> or <code>for</code> are for tests that will require a <code>dataProvider</code> method and will generate the data provider and the associated variables by default as seen in the first, second and fifth line above.
The plugin will also avoid generating duplicate data provider methods.
Appending a trailing <code>-</code> to the line will prevent the plugin from generating a data provider method

    add default throws for null value argument-

will generate

    public function testAddDefaultThrowsForNullValueArgument()
    {
        $this->markTestIncomplete('This test has not been implemented yet.');
    }

while 

    add default throws for null value argument

would generate the test method and the data provider method as well

    public function NullValueArgumentProvider()
    {
        // $nullValueArgument
        return array(
            array(null)
        );
    }

    /**
    * @dataProvider NullValueArgumentProvider
    */
    public function testAddDefaultThrowsForNullValueArgument($nullValueArgument)
    {
        $this->markTestIncomplete('This test has not been implemented yet.');
    }

which might not always be the desired result.
