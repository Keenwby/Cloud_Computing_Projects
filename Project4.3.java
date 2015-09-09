package baiyangw;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator; 

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable; 
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.hbase.mapreduce.TableReducer;
import org.apache.hadoop.hbase.util.Bytes;

public class Lanmdl {
	public static Configuration conf = HBaseConfiguration.create();
	public static class Mappers extends Mapper<LongWritable, Text, Text, Text>{
		private Text outputphrase = new Text();
		private Text outputword = new Text();
		private int t = 2;
		
		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException{
			String line = value.toString();
			String [] str = line.split("\t");
			int num =  Integer.parseInt(str[1]);
			String [] wd = str[0].split(" ");
			if (wd.length == 1)	return;
			if (num < t) return;
			String phrase = "";
			String word = "";
			for (int i=0; i<wd.length-1;i++)
			{
				phrase += wd[i] + " ";
			}
			word = wd[wd.length-1] + " " + num;
			outputphrase.set(phrase.trim());
			outputword.set(word);
			context.write(outputphrase, outputword);
				}
			}
	public static class Reduce extends TableReducer<Text, Text, ImmutableBytesWritable>{
		private int N = 5;
		public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException{
		Map<String, Integer> rank = new HashMap<String, Integer>();
		Put put = new Put(Bytes.toBytes(key.toString()));
		for (Text val : values){
			String line = val.toString();
			String[] str = line.split(" ");
			String word = str[0];
			int num = Integer.parseInt(str[1]);
			rank.put(word, num);
			}
		
		List<Map.Entry<String, Integer>> sorted_rank = new ArrayList<Map.Entry<String, Integer>>(rank.entrySet());
			Collections.sort(sorted_rank, new Comparator<Map.Entry<String, Integer>>() {   
		    public int compare(Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2) {      
		    	return (o2.getValue() - o1.getValue());
		    }
		});
			
		int size = Math.min(N, sorted_rank.size());
		for (int i=0; i<size;i++){
			int r = i + 1;
			put.add(Bytes.toBytes("family"), Bytes.toBytes(sorted_rank.get(i).getKey()), Bytes.toBytes("Rank " + r));
		}
		context.write(new ImmutableBytesWritable(key.getBytes()), put);
		}
	}
	public static void main(String[] args) throws Exception{
		Configuration conf = new Configuration();
		Job job = new Job(conf, "Project43");
		job.setJarByClass(Lanmdl.class);	
		job.setInputFormatClass(TextInputFormat.class);
		job.setMapperClass(Mappers.class);
		job.setReducerClass(Reduce.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		TableMapReduceUtil.initTableReducerJob("Lanmdl", Reduce.class, job);
		TableMapReduceUtil.addDependencyJars(job);
		FileInputFormat.addInputPath(job, new Path(args[1]));
		//FileOutputFormat.setOutputPath(job, new Path(args[2]));
		conf.set("t", args[2]);
	    conf.set("N", args[3]);

		job.waitForCompletion(true);
	}
}