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
        String regex = "<" + fieldName + ">(.*?)</" + fieldName + ">";

        // Compile the regex pattern
        Pattern pattern = Pattern.compile(regex);

        // Create a matcher for the input XML string
        Matcher matcher = pattern.matcher(xmlString);

        if (matcher.find()) {
            // Get the matched value
            String matchedValue = matcher.group(1);

            System.out.println("Current matched value = "+matchedValue);

            // Replace the matched value with the new value
            String replacedString = matcher.replaceAll("<" + fieldName + ">" + newValue + "</" + fieldName + ">");

            // Return the replaced string
            return replacedString;
        } else {
            // If no match found, return the original string
            return xmlString;
        }
    }
}


