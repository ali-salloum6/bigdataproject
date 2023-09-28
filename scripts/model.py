from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression, RandomForestRegressor
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.evaluation import RegressionEvaluator

spark = SparkSession.builder\
        .appName("BigData Project")\
        .config("spark.sql.catalogImplementation","hive")\
        .config("hive.metastore.uris", "thrift://sandbox-hdp.hortonworks.com:9083")\
        .config("spark.sql.avro.compression.codec", "snappy")\
        .enableHiveSupport()\
        .getOrCreate()

sc = spark.sparkContext
sc.setLogLevel('WARN')

comments = spark.read.format("avro").table('projectbigdata.comments')
comments.createOrReplaceTempView('comments')

course = spark.read.format("avro").table('projectbigdata.course')
course.createOrReplaceTempView('course')

comments_df = spark.read.table("comments")
course_df = spark.read.table("course")

feature_cols = ["subscriber", "rating", "num_reviews", "num_comments", "num_lecture"]
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
course_df = assembler.transform(course_df)

(training_data, testing_data) = course_df.randomSplit([0.7, 0.3], seed=2021)

lr = LinearRegression(featuresCol="features", labelCol="price")

param_grid_lr = ParamGridBuilder() \
    .addGrid(lr.maxIter, [5, 10, 20]) \
    .addGrid(lr.regParam, [1.0, 0.1, 0.01]) \
    .build()

crossval_lr = CrossValidator(estimator=lr, estimatorParamMaps=param_grid_lr, evaluator=RegressionEvaluator(labelCol="price", predictionCol="prediction", metricName="rmse"), numFolds=4)

print("Start training of Linear Regression")
cv_model_lr = crossval_lr.fit(training_data)

results = []
for par, metric in zip(param_grid_lr, cv_model_lr.avgMetrics):
    step = {
        'Param': str(par),
        'Mean RMSE': str(metric)
    }
    print("Param:", par, "\n", "Mean RMSE:", metric)
    results.append(step)

results_df = spark.createDataFrame(results)

results_df.coalesce(1).write.mode("overwrite").format("csv").option("sep", ",").option("header","true").csv("output/q6.csv")

best_model_lr = cv_model_lr.bestModel

print("Start testing of Linear Regression")
predictions_lr = best_model_lr.transform(testing_data)

evaluator = RegressionEvaluator(labelCol="price", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions_lr)
print("RMSE: %.3f" % rmse)
best_model_lr.write().overwrite().save('models/best_model_lr.model')

rf = RandomForestRegressor(featuresCol="features", labelCol="price")

param_grid = ParamGridBuilder() \
    .addGrid(rf.maxDepth, [5, 10, 20]) \
    .addGrid(rf.numTrees, [5, 10, 20]) \
    .build()

crossval = CrossValidator(estimator=rf, estimatorParamMaps=param_grid, evaluator=RegressionEvaluator(labelCol="price", predictionCol="prediction", metricName="rmse"), numFolds=4)

print("Start training of Random Forest")
cv_model = crossval.fit(training_data)

results_rf = []
print("Result:")
for par, metric in zip(param_grid, cv_model.avgMetrics):
    step = {
        'Param': str(par),
        'Mean RMSE': str(metric)
    }
    print("Param:", par, "\n", "Mean RMSE:", metric)
    results_rf.append(step)

results_rf_df = spark.createDataFrame(results_rf)

results_rf_df.coalesce(1).write.mode("overwrite").format("csv").option("sep", ",").option("header","true").csv("output/q7.csv")

best_model = cv_model.bestModel

print("Start testing of RandomForestRegressor")
predictions = best_model.transform(testing_data)

evaluator = RegressionEvaluator(labelCol="price", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions)
print("RMSE: %.3f" % rmse)

best_model.write().overwrite().save('models/best_model_rf.model')

