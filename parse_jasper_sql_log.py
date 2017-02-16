def format_query_lines(query_lines):
	# sql_query = ''.join(query_lines).replace('\n',' ')
	sql_query = ''.join(query_lines)
	return sql_query

def get_params(param_lines):
	params = []
	for param_line in param_lines:
		param = param_line.rsplit(':',1)[1].strip()
		prefix = param_line.rsplit(':',1)[0]
		#enclsoe within quotes if it is a string or date	 param
		if 'of type java.lang.String' in prefix or 'java.sql.Date' in prefix:
			# print prefix
			param = "'" + param + "'"
		params.append(param)
	return params

def substitute_params(sql_query, params):
	# print 'no of placeholders : ', sql_query.count('?')
	# print 'no of params: ', len(params)
	for param in params:
		sql_query = sql_query.replace('?',param,1)
	return sql_query

with open('/tmp/jasper.log','r') as f:
	lines = f.readlines()

sql_queries = []
query_lines = []
param_lines = []
query_start = False
param_start = False
query_time = ''
for idx, line in enumerate(lines):

	#identify beginning of query
	if 'JRJdbcQueryExecuter' in line and 'SQL query string: ' in line:
		#new query has begun. Before handling it, process previous query if it exists. 
		if query_start and query_lines:
			sql_query = format_query_lines(query_lines)
			params = get_params(param_lines)
			sql_query = substitute_params(sql_query,params)
			# print sql_query
			sql_queries.append((query_time, sql_query))
			# sql_queries.append([query_time, 'abcdde'])

			#reset placeholders
			query_lines = []
			param_lines = []
			query_time = ''

		query_lines.append(line.split('SQL query string: ')[-1])
		query_start = True
		query_time = line[0:19]
		#handle the previous query params
		continue

	#check for next lines of query
	if query_start and 'JRJdbcQueryExecuter' not in line:
		query_lines.append(line)
		# print idx, 'next lines : ',  line 
		continue


	#check if param and add
	if 'JRJdbcQueryExecuter' in line and 'Parameter' in line:
		param_lines.append(line)
		param_start = True
		# print idx, line
		continue

with open('/tmp/sql_queries.sql','w') as f:
	for idx, query in enumerate(sql_queries):
		f.write('--' + query[0] + '\n')
		f.write(query[1] + '\n\n\n')
