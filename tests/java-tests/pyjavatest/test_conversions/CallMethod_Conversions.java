package pyjavatest.test_conversions;

import pyjavatest.utils.Report;


public class CallMethod_Conversions {

    private static Child __object = new Child();

    public void v_ii(int a, int b)
    {
        Report.assertEqual(a, 12);
        Report.assertEqual(b, -5);
    }

    public int i_fc(float a, char b)
    {
        Report.assertAlmostEqualF(a, 12.5f);
        Report.assertEqual(b, 'א'); /* non-ascii for added fun */
        return -7;
    }

    public static boolean _b_Bs(byte a, short b)
    {
        Report.assertEqual(a, (byte)0x42);
        Report.assertEqual(b, (short)13042);
        return false;
    }

    public char c_lS(long a, String b)
    {
        Report.assertEqual(a, -70458L);
        Report.assertEqual(b, "Rémi");
        return 'א'; /* non-ascii */
    }

    public double d_iSb(int a, String b, boolean c)
    {
        Report.assertEqual(a, 0);
        Report.assertEqual(b, "");
        Report.assertEqual(c, true);
        return 197.9986e17;
    }

    public static float _f_()
    {
        return -0.07f;
    }

    public String S_()
    {
        return "éê\0è"; /* embedded zero -- it's a trap! */
    }

    public Object o_b(boolean a)
    {
        Report.assertEqual(a, false);
        return __object;
    }

    public byte B_loi(long a, Parent b, int c)
    {
        Report.assertEqual(a, 142005L);
        Report.assertEqual(b, __object);
        Report.assertEqual(c, -100);
        return 0x20;
    }

    public static short _s_So(String a, Child b)
    {
        Report.assertEqual(a, "\0┬──┬");
        Report.assertEqual(b, __object);
        return -15;
    }

    public static Object _o_S(String a)
    {
        Report.assertEqual(a, null);
        return null;
    }

    public void v_o(String a)
    {
        Report.assertEqual(a, null);
    }

    public static Class<?> _C_()
    {
        return TestClass.class;
    }

}
