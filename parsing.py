import collections
import re
class parser():
	def open_file(self, src):
		log = open(src, 'r').read() 
		user_list = re.findall(r'user\w+', log)
		result = collections.Counter(user_list).most_common()
		t=[]
		for key, value in result:
			t.append({'user': key, 'commit': value})
		for elem in t:
			print('user: ' + elem['user'] + ' - ' + 'commit: ' + str(elem['commit']) )
if __name__ == "__main__":
	parser1=parser()
	src = raw_input('Vvedite pyt: ')
	parser1.open_file(src);
