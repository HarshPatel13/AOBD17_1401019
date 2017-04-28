package dataclean;

import java.util.ArrayList;
import java.util.Map;
import org.jblas.DoubleMatrix;
import org.json.JSONObject;


public class Cleandata {
    public static void main(String[] args) 
    {
        clean obj = new clean();
        String path = "CandidateProfileData/";
        
        String data = obj.readFile("single_can.txt");
        JSONObject can = new JSONObject(data);
        
       
        
    }
}
