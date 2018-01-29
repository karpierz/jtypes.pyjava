package pyjavatest.utils;

public class Report {

    private static String hex(String s)
    {
        StringBuilder ret = new StringBuilder();
        for(int i = 0; i < s.length(); ++i)
        {
            ret.append(Integer.toString(s.charAt(i), 16));
            if(i+1 < s.length())
                ret.append(' ');
        }

        return ret.toString();
    }

    private static String format(Object o)
    {
        if(o == null)
            return "null";
        else if(o instanceof String)
            return String.format("'%s' [%s] (String)",
                    o, hex((String)o));
        else
            return String.format("'%s' (%s) != '%s' (%s)",
                    o.toString(), o.getClass().getName());
    }

    private static void fail(String msg)
    {
        System.err.println("assert failed in Java code: " + msg);
        (new Throwable()).printStackTrace(System.err);
        System.err.println("Terminating process...");
        System.exit(1);
    }

    public static void assertEqual(Object a, Object b)
    {
        if( (b == null && a != null) || (b != null && !b.equals(a)) )
            fail(format(a) + " != " + format(b));
    }

    public static void assertAlmostEqualF(float a, float b)
    {
        if(Math.abs(a-b) > 0.001f)
            fail(String.format("%f !~= %f", a, b));
    }

    public static void assertAlmostEqualD(double a, double b)
    {
        if(Math.abs(a-b) > 0.001f)
            fail(String.format("%f !~= %f", a, b));
    }

}
