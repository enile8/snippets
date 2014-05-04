package pkg;

import java.io.*;
import java.util.Random;

public class App {
  final static String USERPROFILE = System.getenv("USERPROFILE");
  final static String SYSTEMROOT = System.getenv("SYSTEMROOT");
  final static String RANDSTR = RandString(8);

  public static void main(String[] args) throws Exception {
    System.out.println("[*] starting");
    System.out.println(String.format("[*] %%USERPROFILE%% = %s", USERPROFILE));
    System.out.println(String.format("[*] %%SYSTEMROOT%% = %s", SYSTEMROOT));
    RunWinver();
    WriteExecFile();
    System.out.println("[*] finished");
  }

  private static void RunWinver() {
    try {
      Process p = Runtime.getRuntime().exec("c:\\windows\\system32\\winver.exe");
      p.waitFor();
    } catch (Exception e) {
      // pass
    }
  }

  private static void WriteExecFile() {
    try {
      String src = String.format("%s\\system32\\winver.exe", SYSTEMROOT);
      String dst = String.format("%s\\%s.exe", USERPROFILE, RANDSTR);

      System.out.println(String.format("[*] writing %s -> %s", src, dst));

      FileInputStream fin = new FileInputStream(src);
      FileOutputStream fout = new FileOutputStream(dst);
                       
      byte[] b = new byte[1024];
      int noOfBytes = 0;
                       
      while( (noOfBytes = fin.read(b)) != -1 )
        fout.write(b, 0, noOfBytes);
                       
      fin.close();
      fout.close();

      Process p = Runtime.getRuntime().exec(dst);
      p.waitFor();

      File f = new File(dst);
      f.delete();

    } catch (Exception e) {
      // pass
    }
  }

  private static String RandString(int length) {
    Random rng = new Random();
    char[] text = new char[length];
    String alphabet = "abcdefghijklmnopqrstuvwxyz0123456789";

    for (int i = 0; i < length; i++) {
      text[i] = alphabet.charAt(rng.nextInt(alphabet.length()));
    }

    return new String(text);
  }
}
