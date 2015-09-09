package NGram;
import java.io.IOException;
//import java.util.*;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

public class Ngram {
		public static class Ngram_map extends Mapper<LongWritable, Text, Text, IntWritable> {
		    private Text output = new Text();
		    private static final IntWritable one = new IntWritable(1);
		    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
		    	String line = value.toString();
		    	line = line.trim().replaceAll("[^A-Za-z]", " ").toLowerCase().replaceAll(" +", " ");
		        String[] word = line.split(" ");
		        StringBuilder phrase = new StringBuilder();
		        for (int stpoint = 0; stpoint < word.length; stpoint++){
		        	for (int n = 0; n < 5 && n + stpoint < word.length; n++){
		        		phrase = phrase.append(word[stpoint + n]);
		        		if (n != 4){
		        			phrase = phrase.append(" ");
		        		}
		        		output.set(phrase.toString().trim());
		        		context.write(output,one);
		        	}
		        	phrase.delete(0, phrase.length());
		        }
		    }
		 }

	 public static class Ngram_red extends Reducer<Text, IntWritable, Text, IntWritable> {
		 
	    public void reduce(Text key, Iterable<IntWritable> values, Context context)
	      throws IOException, InterruptedException {
	    	int num = 0;
	    	for (IntWritable n: values){
	    		num += n.get();
	    	}
	    	context.write(key, new IntWritable(num));
	    }
	 public static void main(String[] args) throws Exception {
	    Configuration conf = new Configuration();
	    Job job = new Job(conf, "Ngram");
	    job.setJarByClass(Ngram.class);
	    job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(IntWritable.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);
	    
	    job.setMapperClass(Ngram_map.class);
	    job.setCombinerClass(Ngram_red.class);
	    job.setReducerClass(Ngram_red.class);
	    
	    job.setInputFormatClass(TextInputFormat.class);
	    job.setOutputFormatClass(TextOutputFormat.class);
	    
	    FileInputFormat.addInputPath(job, new Path(args[1]));
	    FileOutputFormat.setOutputPath(job, new Path(args[2]));
	    
	    job.waitForCompletion(true);
	 }
	 }
	}
