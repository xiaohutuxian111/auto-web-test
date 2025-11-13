import json
import os


def analyse_har(filepath, rspTime=1000):
    file = open(filepath, "r")
    har_context = file.read()
    har = json.loads(har_context)
    har_entries = har["log"]["entries"]
    analyse_list = []
    for entry in har_entries:
        if entry.get("timings") and entry.get("time") > rspTime:
            request_method = str(entry["request"]["method"]).lower()
            url = entry["request"]["url"]
            time = entry["time"]
            if request_method in ["get", "head", "options", "trace", "delete"]:
                if ".js" in entry["request"]["url"]:
                    continue
                elif "?" in entry["request"]["url"]:
                    url_list = url.split("?")
                    one_list = [request_method] + url_list + [time]

                else:
                    one_list = [request_method, url, "", time]
            else:
                postdata = entry["request"].get("postData")
                one_list = [request_method, url, postdata, time]
            analyse_list.append(one_list)
    return analyse_list


def analyse_har_folder(folder, rspTime=1000):
    har_file_list = []
    analyse_big_list = []
    for filewalks in os.walk(folder):
        for files in filewalks[2]:
            # print('true files',files)
            if ".har" in files:
                har_file_list.append(os.path.join(filewalks[0], files))
    for har in har_file_list:
        analyse_list = analyse_har(har, rspTime)
        analyse_big_list.extend(analyse_list)
    return analyse_big_list
