package pyjavatest;

import java.util.HashMap;


public class ObjFactory {

    private static Object[] objs = new Object[]{
        "lala",
        new HashMap<Integer, Object>()
    };

    public static Object makeObject(int i)
    {
        return objs[i-1];
    }

}
