import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Enumeration;
import java.util.zip.ZipEntry;

import org.apache.tika.exception.TikaException;
import org.apache.tika.langdetect.OptimaizeLangDetector;
import org.apache.tika.language.detect.LanguageResult;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.mime.MediaType;
import org.apache.tika.mime.MimeTypes;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.sax.BodyContentHandler;
import org.xml.sax.SAXException;

public class Exercise2
{

    private static final String DATE_FORMAT = "yyyy-MM-dd";
    private OptimaizeLangDetector langDetector;

    public static void main(String[] args) throws ParseException
    {
        Exercise2 exercise = new Exercise2();
        exercise.run();
    }

    private void run() throws ParseException
    {
        try
        {
            if (!new File("./outputDocuments").exists())
            {
                Files.createDirectory(Paths.get("./outputDocuments"));
            }

            initLangDetector();

            File directory = new File("./documents");
            File[] files = directory.listFiles();
            for (File file : files)
            {
                processFile(file);
            }
        } catch (IOException | SAXException | TikaException e)
        {
            e.printStackTrace();
        }

    }

    private void initLangDetector() throws IOException
    {
        // loading languages and creating detector
    	langDetector=new OptimaizeLangDetector();
    	langDetector.loadModels();
    }

    private void processFile(File file) throws IOException, SAXException, TikaException, ParseException
    {
    	DateFormat df = new SimpleDateFormat("yyyy-mm-ddhh:mm:ss");
    	Date dlsave=null, dcreat=null;
    	String creato=null;
    	//Just Parsing
    	InputStream stream=new FileInputStream(file);
        AutoDetectParser parser=new AutoDetectParser();
        Metadata meth=new Metadata();
        BodyContentHandler handle = new BodyContentHandler(-1);
        parser.parse(stream, handle, meth);
        
        //Extracting metadata
        String[] metadataNames=meth.names();
        for(String name : metadataNames) {		        
            System.out.println(name + ": " + meth.get(name));
            if (name=="Creation-Date" || name=="meta:creation-date" || name=="dcterms:created") dcreat=df.parse(meth.get(name).substring(0, 10)+meth.get(name).substring(11, 19));
            if (name=="Last-Save-Date" || name=="Last-Modified" || name=="meta:save-date") 		dlsave=df.parse(meth.get(name).substring(0, 10)+meth.get(name).substring(11, 19));
            if (name=="creator" || name=="meta:author" || name=="Author") 						creato=meth.get(name);
         }
        //Language, mime type extraction
        LanguageResult reslang=langDetector.detect(handle.toString());
        MimeTypes mt=new MimeTypes();
        InputStream bufferedIn = new BufferedInputStream(stream);
        MediaType mime=mt.detect(bufferedIn, meth);
        saveResult(file.getName(), reslang.getLanguage(), creato, dcreat, dlsave, mime.toString(), handle.toString()); //TODO: fill with proper values
    }

    private void saveResult(String fileName, String language, String creatorName, Date creationDate,
                            Date lastModification, String mimeType, String content)
    {
    	System.out.println("##############################################");
    	System.out.println(fileName);
    	System.out.println(language);
    	System.out.println(creatorName);
    	System.out.println(creationDate);
		System.out.println(lastModification);
		System.out.println(mimeType);
		System.out.println("##############################################");

        SimpleDateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT);
        int index = fileName.lastIndexOf(".");
        String outName = fileName.substring(0, index) + ".txt";
        try
        {
            PrintWriter printWriter = new PrintWriter("./outputDocuments/" + outName);
            printWriter.write("Name: " + fileName + "\n");
            printWriter.write("Language: " + (language != null ? language : "") + "\n");
            printWriter.write("Creator: " + (creatorName != null ? creatorName : "") + "\n");
            String creationDateStr = creationDate == null ? "" : dateFormat.format(creationDate);
            printWriter.write("Creation date: " + creationDateStr + "\n");
            String lastModificationStr = lastModification == null ? "" : dateFormat.format(lastModification);
            printWriter.write("Last modification: " + lastModificationStr + "\n");
            printWriter.write("MIME type: " + (mimeType != null ? mimeType : "") + "\n");
            printWriter.write("\n");
            printWriter.write(content + "\n");
            printWriter.close();
        } catch (FileNotFoundException e)
        {
            e.printStackTrace();
        }
    }

}
