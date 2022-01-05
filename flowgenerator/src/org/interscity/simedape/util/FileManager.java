package org.interscity.simedape.util;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.LineNumberReader;
import java.io.OutputStream;

public class FileManager {
	
	public static void create(File file, String content) throws IOException {		  
		if (file.createNewFile()) {
		    System.out.println("File is created: "+file.getName());
		} else {
			file.delete();
			file.createNewFile();
		    System.out.println("File already exists.");
		}
		FileWriter writer = new FileWriter(file);
		writer.write(content);
		writer.close();
	}
	
	public static void writer(File file, String data) {
        FileWriter fileWriter = null;
        try {
        	if (!file.exists()) {
        		file.createNewFile();
        	}
        	fileWriter = new FileWriter(file);
        	fileWriter.write(data);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
            	fileWriter.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
	
	public static void copy(File source, File dest) throws IOException {
	    InputStream is = null;
	    OutputStream os = null;
	    try {
	        is = new FileInputStream(source);
	        os = new FileOutputStream(dest);
	        byte[] buffer = new byte[1024];
	        int length;
	        while ((length = is.read(buffer)) > 0) {
	            os.write(buffer, 0, length);
	        }
	    } finally {
	        is.close();
	        os.close();
	    }
	}
	
	public static String reader(File file) throws IOException {
		BufferedReader fileReader = new BufferedReader(new FileReader(file));
		String row = null;
		StringBuilder content = new StringBuilder();
		while ((row = fileReader.readLine()) != null) {
			content.append(row).append("\n");
		}
		fileReader.close();
		return content.toString();
	}
	
	public static synchronized void append(File file, StringBuilder content) throws IOException {    
	    BufferedWriter writer = new BufferedWriter(
	                                new FileWriter(file, true)
	                            );  
	    writer.newLine();
	    writer.write(content.toString());
	    writer.close();
	}
	
	public static Long countLineNumberReader(File file) {
		Long lines = 0L;
		try (LineNumberReader lnr = new LineNumberReader(new FileReader(file))) {
			while (lnr.readLine() != null)
				;
			lines = (long) lnr.getLineNumber();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return lines;
	}

}
