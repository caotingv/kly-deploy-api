from flask import jsonify
import time


class DataModel:
    def model(self, code, data, message=None, path=None):
        return jsonify({
            'timestamp': int(time.time() * 1000),
            'state': 200,
            'code': code,
            'message': message,
            'path': path,
            'data': data
        })
    
    def history_deploy_model(self, startTime, endtime, paramsJson, log="",result="", message="" ,key="deploy:klcloud-fsd", id=1, uuid=""):    
        return {
            'paramsJson': paramsJson,
            'log': log,
            'message': message,
            'uuid': uuid,
            'result': result,
            'startTime': startTime,
            'id': id,
            'endtime': endtime,
            'key': key
        }

    def history_upgarde_model(self, new_version, endtime, version='', result='', message=''):    
        return {
            'version': version,
            'new_version': new_version,
            'result': result,
            'message': message,
            'endtime':  endtime
        }

    def history_extend_model(self, params_json, log, message, result, start_time, endtime):    
        return {
            'paramsJson': params_json,
            'log': log,
            'message': message,
            'result': result,
            'startTime': start_time,
            'endtime':  endtime
        }