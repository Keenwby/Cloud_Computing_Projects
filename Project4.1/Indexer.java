package MapReduce_try;

import java.io.IOException;
import java.util.*;

import org.apache.hadoop.conf.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.filecache.DistributedCache;

import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;


public class Indexer {
	public static class Map extends Mapper<LongWritable, Text, Text, Text> {
	    private final static Text word = new Text();
	    private final static Text location = new Text();
	    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
	    	FileSplit fs = (FileSplit) context.getInputSplit();
	    	String name = fs.getPath().getName();
	    	location.set(name);
	        String line = value.toString().replaceAll("[^A-Za-z0-9]", " ");
	        StringTokenizer tokenizer = new StringTokenizer(line.toLowerCase());
	        while (tokenizer.hasMoreTokens()) {
	            word.set(tokenizer.nextToken());
	            context.write(word, location);
	        }
	    }
	 }

 public static class Reduce extends Reducer<Text, Text, Text, Text> {
	 private Text Returntext = new Text();
	 private Set<String> hash = new HashSet<String>();
    public void reduce(Text key, Iterable<Text> values, Context context)
      throws IOException, InterruptedException {
    	String Returnstring = key.toString() + " " + ":";
    	for (Text elem1:values){
    		hash.add(elem1.toString());
    	}
    	for (String elem2:hash){
    		Returnstring += (" " + elem2); 
    	}
    	Returntext.set(Returnstring);
    	context.write(Returntext, null);
    	hash.clear();
    }
 public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = new Job(conf, "Indexer");
    job.setJarByClass(Indexer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);
    
    job.setMapperClass(Map.class);
    job.setReducerClass(Reduce.class);
    
    job.setInputFormatClass(TextInputFormat.class);
    job.setOutputFormatClass(TextOutputFormat.class);
    
    FileInputFormat.addInputPath(job, new Path(args[1]));
    FileOutputFormat.setOutputPath(job, new Path(args[2]));
    
    job.waitForCompletion(true);
 }
 }
}
