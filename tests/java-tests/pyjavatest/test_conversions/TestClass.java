package pyjavatest.test_conversions;

import pyjavatest.utils.Report;

public class TestClass {

    public TestClass(int a)
    {
        Report.assertEqual(a, 17);
    }

    public int i_()
    {
        return 42;
    }

}
