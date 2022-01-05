package org.interscity.simedape;

import java.io.File;
import java.io.IOException;

import org.interscity.simedape.util.FlowGenerateUtil;

public class Main {
	
	public static void main(String[] args) throws IOException {
		FlowGenerateUtil.outputFolder = args[1];
		FlowGenerateUtil.generate(new File(args[0]), args[2], true);
	}

}
