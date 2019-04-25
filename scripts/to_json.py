import scripts.fetch_util as fet
import json


test=fet.fetch_util_main()
#{'name' : 10 , 'surname' : 20}
j=json.dumps(test)
print(j)