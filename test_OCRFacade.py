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
    

def test_findNextStartIndex():
    AnOCR = OCR();
    testIndex = AnOCR.findNextStartIndex("John Smith-Brown ghi ",0)
    assert testIndex == 5;