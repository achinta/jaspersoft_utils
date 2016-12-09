### Purpose
If you developed reports using Jaspersoft Studio and deployed the reports, how to get SQL queries fired at run time (along with parameters)? We can enable SQL logging by changing the following parameters in log4j.properties. 

*log4j.logger.net.sf.jasperreports.engine.query.JRJdbcQueryExecuter=debug*

But the log file does not give the exact query. Parameters are written in separate lines after the query. If your query contains a lot of parameters, it becomes very difficult to re-constrcut the original query. The purpose of the parser is to extract the SQL query from the log files. 

### How to use it?



