# import tensorflow
# import ampligraph

# print('tensorflow version: {}'.format(tensorflow.__version__))
# print('ampligraph version: {}'.format(ampligraph.__version__))


from preprocessing.log2dataset import Log2DatasetConverter

# here, need to copy a .labeled file to cwd
# set arg retrieve_size to specify how much data to convert
c = Log2DatasetConverter('conn.log.labeled', retrieve_size=50000)
c.convert()
c.save('output.csv')
