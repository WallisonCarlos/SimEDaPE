package org.interscity.simedape.util;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class FileManagerCsv {

	public static List<String[]> reader(File file, String delimiter, Boolean header) throws IOException {
		BufferedReader csvReader = new BufferedReader(new FileReader(file));
		List<String[]> fileReaded = new ArrayList<>();
		String row = null;
		if (!header) {
			row = csvReader.readLine();
		}
		while ((row = csvReader.readLine()) != null) {
			String[] line = row.split(delimiter);
			fileReaded.add(line);
		}
		csvReader.close();
		return fileReaded;
	}
	
	public static void split(File file, Boolean header, String outputPrefix, Integer sizeParts) throws IOException {
		BufferedReader csvReader = new BufferedReader(new FileReader(file));
		StringBuilder content = new StringBuilder();
		String row = null;
		if (!header) {
			row = csvReader.readLine();
		}
		Long totalLines = FileManager.countLineNumberReader(file);
		Integer i = 0;
		Integer j = 0;
		while (i < totalLines && csvReader.readLine() != null) {
			while ((row = csvReader.readLine()) != null) {
				content.append(row).append("\n");
				j++;
				if (j >= sizeParts || j == totalLines - i) {
					FileManager.create(new File("output/split_csv/"+outputPrefix+"_"+i+"-"+(i + sizeParts)+".csv"), content.toString());
					j = 0;
					i += sizeParts;
					content = new StringBuilder();
				}
			}
		}
		csvReader.close();
	}
	
	
	
}
