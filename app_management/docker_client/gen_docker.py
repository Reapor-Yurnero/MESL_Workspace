import subprocess

def run_docker(container_name,image_name,parameters=None,arguments=None):
	# subprocess.run(["docker", "ps"])
	# docker run -p 9999:9999 -it --rm --name client_remote client_to_remote python ./client.py 172.17.0.1 2222
	if not isinstance(container_name, str) or not isinstance(image_name, str):
		print("Container/Image Name Invalid (Expected to be Str)")
		return
	if parameters == None:
		parameters = []
	elif not (isinstance(parameters,list) and all(isinstance(x,str) for x in parameters)):
		print("Parameters is Expected to be a List of Str")
		return
	if arguments == None:
		arguments = []
	elif not (isinstance(arguments,list) and all(isinstance(x,str) for x in arguments)):
		print("Arguments is Expected to be a List of Str")
		return
	subprocess.run(["docker","run"]+parameters+["--name",container_name,image_name]+arguments)
	#subprocess.run(["docker", "run", "-p", "9999:9999", "-it", "--rm", "-d", "--name", "client1", "client", "python", "./client.py", "172.17.0.1", "2222"])

if __name__ == "__main__":
	run_docker("client1", "client", ["-p", "9999:9999", "-it", "--rm"], ["172.17.0.1", "2222"])
