import tensorflow as tf

tf.strings.regex_replace(
    'abcd',
    'abc',
    'g',
    replace_global=True,
    name=None
)
sess = tf.compat.v1.Session()



def _initialize_session_variables():
    sess.run(tf.group(
        tf.compat.v1.global_variables_initializer(),
        tf.compat.v1.local_variables_initializer(),
        tf.compat.v1.tables_initializer()))




finename = 'abcdCWE-119'
s = tf.strings.regex_replace(
    'abcdCWE-119',
    'CWE-119',
    '1',
    replace_global=True,
    name=None
)

subs = tf.strings.substr(
    'abcdCWE-119',
    len(finename)-7,
    7,
    unit='BYTE',
    name=None
)


s1 = tf.strings.regex_replace(
    subs,
    'CWE-119',
    '3',
    replace_global=True,
    name=None
)


keys_tensor = tf.constant(['CWE119', 'CWE399'])
vals_tensor = tf.constant([0, 1])
input_tensor = tf.constant(['CWE399','CWE119', 'CWE399','CWE119', 'CWE399','CWE119', 'CWE399','CWE119', 'CWE399'])
table = tf.lookup.StaticHashTable(
    tf.lookup.KeyValueTensorInitializer(keys_tensor, vals_tensor), -1)
tabl = table.lookup(input_tensor)
input = tf.constant([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


d = tf.constant([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
e = d[:, :-2]
output = input[0, :]
#se = tf.strings.split('hello world')
se1 = tf.compat.v2.strings.split('hello|world|d|g|gd|re',sep='|',maxsplit=-1)
se2 = tf.shape(se1)[0]
last = se1[se2]
_initialize_session_variables()
e_ = sess.run(e)
h___0 = sess.run(se1)
#las = h___0[6]
s = sess.run(s)
s1 = sess.run(s1)
sub = sess.run(subs)
shape = sess.run(se2)
table = sess.run(tabl)

output_ = sess.run(input[0])
las_ = sess.run(se1[-1])
#las = sess.run(last)
digits = tf.ragged.constant([[3, 1, 4, 1], [], [5, 9, 2], [6], []])
words = tf.ragged.constant([["So", "long"], ["thanks", "for", "all", "the", "fish"]])
print(tf.add(digits, 3))
print(tf.reduce_mean(digits, axis=1))
print(tf.concat([digits, [[5, 3]]], axis=0))
print(tf.tile(digits, [1, 2]))
print(tf.strings.substr(words, 2, -2))

s___= sess.run()

print('adffd',s)
print('adffd',s1)
print('adffd',sub)
