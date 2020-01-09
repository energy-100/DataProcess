import bioread

data = bioread.read('A01-T2-2.acq')
print(data)
print(data.graph_header)
print(data.channel_headers)
print(data.foreign_header)
print(data.channel_dtype_headers)
print(data.samples_per_second)
