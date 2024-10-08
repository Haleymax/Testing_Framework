from core.mongo import MongoClint
from core.games_info import TestInfo


def get_test(get_mongourl, get_database, get_devices, get_games):
    client = MongoClint()
    client.connect(get_mongourl)
    client.use_database(get_database)
    devices = client.find_collection(get_devices)
    games = client.find_collection(get_games)

    webgl_host_data = {}
    for device in devices:
        infoObject = TestInfo()
        infoObject.serial = device




def get_data(get_mongourl,get_database,get_collection):
    client = MongoClint()
    mogourl = get_database
    database = get_database
    collection = get_collection
    client.connect(mogourl)
    client.use_database(database)
    data = client.find_collection(collection)
    result = []
    webgl_host_data = {}
    for x in data:
        linedata = []
        deviceid = x['deviceid']
        packagename = x['packagename']
        typename = x['type']
        gamelist = x['gamelist']
        linedata.append(deviceid)
        linedata.append(packagename)
        linedata.append(typename)
        for key, value in gamelist.items():
            line2 = linedata[:]
            line2.append(str(key))
            line2.append(str(value))
            result.append(line2)
        webgl_host_data['test_webgl_host'] = result
    return webgl_host_data



webgl_host_data = get_data()