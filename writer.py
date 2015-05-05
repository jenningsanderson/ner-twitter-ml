import csv




def write_final_performance(outfile, to_csv, meta):
	'''
	Write CSV file with performance data for binary learner
	'''
	with open(outfile, 'wb') as csvfile:
	    writer = csv.writer(csvfile, delimiter=',',
	                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
	    
	    writer.writerow( ['Total Words Loaded', meta['limit']] )
	    writer.writerow( ['Outer Iterations', meta['outer_iterations']] )
	    writer.writerow( ['Cross Validation:', meta['iterations']] )
	    writer.writerow( ['Features Used: '] + meta['features'])

	    writer.writerow([])
	    writer.writerow([])

	    for entry in to_csv:
	    	writer.writerow([entry['title']])
	    	writer.writerow(['','precision', 'recall','f1-score','support'])

	    	#Write the Data
	    	for idx, label in enumerate(entry['labels']):
	    		this_row = [label]
	    		for ii in range(4):
	    			this_row.append(entry['data'][ii][idx])
	    		writer.writerow(this_row)
	    	writer.writerow([])
	    	writer.writerow(['Accuracy', entry['accuracy']])
	    	writer.writerow([])
	    	writer.writerow([])
	    