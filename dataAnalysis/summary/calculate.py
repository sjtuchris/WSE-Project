#coding=utf8
# this file is used to calculate average data for variaty of data
import sys
import csv


def load_to_dict(file):
    dictionary = {}
    with open(file, "r") as f:
        for line in f:
            split = line.split("\t")
            dictionary[split[0]] = float(split[1])
    return dictionary


def cal_avg_result(state_dict, other_dict):
    result = {}
    for key in state_dict:
        try:
            result[key] = other_dict[key] / state_dict[key]
        except:
            continue
    return result


def write_to_csv(dictionary, filepath, filename, rows):
    csv_file = file(filepath+filename, "wb")
    writer = csv.writer(csv_file)
    writer.writerow(rows)
    for key in dictionary:
        l = list()
        l.append(key)
        l.append(dictionary[key])
        writer.writerow(l)

    csv_file.close()


if __name__ == "__main__":
    # load state file first
    input_folder = sys.argv[1]
    input_file = "result.out"
    output_folder = sys.argv[2]

    state_dict = load_to_dict(input_folder + "/by_state/" + input_file)
    # print state_dict
    write_to_csv(state_dict, output_folder, "state.csv", ["states", "frequency"])

    # avg backers
    backers_dict = load_to_dict(input_folder + "/by_backers/" + input_file)
    avg_backers_dict = cal_avg_result(state_dict, backers_dict)
    #print avg_backers_dict
    write_to_csv(avg_backers_dict, output_folder, "avg_backers.csv", ["states", "backers"])

    # avg comment
    comment_dict = load_to_dict(input_folder + "/by_comment_num/" + input_file)
    avg_comment_dict = cal_avg_result(state_dict, comment_dict)
    # print avg_comment_dict
    write_to_csv(avg_comment_dict, output_folder, "avg_comment.csv", ["states", "comments"])

    pledged_dict = load_to_dict(input_folder + "/by_pledged/" + input_file)
    avg_pledged_dict = cal_avg_result(state_dict, pledged_dict)
    #print avg_pledged_dict
    write_to_csv(avg_pledged_dict, output_folder, "avg_pledged.csv", ["states", "pledged"])

    goal_dict = load_to_dict(input_folder + "/by_goal/" + input_file)
    avg_goal_dict = cal_avg_result(state_dict, goal_dict)
    # print avg_goal_dict
    write_to_csv(avg_goal_dict, output_folder, "avg_goal.csv", ["states", "goal"])

    catgegory_dict = load_to_dict(input_folder + "/by_category/" + input_file)
    #print catgegory_dict
    write_to_csv(catgegory_dict, output_folder, "category.csv", ["category", "frequency"])

    subcatgegory_dict = load_to_dict(input_folder + "/by_sub_category/" + input_file)
    #print subcatgegory_dict
    write_to_csv(subcatgegory_dict, output_folder, "subcategory.csv", ["subcategory", "frequency"])

    success_category_dict = load_to_dict(input_folder + "/by_success_category/" + input_file)
    # print success_category_dict
    write_to_csv(success_category_dict, output_folder, "success_category.csv", ["category", "frequency"])

    fail_category_dict = load_to_dict(input_folder + "/by_fail_category/" + input_file)
    #print fail_category_dict
    write_to_csv(fail_category_dict, output_folder, "fail_category.csv", ["category", "frequency"])

    success_subcategory_dict = load_to_dict(input_folder + "/by_success_subcategory/" + input_file)
    #print success_subcategory_dict
    write_to_csv(success_subcategory_dict, output_folder, "success_subcategory.csv", ["category", "frequency"])

    fail_category_dict = load_to_dict(input_folder + "/by_fail_subcategory/" + input_file)
    #print fail_category_dict
    write_to_csv(fail_category_dict, output_folder, "fail_subcategory.csv", ["category", "frequency"])

    country_dict = load_to_dict(input_folder + "by_country/" + input_file)
    # print country_dict
    write_to_csv(country_dict, output_folder, "country.csv", ["country", "frequency"])

    duration = load_to_dict(input_folder + "by_duration/" + input_file)
    avg_duration = cal_avg_result(state_dict, duration)
    #print avg_duration
    write_to_csv(avg_duration, output_folder, "avg_duration.csv", ["states", "days"])

    update_dict = load_to_dict(input_folder + "by_update/" + input_file)
    avg_update = cal_avg_result(state_dict, update_dict)
    # print avg_update
    write_to_csv(avg_update, output_folder, "avg_update.csv", ["states", "frequency"])

    by_city = load_to_dict(input_folder + "by_city/" + input_file)
    # print by_city
    write_to_csv(by_city, output_folder, "by_city.csv", ["city", "frequency"])

    by_us_state = load_to_dict(input_folder + "by_us_states/" + input_file)
    #print by_us_state
    write_to_csv(by_us_state, output_folder, "us_states.csv", ["states", "frequency"])
