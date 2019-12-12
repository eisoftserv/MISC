#
# handling commmand line arguments
#
def main():
	from sys import argv
	if (len(argv) < 2 or (argv[1] != "i" and argv[1] != "s")):
		print("Use command line argument 'i' for import, or 's' for showing data structures")
		print("In case of importing: book.csv should be nearby import.py!")
		return
	if (argv[1] == "s"):
		my_show()
	else:
		my_import("books.csv")


#
# displaying raw table column and index information
# here I'm using the autocommit feature of "engine.exec"
#
def my_show():
	
	from os import getenv
	from sqlalchemy import create_engine, text

	eng = create_engine(getenv("DATABASE_URL"))
	mytables = ["users", "books", "reviews"]

	for mytable in mytables:
		print(f"----------------------- {mytable} column info")
		mycommand = text("select * from information_schema.columns where table_name = :my;")
		res = eng.execute(mycommand, {"my":mytable})
		for row in res:
		     print(row)
		print(f"----------------------- {mytable} index info")
		mycommand = text("select indexname, indexdef from pg_indexes where tablename = :my;")
		res = eng.execute(mycommand, {"my":mytable})
		for row in res:
		     print(row)

#
# using connection; loading "books.csv" in chunks of 100 rows;
# each chunk is handled in a new transaction (over the same connection)
#
def my_import(myfile):
	
	import csv
	from os import getenv
	from sqlalchemy import create_engine, text

	eng = create_engine(getenv("DATABASE_URL"))
	myconn = eng.connect()

	try:		
		page_rows = 100
		page_row_counter = 0
		total_rows = 0
		last = "-"
	
		with open(myfile) as infile:
			reader = csv.reader(infile, delimiter=",")
			
			for row in reader:		
				total_rows += 1
				last = row[0]
				if total_rows < 2:
					mytran = myconn.begin()	# build new transaction	
					continue
				if page_row_counter < page_rows:
					page_row_counter += 1
				else:
					mytran.commit() # commit current transaction
					mytran = myconn.begin()	# build new transaction
					page_row_counter = 1
					print(f"-- Total rows: {total_rows}")
				mycommand = text("insert into books (isbn, title, author, year) values (:isb, :tit, :aut, :yea);")
				myconn.execute(mycommand, {"isb":row[0], "tit":row[1], "aut":row[2], "yea":row[3]})
			
			if page_row_counter < page_rows:
				print(f"-- Last page length: {page_row_counter}")
			if page_row_counter > 0:
				mytran.commit()	# commit last transaction
			else:
				mytran.rollback() # here we have an empty transaction
			print(f"-- Last code: {last} Total rows: {total_rows}")	
					
	except Exception as exep:
		print("----- Error: ", exep)
	else:
		print("----- no error(s)")
	finally:
		myconn.close()
		print("----- done")



if __name__ == "__main__":
    main()