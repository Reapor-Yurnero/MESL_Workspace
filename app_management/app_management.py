import subprocess
from shlex import split


def register_app(app_name:str, ver:str, src_dir:str, start_cmd:str, build_env:str, port:int or None = None, build_cmd:str = '') -> None:
	"""
	Register an new app or update an existing app as runnable docker images.

	Parameters
	----------
	app_name
		desired name of the application
	ver
		version number, could be a regular version number string or 'latest'
	src_dir
		source code directory location
	start_cmd
		starting command as the entry point for the docker
	build_env
		desired building environment i.e. parent docker image)
	port: optional
		port number to be exposed
	build_cmd: optional
		the command used prebuilding to setup the env

	Returns
	-------
	None

	Examples
	--------
	>>> register_app("webapp", "latest", "./hello_world_web","python index.py", "python:3", 5000)

	"""
	# type check
	if not isinstance(app_name, str):
		raise TypeError("app name is expected to be str")
	if not isinstance(ver, str):
		raise TypeError("version number is expected to be str")
	if not isinstance(src_dir, str):
		raise TypeError("source directory is expected to be str")
	if not isinstance(build_cmd, str):
		raise TypeError("building command is expected to be str")
	if not isinstance(start_cmd, str):
		raise TypeError("starting command is expected to be str")
	if not isinstance(build_env, str):
		raise TypeError("building environment is expected to be str")
	if not isinstance(port, int):
		raise TypeError("port is expected to be int")

	# generate corresponding Dockerfile in the root directory of the source code
	with open(src_dir+"/Dockerfile", 'w') as f:
		contents = [
			"FROM "+build_env+"\n",
			"COPY . /"+app_name+"\n",
			"WORKDIR /"+app_name+"\n",
		]
		if build_cmd is not '':
			contents += ["RUN "+build_cmd+"\n"]
		if port is not None:
			contents += ["EXPOSE "+str(port)+"\n"]
		contents += [parse_start_cmd(start_cmd)]
		f.writelines(contents)

	# build the docker image
	subprocess.run(["docker", "build", src_dir, "-t", app_name+":"+ver])


def parse_start_cmd(start_cmd:str) -> str:
	"""a helper function to parse a str command into ENTRYPOINT[List[str]] format"""
	l = split(start_cmd)
	return 'ENTRYPOINT [' + ", ".join('"'+x+'"' for x in l) + ']'


def spawn_app(app_name:str, user_id:str, arguments:str = '') -> str:
	"""
	Run the target application docker image under specific user with given arguments for that application

	Parameters
	----------
	app_name
		the application name, same as the one used to register
	user_id
		the identification of the user who's using the app
	arguments: List[str], optional
		arguments for the application

	Returns
	-------
	str
		The name of the container which accommodates the spawned app

	Examples
	--------
	>>> print(spawn_app("toy_web", "3", "--port 5555"))
	toy_web3

	"""
	# return run_container(app_name+user_id, app_name, ["-it", "-m", "64MB", "--network", "isolated_nw", "--rm"], arguments)

	# type check
	if not isinstance(app_name, str):
		raise TypeError("app name is expected to be str")
	if not isinstance(user_id, str):
		raise TypeError("user id is expected to be str")
	if not isinstance(arguments, str):
		raise TypeError("arguments is expected to be str")

	# default parameter, could be modified to kwargs in the future for more flexible settings
	parameters = ["-d", "-m", "64MB", "--network", "isolated_nw", "--rm"]
	# container naming is subject to changes
	container_name = app_name+"-"+user_id
	# parse the arguments to List(str)
	arguments = split(arguments)
	# run the docker image in container
	subprocess.run(["docker", "run"]+parameters+["--name", container_name, app_name]+arguments)
	return container_name


#def run_container(container_name:str, image_name:str, parameters:List[str]=None, arguments:List[str]=None) -> str:
#	"""helper function for spawn_app"""
	# subprocess.run(["docker", "ps"])
	# docker run -p 9999:9999 -it --rm --name client_remote client_to_remote python ./client.py 172.17.0.1 2222


def stop_container(container_name:str) -> None:
	"""
	stop the container with the name
	Note when --rm is included in parameters for run, this container will be removed after it's stopped.

	Parameters
	----------
	container_name
		name of the container, returned by spawn_app

	Returns
	-------
	None

	"""
	if not isinstance(container_name, str):
		raise TypeError("container name is expected to be str")
	subprocess.run(["docker", "stop", container_name])


def start_container(container_name:str) -> None:
	"""
	start the container with the name

	Parameters
	----------
	container_name
		name of the container, returned by spawn_app

	Returns
	-------
	None

	"""
	if not isinstance(container_name, str):
		raise TypeError("container name is expected to be str")
	subprocess.run(["docker", "start", container_name])


def rm_container(container_name:str) -> None:
	"""force remove the container with the name"""
	if not isinstance(container_name, str):
		print("Container Name is Expected to be Str")
		return
	subprocess.run(["docker", "rm", "--force", container_name])


def get_container_ip(container_name:str) -> str:
	"""
	Get container ip address based on its name

	Parameters
	----------
	container_name
		name of the container, returned by spawn_app

	Returns
	-------
	str
		the ip address in str

	"""
	rt = subprocess.run(split("docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "+
							  container_name),stdout=subprocess.PIPE)
	return rt.stdout.decode("UTF-8")[:-1]
