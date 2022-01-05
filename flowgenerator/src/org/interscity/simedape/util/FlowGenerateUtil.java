package org.interscity.simedape.util;

import static java.lang.Integer.parseInt;
import static java.lang.Long.parseLong;
import static java.time.LocalDateTime.now;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.interscity.simedape.model.TupleCountTime;

public class FlowGenerateUtil {
	
	private static Map<Long, List<TupleCountTime>> accessPerTime = new HashMap<>();
	public static String outputFolder = "events-movment-wally-fixed";
	private static final Integer ENTERED_LINK = 1;
	private static final Integer LEFT_LINK = 2;
	
	
	public static void generate(File file, String delimiter, Boolean header) throws IOException {
		System.out.println("Reading number of lines...");
		Long numberOfLines = FileManager.countLineNumberReader(file);
		System.out.println("Number of lines readed!");
		BufferedReader csvReader = new BufferedReader(new FileReader(file));
		String row = null;
		if (!header) {
			row = csvReader.readLine();
		}
		System.out.println("Start process...");
		Long countLines = 1L;
		while ((row = csvReader.readLine()) != null) {
				String[] line = row.split(delimiter);
				if (line[1].equals("entered link") || line[1].equals("left link")) {
					List<TupleCountTime> counts = accessPerTime.get(parseLong(line[3]));
					Integer indecrement = (line[1].equals("entered link")) ? 1 : -1;
					if (counts == null) {
						counts = new ArrayList<>();
						counts.add(new TupleCountTime(indecrement, parseInt(line[0]), line[2], ENTERED_LINK));
					} else {
						try {
							Integer count = counts.get(counts.size() - 1).getCount() + indecrement;
							TupleCountTime tupleCountTime = counts.get(counts.size() - 1);
							if (parseInt(line[0]) == tupleCountTime.getTime()) {
								tupleCountTime.setCount(count);
							} else {
								counts.add(new TupleCountTime(count, parseInt(line[0]), line[2], LEFT_LINK));
							}	
						} catch (IndexOutOfBoundsException e) {
							System.out.println(counts);
							System.out.println(line[1]+" "+line[2]+" "+line[3]);
							break;
						}
					}
					accessPerTime.put(parseLong(line[3]), counts);
				}
				if (countLines % 1000000 == 0) {
					System.out.println("Salving...");
					save(file, delimiter, header);
					System.out.println("Salve!");
				}
				countLines++;
				System.out.print("\033[H\033[2J");  
				System.out.flush();  
				System.out.println(((countLines.doubleValue() / numberOfLines.doubleValue()) * 100)+"%");
		}
		save(file, delimiter, header);
		csvReader.close();
	}

	public static void save(File file, String delimiter, Boolean header) throws IOException {
		StringBuilder content = new StringBuilder();
		File dir = new File(outputFolder+"/");
		if (!dir.exists()) {
			dir.mkdirs();
		}
		for (Entry<Long, List<TupleCountTime>> entry : accessPerTime.entrySet()) {
			File output = new File(outputFolder+"/"+entry.getKey()+"-flow-access-to-link-per-time.csv");
			if (!output.exists()) {
				content.append("time;vehicle;count\n");
			}
			for (Integer i = 0;i < entry.getValue().size() - 1;i++) {
				TupleCountTime count = entry.getValue().get(i);
				content.append(count.getTime())
				.append(";")
				.append(count.getVehicle())
				.append(";")
				.append(count.getCount()) 
				.append("\n");
			}
			if (!entry.getValue().isEmpty()) {
				if (!output.exists()) {
					FileManager.writer(output, content.toString());
				} else {
					FileManager.append(output, content);
				}
				TupleCountTime count = entry.getValue().get(entry.getValue().size() - 1);
				count = new TupleCountTime(count.getCount(), count.getTime(), count.getVehicle(), count.getEvent());
				entry.getValue().clear();
				entry.getValue().add(count);
			}
			content = new StringBuilder();
		}
		
	}
	
	public static void generateVehicleFlowId(File file, String delimiter, Boolean header) throws IOException {
		StringBuilder content = new StringBuilder();
		String folder = outputFolder;
		File dir = new File("output/reports/"+folder+"/");
		if (!dir.exists()) {
			dir.mkdirs();
		}
		for (Entry<Long, List<TupleCountTime>> entry : accessPerTime.entrySet()) {
			content.append("time;vehicle;event\n");
			for (TupleCountTime count : entry.getValue()) {
				content.append(count.getTime())
				.append(";")
				.append(count.getVehicle())
				.append(";")
				.append(count.getEvent())
				.append("\n");
			}			
			entry.getValue().clear();
			FileManager.writer(new File("output/reports/"+folder+"/"+entry.getKey()+"-flow-access-to-link-per-time-"+now()+".csv"), content.toString());
			content = new StringBuilder();
		}
		
	}

}
