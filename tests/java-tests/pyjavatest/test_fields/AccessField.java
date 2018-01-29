package pyjavatest.test_fields;

import pyjavatest.utils.Report;


public class AccessField {

    public static int a = 7;
    public static Object b = "test";
    public static String c = null;

    public short d = -7;
    public Object e = null;
    public String f = "4";

    public void test()
    {
        Report.assertEqual(a, 42);
        Report.assertEqual(b, null);
        Report.assertEqual(c, "Hello");
        Report.assertEqual(d, -42);
        Report.assertEqual(e, this);
        Report.assertEqual(f, "Rémi");
    }

}
