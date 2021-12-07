import requests,re


def method(line):
    parts = line.split(" ")
    req_method = parts[0].lower()
    req_func = getattr(requests,req_method)
    return req_func


def path(line):
    parts = line.split(" ")
    req_path = parts[1]
    return req_path



def body(lines,body_index):
	return "\n".join(lines[body_index:])



def construct(raw):
    header_regex = r"([\w-]+): (.*)"
    lines = raw.strip().split("\n")
    first_line = lines[0]
    req_func = method(first_line)             				          # Ex: req_func = requests.get


    req_path = path(first_line)               				          # Ex: /index.html


    req_headers = {}			      					  # HTTP headers Ex : Host: google.com

    for header in range(1,len(lines)):
        parsed_header = re.search(header_regex,lines[header])			  #
        if parsed_header != None:						  #
                key = parsed_header[1]					          #
                value = parsed_header[2]					  #
                req_headers.update({key:value})				          #	HTTP headers parsing
        else :									  #
                body_index = header+1						  #
                break								  #


    req_domain = req_headers["Host"]						  # 	Target domain



    req_data = None								  #
    if req_func != requests.get :						  #	Request body
        req_data = body(lines,body_index)					  #


    # print(req_func)								  #
    # print(req_path)								  #
    # print(req_headers)							  #	Debug prints for request components
    # print(req_data)								  #
    # print(req_domain)								  #

    return {"method":req_func,"domain":req_domain,"path":req_path,"headers":req_headers,"data":req_data}



def send(raw,secure=False):
    protocol = "http://"
    if secure :
        protocol == "https://"

    req_object = construct(raw)
    req = req_object["method"]
    req_url = protocol + req_object["domain"] + req_object["path"]
    req_headers = req_object["headers"]
    req_data = req_object["data"]
    return req(req_url, headers=req_headers, data=req_data)



'''
#				USAGE



x = """
POST /test.php?x=sss HTTP/1.1
Host: 192.168.23.128
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 5

y=ggg
"""

print(send(x).text)
'''
