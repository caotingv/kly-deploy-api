import json

from common import types
from deploy.recommend_config import ReckRecommendConfigCommon, ShowRecommendConfig
from models.deploy_history import DeployHistoryModel


class ExtendReckRecommendConfigCommon(ReckRecommendConfigCommon):
    def __init__(self):
        super().__init__()
        self.deploy_history_model = DeployHistoryModel()

    def post(self):
        nodes_info = self.get_nodes_from_request()
        ceph_service_flag = nodes_info['cephServiceFlag']
        local_service_flag = nodes_info['localServiceFlag']
        service_type = nodes_info["serviceType"]
        storage_list = nodes_info["storages"]
        self.classify_disks(storage_list)

        data = {}
        if ceph_service_flag:
            ceph_copy_num_default = nodes_info["cephCopyNumDefault"]
            nodes = nodes_info["nodes"]
            extend_pg_all = len(nodes) * len(self.ceph_data_storage) * 100
            all_pgs = self.get_deploy_history_pgs() + extend_pg_all
            data = self.calculate_ceph_storage(len(nodes), service_type, ceph_copy_num_default, all_pgs)
            data['shareSizeMax'] = '0GB'

        if local_service_flag:
            local_storage_data = self.calculate_local_storage()
            data['shareSizeMax'] = local_storage_data['share_size_max']
            data['localSizeMax'] = local_storage_data['local_size_max']

        if len(service_type) >= 2:
            nodes = nodes_info["nodes"]
            total_memory = nodes[0]['memTotal']
            osd_num = len(self.ceph_data_storage) / len(nodes)
            data['memorySizeMax'] = self.calculate_memory_free_size(total_memory, osd_num)

        return types.DataModel().model(code=0, data=data)

    def get_deploy_history_pgs(self):
        history_data = self.deploy_history_model.get_deploy_history()
        datas_json = json.loads(history_data[1])
        ceph_datas_num = 0
        for node in datas_json['nodes']:
            for storage in node['storages']:
                if storage['purpose'] == 'CEPH_DATA':
                    ceph_datas_num += 1
        return ceph_datas_num * 100


# 个性化pg计算
class ExtendShowRecommendConfig(ExtendReckRecommendConfigCommon, ShowRecommendConfig):
    def post(self):
        nodes_info = self.get_nodes_from_request()
        ceph_service_flag = nodes_info['cephServiceFlag']
        local_service_flag = nodes_info['localServiceFlag']
        nodes = nodes_info["nodes"]
        service_type = nodes_info["serviceType"]
        
        for node in nodes:
            self.classify_disks(node['storages'])

        data = {}
        if ceph_service_flag:
            ceph_copy_num_default = nodes_info["cephCopyNumDefault"]
            extend_pg_all = len(self.ceph_data_storage) * 100
            all_pgs = self.get_deploy_history_pgs() + extend_pg_all
            data = self.calculate_ceph_storage(
                1, service_type, ceph_copy_num_default, all_pgs)
            data['shareSizeMax'] = '0GB'
        
        if local_service_flag:
            local_storage_data = self.calculate_node_local_storage(nodes)
            data['shareSizeMax'] = local_storage_data['share_size_max']
            data['localSizeMax'] = local_storage_data['local_size_max']

        if len(service_type) >= 2:
            data['memorySizeMax'] = self.get_node_memory_free_size(nodes)
        
        return types.DataModel().model(code=0, data=data)
