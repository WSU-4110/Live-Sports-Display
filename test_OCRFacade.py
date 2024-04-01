from OCRFacade import OCR

def test_cleanText():
    AnOCR = OCR();    
    testString = AnOCR.cleanText("John ()()()())))Smit***&*&!h-Brown ////#$@^#^ghi")
    assert testString == "John Smith-Brown ghi";
    testString = AnOCR.cleanText("")
    assert testString == "";
    testString = AnOCR.cleanText(4536)
    assert testString == -1
    

def test_findFullName():
    AnOCR = OCR();
    testString = AnOCR.findFullName("John Smith-Brown ghi ",0)
    assert testString == "John Smith-Brown";
    testString = AnOCR.findFullName("John Smith-Brown ghi ",5)
    assert testString == "Smith-Brown ghi";
    testString = AnOCR.findFullName(345,0)
    assert testString == -1;
    testString = AnOCR.findFullName("John Smith-Brown ghi ","ibfbdajkno")
    assert testString == -1;
    testString = AnOCR.findFullName("John",0)
    assert testString == "John";
    testString = AnOCR.findFullName("John Smith-Brown ghi ",17)
    assert testString == "ghi ";
    

def test_findNextStartIndex():
    AnOCR = OCR();
    testIndex = AnOCR.findNextStartIndex("John Smith-Brown ghi ",0)
    assert testIndex == 5;
    testIndex = AnOCR.findNextStartIndex("John Smith-Brown ghi ",5)
    assert testIndex == 17;
    testIndex = AnOCR.findNextStartIndex(47,5)
    assert testIndex == -1;
    testIndex = AnOCR.findNextStartIndex("John Smith-Brown ghi ","ekfaiwhGEIUTF6")
    assert testIndex == -1;
    testIndex = AnOCR.findNextStartIndex("John ",0)
    assert testIndex >= 5;
    testIndex = AnOCR.findNextStartIndex("John Smith-Brown ghi ",17)
    assert testIndex >= 21;

def test_getLastNameFromString():
    AnOCR = OCR();
    testString = AnOCR.getLastNameFromString("John Smith")
    assert testString == "Smith";
    testString = AnOCR.getLastNameFromString("John")
    assert testString == -1;
    testString = AnOCR.getLastNameFromString("John ")
    assert testString == "";
    testString = AnOCR.getLastNameFromString(56)
    assert testString == -1;


def test_isPlayer():
    AnOCR = OCR();
    testString = AnOCR.isPlayer("LeBron James")
    assert testString == "LeBron James";
    testString = AnOCR.isPlayer("L James")
    assert testString == "LeBron James";
    testString = AnOCR.isPlayer("Random Text")
    assert testString == 0;
    testString = AnOCR.isPlayer(354)
    assert testString == -1;
    

def test_searchForNames():
    AnOCR = OCR();
    testArray = AnOCR.searchForNames("LeBron James rsoafaoshj ouerads S M Bamba")
    assert testArray == ["LeBron James","Mo Bamba"];
    testArray = AnOCR.searchForNames("")
    assert testArray == [];
    testArray = AnOCR.searchForNames(326)
    assert testArray == -1;
    testArray = AnOCR.searchForNames("LeB James rsoafaoshj ouerads S Mo3567 Bamba")
    assert testArray == ["LeBron James","Mo Bamba"];
    