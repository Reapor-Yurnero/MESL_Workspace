import grpc

# import the generated classes
import iptables_manager_pb2_grpc
import iptables_manager_pb2

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = iptables_manager_pb2_grpc.IptablesManagerStub(channel)

# create a chain
cname = iptables_manager_pb2.Cname(container_name="chishi")
res = stub.CreateChain(cname)
print(res)

# delete a chain
cname = iptables_manager_pb2.Cname(container_name="chishi")
res = stub.DeleteChain(cname)
print(res)

# request external access right
# request = iptables_manager_pb2.ExternalAccessRequest(container_name="chishi",container_ip="172.0.25.2",protocol="tcp",dst_ip="",dst_port="2222")
# res = stub.GrantExternalAccess(request)
# print(res)

# revoke external access right
# request = iptables_manager_pb2.ExternalAccessRequest(container_name="chishi",container_ip="172.0.25.2",protocol="tcp",dst_ip="",dst_port="2222")
# res = stub.RevokeExternalAccess(request)
# print(res)

# request host access right
# request = iptables_manager_pb2.HostAccessRequest(container_name="chishi",container_ip="172.0.25.2",protocol="tcp",dst_port="2222")
# res = stub.GrantHostAccess(request)
# print(res)

# revoke host access right
# request = iptables_manager_pb2.HostAccessRequest(container_name="chishi",container_ip="172.0.25.2",protocol="tcp",dst_port="2222")
# res = stub.RevokeHostAccess(request)
# print(res)

# flush chain
# cname = iptables_manager_pb2.RevokeAllRequest(container_name="chishi")
# res = stub.RevokeAllAccess(cname)
# print(res)