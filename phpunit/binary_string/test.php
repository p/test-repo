<?php

class StackTest extends PHPUnit_Framework_TestCase
{
    public function testPushAndPop()
    {
        // Unicode characters copy pasted from phpbb language files
        $chars = "’ » “ ” …";
        $expected = "This is a text string. Most of it is text. But it includes 6 Unicode characters: $chars";
        $actual = "none of those";
        $this->assertEquals($expected, $actual);
    }
}
