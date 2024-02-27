package xml.transformer;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class XMLStringReplace {
    public static void main(String[] args) {
        // File path of the XML file
        String filePath = "src/main/java/xml/transformer/sample.xml";

        try {
            // Read XML file as string
            String xmlString = readXMLFile(filePath);

            // Replace a specific value using regex
            String modifiedXMLString = replaceFieldValue(xmlString, "OrgnlUETR", "NewValue");

            // Print the modified XML string
            System.out.println(modifiedXMLString);
        } catch (IOException e) {
            System.err.println("Error reading the XML file: " + e.getMessage());
        }
    }

    // Method to read XML file as string
    private static String readXMLFile(String filePath) throws IOException {
        StringBuilder xmlStringBuilder = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                xmlStringBuilder.append(line).append("\n");
            }
        }
        return xmlStringBuilder.toString();
    }

    // Method to replace field value using regex
    private static String replaceFieldValue(String xmlString, String fieldName, String newValue) {
        // Construct regex pattern to match the field and its value
        String regex = "<" + fieldName + ">(.*?)</" + fieldName + ">";

        // Compile the regex pattern
        Pattern pattern = Pattern.compile(regex);

        // Create a matcher for the input XML string
        Matcher matcher = pattern.matcher(xmlString);

        // Replace the field value with the new value
        return matcher.replaceAll("<" + fieldName + ">" + newValue + "</" + fieldName + ">");
    }
}


