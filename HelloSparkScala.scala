package com.rab.dataproc

import org.apache.spark.{SparkConf,SparkContext}

object HelloSparkScala {

  val conf = new SparkConf().setAppName("HelloSparkScala")
  val sc =  new SparkContext(conf)

  def main(args: Array[String]): Unit = {
    val wrdd = sc.parallelize(Seq("Hello", "Spark", "Scala", "Python", "Java"))
    wrdd.collect().foreach(f => println(f))
  }

}

